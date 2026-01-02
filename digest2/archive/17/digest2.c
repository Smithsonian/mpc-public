// digest2.c
//
// Public domain.

/*
This program uses statistical ranging techniques on short arc astrometry to
compute probabilities that observed objects are of various orbit classes.

See external file README for additional information.
*/

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "digest2.h"

// thread coordination
//-----------------------------------------------------------------------------

int cores;
tracklet *stage;                // staging for tracklet to be scored
tracklet **ring;                // ring data structure
int ringFree;                   // number of free trackets
int ringNext;                   // index of next free tracklet

// deadlock avoidance:
// a thread holding one never asks for the other.
pthread_mutex_t mStage = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t mRing = PTHREAD_MUTEX_INITIALIZER;

// signaled by main thread when data is staged.
// mutex: mStage
// pre-condition:  stage == 0
// while locked:  set stage
// post-condition:  stage non-zero
pthread_cond_t cReady = PTHREAD_COND_INITIALIZER;

// signaled by scoring thread when it begins work.
// mutex: mStage
// pre-condition:  stage non-zero
// while locked:  zero stage
// post-condition:  stage == 0
pthread_cond_t cFree = PTHREAD_COND_INITIALIZER;

// signaled by scoring thread when it returns a token to the ring
// mutex: mRing
// post-condition: ringFree > 0
pthread_cond_t cDone = PTHREAD_COND_INITIALIZER;

// "constant" global data
//-----------------------------------------------------------------------------
// global data that is constant, at least after being initialized, and so
// can be shared by threads.

site siteTable[obscodeNamespaceSize];
int outputLineSize;
char *outputLine;

/* resetInvalid

reset tracklet struct for processing a new object.

Notes;
   zero the struct, except retain the allocated olist and it's capacity.
   also initialize number lines to 1.  that's all that's needed to indicate
   an invalid observation line.
*/
tracklet *resetInvalid(void)
{
  // get a free tk from the ring
  pthread_mutex_lock(&mRing);
  while (ringFree == 0)
    pthread_cond_wait(&cDone, &mRing);
  tracklet *tk = ring[ringNext];
  ringNext = (ringNext + 1) % cores;
  ringFree--;
  pthread_mutex_unlock(&mRing);

  // reset
  int saveObsCap = tk->obsCap;
  observation *saveOlist = tk->olist;
  uint64_t saveRand = tk->rand64;
  perClass *saveClass = tk->class;
  memset(tk, 0, sizeof(tracklet));
  tk->obsCap = saveObsCap;
  tk->olist = saveOlist;
  tk->rand64 = saveRand;
  tk->class = saveClass;
  tk->lines = 1;
  return tk;
}

/* resetValid

reset tracklet struct, intializing with a valid observation.

Notes:
    call for first observation of a tracklet.

    resetInvalid does common initialization chores.
*/
tracklet *resetValid(char *desig, observation * obsp)
{
  tracklet *tk = resetInvalid();
  tk->status = UNPROC;
  strcpy(tk->desig, desig);
  memcpy(tk->olist, obsp, sizeof(observation));
  memset(tk->class, 0, nClassCompute * sizeof(perClass));
  return tk;
}

/* continueValid

call for subsequent observations of a tracklet
*/
void continueValid(tracklet * tk, char *desig, observation * obsp)
{
  if (tk->lines == tk->obsCap) {
    tk->obsCap += 10;
    tk->olist = (observation *) realloc(tk->olist,
                                        tk->obsCap * sizeof(observation));
    if (!tk->olist)
      fatal(msgMemory);
  }

  memcpy(tk->olist + tk->lines, obsp, sizeof(observation));
  tk->lines++;
}

void continueInvalid(tracklet * tk)
{
  tk->lines++;
}

// ringAdd is called when a tracklet is completed.  it outputs a result
// to stdout and recycles the tracklet struct by returning it to the ring.
// note the global variable outputLine is a required input.
void ringAdd(tracklet * tk)
{
  pthread_mutex_lock(&mRing);
  // puts needs to be in mutex here because it is not thread safe
  if (*outputLine)              // empty line means --limit
    puts(outputLine);
  ring[(ringNext + ringFree) % cores] = tk;
  ringFree++;
  pthread_cond_signal(&cDone);
  pthread_mutex_unlock(&mRing);
}

/* eval (tracklet method)

evaluate tracklet

handle degenerate cases, compute scores for good tracklets,
and output results.

Notes:
   outputs explanatory text if tracklet cannot be scored for any reason.

   otherwise, calls initTracklet for setup, calls dRange to drive
   computations, then computes, formats, and outputs final scores.
*/
void eval(tracklet * tk)
{
  if (tk->status == INVALID) {
    snprintf(outputLine, outputLineSize,
             "              %d lines skipped.", tk->lines);
    ringAdd(tk);
    return;
  }

  if (tk->status != UNPROC)
    fatal(msgStatus);

  // working with 12 character designation field was expedient so far.
  // now compact it to save output columns:  if 5 character field is
  // non-blank, shift it into 7 character field.
  if (strncmp(tk->desig, "     ", 5)) {
    tk->desig[5] = ' ';
    tk->desig[6] = ' ';
    strncpy(tk->desig + 7, tk->desig, 5);
  }

  if (tk->lines == 1) {
    snprintf(outputLine, outputLineSize,
             "%s  single observation.  skipped.", tk->desig + 5);
    ringAdd(tk);
    return;
  }
  // select first and last observations
  observation *obsFirst = tk->olist;
  observation *obsLast = obsFirst + tk->lines - 1;

  // sanity check on time
  if (obsLast->mjd < obsFirst->mjd) {
    snprintf(outputLine, outputLineSize,
             "%s  observations out of order.", tk->desig + 5);
    ringAdd(tk);
    return;
  }
  // sanity check on movement
  if (obsFirst->ra == obsLast->ra && obsFirst->dec == obsLast->dec) {
    snprintf(outputLine, outputLineSize,
             "%s  tracklet shows no motion.", tk->desig + 5);
    ringAdd(tk);
    return;
  }
  // average whatever magnitudes are there.  default to V=21 if none.
  // this is here rather than d2math.c just to keep d2math.c more general
  // and, as much as practical, not specific to the kind of observations
  // being processed.  code here is specific to the case of typical MPC
  // observations varying in number, often missing magnitudes, and having
  // limiting magnitude around 21.
  double msum = 0;
  int mcount = 0;

  for (int i = 0; i < tk->lines; i++)
    if (obsFirst[i].vmag > 0.) {
      msum += obsFirst[i].vmag;
      mcount++;
    }

  tk->vmag = mcount > 0 ? msum / mcount : 21.;

  // wait for stage to be free
  pthread_mutex_lock(&mStage);
  while (stage)
    pthread_cond_wait(&cFree, &mStage);

  // stage tk
  stage = tk;

  // precondition met for cReady
  pthread_cond_signal(&cReady);
  pthread_mutex_unlock(&mStage);
}

void fmtScores(tracklet * tk)
{
  // test any --limit
  perClass *cl;
  if (limitSpec) {
    cl = tk->class + limitClass;
    if ((int)((limitRaw ? cl->rawScore : cl->noIdScore) + .5) < limit) {
      // no output if below limit
      *outputLine = 0;
      return;
    }
  }
  // build line for atomic write and print results.
  int len = snprintf(outputLine, outputLineSize, "%s", tk->desig + 5);
  if (rms) {
    // we expect 6 new bytes.  more than that means field overflow
    if (snprintf
        (outputLine + len, outputLineSize - len, " %5.2f", tk->rms) != 6)
      strcpy(outputLine + len, " **.**");
    len += 6;
  }
  int c;
  if (classPossible) {
    // specified columns first
    for (c = 0; c < nClassColumns; c++) {
      cl = tk->class + classColumn[c];
      if (raw)
        len +=
          snprintf(outputLine + len,
                   outputLineSize - len, " %3.0f", cl->rawScore);
      if (noid)
        len +=
          snprintf(outputLine + len,
                   outputLineSize - len, " %3.0f", cl->noIdScore);
    }
    // then other possibilities
    for (c = 0; c < D2CLASSES; c++) {
      int cc;
      for (cc = 0; cc < nClassColumns && classColumn[cc] != c; cc++) ;
      if (cc < nClassColumns)
        continue;               // already in a column
      // else output if possible
      cl = tk->class + c;
      double pScore = noid ? cl->noIdScore : cl->rawScore;
      if (pScore > .5)
        len +=
          snprintf(outputLine + len,
                   outputLineSize - len, " (%s %.0f)", classAbbr[c], pScore);
      else if (pScore > 0)
        len +=
          snprintf(outputLine + len,
                   outputLineSize - len, " (%s <1)", classAbbr[c]);

    }
  } else {
    // other possibilities not computed.
    for (c = 0, cl = tk->class; c < nClassCompute; c++, cl++) {
      if (raw)
        len +=
          snprintf(outputLine + len,
                   outputLineSize - len, " %3.0f", cl->rawScore);
      if (noid)
        len +=
          snprintf(outputLine + len,
                   outputLineSize - len, " %3.0f", cl->noIdScore);
    }
  }
}

void *scoreStaged(void *id)
{
  while (1) {
    pthread_mutex_lock(&mStage);
    while (!stage)
      pthread_cond_wait(&cReady, &mStage);

    // process cReady
    tracklet *tk = stage;
    stage = NULL;

    // pre-condition met for cFree
    pthread_cond_signal(&cFree);
    pthread_mutex_unlock(&mStage);

    // do math, not holding any mutex
    if (repeatable)
      tk->rand64 = 3;

    score(tk);
    fmtScores(tk);
    ringAdd(tk);
  }
  return NULL;
}

/* main
-------------------------------------------------------------------------------
process MPC 80 column observation records and output scores to stdout

specify file to process on command line
*/
int main(int argc, char **argv)
{
  // sets up globals and terminates on error
  char *fnObs = parseCl(argc, argv);

  // read model
  if (fnObs) {
    if (modelSpec) {
      // fast path using binary model file only. no csv checks.
      mustReadModel();
    } else {
      mustReadModelStatCSV();   // with model/csv caching logic
    }
  } else if (modelSpec) {
    // generate model only, no computations
    struct stat csv;
    mustReadCSV(&csv);
    writeModel(&csv);
  }
  // similar logic for obscode dat
  if (fnObs) {
    if (ocdSpec) {
      mustReadOCD();
    } else {
      mustReadGetOCD();         // with caching logic
    }
  } else if (ocdSpec) {
    // get obscode dat only, no need to read it.
    getOCD();
  }

  if (!fnObs) {
    exit(0);                    // just generating model or getting obscode dat.
  }
  // continue to computations

  char *obsFnPrint = strcmp(fnObs, "-") ? fnObs : "stdin";
  FILE *fobs = strcmp(fnObs, "-") ? fopen(fnObs, "r") // test that file can be opened
    : stdin;
  if (!fobs)
    fatal1(msgOpen, obsFnPrint);

  if (!fgets(line, LINE_SIZE, fobs)) { // test that file can be read
    // no data is not an error, just issue message and exit.
    // this is important for the web service.  errors from digest2 turn into
    // status 500s or similar because error conditions are out of the user's
    // control and so are not reported to the user.
    if (feof(fobs)) {
      fclose(fobs);
      puts("\nNo input data.");
      exit(0);
    }
    fatal1(msgRead, obsFnPrint); // anything else is a problem
  }
  // three more that set up globals and terminate on error
  initGlobals();

  // default configuration
  classPossible = 1;
  nClassColumns = 4;
  classColumn[0] = 0;           // MPC interesting.  see d2model.c
  classColumn[1] = 1;           // neo
  classColumn[2] = 2;           // n22
  classColumn[3] = 3;           // n18
  for (nClassCompute = 0; nClassCompute < D2CLASSES; nClassCompute++)
    classCompute[nClassCompute] = nClassCompute;
  headings = 1;
  rms = 1;
  raw = 0;
  noid = 1;

  readConfig();                 // configures globals and terminates on error

  // for --limit, validate that option is configured
  if (limitSpec) {
    for (int i = 0;; i++) {
      if (i == nClassCompute)
        fatal(msgLimitClassNotConfig);
      if (classCompute[i] == limitClass)
        break;
    }
    if (limitRaw ? !raw : !noid)
      fatal(msgLimitScoreNotConfig);
  }
  // thread setup
  if (!cpuSpec)
    cores = sysconf(_SC_NPROCESSORS_CONF);
  if (cores <= 0)
    cores = 1;
  else if (cores > 1024)
    cores = 1024;
  ringFree = cores;
  if (!(ring = malloc(sizeof(tracklet *) * cores)))
    fatal(msgMemory);

  pthread_t *thPool;
  if (!(thPool = malloc(sizeof(pthread_t) * cores)))
    fatal(msgMemory);

  pthread_attr_t attr;
  pthread_attr_init(&attr);
  // neophyte code:  the program seems to work with any non-negative
  // stack size, right down to zero.  default is 10M?  anyway, even with
  // recursive functions in d2math.c, seems even a single 4K page would do.
  pthread_attr_setstacksize(&attr, 8192);
  // and, I hear you're supposed to do this, even though it seems to be
  // the default.
  pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_JOINABLE);

  // per-thread tracklet setup 
  //
  // also note here are the elements that must be preserved to recycle a
  // a tracklet structure.  see resetValid, resetInvalid.
  for (int th = 0; th < cores; th++) {
    if (pthread_create(thPool + th, &attr, scoreStaged, NULL))
      fatal(msgThread);

    tracklet *tk = (tracklet *) calloc(1, sizeof(tracklet));
    if (!tk)
      fatal(msgMemory);
    // per-thread LCG setup.  I think NAG needs an odd number for a seed.
    // see additional notes in d2math.c
    tk->rand64 = 2 * (rand() / 2) + 1;
    tk->obsCap = 5;
    tk->olist = (observation *) malloc(tk->obsCap * sizeof(observation));
    if (!tk->olist)
      fatal(msgMemory);
    ring[th] = tk;
    tk->class = (perClass *) calloc(nClassCompute, sizeof(perClass));
    if (!tk->class)
      fatal(msgMemory);
  }

  // column headings, delayed until now to avoid printing column headings
  // only to terminate with an error message if some initialization fails
  if (headings) {
    int c;
    // heading line 1
    if (raw && noid && nClassColumns) {
      printf("-------");
      if (rms)
        printf("  ----");
      for (c = 0; c < nClassColumns; c++)
        printf("   %3.3s  ", classAbbr[classColumn[c]]);
      puts(classPossible ? " ---------------" : "");
    }
    // heading line 2
    printf("Desig. ");
    if (rms)
      printf("   RMS");
    for (c = 0; c < nClassColumns; c++)
      if (raw && noid)
        printf(" Raw NID");
      else
        printf(" %3.3s", classAbbr[classColumn[c]]);
    puts(classPossible
         ? nClassColumns ? " Other Possibilities" : " Possibilities" : "");
  }

  outputLineSize = 13 + (nClassColumns) * 14;
  if (classPossible)
    outputLineSize += (D2CLASSES - nClassColumns) * 9;

  outputLine = malloc(outputLineSize);
  if (!outputLine)
    fatal(msgMemory);

  // a little more setup to prime the main loop
  observation obs1;

  tracklet *tk = parseMpc80(line, &obs1)
    ? resetValid(line, &obs1) : resetInvalid();

  // main loop
  while (fgets(line, LINE_SIZE, fobs)) {
    _Bool pGood;

    if (line[14] == 's') {
      if (tk->lines && parseMpcSat(line, tk->olist + tk->lines - 1))
        continue;
      pGood = 0;
    } else
      pGood = parseMpc80(line, &obs1);

    if (pGood)
      if (tk->status == INVALID || strcmp(line, tk->desig)) {
        eval(tk);
        tk = resetValid(line, &obs1);
      } else
        continueValid(tk, line, &obs1);
    else if (tk->status == INVALID)
      continueInvalid(tk);
    else {
      eval(tk);
      tk = resetInvalid();
    }
  }

  eval(tk);
  fclose(fobs);

  // wait for that last job to start
  pthread_mutex_lock(&mStage);
  while (stage)
    pthread_cond_wait(&cFree, &mStage);
  pthread_mutex_unlock(&mStage);

  // wait for all jobs to finish
  pthread_mutex_lock(&mRing);
  while (ringFree < cores)
    pthread_cond_wait(&cDone, &mRing);
}

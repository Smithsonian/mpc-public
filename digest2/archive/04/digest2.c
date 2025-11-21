//! C99

/* Digest2.c

Copyright (c) 2010 Sonia Keys
Copyright (c) 2005,2006 Kyle Smalley, Carl Hergenrother, Robert McNaught,
David Asher

See external file LICENSE, distributed with this software.

-------------------------------------------------------------------------------
Digest2.c

This program uses statistical ranging techniques on short arc astrometry to
compute probabilities that observed objects are of various orbit classes.

See external file README for additional information.
*/
#include <ctype.h>
#include <errno.h>
#include <limits.h>
#include <math.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "digest2.h"


// thread coordination
//-----------------------------------------------------------------------------

int cores;
tracklet *stage; // staging for tracklet to be scored
tracklet **ring; // ring data structure
int ringFree;    // number of free trackets
int ringNext;    // index of next free tracklet

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

site siteTable[2000];
int classConfig[D2CLASSES];
int nClassConfig;
_Bool classPossible;
int outputLineSize;
char *outputLine;

char msgMemory[] = "Memory allocation failed.\n";
char msgOpen[]   = "Open %s failed.\n";
char msgRead[]   = "Read %s failed.\n";
char msgStatus[] = "Internal error:  Unexpected tracklet status.\n";
char msgThread[] = "Thread creation failed.\n";
char msgSwitch[] = "Unknown switch.\n";
char msgUsage[]  = "\
Usage: digest2 <obsfile>       score observations\n\
       digest2 -c              list available orbit classes\n\
       digest2 -h or --help    display help file\n";
char msgHelp[] = "\
Digest2 help\n\
\n\
Digest2 uses statistical ranging techniques on short arc astrometry to\n\
compute probabilities that observed objects are of various orbit classes.\n\
Input is a file of 80 column MPC-format observations, with at least two\n\
observations per object.  Output is orbit class scores for each object.\n\
\n\
See README for additional information.\n";

// functions
//-----------------------------------------------------------------------------

/* fatal

print message to stdout and terminate program.
*/
void fatal(char *msg) {
   printf(msg);
   exit(-1);
}

void fatal1(char *msg, char *arg) {
   printf(msg, arg);
   exit(-1);
}

/* mustStrtod

for required fields.  a version of atof that sets errno on blank input.
also allows whitespace after sign
*/
double mustStrtod(char *str) {
   char *endp;
   _Bool neg = *str == '-';
   if (neg || *str == '+')
      str++;
   double result = strtod(str, &endp);
   if (!errno && endp == str)
      errno = EINVAL;
   return neg ? -result : result;
}

/* mustStrtoi

returns int but actually disallows negatives.
*/
int mustStrtoi(char *str) {
   char *endp;
   long result = strtol(str, &endp, 10);
   if (!errno)
      if (endp == str || result < 0 || result > INT_MAX)
         errno = EINVAL;
   return result;
}
   
/* readModel()

read population model into memory

Notes:
   on error, prints message to stdout and terminates.
*/
void readModel() {
   char *fn = "digest2.muk";
   FILE * fmuk = fopen(fn, "r");
   if (!fmuk)
      fatal1(msgOpen, fn);

   if (!fread(modelAllSS, sizeof modelAllSS, 1, fmuk) ||
       !fread(modelUnkSS, sizeof modelUnkSS, 1, fmuk) ||
       !fread(modelAllClass, sizeof modelAllClass, 1, fmuk) ||
       !fread(modelUnkClass, sizeof modelUnkClass, 1, fmuk))
      fatal1(msgRead, fn);

   fclose(fmuk);
}

/* resetInvalid

reset tracklet struct for processing a new object.

Notes;
   zero the struct, except retain the allocated olist and it's capacity.
   also initialize number lines to 1.  that's all that's needed to indicate
   an invalid observation line.
*/
tracklet * resetInvalid(void) {
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
   uint64_t saveRand = tk->rand;
   perClass *saveClass = tk->class;
   memset(tk, 0, sizeof(tracklet));
   tk->obsCap = saveObsCap;
   tk->olist = saveOlist;
   tk->rand = saveRand;
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
tracklet * resetValid(char *desig, observation *obsp) {
   tracklet *tk = resetInvalid();
   tk->status = UNPROC;
   strcpy(tk->desig, desig);
   memcpy(tk->olist, obsp, sizeof(observation));
   memset(tk->class, 0, nClassConfig * sizeof(perClass));
   return tk;
}

/* continueValid

call for subsequent observations of a tracklet
*/
void continueValid(tracklet *tk, char *desig, observation *obsp) {
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

void continueInvalid(tracklet *tk) {
   tk->lines++;
}

void ringAdd(tracklet *tk) {
   pthread_mutex_lock(&mRing);
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
void eval(tracklet *tk) {
   if (tk->status == INVALID) {
      printf("              %d lines skipped.\n", tk->lines);
      ringAdd(tk);
      return;
   }

   if (tk->status != UNPROC)
      fatal(msgStatus);

   if (tk->lines == 1) {
      printf("%s  single observation.  skipped.\n", tk->desig);
      ringAdd(tk);
      return;
   }

   // select first and last observations
   observation *obsFirst = tk->olist;
   observation *obsLast = obsFirst + tk->lines - 1;

   // sanity check on time
   if (obsLast->mjd < obsFirst->mjd) {
      printf("%s  observations out of order.\n", tk->desig);
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

void *scoreStaged(void *id) {
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
      score(tk);

      // build line for atomic write and print results.
      int len = snprintf(outputLine, outputLineSize, "%s", tk->desig);
      perClass *cl;
      int c;
      if (classPossible) {
         cl = tk->class + 1;
         len += snprintf(outputLine + len, outputLineSize - len,
               "  %6.2f  %6.2f ", cl->rawScore, cl->noIdScore);
         for (c = 2; c < D2CLASSES; c ++) {
            cl = tk->class + c;
            if (cl->rawScore > 0)
               len += snprintf(outputLine + len, outputLineSize - len,
                  " (%s %.0f)", classAbbr[c], cl->noIdScore);
         }
      } else {
         for (c = 0, cl = tk->class; c < nClassConfig; c++, cl++)
            len += snprintf(outputLine + len, outputLineSize - len,
               "  %6.2f  %6.2f", cl->rawScore, cl->noIdScore);
      }
      puts(outputLine);

      // work done
      ringAdd(tk);
   }
   return NULL;
}

void readConfig(void) {
   FILE *fcfg = fopen("digest2.cfg", "r");

   if (!fcfg)
      return;

   char line[20];
   if (!fgets(line, sizeof(line), fcfg)) {
      puts("digest2.cfg read failed");
      return;
   }

   if (!strncmp(line, "possible", 8))
      return;

   classPossible = 0;
   nClassConfig = 0;
   do {
      if (line[strlen(line)-1] == '\n')
         line[strlen(line)-1] = 0;

      for (int c = 0; c < D2CLASSES; c++)
         if (!strcmp(line, classHeading[c]) || !strcmp(line, classAbbr[c])) {
            classConfig[nClassConfig++] = c;
            break;
         }
   }
   while
      (nClassConfig < D2CLASSES && fgets(line, sizeof(line), fcfg));
}

/* main
-------------------------------------------------------------------------------
process MPC 80 column observation records and output scores to stdout

specify file to process on command line

other prerequisite is file digest2.muk, prepared by running muk.c.  see
muk.c internal documentation.

limitations of this driver:
   - processes only MPC 80 column earth-based observation records.
     support for data in other formats should be possible.

   - single threaded.  but it shouldn't be too hard to process tracklets
     on separate threads to take advantage of multiple cores.  global data
     is all constant, tracklet data is all contained in the tracklet struct.
     allocate a tracklet for each core and just write code to dispatch the
     work and handle results.

   - results are text on stdout.  again, modifications shouldn't be hard.
*/
int main (int argc, char **argv) {
   // argv[1] is input file of observations
   if (argc != 2)                      // test that arg is supplied
      fatal(msgUsage);

   if (!strcmp(argv[1], "-c")) {
      for (int c = 0; c < D2CLASSES; c++)
         printf("%3s %20s\n",classAbbr[c],classHeading[c]);
      return 0;
   }

   if (!strcmp(argv[1], "-h") || !strcmp(argv[1], "--help")) {
      puts(msgHelp);
      return 0;
   }

   if (*argv[1] == '-') {
      puts(msgSwitch);
      fatal(msgUsage);
   }

   FILE *fobs = fopen(argv[1], "r");   // test that file can be opened
   if (!fobs)
      fatal1(msgOpen, argv[1]);

   const int LINE_SIZE = 82;
   char line[LINE_SIZE];
   if (!fgets(line, LINE_SIZE, fobs))  // test that file can be read
      fatal1(msgRead, argv[1]);

   // these three set up globals and terminate on error
   initGlobals();
   readMpcOcd();
   readModel();

   // default classes unless changed by config
   classPossible = 1;
   for (nClassConfig = 0; nClassConfig < D2CLASSES; nClassConfig++)
      classConfig[nClassConfig] = nClassConfig;

   readConfig();

   // thread setup
   cores = sysconf(_SC_NPROCESSORS_CONF);
   if (cores <= 0)
      cores = 1;
   ringFree = cores;
   if (!(ring = malloc(sizeof(tracklet *) * cores)))
      fatal(msgMemory);

   pthread_t * thPool;
   if (!(thPool = malloc(sizeof(pthread_t) * cores)))
      fatal(msgMemory);

   pthread_attr_t attr;
   pthread_attr_init(&attr);
   // neophyte code:  the program seems to work with any non-negative
   // stack size, right down to zero.  default is 10M?  anyway, even with
   // recursive functions in d2math.c, seems even a single 4K page whould do.
   pthread_attr_setstacksize(&attr, 8192);
   // and, I hear you're supposed to do this, even though it seems to be
   // the default.
   pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_JOINABLE);

   // per-thread tracklet setup 
   //
   // also note here are the elements that must be preserved to recycle a
   // a tracklet structure.  see resetValid, resetInvalid.
   for (int th = 0; th < cores; th++) {
      if (pthread_create(thPool+th, &attr, scoreStaged, NULL))
         fatal(msgThread);

      tracklet *tk = (tracklet *) calloc(1, sizeof(tracklet));
      if (!tk)
         fatal(msgMemory);
      // per-thread LCG setup.  I think NAG needs an odd number for a seed.
      // see additional notes in d2math.c
      tk->rand = 2*(rand()/2)+1;
      tk->obsCap = 5;
      tk->olist = (observation *) malloc(tk->obsCap * sizeof(observation));
      if (!tk->olist)
         fatal(msgMemory);
      ring[th] = tk;
      tk->class = (perClass *) calloc(nClassConfig, sizeof(perClass));
      if (!tk->class)
         fatal(msgMemory);
   }

   // column headings, delayed until now to avoid printing column headings
   // only to terminate with an error message if some initialization fails
   if (classPossible) {
      printf("-----------  %15.15s\n", classHeading[1]);
      outputLineSize = printf("Designation     Raw   No-ID   ");
      printf("Other Possibilities\n");
      outputLineSize += (D2CLASSES - 2) * 9;
   } else {
      printf("----------- ");
      for (int c = 0; c < nClassConfig; c++)
         outputLineSize += printf(" %15.15s", classHeading[classConfig[c]]);
      outputLineSize += printf("\nDesignation ");
      for (int c = 0; c < nClassConfig; c++)
         printf("     Raw   No-ID");
      puts("");
   }

   outputLine = malloc(outputLineSize);
   if (!outputLine)
      fatal(msgMemory);

   // a little more setup to prime the main loop
   observation obs1;

   tracklet *tk = parseMpc80(line, &obs1)
      ? resetValid(line, &obs1)
      : resetInvalid();
      
   // main loop
   while (fgets(line, LINE_SIZE, fobs)) {
      _Bool pGood;

      if (line[14] == 's') {
         if (tk->lines && parseMpcSat(line, tk->olist + tk->lines - 1))
            continue;
         pGood = 0;
      }
      else
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

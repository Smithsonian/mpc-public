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
#include <getopt.h>
#include <limits.h>
#include <math.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "digest2.h"

// stuff used for parsing command line
//-----------------------------------------------------------------------------
char sOpt[] = "hvc:m:o:p:";
struct option lOpt[] = {
   {"help",    no_argument, 0, 'h'},
   {"version", no_argument, 0, 'v'},
   {"config",      required_argument, 0, 'c'},
   {"model",       required_argument, 0, 'm'},
   {"obscodes",    required_argument, 0, 'o'},
   {"config-path", required_argument, 0, 'p'},
   {0, 0, 0, 0}
};
_Bool configSpec = 0;
_Bool modelSpec = 0;
_Bool ocdSpec = 0;
_Bool pathSpec = 0;

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

char *fnConfig = "digest2.config";
char *fnModel  = "digest2.model";
char *fnOcd    = "digest2.obscodes";
char *fpConfig = "";

site siteTable[2000];
int classCompute[D2CLASSES];
int classColumn[D2CLASSES];
int nClassCompute;
int nClassColumns;
_Bool classPossible;
_Bool raw, noid;
_Bool headings, rms;
int outputLineSize;
char *outputLine;

char msgConfig[]  = "Unrecognized line in config file:  %s\n";
char msgMemory[] = "Memory allocation failed.\n";
char msgOpen[]   = "Open %s failed.\n";
char msgRead[]   = "Read %s failed.\n";
char msgStatus[] = "Internal error:  Unexpected tracklet status.\n";
char msgThread[] = "Thread creation failed.\n";
char msgOption[] = "Unknown option: %s\n";
char msgUsage[]  = "\
Usage: digest2 [options] <obsfile>    score observations in file\n\
       digest2 [options] -            score observations from stdin\n\
       digest2 -h or --help           display help and quick reference\n\
       digest2 -v or --version        display version information\n\
\n\
Options:\n\
       -c or --config <config-file>\n\
       -m or --model <model-file>\n\
       -o or --obscodes <obscode-file>\n\
       -p or --config-path <path>\n";

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
   FILE * fmuk = openCP(fnModel, modelSpec);
   if (!fmuk)
      fatal1(msgOpen, fnModel);

   if (!fread(modelAllSS, sizeof modelAllSS, 1, fmuk) ||
       !fread(modelUnkSS, sizeof modelUnkSS, 1, fmuk) ||
       !fread(modelAllClass, sizeof modelAllClass, 1, fmuk) ||
       !fread(modelUnkClass, sizeof modelUnkClass, 1, fmuk))
      fatal1(msgRead, fnModel);

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
   memset(tk->class, 0, nClassCompute * sizeof(perClass));
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

   // working with 12 character designation field was expedient so far.
   // now compact it to save output columns:  if 5 character field is
   // non-blank, shift it into 7 character field.
   if (strncmp(tk->desig, "     ", 5)) {
       tk->desig[5] = ' ';
       tk->desig[6] = ' ';
       strncpy(tk->desig+7, tk->desig, 5);
   }

   if (tk->lines == 1) {
      printf("%s  single observation.  skipped.\n", tk->desig+5);
      ringAdd(tk);
      return;
   }

   // select first and last observations
   observation *obsFirst = tk->olist;
   observation *obsLast = obsFirst + tk->lines - 1;

   // sanity check on time
   if (obsLast->mjd < obsFirst->mjd) {
      printf("%s  observations out of order.\n", tk->desig+5);
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
      int len = snprintf(outputLine, outputLineSize, "%s", tk->desig+5);
      if (rms)
         len += snprintf(outputLine + len, outputLineSize - len,
            " %5.2f", tk->rms);
      perClass *cl;
      int c;
      if (classPossible) {
         // specified columns first
         for (c = 0; c < nClassColumns; c++) {
            cl = tk->class + classColumn[c];
            if (raw)
               len += snprintf(outputLine + len, outputLineSize - len,
                  " %3.0f", cl->rawScore);
            if (noid)
               len += snprintf(outputLine + len, outputLineSize - len,
                  " %3.0f", cl->noIdScore);
         }
         // then other possibilities
         for (c = 0; c < D2CLASSES; c++) {
            int cc;
            for (cc = 0; cc < nClassColumns && classColumn[cc] != c; cc++)
                ;
            if (cc < nClassColumns)
                continue;  // already in a column
            // else output if possible
            cl = tk->class + c;
            double pScore = noid ? cl->noIdScore : cl->rawScore;
            if (pScore > .5)
               len += snprintf(outputLine + len, outputLineSize - len,
                  " (%s %.0f)", classAbbr[c], pScore);
            else if (pScore > 0)
               len += snprintf(outputLine + len, outputLineSize - len,
                  " (%s <1)", classAbbr[c]);

         }
      } else {
         // other possibilities not computed.
         for (c = 0, cl = tk->class; c < nClassCompute; c++, cl++) {
            if (raw)
               len += snprintf(outputLine + len, outputLineSize - len,
                  " %3.0f", cl->rawScore);
            if (noid)
               len += snprintf(outputLine + len, outputLineSize - len,
                  " %3.0f", cl->noIdScore);
         }
      }
      puts(outputLine);

      // work done
      ringAdd(tk);
   }
   return NULL;
}

FILE *openCP(char *fn, _Bool spec) {
   if (!spec && pathSpec) {
      char *p = malloc(strlen(fpConfig) + strlen(fn) + 2);
      sprintf(p, "%s/%s", fpConfig, fn);
      fn = p;
   }
   return fopen(fn, "r");
}

void readConfig() {
   FILE *fcfg = openCP(fnConfig, configSpec);

   if (!fcfg) {
      if (!configSpec)
         // config file not required to exist unless a config file name
         // is specified on the command line
	     return;

      fatal1(msgOpen, fnConfig);
   }

   char line[20];
   if (!fgets(line, sizeof(line), fcfg)) {
      printf(msgRead, fnConfig);
      if (!configSpec)
         return;
      exit(-1);
   }

   _Bool rawSpec = 0;
   _Bool classSpec = 0;
   do {
      if (line[strlen(line)-1] == '\n')
         line[strlen(line)-1] = 0;

      if (*line == 0 || *line == '#')
         continue; // skip empty lines and comments

      if (!strcmp(line, "headings")) {
         headings = 1;
         continue;
      }
      if (!strcmp(line, "noheadings")) {
         headings = 0;
         continue;
      }
      if (!strcmp(line, "rms")) {
         rms = 1;
         continue;
      }
      if (!strcmp(line, "norms")) {
         rms = 0;
         continue;
      }
      if (!strcmp(line, "raw")) {
         if (!rawSpec) {
            rawSpec = 1;
            noid = 0;
         }
         raw = 1;
         continue;
      }
      if (!strcmp(line, "noid")) {
         if (!rawSpec) {
            rawSpec = 1;
            raw = 0;
         }
         noid = 1;
         continue;
      }
      if (!strcmp(line, "poss")) {
         if (!classSpec) {
            classSpec = 1;
            nClassColumns = 0;
         }
         classPossible = 1;
         continue;
      }

      for (int c = 0; ; c++) {
         if (c == D2CLASSES)
			fatal1(msgConfig, line);
         if (!strcmp(line, classHeading[c]) || !strcmp(line, classAbbr[c])) {
            if (!classSpec) {
               classSpec = 1;
               nClassColumns = 0;
               classPossible = 0;
            }
            classColumn[nClassColumns++] = c;
            break;
         }
      }
   }
   while
      (fgets(line, sizeof(line), fcfg));

   // by default, we were going to compute all classes, but if classes
   // have been specified here and poss was not specified, then only
   // the specified classes need to be computed.
   if (classSpec && !classPossible)
      for (nClassCompute = 0; nClassCompute < nClassColumns; nClassCompute++)
          classCompute[nClassCompute] = classColumn[nClassCompute];
}

char *parseCl(int argc, char **argv) {
   while (1) {
      int ox;
	  int oc = getopt_long(argc, argv, sOpt, lOpt, &ox);

      switch (oc) {
      case 'h':
         puts("\
Digest2 help\n\
\n\
Digest2 uses statistical ranging techniques on short arc astrometry to\n\
compute probabilities that observed objects are of various orbit classes.\n\
Input is a file of 80 column MPC-format observations, with at least two\n\
observations per object.  Output is orbit class scores for each object.\n\
\n\
Config file keywords:\n\
   headings\n\
   noheadings\n\
   rms\n\
   norms\n\
   raw\n\
   noid\n\
   poss\n\
\n\
Orbit classes:");
         for (int c = 0; c < D2CLASSES; c++)
            printf("   %-5s %-15s\n",classAbbr[c],classHeading[c]);
         puts("\nSee README for additional information.");
         exit(0);
      case 'v':
         puts("Digest2 version 0.10");
         puts("Released Apr 19 2011");
         printf("Compiled %s\n", __DATE__);
         exit(0);
      case 'c':
         fnConfig = optarg;
         configSpec = 1;
         break;
      case 'm':
         fnModel = optarg;
         modelSpec = 1;
         break;
      case 'o':
         fnOcd = optarg;
         ocdSpec = 1;
         break;
      case 'p':
         fpConfig = optarg;
         pathSpec = 1;
         int last = strlen(fpConfig)-1;
         if (fpConfig[last] == '/')
            fpConfig[last] = 0;
         break;
      case -1:
         // exactly one arg should be left, the input observation file
         if (optind != argc-1)
            fatal(msgUsage); // no arg left
         char *fnObs = argv[optind];
         // the single character '-' is allowed for the arg and means
         // read from stdin.
         if (fnObs[0] == '-' && fnObs[1] != 0)
            fatal(msgUsage); // "--" or -anything else is invalid
         return argv[optind];
      default:
         fatal(msgUsage);
      }
   }
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

   - results are text on stdout.
*/
int main (int argc, char **argv) {
   char *fnObs = parseCl(argc, argv); // sets up globals and terminates on error

   FILE *fobs = strcmp(fnObs, "-")
      ? fopen(fnObs, "r")   // test that file can be opened
      : stdin;
   if (!fobs)
      fatal1(msgOpen, fnObs);

   // 83 = 80 column record + optional cr + nl + terminating 0
   const int LINE_SIZE = 83;
   char line[LINE_SIZE];
   if (!fgets(line, LINE_SIZE, fobs))  // test that file can be read
      fatal1(msgRead, argv[1]);

   // three more that set up globals and terminate on error
   initGlobals();
   readMpcOcd();
   readModel();

   // default configuration
   classPossible = 1;
   nClassColumns = 4;
   classColumn[0] = 0; // MPC interesting.  see d2model.c
   classColumn[1] = 1; // neo
   classColumn[2] = 2; // n22
   classColumn[3] = 3; // n18
   for (nClassCompute = 0; nClassCompute < D2CLASSES; nClassCompute++)
      classCompute[nClassCompute] = nClassCompute;
   headings = 1;
   rms = 1;
   raw = 0;
   noid = 1;

   readConfig(); // configures globals and terminates on error

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
         ? nClassColumns
            ? " Other Possibilities"
            : " Possibilities"
         : "");
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

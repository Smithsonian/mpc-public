//! C99

/* gcr.c

Copyright (c) 2010 Sonia Keys

See external file LICENSE, distributed with this software.
*/

// POSIX for getopt()
#define _POSIX_C_SOURCE 2

#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "gcf.h"

#define LINE_SIZE 83

typedef struct {
   char   line[LINE_SIZE];
   char   line2[LINE_SIZE];
   char   desig[13];
   double mjd;
   double ra;
   double dec;
   double mag;
} observation;

typedef struct {
   int nObs;
   int oCap;
   observation *olist;
} tracklet;

char *msgOpen = "Open %s failed.\n";
char *msgRead = "Read %s failed.\n";
char *msgWrite = "Write %s failed.\n";
char *msgMemory = "Memory allocation failed.";
char *msgUsage = "Usage:  gcr [options] <obsfile>\n\
Options:\n\
   -c <rms cutoff>  -- set cutoff, in arc seconds.\n\
   -p <pass file>   -- create file with tracklets with rms < cutoff.\n\
   -f <fail file>   -- create file with tracklets with rms >= cutoff.\n\
   -q               -- quiet.  supress normal output.\n\
   -h               -- print program help.";
char *msgHelp = "\n\
Obsfile is required and must be a file of 80 column MPC format observations.\n\
By default, statistics are printed to stdout.  If any of the options\n\
-c -p -f or -q are used, pass file and fail file are created.  Valid\n\
tracklets in the input are copied into one of the two files depending on\n\
the computed rms.";

_Bool split;
_Bool quiet;
double rmsCutoff;
char *passFile;
char *failFile;
FILE *fpass;
FILE *ffail;

void fatal(char *msg) {
   puts(msg);
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

_Bool parseMpc80(observation *obsp) {
   if (strlen(obsp->line) < 80)
      return 0;
   char line[80];
   strncpy(line, obsp->line, 80);
   line[12] = 0;
   memcpy(obsp->desig, line, 13);
   if (obsp->line[14] == 's')
      return 1;
   if (line[14] != 'C' && line[14] != 'S')
      return 0;
   obsp->line2[14] = 0;
   // parse right to left so we can punch line with zeros as needed
   line[70] = 0;
   errno = 0;
   // strtod meets our needs here to return 0 without error on blank input
   obsp->mag = strtod(line+65, 0);
   line[56] = 0;
   // other fields are required.  use mustStrtod.
   double decs = mustStrtod(line+51);
   line[50] = 0;
   int decm = mustStrtoi(line+48);
   line[47] = 0;
   int decd = mustStrtoi(line+45);
   char decg = line[44];
   line[44] = 0;
   double ras = mustStrtod(line+38);
   line[37] = 0;
   int ram = mustStrtoi(line+35);
   line[34] = 0;
   int rah = mustStrtoi(line+32);
   line[32] = 0;
   double day = mustStrtod(line+23);
   line[22] = 0;
   int month = mustStrtoi(line+20);
   line[19] = 0;
   int year = mustStrtoi(line+15);
   if (errno)
      return 0;
   static int flookup[] =
      {0, 306, 337, 0, 31, 61, 92, 122, 153, 184, 214, 245, 275};

   int z = year + (month-14)/12;
   int m = flookup[month] + 365*z + z/4 - z/100 + z/400 - 678882;
   obsp->mjd = m + day;
   obsp->ra = ((rah*60+ram)*60 + ras) * M_PI / (12 * 3600);
   double dec = ((decd*60+decm)*60 + decs) * M_PI / (180 * 3600);
   obsp->dec = decg == '-' ? -dec : dec;
   return 1;
}

void evaltk(tracklet *tk) {
   int nObs = tk->nObs;

   if (!nObs)
      return;

   double t[nObs];
   double c[nObs][2];
   for (int i = 0; i < nObs; i++) {
      t[i] = tk->olist[i].mjd;
      c[i][0] = tk->olist[i].ra;
      c[i][1] = tk->olist[i].dec;
   }
   gcfparam gcf;
   gcf.nObs = nObs;
   double nt[nObs];
   double rs[nObs][2];
   gcf.ntime = nt;
   gcf.rs = rs;
   gcFit(&gcf, t, c);
   double res[nObs][2];
   double rms = gcRmsRes(&gcf, res);
   if (!quiet) {
      printf("%s    %7.2f\n",tk->olist->desig,rms);
      for (int i = 0; i < nObs; i++)
          printf("%12.6f %6.2f %6.2f\n",t[i],res[i][0],res[i][1]);
   }
   if (split)
      for (int i = 0; i < nObs; i++) {
         FILE *ofile = rms < rmsCutoff ? fpass : ffail;
         fputs(tk->olist[i].line, ofile);
         if (tk->olist[i].line[14] == 'S' && tk->olist[i].line2[14] == 's')
            fputs(tk->olist[i].line2, ofile);
      }
}

void continuetk(tracklet *tk, observation *obsp) {
   int p = tk->nObs;
   if (!p)
      return;
   observation *obs1 = tk->olist + p;
   if (obsp->line[14] == 's') {
      if ((--obs1)->line[14] == 'S' && !strcmp(obsp->desig, obs1->desig))
         strcpy(obs1->line2, obsp->line);
      return;
   }
   if (++tk->nObs > tk->oCap) {
      tk->oCap += 10;
      tk->olist = realloc(tk->olist, tk->oCap * sizeof(observation));
      if (!tk->olist)
         fatal(msgMemory);
   }
   memcpy(obs1, obsp, sizeof(observation));
}

void resettk(tracklet *tk, observation *obsp) {
   tk->nObs = 1;
   memcpy(tk->olist, obsp, sizeof(observation));
}

int main(int argc, char **argv) {

   int c;

   while ((c = getopt (argc, argv, "c:f:p:qh")) != -1)
      switch (c) {
      case 'c':
         rmsCutoff = atof(optarg);
         split = 1;
         if (rmsCutoff <= 0)
            fatal("-c Invalid RMS Cutoff");
         continue;
      case 'f':
         failFile = optarg;
         split = 1;
         continue;
      case 'p':
         passFile = optarg;
         split = 1;
         continue;
      case 'q':
         quiet = 1;
         split = 1;
         continue;
      case 'h':
         puts("");
         puts(msgUsage);
         fatal(msgHelp);
      default:
         fatal(msgUsage);
      }

   // argv[1] is input file of observations
   if (argc - optind != 1)             // test that filename arg is supplied
      fatal(msgUsage);

   char *fileIn = argv[optind];
   FILE *fobs = fopen(fileIn, "r");    // test that file can be opened
   if (!fobs)
      fatal1(msgOpen, fileIn);

   observation obs;
   if (!fgets(obs.line, LINE_SIZE, fobs))  // test that file can be read
      fatal1(msgRead, fileIn);

   if (split) {
      if (rmsCutoff == 0.)
         rmsCutoff = 2.;

      int fileInLen = strlen(fileIn);
      if (fileIn[fileInLen - 1] == '.')
         fileInLen--;

      if (!passFile) {
         if (!(passFile = malloc(fileInLen + 6)))
            fatal(msgMemory);
         memcpy(passFile, fileIn, fileInLen);
         memcpy(passFile + fileInLen, ".pass", 6);
      }

      if (!failFile) {
         if (!(failFile = malloc(fileInLen + 6)))
            fatal(msgMemory);
         memcpy(failFile, fileIn, fileInLen);
         memcpy(failFile + fileInLen, ".fail", 6);
      }

      if (!(fpass = fopen(passFile, "w")))
         fatal1(msgOpen, passFile);
      if (!(ffail = fopen(failFile, "w")))
         fatal1(msgOpen, failFile);
   }

   char desig[13];
   tracklet tk;
   tk.nObs = 0;
   tk.oCap = 5;
   tk.olist = malloc(tk.oCap * sizeof(observation));
   if (!tk.olist)
      fatal(msgMemory);

   if (!quiet) {
      puts("");
      puts(" designation     2d rms");
      puts("  mjd            ra    dec");
      puts("--------------------------");
   }

   do {
      if (!parseMpc80(&obs))
         continue;

      if (strcmp(obs.desig, desig)) {
         evaltk(&tk);
         resettk(&tk, &obs);
         strcpy(desig, obs.desig);
      } else
         continuetk(&tk, &obs);
   }
   while
      (fgets(obs.line, LINE_SIZE, fobs));

   evaltk(&tk);
}

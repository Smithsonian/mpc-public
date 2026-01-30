//! C99

/* gcr.c

Copyright (c) 2010 Sonia Keys

See external file LICENSE, distributed with this software.
*/

#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "gcf.h"

typedef struct {
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

_Bool parseMpc80(char *line, observation *obsp) {
   if (line[14] != 'C' && line[14] != 'S')
      return 0;
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
   line[12] = 0;
   return 1;
}

void evaltk(tracklet *tk, char *desig) {
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
   printf("%s    %7.2f\n",desig,rms);
   for (int i = 0; i < nObs; i++)
       printf("%12.6f %6.2f %6.2f\n",t[i],res[i][0],res[i][1]);
}

void continuetk(tracklet *tk, observation *obsp) {
   int p = tk->nObs;
   if (++tk->nObs > tk->oCap) {
      tk->oCap += 10;
      tk->olist = realloc(tk->olist, tk->oCap * sizeof(observation));
      if (!tk->olist) {
         puts("memory allocation failed");
         exit(-1);
      }
   }
   memcpy(tk->olist+p, obsp, sizeof(observation));
}

void resettk(tracklet *tk, observation *obsp) {
   tk->nObs = 1;
   memcpy(tk->olist, obsp, sizeof(observation));
}

int main(int argc, char **argv) {
   // argv[1] is input file of observations
   if (argc != 2) {                     // test that arg is supplied
      puts("Usage: gcr <obsfile>");
      return -1;
   }

   FILE *fobs = fopen(argv[1], "r");    // test that file can be opened
   if (!fobs) {
      puts("Open failed");
      return -1;
   }

   const int LINE_SIZE = 82;
   char line[LINE_SIZE];
   if (!fgets(line, LINE_SIZE, fobs)) { // test that file can be read
      puts("Read failed");
      return -1;
   }

   char desig[13];
   tracklet tk;
   tk.nObs = 0;
   tk.oCap = 5;
   tk.olist = malloc(tk.oCap * sizeof(observation));
   if (!tk.olist) {
      puts("memory allocation failed");
      return -1;
   }

   puts("");
   puts(" designation     2d rms");
   puts("  mjd            ra    dec");
   puts("--------------------------");

   do {
      observation obs;

      if (!parseMpc80(line, &obs))
         continue;

      if (strcmp(line, desig)) {
         evaltk(&tk, desig);
         resettk(&tk, &obs);
         strcpy(desig, line);
      } else
         continuetk(&tk, &obs);
   }
   while
      (fgets(line, LINE_SIZE, fobs));

   evaltk(&tk, desig);
   fclose(fobs);
}

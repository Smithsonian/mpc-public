//! C99

/* muk.c

Copyright (c) 2010 Sonia Keys

See external file LICENSE, distributed with this software.

-------------------------------------------------------------------------------
muk.c

This program preprocesses an asteroid model for use by Digest2.

There are two inputs.  A model of the predicted entire asteroid population, and
a list of known asteroids.  The predicted model is S3M, a list of synthetic
orbits.  The list of known asteroids is astorb.dat.

Digest2 uses the 4-D histogram format in variations that allow it
to easily compute statistics.  The variations are:

all_ss:      The input model, binned into the histogram.
unk_ss:      A subset of the model representing only undiscovered objects.
all_class:   A subset of the model with only orbits of a certain class, such
             as "NEO"
unk_class:   A subset of the model representing only undiscovered
             objects of the class.

These arrays are dumped to the file digest2.muk as program output.

-------------------------------------------------------------------------------
Some notes on use of astorb.dat:

The "No-ID" score of digest2 is meaningful when applied to observations which
have failed to identify with known objects.  Thus, the meaning of "known" to
this program is "objects which are reliably identifiable given the short arcs
input to Digest2."  This set is not well defined, especially without knowledge
of identification techniques used.  This program uses ephemeris uncertainty
though, as a simple way of selecting a subset of cataloged objects that would
likely identify.

Astorb.dat was chosen because it is easy to obtain and use and because it
provides computed ephemeris uncertainties.  Of the various uncertainties
provided.  This program uses Parameter 24, which is a peak uncertainty over a
period of at least ten years, and it selects asteroids with an uncertainty of 1
arc minute or less.
*/

#include <errno.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "d2model.h"

#define LINE_SIZE 300

// structure of binned population model

double  all_ss      [QX][EX][IX][HX];
double  known_ss    [QX][EX][IX][HX];
double  unk_ss      [QX][EX][IX][HX];
double  all_class   [D2CLASSES][QX][EX][IX][HX];
double  known_class [D2CLASSES][QX][EX][IX][HX];
double  unk_class   [D2CLASSES][QX][EX][IX][HX];

int nAll;
int nClass[D2CLASSES];

void fatal(char *msg) {
   puts(msg);
   exit(-1);
}

void fatal1(char *msg, char *arg) {
   printf(msg, arg);
   exit(-1);
}

int main() {
   char *fn = "s3m.dat";
   FILE *fs3m = fopen(fn, "r");
   if (!fs3m) {
      printf("Open %s failed\n", fn);
      return -1;
   }

   char line[300];
   fgets(line, sizeof(line), fs3m);
   if (strcmp(line, "S3M binned\n"))
      fatal1("muk: unexpected format in %s line 1.\n", fn);
   fgets(line, sizeof(line), fs3m);
   if (strcmp(line,"q 0.4 0.7 0.8 0.9 1 1.1 1.2 1.3 1.4 1.5 1.67 1.8 2 2.2 2.4 2.6 2.8 3 3.2 3.5 4 4.5 5 5.5 10 20 30 40 100\n"))
      fatal1("muk: unexpected format in %s line 2.\n", fn);
   fgets(line, sizeof(line), fs3m);
   if (strcmp(line, "e 0.1 0.2 0.3 0.4 0.5 0.7 0.9 1.1\n"))
      fatal1("muk: unexpected format in %s line 3.\n", fn);
   fgets(line, sizeof(line), fs3m);
   if (strcmp(line, "i 2 5 10 15 20 25 30 40 60 90 180\n"))
      fatal1("muk: unexpected format in %s line 4.\n", fn);
   fgets(line, sizeof(line), fs3m);
   if (strcmp(line, "h 6 8 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25.5\n"))
      fatal1("muk: unexpected format in %s line 5.\n", fn);

   float n;
   int c,iq,ie,ii,ih;
   for (iq = 0; iq < QX; iq++)
      for (ie = 0; ie < EX; ie++)
         for (ii = 0; ii < IX; ii++)
            for (ih = 0; ih < HX; ih++) {
               if (fscanf(fs3m, " %g", &n) != 1)
                  fatal1("muk: unexpected format in %s. bin count expected.\n", fn);

               all_ss[iq][ie][ii][ih] = n;
               nAll += n;
            }

   for (c = 0; c < D2CLASSES; c++) {
      fgets(line, sizeof(line), fs3m);
      fgets(line, sizeof(line), fs3m);
      line[strlen(classHeading[c])] = 0;
      if (strcmp(line, classHeading[c]))
         fatal1("muk: unexpected format in %s. class name expected.\n", fn);

      for (iq = 0; iq < QX; iq++)
         for (ie = 0; ie < EX; ie++)
            for (ii = 0; ii < IX; ii++)
               for (ih = 0; ih < HX; ih++) {
                  if (fscanf(fs3m, " %g", &n) != 1)
                     fatal1("muk: unexpected format in %s. class bin count expected.\n", fn);

                  all_class[c][iq][ie][ii][ih] = n;
                  nClass[c] += n;
               }
   }

   printf("%d orbits in s3m\n", nAll);

   for (c = 0; c < D2CLASSES; c++)
      printf("   %13.13s %8d\n", classHeading[c], nClass[c]);

   fn = "astorb.dat";
   printf("Reading %s:\n", fn);
   FILE * forb = fopen(fn, "r");
   if (!forb) {
      printf("Open %s failed.\n", fn);
      return(-1);
   }

   if (!fgets(line, LINE_SIZE, forb)) {
      printf("Read %s failed.\n", fn);
      fclose(forb);
      return(-1);
   }

   int lines = 0;
   int good = 0;
   int decpeuy_fails = 0;
   int decpeu_rejects = 0;
   int parsefails = 0;
   int outofmodel = 0;
   do {
      lines++;
      line[246] = 0; /* ok to step on month */
      int decpeuy = atoi(line+242);
      if (errno || decpeuy < 2000) {
         decpeuy_fails++;
         continue;
      }
      line[241] = 0; /* ok, this is just a space */
      double decpeu = atof(line+234);
      if (errno || decpeu > 60.) {
         decpeu_rejects++;
         continue;
      }
      line[181] = 0; /* just a space */
      double a = atof(line+169);
      if (errno) {
         parsefails++;
         continue;
      }
      line[168] = 0;
      double e = atof(line+158);
      if (errno) {
         parsefails++;
         continue;
      }
      line[157] = 0;
      double i = atof(line+147);
      if (errno) {
         parsefails++;
         continue;
      }
      line[47] = 0;
      double h = atof(line+42);
      if (errno) {
         parsefails++;
         continue;
      }

      double q = a * (1 - e);
      int bin[4];
      if (!qeihToBin(q, e, i, h, bin)) {
         outofmodel++;
         continue;
      }

      good++;
      int iq = bin[0];
      int ie = bin[1];
      int ii = bin[2];
      int ih = bin[3];
      known_ss[iq][ie][ii][ih]++;

      for (c = 0; c < D2CLASSES; c++)
         if ((*isClass[c])(q, e, i, h))
            known_class[c][iq][ie][ii][ih]++;
   }
   while
      (fgets(line, LINE_SIZE, forb));
   fclose(forb);

   printf("%d lines in astorb.dat\n", lines);
   if (parsefails)
      printf("%d parse fails\n", parsefails);
   printf("%d decpeuy fails\n", decpeuy_fails);
   printf("%d decpeu rejects\n", decpeu_rejects);
   printf("%d out of model\n", outofmodel);
   printf("%d usable\n", good);

   // done computing "known" model.  now fix up "all" model to be consistent
   // with known.  That is, expand all_ss as needed where known population
   // exceedes model population. */
   for (iq = 0; iq < QX; iq++)
      for (ie = 0; ie < EX; ie++)
         for (ii = 0; ii < IX; ii++)
            for (ih = 0; ih < HX; ih++) {
               if (known_ss[iq][ie][ii][ih] > all_ss[iq][ie][ii][ih])
                  all_ss[iq][ie][ii][ih] = known_ss[iq][ie][ii][ih];
               for (c = 0; c < D2CLASSES; c++)
                  if (known_class[c][iq][ie][ii][ih] > all_class[c][iq][ie][ii][ih])
                     all_class[c][iq][ie][ii][ih] = known_class[c][iq][ie][ii][ih];
            }

   // done with "known" and "all".  "unk" is now computed as the difference.
   // as a final step here, bins are scaled by the sqrt of their "volume."
   // this is because bin partions are variable size, so the four-dimensional
   // bin volume varies.  digest2 searches for the intersection of a 2d
   // surface through this 4d space.  the count that is meaningful to
   // accumulate then, is a 2d slice of the 4d bin, that is, the square root.
   double q0, e0, i0, h0;
   double q1, e1, i1, h1;
   double dq, dqe, dqei, isqv;
   q0 = 0;
   for (iq = 0; iq < QX; iq++) {
      q1 = qpart[iq];
      dq = q1 - q0;
      q0 = q1;
      e0 = 0;
      for (ie = 0; ie < EX; ie++) {
         e1 = epart[ie];
         dqe = dq*(e1 - e0);
         e0 = e1;
         i0 = 0;
         for (ii = 0; ii < IX; ii++) {
            i1 = ipart[ii];
            dqei = dqe*(i1 - i0);
            i0 = i1;
            h0 = 0;
            for (ih = 0; ih < HX; ih++) {
               h1 = hpart[ih];
               isqv = 1/sqrt(dqei*(h1 - h0));
               h0 = h1;
               unk_ss[iq][ie][ii][ih] = (all_ss[iq][ie][ii][ih] -
                  known_ss[iq][ie][ii][ih]) * isqv;
               all_ss[iq][ie][ii][ih] *= isqv;
               for (c = 0; c < D2CLASSES; c++) {
                  unk_class[c][iq][ie][ii][ih] = (all_class[c][iq][ie][ii][ih] -
                     known_class[c][iq][ie][ii][ih]) * isqv;
                  all_class[c][iq][ie][ii][ih] *= isqv;
               }
            }
         }
      }
   }

   // done with computations.  create output.
   fn = "digest2.model";
   FILE * fmuk = fopen(fn, "w");
   if (!fmuk) {
      printf("Create %s failed", fn);
      return(-1);
   }

   if (!fwrite(all_ss, sizeof all_ss, 1, fmuk) ||
       !fwrite(unk_ss, sizeof unk_ss, 1, fmuk) ||
       !fwrite(all_class, sizeof all_class, 1, fmuk) ||
       !fwrite(unk_class, sizeof unk_class, 1, fmuk)) {
      printf("Error writing %s.", fn);
      fclose(fmuk);
      return(-1);
   }

   fclose(fmuk);
   return(0);
}

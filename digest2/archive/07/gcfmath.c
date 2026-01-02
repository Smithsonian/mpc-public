//! C99

/* gcfmath.c

Copyright (c) 2010 Sonia Keys

See external file LICENSE, distributed with this software.

-------------------------------------------------------------------------------
gcfmath.c

Math for great circle fit and residual calculator.  Input is observation
triples of time, RA, and Dec.  Code here least-squares fits a great circle
to RA and Dec with time as the independent variable.  It also computes
residuals and an RMS of the residuals.
*/

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "gcf.h"

const double TWO_PI = 2 * M_PI;

// one arc second, in radians;
const double arcsecrad = M_PI / (180 * 3600);

// rotation tolerance = 1 arc sec.  roughly, if I rotate something and
// it doesn't end up within an arc second of where I expect, there's a
// problem.
const double rtol = M_PI / (180 * 3600);

/* dot3

vector dot product
*/
double dot3(double a1[3], double a2[3]) {
   return a1[0]*a2[0] + a1[1]*a2[1] + a1[2]*a2[2];
}

/* cross3

vector cross product

Args:
   a, b:  three element vectors of double

Returns:
   a x b
*/
void cross3(double result[3], double a[3], double b[3]) {
   result[0] = a[1]*b[2] - a[2]*b[1];
   result[1] = a[2]*b[0] - a[0]*b[2];
   result[2] = a[0]*b[1] - a[1]*b[0];
} 

/* dSphr2Cart

Spherical (RA, Dec, in radians) to Cartesian (X, Y, Z unit vector)

operates on arrays of coordinate tuples.
first parameter is length of arrays.
*/
void dSphr2Cart(int len, double s[len][2], double c[len][3]) {
   for (int i = 0; i < len; i++) {
      double t = cos(s[i][1]);
      c[i][0] = t * cos(s[i][0]);
      c[i][1] = t * sin(s[i][0]);
      c[i][2] = sin(s[i][1]);
   }
}

void dCart2Sphr(int len, double c[len][3], double s[len][2]) {
   for (int i = 0; i < len; i++) {
      s[i][0] = fmod(atan2(c[i][1],c[i][0])+TWO_PI,TWO_PI);
      s[i][1] = atan2(c[i][2],sqrt(dot3(c[i],c[i])));
   }
}

/* mult3

matrix multiplication, specialized to broadcast multiplication of
a 3 by 3 (rotation matrix) to n rows individually.

Input args:
   rm  -- 3 by 3
   a   -- n by 3 -- multiplication is broacast to each row.  

Result:
   rm x a -- n by 3 again.
*/

void mult3(int n, double result[n][3], double rm[3][3], double a[n][3]) {
  for (int i = 0; i < n; i++)
     for (int r = 0; r < 3; r++) {
        double s = 0;
        for (int c = 0; c < 3; c++)
           s += rm[r][c] * a[i][c];
        result[i][r] = s;
  }
}

void transpose3(double m[3][3]) {
   double t = m[0][1];
   m[0][1] = m[1][0];
   m[1][0] = t;
   t = m[0][2];
   m[0][2] = m[2][0];
   m[2][0] = t;
   t = m[1][2];
   m[1][2] = m[2][1];
   m[2][1] = t;
}

/* gcFit

Great circle fit.

Args:
   gcf  -- great circle fit parameters, can be used in subsequent calls
           to statistics functions
   mjd  -- mjd times of observations
   sphr -- ra, dec, in radians
*/
void gcFit(gcfparam *gcf, double mjd[gcf->nObs], double sphr[gcf->nObs][2]) {
   int nObs = gcf->nObs;

   // convert obs to cartesian
   double cart[nObs][3];
   dSphr2Cart(nObs, sphr, cart);

   // vector normal to motion
   double n[3];
   cross3(n, cart[0], cart[nObs-1]);
   double nmag2 = dot3(n,n);
   double nmag = sqrt(nmag2);

   // rotation axis is right angle to n projected onto z=0 plane
   // and normalized to unit vector
   double nxy = 1 / sqrt(n[0]*n[0] + n[1]*n[1]);
   double gcix = n[1] * nxy;
   double gciy = -n[0] * nxy;

   // rotation angle is angle from n to +z
   double sina = sqrt(nmag2 - n[2]*n[2]) / nmag;
   double cosa = n[2] / nmag;

   // build mRot, rotation matrix that will rotate the coordinate system
   // to the obs, so that a cylindrical projection will have negligible
   // distortion.)
   double sinagx = sina * gcix;
   double sinagy = sina * gciy;
   double onemcosa = 1 - cosa;
   double onemcosagx = onemcosa * gcix;
   double onemcosagxgy = onemcosagx * gciy;
   gcf->mRot[0][0] = cosa + onemcosagx*gcix;
   gcf->mRot[0][1] = onemcosagxgy;
   gcf->mRot[0][2] = sinagy;
   gcf->mRot[1][0] = onemcosagxgy;
   gcf->mRot[1][1] = cosa + onemcosa*gciy*gciy;
   gcf->mRot[1][2] = -sinagx;
   gcf->mRot[2][0] = -sinagy;
   gcf->mRot[2][1] = sinagx;
   gcf->mRot[2][2] = cosa;

   // rotate all of cart
   double rotated[nObs][3];
   mult3(nObs, rotated, gcf->mRot, cart);

   // transpose rotation array  so it will derotate, after least-squares fit.
   transpose3(gcf->mRot);

   // invariant:  first and last points should be on the z=0 plane
   // of the rotated coordinate system now.
   if (fabs(rotated[0][2]) > rtol || fabs(rotated[nObs-1][2]) > rtol) {
      puts("*** rotation failed ***");
      exit(-1);
   }

   // convert back to spherical coordinates for adjustment.
   // (this does the cylindrical projection.)
   double rs[nObs][2];
   dCart2Sphr(nObs, rotated, rs);

   // normalize ra to near 0 to avoid wraparound problems
   double ra0;
   gcf->ra0 = ra0 = rs[0][0];
   for (int i = 0; i < nObs; i++)
      rs[i][0] = fmod(rs[i][0] + 3 * M_PI - ra0, TWO_PI) - M_PI;

   // normalize time to near 0 to maintain precision
   double t0;
   double ntime[nObs];
   gcf->t0 = t0 = mjd[0];
   for (int i = 0; i < nObs; i++)
      ntime[i] = mjd[i] - t0;

   // save copies of rs and ntime;
   memcpy(gcf->rs, rs, sizeof(rs));
   memcpy(gcf->ntime, ntime, sizeof(ntime));

   if (nObs == 2) {
      gcf->r0 = 0;
      gcf->rr = rs[1][0] / ntime[1];
      gcf->d0 = 0;
      gcf->dr = 0;
   } else {
      // here's the least squares stuff
      double sumt = 0;
      double sumra = 0;
      double sumdec = 0;
      double sumt2 = 0;
      double sumtra = 0;
      double sumtdec = 0;
      for (int i = 0; i < nObs; i++) {
         sumt += ntime[i];
         sumra += rs[i][0];
         sumdec += rs[i][1];
         sumt2 += ntime[i] * ntime[i];
         sumtra += ntime[i] * rs[i][0];
         sumtdec += ntime[i] * rs[i][1];
      }
      double invd = 1 / (nObs * sumt2 - sumt * sumt);
      gcf->r0 = invd * (sumra * sumt2 - sumtra * sumt);
      gcf->rr = invd * (nObs * sumtra - sumra * sumt);
      gcf->d0 = invd * (sumdec * sumt2 - sumtdec * sumt);
      gcf->dr = invd * (nObs * sumtdec - sumdec * sumt);
   }
}

void gcPos(gcfparam *gcf, double t, double *ra, double *dec) {
   // compute position on fitted great circle
   double nt = t - gcf->t0;
   double rsc[2];
   double rcc[3];
   double sc[2];
   double cc[3];
   rsc[0] = gcf->r0 + gcf->rr * nt + gcf->ra0;
   rsc[0] = gcf->d0 + gcf->dr * nt;

   // rotate back up to original place in the sky
   dSphr2Cart(1, &rsc, &rcc);
   mult3(1, &cc, gcf->mRot, &rcc);
   dCart2Sphr(1, &cc, &sc);

   // return coordinates
   *ra = sc[0];
   *dec = sc[1];
}

void gcRes(gcfparam *gcf, double res[gcf->nObs][2]) {
   int nObs = gcf->nObs;

   // computed positions on fitted great circle
   double rsc[nObs][2];
   for (int i = 0; i < nObs; i++) {
      rsc[i][0] = gcf->r0 + gcf->rr * gcf->ntime[i];
      rsc[i][1] = gcf->d0 + gcf->dr * gcf->ntime[i];
   }

   // residuals are computed on rotated-and-derotated observed to
   // minimize any systematic errors from rotating and derotating the
   // computed.

   // fix up ra on both observed and computed
   for (int i = 0; i < nObs; i++) {
      gcf->rs[i][0] += gcf->ra0;
      rsc[i][0] += gcf->ra0;
   }

   // rotate both back up to original place in the sky
   double rco[nObs][3];
   double rcc[nObs][3];
   dSphr2Cart(nObs, gcf->rs, rco);
   dSphr2Cart(nObs, rsc, rcc);
   double co[nObs][3];
   double cc[nObs][3];
   mult3(nObs, co, gcf->mRot, rco);
   mult3(nObs, cc, gcf->mRot, rcc);
   double so[nObs][2];
   double sc[nObs][2];
   dCart2Sphr(nObs,co,so);
   dCart2Sphr(nObs,cc,sc);

   for (int i = 0; i < nObs; i++) {
      res[i][1] = (so[i][1] - sc[i][1]) / arcsecrad;
      res[i][0] = (so[i][0] - sc[i][0]) * cos(sc[i][1]) / arcsecrad;
   }
}

/* gcRmsRes

returns rms of 2d residual, and the component ra and dec residuals.

Note:  The 2d residual is the 2d distance between computed and observed.
The rms of the ra and dec residuals considered as separate values--if that's
what you are looking for--is smaller by a factor of sqrt(2).
*/
double gcRmsRes(gcfparam *gcf, double res[gcf->nObs][2]) {
   int nObs = gcf->nObs;
   gcRes(gcf, res);
   double s = 0;
   for (int i = 0; i < nObs; i++)
      s += res[i][0]*res[i][0] + res[i][1]*res[i][1];
   return sqrt(s / nObs);
}

/* gcRms

just return the Rms, never mind the residuals.
*/
double gcRms(gcfparam *gcf) {
   double res[gcf->nObs][2];
   return gcRmsRes(gcf, res);
}


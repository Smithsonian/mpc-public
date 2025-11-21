//! C99

/* d2math.c

Copyright (c) 2010 Sonia Keys
Copyright (c) 2005,2006 Kyle Smalley, Carl Hergenrother, Robert McNaught,
David Asher

See external file LICENSE, distributed with this software.

-------------------------------------------------------------------------------
d2math.c

the heart of digest2.  i/o, file formats, and so on are in other .c files.
this file contains stuff like vector math, orbit calculations, and bin
statistics.  "q" bin model is q, e, i, h, non-uniform bin spacing.
*/

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "digest2.h"

// near distance limit of .05 is kind of arbitrary, but seems to work.
#define MIN_DISTANCE .05
#define MAX_DISTANCE 100.

double K, INV_K, U, TWO_PI;
uint64_t LCGA, LCGM;
double invLCGM;

void initGlobals(void) {
   // a little bit of one time setup 
   K = .01720209895;
   INV_K = 1. / K;
   U = K * K;
   TWO_PI = M_PI * 2.;

   // Random numbers are used in aRange() in this file.  Linear congruential
   // generator (LCG) code is here because library rand() has overhead from
   // thread-safe stuff I don't need.  I use time(0) here to get a different
   // seed for every program run, then rand() in the per-thread setup in
   // main() (in digest2.c) to get a different LCG seed for each thread.
   srand(time(0));
   LCGA = pow(13, 13); // per NAG
   LCGM = 1;
   LCGM <<= 59;
   invLCGM = 1. / LCGM;
   LCGM--;
}

/* se2000

solar ephemeris, J2000

Args:
   mjd

Returns:
   *psun_earth:  sun-earth vector in equatorial coordinates.
   *psoe, *pcoe:  sine and cosine of ecciptic.

Notes:
   Approximate solar coordinates, per USNO.  Originally from
   http://aa.usno.navy.mil/faq/docs/SunApprox.html, page now at
   http://www.usno.navy.mil/USNO/astronomical-applications/
   astronomical-information-center/approx-solar.  Angles on that
   page converted to radians here to simplify computations.
*/
void se2000(double mjd, double *psun_earth, double *psoe, double *pcoe) {
   double d = mjd - 51544.5;
   double g = 6.240058 + .01720197 * d;
   double q = 4.894933 + .01720279 * d;
   double g2 = g + g;

   // ecliptic longitude
   double l = q + .03342306 * sin(g) + .0003490659 * sin(g2);

   // distance in AU
   double r = 1.00014 - .01671 * cos(g) - .00014 * cos(g2);

   // obliquity of ecliptic
   double e = .409088 - 6.283e-9 * d;
   *psoe = sin(e);
   *pcoe = cos(e);

   // equatorial coordinates
   psun_earth[0] = r * cos(l);
   psun_earth[1] = r * sin(l);
   psun_earth[2] = psun_earth[1] * *psoe;
   psun_earth[1] *= *pcoe;
}

/* sub3

compute a1 -= a2 where a1 and a2 are 3-element arrays of doubles.
*/
void sub3(double a1[3], double a2[3]) {
   a1[0] -= a2[0];
   a1[1] -= a2[1];
   a1[2] -= a2[2];
} 

/* ecRotate

rotate to ecliptic coordinates.

Args:
   c:         vector in equatorial coordinates.
   soe, coe:  sine, cosine of eccliptic.

Side effect:
   c rotated in place.
*/
void ecRotate(double c[3], double soe, double coe) {
   double e1 = c[2]*soe + c[1]*coe;
   c[2] = c[2]*coe - c[1]*soe;
   c[1] = e1;
}

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

/* lst

local sidereal time
*/
double lst(double j0, double longitude) {
   double t = (j0 - 15019.5) / 36525.;
   double th = (6.6460656 + (2400.051262 + 0.00002581 * t) * t) / 24.;
   double ut = fmod(1., j0 - .5);
   return fmod(th + ut + longitude, TWO_PI);
}

/* tagAngle (tracklet method)

process a single distance-angle combination.

Args:
   tk:  tracklet with distance setup already done.
   an:  angle for orbit solution

Notes:
   solves orbit for passed angle, converts to bin indicies, sets bin tag
   and updates tag count.
*/
_Bool tagAngle(tracklet *tk, double an) {
   double d2 = tk->observer1_object0_mag * sin(an) / sin(M_PI - an - tk->tz);

   // velocity scaled by gravitational constant
   double v[3];
   for (int i = 0; i < 3; i++)
      v[i] = (d2 * tk->observer_object_unit[1][i] - tk->observer1_object0[i])
         * tk->invdt * INV_K;

   // momentum vector
   double hv[3];
   cross3(hv, tk->sun_object0, v);
   double hsq = dot3(hv, hv);
   double hm = sqrt(hsq);

   // solve for semi-major axis
   // (and the inverse--it comes in handy)
   double vsq = dot3(v, v);
   double temp = 2. - tk->sun_object0_mag * vsq;

   // for model, require a < 6
   // (for stability, require a < 100 anyway)
   if (tk->sun_object0_mag > temp * 6.)
      return 0;

   double orbit_a = tk->sun_object0_mag / temp;
   double inva = temp / tk->sun_object0_mag;

   // solve for eccentricity
   // (stability test on a (above) should keep result real)
   double orbit_e = sqrt(1. - hsq * inva);

   // stability test:  require e < .99
   if (orbit_e > .99)
      return 0;

   // solve for inclination.

   // reliable check for i=0.  handles
   // loss of precision in h computation.
   _Bool izero = hv[2] >= hm;

   // combination of stability tests on a and e (above) should
   // ensure that hm is well above zero.
   double orbit_i = izero ? 0. : acos(hv[2] / hm) * 180. / M_PI;

   int bin[3];
   double q = orbit_a*(1-orbit_e);
   if (!qeiToBin(q, orbit_e, orbit_i, bin))
      return 0;

   int iq = bin[0];
   int ie = bin[1];
   int ii = bin[2];
   int ih = tk->hmag_bin;

   _Bool newTag = 0;

   for (int c = 0; c < nClassConfig; c++) {
      perClass *cl = tk->class + c;
      if ((*isClass[classConfig[c]])(q, orbit_e, orbit_i)) {
         if (!cl->dInClass[iq][ie][ii][ih]) {
            cl->dInClass[iq][ie][ii][ih] = 1;
            newTag = 1;
         }
      } else {
         if (!cl->dOutOfClass[iq][ie][ii][ih]) {
            cl->dOutOfClass[iq][ie][ii][ih] = 1;
            newTag = 1;
         }
      }
   }

   if (newTag)
   {
      tk->dNewTag = 1;
      tk->dTag[iq][ie][ii][ih] = 1;
   }

   return newTag;
}

/* aRange (tracklet method)

recursive function explores the space between two angles (at a set distance)

Args:
   tk:  tracklet with distance setup already done
   ang1, ang2:  search boundaries.

Algorithm:
   - pick mid point.  a little jiggle is thrown in to help find new bins at
     closely adjacent distances.

   - solve angle at mid point.  if it resulted in tagging a new bin, recurse
     both halves.

   - if passed angle range is sufficiently large, recurse.

   - age criterion: if a passed angle recently yielded a new bin, recurse.
*/
void aRange(tracklet *tk, double ang1, double ang2, int age) {
   // see LCG notes above, in this file
   tk->rand = (tk->rand * LCGA) & LCGM;
   double d3 = (ang2 - ang1) / 3.;
   double mid = ang1 + d3 + d3 * tk->rand * invLCGM;

   if (tagAngle(tk, mid) || d3 > .1) {
      aRange(tk, ang1, mid, 0);
      aRange(tk, mid, ang2, 0);
      return;
   }

   if (age < 1) {
      aRange(tk, ang1, mid, age + 1);
      aRange(tk, mid, ang2, age + 1);
   }
}

/* searchDistance (tracklet method)

for specified distance, set up computations and search angle space

Args:
   tk:  tracklet
   d:  distance for computations

Algorithm:
   - setup stuff common to all possible orbits at this distance.  this
     includes some vectors, H magnitude, and limits on possible angles.
     Also tags are reset for the distance.

   - search angle space, which results in tags being set.

   - note newly set tags, and accumulate population totals needed for
     final computation of scores.

Returns:
   true if any new bins were tagged.
   false if this distance saw no bins that hadn't been seen at other distances.
*/
_Bool searchDistance(tracklet *tk, double d) {
   int i;

   tk->dNewTag = 0;

   // solve some distance dependent vectors:
   // observer_object0
   tk->observer_object0_mag = d;
   for (i = 0; i < 3; i++)
       tk->observer_object0[i] =
          tk->observer_object_unit[0][i] * tk->observer_object0_mag;

   // sun_object0
   for (i = 0; i < 3; i++)
       tk->sun_object0[i] = tk->sun_observer[0][i] + tk->observer_object0[i];
   tk->sun_object0_magsq = dot3(tk->sun_object0, tk->sun_object0);
   tk->sun_object0_mag = sqrt(tk->sun_object0_magsq);

   // observer1_object0
   for (i = 0; i < 3; i++)
       tk->observer1_object0[i] = tk->sun_object0[i] - tk->sun_observer[1][i];
   tk->observer1_object0_magsq =
       dot3(tk->observer1_object0, tk->observer1_object0);
   tk->observer1_object0_mag = sqrt(tk->observer1_object0_magsq);

   // solve H mag
   double rdelta = tk->observer_object0_mag * tk->sun_object0_mag;
   double cospsi = dot3(tk->observer_object0, tk->sun_object0) / rdelta;
   double tanhalf,phi1,phi2;

   if (cospsi > -.9999) {
      tanhalf = sqrt(1. - cospsi * cospsi) / (1. + cospsi);
      phi1 = exp(-3.33 * pow(tanhalf, 0.63));
      phi2 = exp(-1.87 * pow(tanhalf, 1.22));
      tk->hmag = tk->vmag
         - 5. * log10(rdelta)
         + 2.5 * log10(.85 * phi1 + .15 * phi2);
   } else
      // object is straight into the sun.  doesn't seem too likely,
      // but anyway, this gives it a valid value.
      tk->hmag = 30.;

   if (!hToBin(tk->hmag, &tk->hmag_bin))
      return 0;

   // solve angle range at this distance
   double th = dot3(tk->observer1_object0, tk->observer_object_unit[1]) /
      tk->observer1_object0_mag;

   tk->tz = acos(th);

   double aa = tk->invdtsq;
   double bb = (-2. * tk->observer1_object0_mag * th) * aa;
   double cc = tk->observer1_object0_magsq * aa - 2. * U / tk->sun_object0_mag;
   double dsc = bb * bb - 4 * aa * cc;

   if (dsc < 0.)
      return 0;

   double sd = sqrt(dsc);
   double sd1 = -sd;
   double inv2aa = .5 / aa;
   double ang1, ang2;
   while (1) {
      double d2 = (-bb + sd1) * inv2aa;
      double d2s = d2 * d2;
      double nns = d2s + tk->observer1_object0_magsq -
         2. * d2 * tk->observer1_object0_mag * th;
      double nn = sqrt(nns);
      double ca = (nns + tk->observer1_object0_magsq - d2s) /
         (2. * nn * tk->observer1_object0_mag);
      double sa = d2 * sin(tk->tz) / nn;
      ang2 = 2. * atan2(sa, 1. + ca);

      if (sd1 == sd)
         break;

      ang1 = ang2;
      sd1 = sd;
   }

   memset(tk->dTag, 0, sizeof(tk->dTag));
   int c = 0;
   perClass *cl = tk->class;
   do {
      memset(cl->dInClass, 0, sizeof(cl->dInClass));
      memset(cl->dOutOfClass, 0, sizeof(cl->dOutOfClass));
      cl++;
      c++;
   } while
      (c < nClassConfig);

   aRange(tk, ang1, ang2, 0);

   if (!tk->dNewTag)
      return 0;

   _Bool newTag = 0;

   for (int iq = 0; iq < QX; iq++)
      for (int ie = 0; ie < EX; ie++)
         for (int ii = 0; ii < IX; ii++)
             for (int ih = 0; ih < HX; ih++) {
                if (tk->dTag[iq][ie][ii][ih] && !tk->tag[iq][ie][ii][ih]) {
                   tk->binsTagged++;
                   tk->tag[iq][ie][ii][ih] = 1;
                }
                perClass *cl = tk->class;
                for (int c = 0; c < nClassConfig; c++, cl++) {
                   if (cl->dInClass[iq][ie][ii][ih]
                         && !cl->tagInClass[iq][ie][ii][ih]) {
                      newTag = 1;
                      cl->tagInClass[iq][ie][ii][ih] = 1;
                      cl->sumAllInClass
                         += modelAllClass[classConfig[c]][iq][ie][ii][ih];
                      cl->sumUnkInClass
                         += modelUnkClass[classConfig[c]][iq][ie][ii][ih];
                   }
                   if (cl->dOutOfClass[iq][ie][ii][ih]
                         && !cl->tagOutOfClass[iq][ie][ii][ih]) {
                      newTag = 1;
                      cl->tagOutOfClass[iq][ie][ii][ih] = 1;
                      cl->sumAllOutOfClass
                         += (modelAllSS[iq][ie][ii][ih]
                            - modelAllClass[classConfig[c]][iq][ie][ii][ih]);
                      cl->sumUnkOutOfClass
                         += (modelUnkSS[iq][ie][ii][ih]
                            - modelUnkClass[classConfig[c]][iq][ie][ii][ih]);
                   }
                }
             }

   return newTag;
}

/* dRange (tracklet method)

recursive function to explore the possible orbit space

Args:
   tk:          tracklet
   d1, d2:      distance limits
   age:         a little history.  0 means a bin was just tagged.  1 is added
                at each level of recursion.

Algorithm:
   much like aRange (above)

   - if new bins were found at mid point, recurse both halves

   - if range is big, recurse anyway

   - if young, recurse
*/

void dRange(tracklet *tk, double d1, double d2, int age) {
   double dmid = (d1 + d2) * .5;

   if (searchDistance(tk, dmid) || d2 - d1 > 1.) {
      dRange(tk, d1, dmid, 0);
      dRange(tk, dmid, d2, 0);
      return;
   }

   if (age < 1) {
      dRange(tk, d1, dmid, age + 1);
      dRange(tk, dmid, d2, age + 1);
   }
}

/* score (tracklet method)

score tracklet.  this is the driver for all the math.

Arg:
   tk:  tracklet.

Preconditions:
   - all globals must be initialized.
   - tk->status must be UNPROC
   - tk->olist must have valid observations
   - tk->lines must say how many
   - tk->vmag must be initialized
   - tk->rand must be odd.
   - with exception of tk->desig and tk->obsCap, which are not used,
     everything else in tk must be zero.
*/
void score(tracklet *tk) {
   // select first and last observations.  others are ignored.
   observation *obsFirst = tk->olist;
   observation *obsLast = obsFirst + tk->lines - 1;

   tk->dt = obsLast->mjd - obsFirst->mjd;
   tk->invdt = 1. / tk->dt;
   tk->invdtsq = tk->invdt * tk->invdt;

   // solve vectors at observation times
   observation *obsp = obsFirst;
   for (int i = 0; i < 2; i++, obsp = obsLast) {
      site *sitep = siteTable + obsp->site;
      double sun_earth[3], soe, coe;
      se2000(obsp->mjd, sun_earth, &soe, &coe);

      // sun-observer vectors in ecliptic coordinates
      double v[3];
      if (obsp->spacebased)
         memcpy(v, obsp->earth_observer, sizeof(v));
      else {
         double th = lst(obsp->mjd, sitep->longitude);
         v[0] = sitep->rhoCosPhi * cos(th);
         v[1] = sitep->rhoCosPhi * sin(th);
         v[2] = sitep->rhoSinPhi;
      }
      sub3(v, sun_earth);
      ecRotate(v, soe, coe);
      memcpy(tk->sun_observer[i], v, sizeof(v));

      // observer-object unit vectors in ecliptic coordinates
      v[0] = cos(obsp->ra) * cos(obsp->dec);
      v[1] = sin(obsp->ra) * cos(obsp->dec);
      v[2] = sin(obsp->dec);
      ecRotate(v, soe, coe);
      memcpy(tk->observer_object_unit[i], v, sizeof(v));
   }

   searchDistance(tk, MIN_DISTANCE);
   searchDistance(tk, MAX_DISTANCE);
   dRange(tk, MIN_DISTANCE, MAX_DISTANCE, 0);

   perClass *cl = tk->class;
   for (int c = 0; c < nClassConfig; c++, cl++) {
      double d = cl->sumAllInClass + cl->sumAllOutOfClass;
      cl->rawScore = d > 0.
         ? 100. * cl->sumAllInClass / d
         : 100.;

      d = cl->sumUnkInClass + cl->sumUnkOutOfClass;
      cl->noIdScore =  d > 0.
         ? 100. * cl->sumUnkInClass / d
         : 100.;
   }
}

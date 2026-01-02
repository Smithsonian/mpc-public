// d2math.c
//
// Public domain.

/*
 * the heart of digest2. i/o, file formats, and so on are in other .c files.
 * this file contains stuff like vector math, orbit calculations, and bin
 * statistics.
 * "q" bin model is q, e, i, h, non-uniform bin spacing.
 */

#include <assert.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "digest2.h"
// near distance limit of .05 is kind of arbitrary, but seems to work.
#define MIN_DISTANCE .05        // AU
#define MAX_DISTANCE 100.       // AU
#define minDistanceStep .2      // AU
#define minAngleStep .1         // radian
#define ageLimit 1
double K, INV_K, U, TWO_PI;
uint64_t LCGA, LCGM;
double invLCGM;
double arcsecrad, rtol;
double obsErr;
regex_t rxObsErr;

void initGlobals(void)
{
  // a little bit of one time setup 
  K = .01720209895;
  INV_K = 1. / K;
  U = K * K;
  TWO_PI = M_PI * 2.;
  arcsecrad = M_PI / (180 * 3600);
  rtol = arcsecrad;

  // Random numbers are used in aRange() in this file.  Linear
  // congruential generator (LCG) code is here because library
  // rand() has overhead from thread-safe stuff I don't need.
  // I use time(0) here to get a different seed for every program run,
  // then rand() in the per-thread setup in main() (in digest2.c)
  // to get a different LCG seed for each thread.
  srand(time(0));
  LCGA = pow(13, 13);           // per NAG
  LCGM = 1;
  LCGM <<= 59;
  invLCGM = 1. / LCGM;
  LCGM--;
  obsErr = 1 * arcsecrad;
  assert(regcomp
         (&rxObsErr, "^[ \t]*([^ \t=]*)[ \t]*=[ \t]*(.+)$", REG_EXTENDED) == 0);
}

/*
 * se2000
 * 
 * solar ephemeris, J2000
 * 
 * Args: mjd
 * 
 * Returns:
 * psun_earth: sun-earth vector in equatorial coordinates.
 * psoe,pcoe: sine and cosine of ecciptic.
 * 
 * Notes: Approximate solar coordinates, per USNO.  Originally from
 * http://aa.usno.navy.mil/faq/docs/SunApprox.html, page now at
 * http://www.usno.navy.mil/USNO/astronomical-applications/
 * astronomical-information-center/approx-solar.  Angles on that page
 * converted to radians here to simplify computations. 
 */
void se2000(double mjd, double *psun_earth, double *psoe, double *pcoe)
{
  // USNO algorithm is in degrees.  To mimimize confusion, work in
  // degrees here too, only converting to radians as needed for trig
  // functions.
  double d = mjd - 51544.5;
  double g = 357.529 + .98560028 * d; // mean anomaly of sun, in degrees
  double q = 280.459 + .98564736 * d; // mean longitude of sun, in degrees
  double g2 = g + g;

  // ecliptic longitude, degrees. (sending radians to trig functions)
  double l = q + 1.915 * sin(g * M_PI / 180.) + .020 * sin(g2 * M_PI / 180.);

  // distance in AU
  double r =
    1.00014 - .01671 * cos(g * M_PI / 180.) - .00014 * cos(g2 * M_PI / 180.);

  // obliquity of ecliptic, degrees
  double e = 23.439 - .00000036 * d;
  *psoe = sin(e * M_PI / 180.);
  *pcoe = cos(e * M_PI / 180.);

  // equatorial coordinates
  psun_earth[0] = r * cos(l * M_PI / 180.);
  psun_earth[1] = r * sin(l * M_PI / 180.);
  psun_earth[2] = psun_earth[1] * *psoe;
  psun_earth[1] *= *pcoe;
}

/*
 * sub3
 * 
 * compute a1 -= a2 where a1 and a2 are 3-element arrays of doubles. 
 */
void sub3(double a1[3], double a2[3])
{
  a1[0] -= a2[0];
  a1[1] -= a2[1];
  a1[2] -= a2[2];
}

/*
 * ecRotate
 * 
 * rotate to ecliptic coordinates.
 * 
 * Args: c: vector in equatorial coordinates. soe, coe: sine, cosine of
 * eccliptic.
 * 
 * Side effect: c rotated in place. 
 */
void ecRotate(double c[3], double soe, double coe)
{
  double e1 = c[2] * soe + c[1] * coe;
  c[2] = c[2] * coe - c[1] * soe;
  c[1] = e1;
}

/*
 * dot3
 * 
 * vector dot product 
 */
double dot3(double a1[3], double a2[3])
{
  return a1[0] * a2[0] + a1[1] * a2[1] + a1[2] * a2[2];
}

/*
 * cross3
 * 
 * vector cross product
 * 
 * Args: a, b: three element vectors of double
 * 
 * Returns: a x b 
 */
void cross3(double result[3], double a[3], double b[3])
{
  result[0] = a[1] * b[2] - a[2] * b[1];
  result[1] = a[2] * b[0] - a[0] * b[2];
  result[2] = a[0] * b[1] - a[1] * b[0];
}

/*
 * lst
 * 
 * local sidereal time 
 */
double lst(double j0, double longitude)
{
  double t = (j0 - 15019.5) / 36525.;
  double th = (6.6460656 + (2400.051262 + 0.00002581 * t) * t) / 24.;
  double ut = fmod(1., j0 - .5);
  return fmod(th + ut + longitude, TWO_PI);
}

/*
 * tagAngle (tracklet method)
 * 
 * process a single distance-angle combination.
 * 
 * Args: tk: tracklet with distance setup already done. an: angle for
 * orbit solution
 * 
 * Notes: solves orbit for passed angle, converts to bin indicies, sets
 * bin tag and updates tag count. 
 */
_Bool tagAngle(tracklet * tk, double an)
{
  double d2 = tk->observer1_object0_mag * sin(an) / sin(M_PI - an - tk->tz);

  // velocity scaled by gravitational constant
  double v[3];
  for (int i = 0; i < 3; i++)
    v[i] =
      (d2 * tk->observer_object_unit[1][i] -
       tk->observer1_object0[i]) * tk->invdt * INV_K;

  // momentum vector
  double hv[3];
  cross3(hv, tk->sun_object0, v);
  double hsq = dot3(hv, hv);
  double hm = sqrt(hsq);

  // solve for semi-major axis
  // (and the inverse--it comes in handy)
  double vsq = dot3(v, v);
  double temp = 2. - tk->sun_object0_mag * vsq;

  // for stability, require a < 100
  if (tk->sun_object0_mag > temp * 100.)
    return 0;

  double orbit_a = tk->sun_object0_mag / temp;
  double inva = temp / tk->sun_object0_mag;

  // solve for eccentricity
  // (stability test on a (above) should keep result real)
  double orbit_e = sqrt(1. - hsq * inva);

  // stability test: require e < .99
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
  double q = orbit_a * (1 - orbit_e);
  if (!qeiToBin(q, orbit_e, orbit_i, bin))
    return 0;

  int iq = bin[0];
  int ie = bin[1];
  int ii = bin[2];
  int ih = tk->hmag_bin;

  _Bool newTag = 0;

  for (int c = 0; c < nClassCompute; c++) {
    perClass *cl = tk->class + c;
    if ((*isClass[classCompute[c]]) (q, orbit_e, orbit_i, tk->hmag)) {
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

  if (newTag) {
    tk->dAnyTag = 1;
    tk->dTag[iq][ie][ii][ih] = 1;
  }

  return newTag;
}

double tkRand(tracklet * tk)
{
  // see LCG notes above, in this file
  tk->rand64 = (tk->rand64 * LCGA) & LCGM;
  return tk->rand64 * invLCGM;
}

/*
 * aRange (tracklet method)
 * 
 * recursive function explores the space between two angles (at a set
 * distance)
 * 
 * Args: tk: tracklet with distance setup already done ang1, ang2: search
 * boundaries.
 * 
 * Algorithm: - pick mid point.  a little jiggle is thrown in to help find 
 * new bins at closely adjacent distances.
 * 
 * - solve angle at mid point.  if it resulted in tagging a new bin,
 * recurse both halves.
 * 
 * - if passed angle range is sufficiently large, recurse.
 * 
 * - age criterion: if a passed angle recently yielded a new bin, recurse. 
 */
void aRange(tracklet * tk, double ang1, double ang2, int age)
{
  double d3 = (ang2 - ang1) / 3.;
  double mid = ang1 + d3 + d3 * tkRand(tk);

  // .1 rad = "sufficiently large"
  if (tagAngle(tk, mid) || d3 > minAngleStep) {
    aRange(tk, ang1, mid, 0);
    aRange(tk, mid, ang2, 0);
    return;
  }

  if (age < ageLimit) {
    aRange(tk, ang1, mid, age + 1);
    aRange(tk, mid, ang2, age + 1);
  }
}

void clearDTags(tracklet * tk)
{
  memset(tk->dTag, 0, sizeof(tk->dTag));
  int c = 0;
  perClass *cl = tk->class;
  do {
    memset(cl->dInClass, 0, sizeof(cl->dInClass));
    memset(cl->dOutOfClass, 0, sizeof(cl->dOutOfClass));
    cl++;
    c++;
  }
  while (c < nClassCompute);
}

void offsetMotionVector(tracklet * tk, int rx, int dx)
{
  // solve unit vectors
  double v[3];
  observation *obsp = tk->obsPair;
  for (int i = 0; i < 2; i++, obsp++) {
    // observer-object unit vectors in ecliptic coordinates
    double dec = obsp->dec + dx * tk->obsErr[i] * .5;
    double cosdec = cos(dec);
    double ra = obsp->ra + rx * tk->obsErr[i] * .5 * cosdec;
    v[0] = cos(ra) * cosdec;
    v[1] = sin(ra) * cosdec;
    v[2] = sin(dec);
    ecRotate(v, tk->soe, tk->coe);
    memcpy(tk->observer_object_unit[i], v, sizeof(v));
    rx = -rx;
    dx = -dx;
  }
}

void setupDistanceDependentVectors(tracklet * tk, double d)
{
  // solve some distance dependent vectors:
  // observer_object0
  tk->observer_object0_mag = d;
  for (int i = 0; i < 3; i++)
    tk->observer_object0[i] =
      tk->observer_object_unit[0][i] * tk->observer_object0_mag;

  // sun_object0
  for (int i = 0; i < 3; i++)
    tk->sun_object0[i] = tk->sun_observer[0][i] + tk->observer_object0[i];
  tk->sun_object0_magsq = dot3(tk->sun_object0, tk->sun_object0);
  tk->sun_object0_mag = sqrt(tk->sun_object0_magsq);

  // observer1_object0
  for (int i = 0; i < 3; i++)
    tk->observer1_object0[i] = tk->sun_object0[i] - tk->sun_observer[1][i];
  tk->observer1_object0_magsq =
    dot3(tk->observer1_object0, tk->observer1_object0);
  tk->observer1_object0_mag = sqrt(tk->observer1_object0_magsq);

  // solve H mag
  double rdelta = tk->observer_object0_mag * tk->sun_object0_mag;
  double cospsi = dot3(tk->observer_object0, tk->sun_object0) / rdelta;
  double tanhalf, phi1, phi2;

  if (cospsi > -.9999) {
    tanhalf = sqrt(1. - cospsi * cospsi) / (1. + cospsi);
    phi1 = exp(-3.33 * pow(tanhalf, 0.63));
    phi2 = exp(-1.87 * pow(tanhalf, 1.22));
    tk->hmag = tk->vmag - 5. * log10(rdelta)
      + 2.5 * log10(.85 * phi1 + .15 * phi2);
  } else
    // object is straight into the sun.  doesn't seem too likely,
    // but anyway, this gives it a valid value.
    tk->hmag = 30.;

  tk->hmag_bin = hToBin(tk->hmag);
}

_Bool solveAngleRange(tracklet * tk, double *ang1, double *ang2)
{
  // solve angle range at this distance
  double th = dot3(tk->observer1_object0,
                   tk->observer_object_unit[1]) / tk->observer1_object0_mag;

  tk->tz = acos(th);

  double aa = tk->invdtsq;
  double bb = (-2. * tk->observer1_object0_mag * th) * aa;
  double cc = tk->observer1_object0_magsq * aa - 2. * U / tk->sun_object0_mag;
  double dsc = bb * bb - 4 * aa * cc;

  // use ! > to catch cases where dsc is Inv or Nan at this point
  // we want to fail in those cases too.
  if (!(dsc > 0.))
    return 0;

  double sd = sqrt(dsc);
  double sd1 = -sd;
  double inv2aa = .5 / aa;
  while (1) {
    double d2 = (-bb + sd1) * inv2aa;
    double d2s = d2 * d2;
    double nns = d2s + tk->observer1_object0_magsq -
      2. * d2 * tk->observer1_object0_mag * th;
    double nn = sqrt(nns);
    double ca = (nns + tk->observer1_object0_magsq - d2s) /
      (2. * nn * tk->observer1_object0_mag);
    double sa = d2 * sin(tk->tz) / nn;
    *ang2 = 2. * atan2(sa, 1. + ca);

    if (sd1 == sd)
      break;

    *ang1 = *ang2;
    sd1 = sd;
  }
  return 1;
}

_Bool searchAngles(tracklet * tk)
{
  double ang1, ang2;
  if (!solveAngleRange(tk, &ang1, &ang2))
    return 0;

  aRange(tk, ang1, ang2, 0);

  if (!tk->dAnyTag)
    return 0;

  _Bool newTag = 0;

  for (int iq = 0; iq < QX; iq++)
    for (int ie = 0; ie < EX; ie++)
      for (int ii = 0; ii < IX; ii++)
        for (int ih = 0; ih < HX; ih++)
          if (tk->dTag[iq][ie][ii][ih]) {
            perClass *cl = tk->class;
            for (int c = 0; c < nClassCompute; c++, cl++) {
              if (cl->dInClass[iq][ie]
                  [ii][ih] && !cl->tagInClass[iq][ie][ii][ih]) {
                newTag = 1;
                cl->tagInClass[iq][ie][ii][ih] = 1;
                cl->sumAllInClass +=
                  modelAllClass[classCompute[c]][iq][ie][ii][ih];
                cl->sumUnkInClass +=
                  modelUnkClass[classCompute[c]][iq][ie][ii][ih];
              }
              if (cl->dOutOfClass[iq]
                  [ie][ii][ih] && !cl->tagOutOfClass[iq][ie][ii][ih]) {
                newTag = 1;
                cl->tagOutOfClass[iq][ie][ii][ih] = 1;
                cl->sumAllOutOfClass += (modelAllSS[iq][ie][ii][ih]
                                         - modelAllClass[classCompute[c]]
                                         [iq][ie][ii][ih]);
                cl->sumUnkOutOfClass +=
                  (modelUnkSS[iq][ie][ii][ih] -
                   modelUnkClass[classCompute[c]][iq][ie][ii][ih]);
              }
            }
          }

  return newTag;
}

/*
 * searchDistance (tracklet method)
 * 
 * for specified distance, set up computations and search angle space
 * 
 * Args: tk: tracklet d: distance for computations
 * 
 * Algorithm: - setup stuff common to all possible orbits at this
 * distance.  this includes some vectors, H magnitude, and limits on
 * possible angles. Also tags are reset for the distance.
 * 
 * - search angle space, which results in tags being set.
 * 
 * - note newly set tags, and accumulate population totals needed for
 * final computation of scores.
 * 
 * Returns: true if any new bins were tagged. false if this distance saw
 * no bins that hadn't been seen at other distances. 
 */
_Bool searchDistance(tracklet * tk, double d)
{
  clearDTags(tk);
  tk->dAnyTag = 0;
  _Bool newTag = 0;

  for (int ri = -1; ri <= 1; ri++)
    for (int di = -1; di <= 1; di++) {
      offsetMotionVector(tk, ri, di);
      setupDistanceDependentVectors(tk, d);
      if (searchAngles(tk))
        newTag = 1;
      if (tk->noObsErr)
        return newTag;
    }
  return newTag;
}

/*
 * dRange (tracklet method)
 * 
 * recursive function to explore the possible orbit space
 * 
 * Args: tk: tracklet d1, d2: distance limits age: a little history.  0
 * means a bin was just tagged.  1 is added at each level of recursion.
 * 
 * Algorithm: much like aRange (above)
 * 
 * - if new bins were found at mid point, recurse both halves
 * 
 * - if range is big, recurse anyway
 * 
 * - if young, recurse 
 */
void dRange(tracklet * tk, double d1, double d2, int age)
{
  double dmid = (d1 + d2) * .5;

  // .2 au = "big"
  if (searchDistance(tk, dmid) || d2 - d1 > minDistanceStep) {
    dRange(tk, d1, dmid, 0);
    dRange(tk, dmid, d2, 0);
    return;
  }

  if (age < ageLimit) {
    dRange(tk, d1, dmid, age + 1);
    dRange(tk, dmid, d2, age + 1);
  }
}

/*
 * dSphr2Cart
 * 
 * Spherical (RA, Dec, in radians) to Cartesian (X, Y, Z unit vector)
 * 
 * operates on arrays of coordinate tuples. first parameter is length of
 * arrays. 
 */
void dSphr2Cart(int len, double s[len][2], double c[len][3])
{
  for (int i = 0; i < len; i++) {
    double t = cos(s[i][1]);
    c[i][0] = t * cos(s[i][0]);
    c[i][1] = t * sin(s[i][0]);
    c[i][2] = sin(s[i][1]);
  }
}

void dCart2Sphr(int len, double c[len][3], double s[len][2])
{
  for (int i = 0; i < len; i++) {
    s[i][0] = fmod(atan2(c[i][1], c[i][0]) + TWO_PI, TWO_PI);
    s[i][1] = asin(c[i][2]);
  }
}

/*
 * mult3
 * 
 * matrix multiplication, specialized to broadcast multiplication of a 3
 * by 3 (rotation matrix) to n rows individually.
 * 
 * Input args: rm -- 3 by 3 a -- n by 3 -- multiplication is broacast to
 * each row.
 * 
 * Result: rm x a -- n by 3 again. 
 */
void mult3(int n, double result[n][3], double rm[3][3], double a[n][3])
{
  for (int i = 0; i < n; i++)
    for (int r = 0; r < 3; r++) {
      double s = 0;
      for (int c = 0; c < 3; c++)
        s += rm[r][c] * a[i][c];
      result[i][r] = s;
    }
}

void transpose3(double m[3][3])
{
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

/*
 * gcFit
 * 
 * Great circle fit.
 * 
 * Args: gcf -- great circle fit parameters, can be used in subsequent
 * calls to statistics functions mjd -- mjd times of observations sphr --
 * ra, dec, in radians 
 */
void gcFit(gcfparam * gcf, double mjd[gcf->nObs], double sphr[gcf->nObs][2])
{
  int nObs = gcf->nObs;

  // convert obs to cartesian
  double cart[nObs][3];
  dSphr2Cart(nObs, sphr, cart);

  // vector normal to motion
  double n[3];
  cross3(n, cart[0], cart[nObs - 1]);
  double nmag2 = dot3(n, n);
  double nmag = sqrt(nmag2);

  // rotation axis is right angle to n projected onto z=0 plane
  // and normalized to unit vector
  double nxy = 1 / sqrt(n[0] * n[0] + n[1] * n[1]);
  double gcix = n[1] * nxy;
  double gciy = -n[0] * nxy;

  // rotation angle is angle from n to +z
  double sina = sqrt(nmag2 - n[2] * n[2]) / nmag;
  double cosa = n[2] / nmag;

  // build mRot, rotation matrix that will rotate the coordinate system
  // to the obs, so that a cylindrical projection will have negligible
  // distortion.)
  double sinagx = sina * gcix;
  double sinagy = sina * gciy;
  double onemcosa = 1 - cosa;
  double onemcosagx = onemcosa * gcix;
  double onemcosagxgy = onemcosagx * gciy;
  gcf->mRot[0][0] = cosa + onemcosagx * gcix;
  gcf->mRot[0][1] = onemcosagxgy;
  gcf->mRot[0][2] = sinagy;
  gcf->mRot[1][0] = onemcosagxgy;
  gcf->mRot[1][1] = cosa + onemcosa * gciy * gciy;
  gcf->mRot[1][2] = -sinagx;
  gcf->mRot[2][0] = -sinagy;
  gcf->mRot[2][1] = sinagx;
  gcf->mRot[2][2] = cosa;

  // rotate all of cart
  double rotated[nObs][3];
  mult3(nObs, rotated, gcf->mRot, cart);

  // transpose rotation array so it will derotate, after least-squares
  // fit.
  transpose3(gcf->mRot);

  // invariant: first and last points should be on the z=0 plane
  // of the rotated coordinate system now.
  if (fabs(rotated[0][2]) > rtol || fabs(rotated[nObs - 1][2]) > rtol) {
    fprintf(stderr, "%f %f %f\n", rotated[0][2], rotated[nObs - 1][2], rtol);
    fputs("*** rotation failed ***\n", stderr);
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

void gcPos(gcfparam * gcf, double t, double *ra, double *dec)
{
  // compute position on fitted great circle
  double nt = t - gcf->t0;
  double rsc[2];
  double rcc[3];
  double sc[2];
  double cc[3];
  rsc[0] = gcf->r0 + gcf->rr * nt + gcf->ra0;
  rsc[1] = gcf->d0 + gcf->dr * nt;

  // rotate back up to original place in the sky
  dSphr2Cart(1, &rsc, &rcc);
  mult3(1, &cc, gcf->mRot, &rcc);
  dCart2Sphr(1, &cc, &sc);

  // return coordinates
  *ra = sc[0];
  *dec = sc[1];
}

void gcRes(gcfparam * gcf, double res[gcf->nObs][2])
{
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
  dCart2Sphr(nObs, co, so);
  dCart2Sphr(nObs, cc, sc);

  for (int i = 0; i < nObs; i++) {
    res[i][1] = (so[i][1] - sc[i][1]) / arcsecrad;
    res[i][0] = (so[i][0] - sc[i][0]) * cos(sc[i][1]) / arcsecrad;
  }
}

/*
 * gcRmsRes
 * 
 * returns rms of 2d residual, and the component ra and dec residuals.
 * 
 * Note: The 2d residual is the 2d distance between computed and observed.
 * The rms of the ra and dec residuals considered as separate values--if
 * that's what you are looking for--is smaller by a factor of sqrt(2). 
 */
double gcRmsRes(gcfparam * gcf, double res[gcf->nObs][2])
{
  int nObs = gcf->nObs;
  gcRes(gcf, res);
  double s = 0;
  for (int i = 0; i < nObs; i++)
    s += res[i][0] * res[i][0] + res[i][1] * res[i][1];
  return sqrt(s / nObs);
}

/*
 * gcRms
 * 
 * just return the Rms, never mind the residuals. 
 */
double gcRms(gcfparam * gcf)
{
  double res[gcf->nObs][2];
  return gcRmsRes(gcf, res);
}

/*
 * void printObs(observation * obsp, char *heading) { puts(heading);
 * printf(" mjd: %f\n", obsp->mjd); printf(" ra: %f\n", obsp->ra);
 * printf(" dec: %f\n", obsp->dec); printf(" vmag: %f\n", obsp->vmag);
 * printf(" site: %d\n", obsp->site); printf(" spacebased: %d\n",
 * obsp->spacebased); printf(" earth_observer: %f %f %f\n",
 * obsp->earth_observer[0], obsp->earth_observer[1],
 * obsp->earth_observer[2]); } 
 */

double
oneObs(int o1, int o2, _Bool arcsUseAllObs, double pt,
       observation * olist, observation * result)
{
  // a default result
  memcpy(result, olist + o1, sizeof(observation));

  // case 1.  simple, only a single obs for the "arc".
  if (o1 == o2)
    return 0;

  // case 2.  two points for the arc.
  if (o1 == o2 - 1) {
    // case 2.1.  fairly simple: if there's stuff between the arcs
    // and the target percentile (17 or 83) is off of this arc,
    // just return the end of the arc.
    if (!arcsUseAllObs) {
      double dt;
      if (o1 == 0) {
        memcpy(result, olist + 1, sizeof(observation));
        dt = result->mjd - pt;
      } else
        dt = pt - result->mjd;
      if (dt < 0)
        return 0;
    }
    // case 2.2.  linearly interpolate along the great circle
    // connecting the points.
    memcpy(result, olist + o1, sizeof(observation));
    double t[2];
    double s[2][2];
    t[0] = olist[o1].mjd;
    s[0][0] = olist[o1].ra;
    s[0][1] = olist[o1].dec;
    t[1] = olist[o2].mjd;
    s[1][0] = olist[o2].ra;
    s[1][1] = olist[o2].dec;
    gcfparam gcf;
    gcf.nObs = 2;
    double nt[2];
    double rs[2][2];
    gcf.ntime = nt;
    gcf.rs = rs;
    gcFit(&gcf, t, s);
    // ? gc  midpoint : gc at pt
    result->mjd = arcsUseAllObs ? (olist[o1].mjd + olist[o2].mjd) * .5 : pt;
    gcPos(&gcf, result->mjd, &result->ra, &result->dec);
    return 0;
  }
  // case 3.  3 or more points in arc.
  double tr;
  if (arcsUseAllObs) {
    // median time of arc
    int is = (o1 + o2) / 2;
    tr = olist[is].mjd;
    if (is + is < o1 + o2)
      tr = (tr + olist[is + 1].mjd) * .5;
  } else {
    double dt;
    if (o1 == 0) {
      memcpy(result, olist + o2, sizeof(observation));
      dt = result->mjd - pt;
    } else {
      memcpy(result, olist + o1, sizeof(observation));
      dt = pt - result->mjd;
    }
    tr = dt < 0 ? result->mjd : pt;
  }

  // gc fit, result is computed obs at time tr
  int np = o2 - o1 + 1;
  double t[np];
  double c[np][2];
  observation *obsp = olist + o1;
  for (int i = 0; i < np; i++, obsp++) {
    t[i] = obsp->mjd;
    c[i][0] = obsp->ra;
    c[i][1] = obsp->dec;
  }
  gcfparam gcf;
  gcf.nObs = np;
  double nt[np];
  double rs[np][2];
  gcf.ntime = nt;
  gcf.rs = rs;
  gcFit(&gcf, t, c);
  memcpy(result, olist + o1, sizeof(observation));
  result->mjd = tr;
  gcPos(&gcf, tr, &result->ra, &result->dec);
  return gcRms(&gcf);
}

// twoObs selects or synthesizes two observations defining the motion
// vector.  It sets tk->obsPair and tk->rms.
// at least two obs must be passed in.
void twoObs(tracklet * tk, double rms[])
{
  int nObs = tk->lines;
  observation *olist = tk->olist;

  // default pair
  memcpy(&tk->obsPair[0], olist, sizeof(observation));
  memcpy(&tk->obsPair[1], olist + nObs - 1, sizeof(observation));

  // simplest case, default just set was the only two points given.
  // leave rms = 0
  if (nObs == 2)
    return;

  // > 2 obs, do a great circle fit over all obs to get rms return
  // value.
  // Fit may also be used in some cases for synthesizing observations.
  double t[nObs];
  double c[nObs][2];
  observation *obsp = olist;
  for (int i = 0; i < nObs; i++, obsp++) {
    t[i] = obsp->mjd;
    c[i][0] = obsp->ra;
    c[i][1] = obsp->dec;
  }
  gcfparam gcf;
  gcf.nObs = nObs;
  double nt[nObs];
  double rs[nObs][2];
  gcf.ntime = nt;
  gcf.rs = rs;
  gcFit(&gcf, t, c);
  tk->rms = gcRms(&gcf);

  // scan obscodes. determine of all obs are from same obscode and
  // any space based observations are present
  _Bool allSame = 1;
  _Bool spaceBased = 0;
  obsp = olist;
  for (int i = 0; i < nObs; i++, obsp++) {
    if (obsp->site != olist->site)
      allSame = 0;
    if (siteTable[obsp->site].rhoCosPhi == 0 &&
        siteTable[obsp->site].rhoSinPhi == 0)
      spaceBased = 1;
  }

  // find observations near 17th and 83rd percentile.
  // percentile is used rather than percent to allow for non-uniformly
  // distributed observation times.
  double whole;
  double fs = modf((nObs - 1) / 6., &whole);
  int is = whole;

  // not always sensible to interpolate space based obs, especially
  // if observer position is ever taken into account.  in this case
  // just use obs at 17th and 83rd percentile.
  if (spaceBased) {
    memcpy(&tk->obsPair[0], olist + is, sizeof(observation));
    memcpy(&tk->obsPair[1], olist + nObs - 1 - is, sizeof(observation));
    return;
  }
  // compute times t17 and t83 at these points of interest.
  // the times will be used in a few different ways.
  double t17 = olist[is].mjd;
  t17 += (olist[is + 1].mjd - t17) * fs;
  is = nObs - 1 - is;
  double t83 = olist[is].mjd;
  t83 -= (t83 - olist[is - 1].mjd) * fs;

  // next case still fairly simple: single obs code, arc < 3 hrs.
  // => use gc fit of whole arc and synthesize obs at the 17th
  // and 83rd percentile times.
  if (allSame && olist[nObs - 1].mjd - olist[nObs - 1].mjd < .125) {
    obsp = &tk->obsPair[0];
    obsp->mjd = t17;
    gcPos(&gcf, t17, &obsp->ra, &obsp->dec);

    obsp = &tk->obsPair[1];
    obsp->mjd = t83;
    gcPos(&gcf, t83, &obsp->ra, &obsp->dec);
    rms[0] = rms[1] = tk->rms;
    return;
  }
  // remaining case is involved.  not appropriate to gc fit the entire
  // arc, but probably possible to derive better endpoints than just
  // first and last obs.

  // first step is to split off initial and final arcs, each arc being
  // all the same code and < 3hrs, but otherwise being as long as
  // possible.
  // if arcs use all obs and are both of same code, they should be as
  // equal in dt as possible.
  int o1 = 0;
  int o2 = nObs - 1;
  int code1 = olist[o1].site;
  int code2 = olist[o2].site;
  double t1 = olist[o1].mjd;
  double t2 = olist[o2].mjd;
  do {
    double dt1 = olist[o1 + 1].mjd - t1;
    if (olist[o1 + 1].site != code1 || dt1 > .125) {
      // initial arc is done, just try to extend final arc
      while (1) {
        int o = o2 - 1;
        if (o == o1 || olist[o].site != code2 || t2 - olist[o].mjd > .125)
          break;
        o2 = o;
      }
      break;
    }
    double dt2 = t2 - olist[o2 - 1].mjd;
    if (olist[o2 - 1].site != code2 || dt2 > .125) {
      // final arc is done, just try to extend initial arc
      while (1) {
        int o = o1 + 1;
        if (o == o2 || olist[o].site != code1 || olist[o].mjd - t1 > .125)
          break;
        o1 = o;
      }
      break;
    }

    if (dt1 < dt2)
      o1++;
    else
      o2--;
  }
  while (o2 > o1 + 1);

  // handle each arc
  rms[0] = oneObs(0, o1, o2 == o1 + 1, t17, olist, &tk->obsPair[0]);
  rms[1] = oneObs(o2, nObs - 1, o2 == o1 + 1, t83, olist, &tk->obsPair[1]);
}

double clipErr(double computedRms, site * sitep)
{
  // look for config file specified obs err for this site
  double defaultErr = sitep->obsErr;
  if (defaultErr == -1)
    // not there, fall back on default (which also may been specified
    // in the config file, or may be hard coded default.)
    defaultErr = obsErr;

  if (defaultErr == 0)
    // if obs err is configured to be zero, that
    // takes precedence over any computed rms
    return 0;

  if (computedRms == 0)
    // if no rms could be computed, use the default obs err.
    return defaultErr;

  // finally, consider rms, except it is in arc seconds.  we need err
  // in radians
  double computedErr = computedRms * arcsecrad;
  // then just return the greater of the two
  return defaultErr > computedErr ? defaultErr : computedErr;
}

/* score (tracklet method)
 * 
 * score tracklet.  this is the driver for all the math.
 * 
 * Arg: tk: tracklet.
 * 
 * Preconditions:
 * - all globals must be initialized.
 * - tk->status must be UNPROC
 * - tk->olist must have valid observations
 * - tk->lines must say how many
 * - tk->vmag must be initialized
 * - tk->rand must be odd.
 * - with exception of tk->desig and tk->obsCap, which are not used,
 * everything else in tk must be zero. 
 */
void score(tracklet * tk)
{
  // sythesize or select two observations to determine motion vector
  double rms[2];
  rms[0] = rms[1] = 0;
  twoObs(tk, rms);

  tk->dt = tk->obsPair[1].mjd - tk->obsPair[0].mjd;
  tk->invdt = 1. / tk->dt;
  tk->invdtsq = tk->invdt * tk->invdt;

  // solve vectors at observation times
  observation *obsp = tk->obsPair;
  for (int i = 0; i < 2; i++, obsp++) {
    site *sitep = siteTable + obsp->site;
    tk->obsErr[i] = clipErr(rms[i], sitep);

    double sun_earth[3];
    se2000(obsp->mjd, sun_earth, &tk->soe, &tk->coe);

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
    ecRotate(v, tk->soe, tk->coe);
    memcpy(tk->sun_observer[i], v, sizeof(v));
  }
  if (tk->obsErr[0] == 0. && tk->obsErr[1] == 0.)
    tk->noObsErr = 1;
  searchDistance(tk, MIN_DISTANCE);
  searchDistance(tk, MAX_DISTANCE);
  dRange(tk, MIN_DISTANCE, MAX_DISTANCE, 0);

  perClass *cl = tk->class;
  for (int c = 0; c < nClassCompute; c++, cl++) {
    double d = cl->sumAllInClass + cl->sumAllOutOfClass;
    cl->rawScore = d > 0.
      ? 100. * cl->sumAllInClass / d : classCompute[c] < 2 ? 100. : 0.;

    d = cl->sumUnkInClass + cl->sumUnkOutOfClass;
    cl->noIdScore = d > 0.
      ? 100. * cl->sumUnkInClass / d : classCompute[c] < 2 ? 100. : 0.;
  }
}

// d2model.c
//
// Public domain.

// object classes available to digest2.  (where object and class are
// not oop terms.  object=solar system object, class=orbit classification.)

#include <math.h>
#include "d2model.h"

#ifndef M_PI
#define M_PI 3.14159265358979323846264338327
#endif

double modelAllSS[QX][EX][IX][HX];
double modelUnkSS[QX][EX][IX][HX];
double modelAllClass[D2CLASSES][QX][EX][IX][HX];
double modelUnkClass[D2CLASSES][QX][EX][IX][HX];

double qpart[QX] = { .4, .7, .8, .9, 1., 1.1, 1.2, 1.3, 1.4, 1.5,
  1.67, 1.8, 2., 2.2, 2.4, 2.6, 2.8, 3., 3.2, 3.5,
  4., 4.5, 5., 5.5, 10., 20., 30., 40., 100.
};
double epart[EX] = { .1, .2, .3, .4, .5, .7, .9, 1.1 };
double ipart[IX] = { 2, 5, 10, 15, 20, 25, 30, 40, 60, 90, 180 };

double hpart[HX] = { 6, 8, 10, 11, 12, 13, 14, 15, 16, 17,
  18, 19, 20, 21, 22, 23, 24, 25.5
};

/* qeihToBin

convert elements q, e, i, h to bin indexes

Returns:
   true if in model, bin indexes returned in parameter 'bin' in order
   q, e, i, h.
   false if out of model
*/
_Bool qeihToBin(double q, double e, double i, double h, int bin[4])
{
  _Bool r;
  if ((r = qeiToBin(q, e, i, bin)))
    bin[3] = hToBin(h);
  return r;
}

_Bool qeiToBin(double q, double e, double i, int bin[3])
{
  for (bin[0] = 0; q >= qpart[bin[0]]; ++bin[0])
    if (bin[0] == QX)
      return 0;
  for (bin[1] = 0; e >= epart[bin[1]]; ++bin[1])
    if (bin[1] == EX)
      return 0;
  for (bin[2] = 0; i >= ipart[bin[2]]; ++bin[2])
    if (bin[2] == IX)
      return 0;
  return 1;
}

int hToBin(double h)
{
  int ih;
  for (ih = 0; h >= hpart[ih] && ih < HX - 1; ++ih) ;
  return ih;
}

// 'MPC interesting' objects
// The definition of MPC interesting implemented here is:
// any of: q < 1.3, e > .5, i > 40, or Q > 10
_Bool isMpcint(double q, double e, double i, double h)
{
  return q < 1.3 || e >= .5 || i >= 40. || q * (1. + e) / (1. - e) > 10.;
}

// 'NEO' objects
// The definition of NEO implemented here is q < 1.3
_Bool isNeo(double q, double e, double i, double h)
{
  return q < 1.3;
}

// H18 NEOs
// H rounded to nearest integer <= 18
_Bool isH18Neo(double q, double e, double i, double h)
{
  return q < 1.3 && h < 18.5;
}

// H22 NEOs
// H rounded to nearest integer <= 22
_Bool isH22Neo(double q, double e, double i, double h)
{
  return q < 1.3 && h < 22.5;
}

// Mars Crosser
// 1.3 <= q < 1.67, Q > 1.58
_Bool isMarsCrosser(double q, double e, double i, double h)
{
  return q < 1.67 && q >= 1.3 && q * (1 + e) / (1 - e) > 1.58;
}

// Hungarias
// 1.78>a>2.0, e<.18, 16 < i < 28
// (a node test would be nice...)
_Bool isHungaria(double q, double e, double i, double h)
{
  if (e > .18 || i < 16 || i > 34)
    return 0;
  double a = q / (1 - e);
  return a < 2 && a > 1.78;
}

// Phocaeas
// q>1.5, 2.2<a<2.45, 20<i<27
_Bool isPhocaea(double q, double e, double i, double h)
{
  if (q < 1.5 || i < 20 || i > 27)
    return 0;
  double a = q / (1 - e);
  return a < 2.45 && a > 2.2;
}

// Inner Main Belt
// q>1.67, 2.1<a<2.5, i<7 at inner edge, <17 at outer
_Bool isInnerMB(double q, double e, double i, double h)
{
  if (q < 1.67)
    return 0;
  double a = q / (1 - e);
  return a < 2.5 && a > 2.1 && i < ((a - 2.1) / .4) * 10 + 7;
}

// Hansas
// 2.55<a<2.72 e<.25, 20<i<23.5
_Bool isHansa(double q, double e, double i, double h)
{
  if (e > .25 || i < 20 || i > 23.5)
    return 0;
  double a = q / (1 - e);
  return a < 2.72 && a > 2.55;
}

// Pallas group
// 2.5<a<2.8, e<.35, 24<i<37
_Bool isPallas(double q, double e, double i, double h)
{
  if (e > .35 || i < 24 || i > 37)
    return 0;
  double a = q / (1 - e);
  return a < 2.8 && a > 2.5;
}

// Mid Main Belt
// 2.5<a<2.8, e<.45, i<20
_Bool isMidMB(double q, double e, double i, double h)
{
  if (e > .45 || i > 20)
    return 0;
  double a = q / (1 - e);
  return a < 2.8 && a > 2.5;
}

// Outer Main Belt
//  2.8<a<3.25 e<.4, i < 20 inner edge, i < 36 outer edge
_Bool isOuterMB(double q, double e, double i, double h)
{
  if (e > .4)
    return 0;
  double a = q / (1 - e);
  return a > 2.8 && a < 3.25 && i < ((a - 2.8) / .45) * 16 + 20;
}

// Hildas
// 3.9<a<4.02, e<.4, i<18
_Bool isHilda(double q, double e, double i, double h)
{
  if (i > 18 || e > .4)
    return 0;
  double a = q / (1 - e);
  return a > 3.9 && a < 4.02;
}

// Trojans
// 5.05<a<5.35, e<.22, i<38
_Bool isTrojan(double q, double e, double i, double h)
{
  if (e > .22 || i > 38)
    return 0;
  double a = q / (1 - e);
  return a > 5.05 && a < 5.35;
}

// Jupiter Family Comets
// 2 < Tj < 3, q >= 1.3
_Bool isJFC(double q, double e, double i, double h)
{
  if (q < 1.3)
    return 0;
  double t =
    5.2 * (1 - e) / q + 2 * sqrt(q * (1 + e) / 5.2) * cos(i * M_PI / 180.);
  return t < 3 && t > 2;
}

// 12 characters looks nice, 13 is ok.
// anything over 13 is truncated at run time.
char *classHeading[D2CLASSES] = {
  "MPC interest.",
  "NEO(q < 1.3)",
  "NEO(H <= 22)",
  "NEO(H <= 18)",
  "Mars Crosser",
  "Hungaria gr.",
  "Phocaea group",
  "Inner MB",
  "Pallas group",
  "Hansa group",
  "Middle MB",
  "Outer MB",
  "Hilda group",
  "Jupiter tr.",
  "Jupiter Comet"
};

char *classAbbr[D2CLASSES] = {
  "Int",
  "NEO",
  "N22",
  "N18",
  "MC",
  "Hun",
  "Pho",
  "MB1",
  "Pal",
  "Han",
  "MB2",
  "MB3",
  "Hil",
  "JTr",
  "JFC"
};

classtest isClass[D2CLASSES] = {
  isMpcint,
  isNeo,
  isH22Neo,
  isH18Neo,
  isMarsCrosser,
  isHungaria,
  isPhocaea,
  isInnerMB,
  isPallas,
  isHansa,
  isMidMB,
  isOuterMB,
  isHilda,
  isTrojan,
  isJFC
};

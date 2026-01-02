//! C99

/* gcf.h

Copyright (c) 2010 Sonia Keys

See external file LICENSE, distributed with this software.
*/

#ifndef M_PI
#define M_PI 3.14159265358979323
#endif

typedef struct {
   // various intermediate values, useful for generating statistics after
   // the fit is done
   int    nObs;
   double mRot[3][3]; // rotation matrix
   double ra0;        // ra offset
   double (*rs)[2];   // rotated ra and dec
   double t0;         // time offset
   double *ntime;     // normalized times
   // fit solution parameters
   double r0;
   double rr;
   double d0;
   double dr;
} gcfparam;

void gcFit(gcfparam *gcf, double mjd[], double sphr[][2]);

// three variations of result functions:

// compute an arbitrary position on the fitted great circle
void gcPos(gcfparam *gcf, double t, double *ra, double *dec);

// compute residuals in ra and dec.
void gcRes(gcfparam *gcf, double res[][2]);

// compute residuals in ra and dec, and the 2d rms.
double gcRmsRes(gcfparam *gcf, double res[][2]);

// compute 2d rms of residuals, don't bother to return residuals
double gcRms(gcfparam *gcf);


/**
 * @File d2ades.h
 * @author Richard Cloete
 * @Email richard.cloete@cfa.harvard.edu
 * @Description header file for d2ades.c
 */

#include "libxml/parser.h"
#include <libxml/xpath.h>
#include <libxml/xpathInternals.h>

#ifndef MPCDEV_DIGEST2_D2ADES_H
#define MPCDEV_DIGEST2_D2ADES_H

#endif //MPCDEV_DIGEST2_D2ADES_H

typedef struct optical {
    xmlChar *provID;
    xmlChar *trkSub;
    xmlChar *obsID;
    xmlChar *trkID;
    xmlChar *mode;
    xmlChar *stn;
    xmlChar *obsTime;
    xmlChar *ra;
    xmlChar *dec;
    xmlChar *rmsRA;
    xmlChar *rmsDec;
    xmlChar *astCat;
    xmlChar *mag;
    xmlChar *rmsMag;
    xmlChar *band;
    xmlChar *logSNR;
    xmlChar *seeing;
    xmlChar *exp;
    xmlChar *subFmt;
    xmlChar *sys;
    xmlChar *pos1;
    xmlChar *pos2;
    xmlChar *pos3;
    xmlChar *ref;
    xmlChar *ctr;
    xmlChar *precTime;
    xmlChar *precRA;
    xmlChar *precDec;

} optical, *opticalPtr;



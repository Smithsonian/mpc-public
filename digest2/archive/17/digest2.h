// digest2.h
//
// Public domain.

#include <regex.h>
#include <stdint.h>
#include <sys/stat.h>

#include "d2model.h"

// M_PI is in math.h, but not defined in some strict modes
#ifndef M_PI
#define M_PI 3.14159265358979323846264338327
#endif

// typedefs
//-----------------------------------------------------------------------------

// observation.
typedef struct {
  double mjd;                   // modified julian date
  double ra;                    // radians
  double dec;
  double vmag;                  // observed magnitude, normalized to V band.
  // 0 means no magnitude.
  int site;                     // index into site table.  basically an integer form of the
  // MPC three character obscode.
  _Bool spacebased;
  double earth_observer[3];
} observation;

// site.  observatory site parallax constants and standard observational error
typedef struct {
  double longitude;             // unit is circles
  double rhoCosPhi;             // unit is AU
  double rhoSinPhi;
  double obsErr;                // unit is radians
} site;

// tkstatus.  traklet status, during processing and as a result code.
typedef enum {
  INVALID,
  UNPROC,
  ACRON,
  FAIL,
  SUCCESS
} tkstatus;

typedef struct {
  double rawScore;
  double noIdScore;
  _Bool tagInClass[QX][EX][IX][HX];
  _Bool tagOutOfClass[QX][EX][IX][HX];
  double sumAllInClass;
  double sumUnkInClass;
  double sumAllOutOfClass;
  double sumUnkOutOfClass;
  _Bool dInClass[QX][EX][IX][HX];
  _Bool dOutOfClass[QX][EX][IX][HX];
} perClass;

// tracklet.  struct holds working variables and everything associated with
// computing scores for a single tracklet.
//
// note: some code relies on this structure being zero initialized.
typedef struct {
  // these few elements really describe the tracklet
  tkstatus status;
  char desig[13];
  observation *olist;
  int obsCap;                   // allocated capacity of olist
  // for status=INVALID, this is the number of consecutive
  // invalid lines.  otherwise, it is the number of valid
  // observations in olist.
  int lines;

  // distance independent working variables.  computed over the course
  // of processing the tracklet.
  observation obsPair[2];       // two obs defining motion vector
  double obsErr[2];             // observational error for two obs
  _Bool noObsErr;               // true if both of above == 0
  uint64_t rand64;              // LCG random numuber
  double vmag;                  // composite value for the tracklet
  double sun_observer[2][3];    // vectors at times t0 and t1
  double observer_object_unit[2][3]; // vectors at times t0 and t1
  double dt;                    // t1 - t0
  double invdt;                 // 1/dt
  double invdtsq;               // 1/(dt**2)
  double soe, coe;
  double rms;

  // distance dependent working variables.  these are computed separately
  // for each distance considered.
  double sun_object0[3];
  double sun_object0_mag;
  double sun_object0_magsq;

  double observer_object0[3];
  double observer_object0_mag;

  double observer1_object0[3];
  double observer1_object0_mag;
  double observer1_object0_magsq;

  double tz;
  double hmag;
  int hmag_bin;
  _Bool dAnyTag;
  _Bool dTag[QX][EX][IX][HX];

  perClass *class;              // array, extent = nClassesComputed
} tracklet;

typedef struct {
  // various intermediate values, useful for generating statistics after
  // the fit is done
  int nObs;
  double mRot[3][3];            // rotation matrix
  double ra0;                   // ra offset
  double (*rs)[2];              // rotated ra and dec
  double t0;                    // time offset
  double *ntime;                // normalized times
  // fit solution parameters
  double r0;
  double rr;
  double d0;
  double dr;
} gcfparam;

#define LINE_SIZE 400
#define FIELD_SIZE 40
extern char line[LINE_SIZE];
extern char field[FIELD_SIZE];

extern char *fnConfig;
extern char *fnCSV;
extern char *fnModel;
extern char *fnOCD;

extern char msgAccess[];
extern char msgCSVData[];
extern char msgCSVHeader[];
extern char msgMemory[];
extern char msgOpen[];
extern char msgRead[];
extern char msgReadInvalid[];
extern char msgWrite[];
extern char msgStatus[];
extern char msgThread[];
extern char msgUsage[];
extern char msgVersion[];
extern char msgLimitClassNotConfig[];
extern char msgLimitScoreNotConfig[];

#define obscodeNamespaceSize 3600
extern site siteTable[obscodeNamespaceSize];
extern double K, INV_K, U, TWO_PI;
extern uint64_t LCGA, LCGM;
extern double invLCGM;
extern double arcsecrad;
extern int nClassCompute;
extern int classCompute[D2CLASSES];
extern double obsErr;
extern regex_t rxObsErr;
extern regex_t rxLimit;
extern int cores;
extern int limit;

void fatal(char *msg);
void fatal1(char *msg, char *arg);

extern _Bool cpuSpec;
extern _Bool modelSpec;
extern _Bool ocdSpec;
extern _Bool classPossible;
extern _Bool raw, noid;
extern _Bool headings, rms, repeatable;
extern _Bool limitSpec;
extern _Bool limitRaw;
extern int nClassCompute;
extern int nClassColumns;
extern int classCompute[D2CLASSES];
extern int classColumn[D2CLASSES];
extern int limitClass;

// functions in d2cli.c
char *CPspec(char *fn, _Bool spec);
FILE *openCP(char *fn, _Bool spec, char *mode);
char *parseCl(int argc, char **argv);
void readConfig();

// functions in d2modelio.c
void mustReadCSV(struct stat *);
void mustReadModel();
void mustReadModelStatCSV();
void writeModel(struct stat *);

// functions in mpc.c
_Bool getOCD();
void mustReadOCD();
void mustReadGetOCD();
int parseCod3(char *);
_Bool parseMpc80(char *line, observation * obsp);
_Bool parseMpcSat(char *line, observation * obsp);

// functions in d2math.c
void initGlobals(void);
void score(tracklet * tk);
double tkRand(tracklet * tk);

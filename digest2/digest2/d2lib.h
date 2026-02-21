// d2lib.h
//
// Public domain.
//
// Library API for digest2 scoring engine.
// This header provides a clean, non-threaded interface to the core
// scoring functionality, suitable for embedding in Python or other
// language bindings.

#ifndef D2LIB_H
#define D2LIB_H

#include "d2model.h"

// Error codes
#define D2_OK            0
#define D2_ERR_MODEL    -1
#define D2_ERR_OBSCODES -2
#define D2_ERR_MEMORY   -3
#define D2_ERR_INPUT    -4
#define D2_ERR_NOINIT   -5

// Observation passed from the caller (mirrors the internal observation struct)
typedef struct {
    double mjd;            // modified julian date
    double ra;             // radians
    double dec;            // radians
    double vmag;           // V magnitude (0 = no magnitude)
    int    site;           // obscode as integer (from d2_parse_obscode)
    int    spacebased;     // boolean: 1 if space-based
    double earth_obs[3];   // for space-based observers
    double rmsRA;          // arcsec (0 = use default)
    double rmsDec;         // arcsec (0 = use default)
} d2_observation;

// Result from scoring a tracklet
typedef struct {
    double raw_scores[D2CLASSES];
    double noid_scores[D2CLASSES];
    double rms;
    double rms_prime;
    int    status;         // 0=success, negative=error code
    int    n_classes;      // number of classes scored (D2CLASSES)
} d2_result;

// Lifecycle
int  d2_init(const char *model_csv_path, const char *obscodes_path);
void d2_cleanup(void);
int  d2_is_initialized(void);

// Configuration
void d2_set_default_obserr(double arcsec);
void d2_set_site_obserr(int site_index, double arcsec);
void d2_set_repeatable(int flag);
void d2_set_no_threshold(int flag);

// Scoring
d2_result d2_score_observations(d2_observation *obs, int n_obs,
                                int *classes, int n_classes,
                                int is_ades);

// Utilities
int         d2_parse_obscode(const char *code3);
int         d2_get_class_count(void);
const char *d2_get_class_abbr(int index);
const char *d2_get_class_name(int index);

#endif // D2LIB_H

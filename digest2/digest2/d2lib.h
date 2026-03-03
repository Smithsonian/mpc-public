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

// Trial orbit data (for orbit element collection)
typedef struct {
    double q;       // perihelion distance (AU)
    double e;       // eccentricity
    double i;       // inclination (degrees)
    double H;       // absolute magnitude
    double d;       // geocentric distance used to generate this orbit (AU)
    double an;      // angle used in orbit solution (radians)
    int    iq;      // q bin index (0..QX-1)
    int    ie;      // e bin index (0..EX-1)
    int    ii;      // i bin index (0..IX-1)
    int    ih;      // H bin index (0..HX-1)
    int    new_tag; // 1 if this orbit tagged a previously unvisited bin
} d2_trial_orbit;

typedef struct d2_orbit_buffer {
    d2_trial_orbit *orbits;
    int count;
    int capacity;
} d2_orbit_buffer;

// Extended result with trial orbits
typedef struct {
    d2_result base;
    d2_trial_orbit *orbits;   // caller must free via d2_free_result_ext
    int n_orbits;
} d2_result_ext;

d2_result_ext d2_score_observations_ext(d2_observation *obs, int n_obs,
                                         int *classes, int n_classes,
                                         int is_ades);
void d2_free_result_ext(d2_result_ext *result);

// Utilities
int         d2_parse_obscode(const char *code3);
int         d2_get_class_count(void);
const char *d2_get_class_abbr(int index);
const char *d2_get_class_name(int index);

#endif // D2LIB_H

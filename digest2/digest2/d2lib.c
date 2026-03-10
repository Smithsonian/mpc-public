// d2lib.c
//
// Public domain.
//
// Library API implementation for digest2 scoring engine.
// Provides init/score/cleanup functions without threading or file I/O
// for observations. Reuses existing d2math.c, d2model.c, d2modelio.c,
// d2mpc.c, and common.c unchanged.

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "d2lib.h"
#include "digest2.h"

// Track initialization state
static int lib_initialized = 0;

// Library-local copies of globals that in CLI mode are set by d2cli.c.
// We define them here so the library can be linked without d2cli.c.
// These are declared extern in digest2.h.
char line[LINE_SIZE];
char field[FIELD_SIZE];

char *fnConfig = "digest2.config";
char *fnCSV    = "digest2.model.csv";
char *fnModel  = "digest2.model";
char *fnOCD    = "digest2.obscodes";

// In library mode these are always false (no command-line path logic)
_Bool configSpec = 0;
_Bool modelSpec  = 0;
_Bool ocdSpec    = 0;
_Bool pathSpec   = 0;
_Bool cpuSpec    = 0;
_Bool limitSpec  = 0;

_Bool classPossible = 1;
_Bool raw  = 1;
_Bool noid = 1;
_Bool headings   = 0;
_Bool rms        = 1;
_Bool repeatable = 1;
_Bool rmsPrime   = 0;
_Bool noThreshold = 0;
_Bool limitRaw   = 0;

int nClassCompute = D2CLASSES;
int nClassColumns = 0;
int classCompute[D2CLASSES];
int classColumn[D2CLASSES];
int limitClass = 0;
int limit = 0;

int cores = 1;

site siteTable[obscodeNamespaceSize];

// These message strings are referenced by other .c files via extern.
char msgAccess[]    = "Cannot access URL %s\n";
char msgCSVData[]   = "Invalid CSV data:  %s\n";
char msgCSVHeader[] = "Invalid CSV header:  %s\n";
char msgMemory[]    = "Memory allocation failed.\n";
char msgOpen[]      = "Open %s failed.\n";
char msgRead[]      = "Read %s failed.\n";
char msgReadInvalid[] = "Read %s failed, contents invalid.\n";
char msgWrite[]     = "Write %s failed.\n";
char msgStatus[]    = "Internal error:  Unexpected tracklet status.\n";
char msgThread[]    = "Thread creation failed.\n";
char msgUsage[]     = "";
char msgLimitClassNotConfig[] = "";
char msgLimitScoreNotConfig[] = "";

// --- Helper functions needed by d2cli.c externs ---

// fatal/fatal1 - in library mode, we can't call exit().
// These are referenced by d2modelio.c and d2mpc.c for error paths.
// In library mode, we redirect these to set an error flag.
static int lib_fatal_flag = 0;
static char lib_fatal_msg[512] = {0};

void fatal(char *msg) {
    lib_fatal_flag = 1;
    strncpy(lib_fatal_msg, msg, sizeof(lib_fatal_msg) - 1);
    lib_fatal_msg[sizeof(lib_fatal_msg) - 1] = '\0';
}

void fatal1(char *msg, char *arg) {
    lib_fatal_flag = 1;
    snprintf(lib_fatal_msg, sizeof(lib_fatal_msg), msg, arg);
}

// CPspec and openCP are used by d2modelio.c and d2mpc.c
char *CPspec(char *fn, _Bool spec) {
    // In library mode, always use bare filename (paths set via d2_init)
    return fn;
}

FILE *openCP(char *fn, _Bool spec, char *mode) {
    return fopen(fn, mode);
}

// --- Library-internal read functions that return error codes ---

// Read population model using smart binary/CSV loading.
// Accepts either a CSV path (*.csv) or binary path; derives the other.
// Uses mustReadModelStatCSV() which prefers binary for speed, falls back
// to CSV, and auto-generates binary cache.
// Returns 0 on success, -1 on failure.
static int lib_read_model(const char *path) {
    char *save_fnCSV = fnCSV;
    char *save_fnModel = fnModel;
    lib_fatal_flag = 0;

    static char csv_buf[1024];
    static char model_buf[1024];
    size_t len = strlen(path);

    if (len >= 4 && strcmp(path + len - 4, ".csv") == 0) {
        // Path is CSV; derive binary by stripping ".csv"
        strncpy(csv_buf, path, sizeof(csv_buf) - 1);
        csv_buf[sizeof(csv_buf) - 1] = '\0';
        size_t model_len = len - 4 < sizeof(model_buf) - 1 ? len - 4 : sizeof(model_buf) - 1;
        memcpy(model_buf, path, model_len);
        model_buf[model_len] = '\0';
    } else {
        // Path is binary; derive CSV by appending ".csv"
        strncpy(model_buf, path, sizeof(model_buf) - 1);
        model_buf[sizeof(model_buf) - 1] = '\0';
        snprintf(csv_buf, sizeof(csv_buf), "%s.csv", path);
    }

    fnCSV = csv_buf;
    fnModel = model_buf;
    mustReadModelStatCSV();

    fnCSV = save_fnCSV;
    fnModel = save_fnModel;
    return lib_fatal_flag ? -1 : 0;
}

// Read observatory codes file. Returns 0 on success, -1 on failure.
static int lib_read_obscodes(const char *ocd_path) {
    char *save_fnOCD = fnOCD;
    fnOCD = (char *)ocd_path;
    ocdSpec = 1;  // tell openCP to use the path directly

    lib_fatal_flag = 0;
    mustReadOCD();

    fnOCD = save_fnOCD;
    ocdSpec = 0;

    if (lib_fatal_flag) {
        return -1;
    }
    return 0;
}

// --- Public API implementation ---

int d2_init(const char *model_path, const char *obscodes_path) {
    if (lib_initialized) {
        d2_cleanup();
    }

    // Initialize mathematical constants and default obsErr
    initGlobals();

    // Set up default class computation (all classes)
    for (int c = 0; c < D2CLASSES; c++) {
        classCompute[c] = c;
    }
    nClassCompute = D2CLASSES;

    // Default configuration
    repeatable = 1;
    raw = 1;
    noid = 1;
    rms = 1;

    // Read population model (binary preferred, CSV fallback)
    if (lib_read_model(model_path) != 0) {
        return D2_ERR_MODEL;
    }

    // Read observatory codes
    if (lib_read_obscodes(obscodes_path) != 0) {
        return D2_ERR_OBSCODES;
    }

    lib_initialized = 1;
    return D2_OK;
}

void d2_cleanup(void) {
    lib_initialized = 0;
}

int d2_is_initialized(void) {
    return lib_initialized;
}

void d2_set_default_obserr(double arcsec) {
    extern double arcsecrad;
    obsErr = arcsec * arcsecrad;
}

void d2_set_site_obserr(int site_index, double arcsec) {
    extern double arcsecrad;
    if (site_index >= 0 && site_index < obscodeNamespaceSize) {
        siteTable[site_index].obsErr = arcsec * arcsecrad;
    }
}

void d2_set_repeatable(int flag) {
    repeatable = flag ? 1 : 0;
}

void d2_set_no_threshold(int flag) {
    noThreshold = flag ? 1 : 0;
}

// --- Internal helpers for tracklet setup/teardown ---

// Validate class filter indices. Returns D2_OK or D2_ERR_INPUT.
static int lib_validate_classes(int *classes, int n_classes) {
    if (classes != NULL && n_classes > 0) {
        if (n_classes > D2CLASSES)
            return D2_ERR_INPUT;
        for (int i = 0; i < n_classes; i++) {
            if (classes[i] < 0 || classes[i] >= D2CLASSES)
                return D2_ERR_INPUT;
        }
    }
    return D2_OK;
}

// Allocate and populate a tracklet from input observations.
// classes/n_classes: per-tracklet class filter (NULL/0 = all classes).
// Returns NULL on error (sets *status to the error code).
static tracklet *lib_alloc_tracklet(d2_observation *obs, int n_obs,
                                     int *classes, int n_classes,
                                     int is_ades, int *status) {
    tracklet *tk = (tracklet *)calloc(1, sizeof(tracklet));
    if (!tk) {
        *status = D2_ERR_MEMORY;
        return NULL;
    }

    // Set up per-tracklet class filter
    if (classes != NULL && n_classes > 0) {
        tk->classFilter = (int *)malloc(n_classes * sizeof(int));
        if (!tk->classFilter) {
            free(tk);
            *status = D2_ERR_MEMORY;
            return NULL;
        }
        memcpy(tk->classFilter, classes, n_classes * sizeof(int));
        tk->nClassFilter = n_classes;
    }
    // else: classFilter = NULL, nClassFilter = 0 (from calloc) -> uses globals

    int nCC = tk->classFilter ? tk->nClassFilter : nClassCompute;

    tk->olist = (observation *)malloc(n_obs * sizeof(observation));
    if (!tk->olist) {
        free(tk->classFilter);
        free(tk);
        *status = D2_ERR_MEMORY;
        return NULL;
    }

    tk->class = (perClass *)calloc(nCC, sizeof(perClass));
    if (!tk->class) {
        free(tk->olist);
        free(tk->classFilter);
        free(tk);
        *status = D2_ERR_MEMORY;
        return NULL;
    }

    tk->status = UNPROC;
    tk->obsCap = n_obs;
    tk->lines = n_obs;
    tk->isAdes = is_ades ? 1 : 0;

    if (repeatable) {
        tk->rand64 = 3;
    } else {
        tk->rand64 = 2 * (rand() / 2) + 1;
    }

    extern double arcsecrad;

    for (int i = 0; i < n_obs; i++) {
        observation *o = &tk->olist[i];
        o->mjd  = obs[i].mjd;
        o->ra   = obs[i].ra;
        o->dec  = obs[i].dec;
        o->vmag = obs[i].vmag;
        o->site = obs[i].site;
        o->spacebased = obs[i].spacebased ? 1 : 0;
        if (o->spacebased) {
            memcpy(o->earth_observer, obs[i].earth_obs, sizeof(o->earth_observer));
        }
        o->rmsRA  = obs[i].rmsRA * arcsecrad;
        o->rmsDec = obs[i].rmsDec * arcsecrad;
    }

    double msum = 0;
    int mcount = 0;
    for (int i = 0; i < n_obs; i++) {
        if (tk->olist[i].vmag > 0.) {
            msum += tk->olist[i].vmag;
            mcount++;
        }
    }
    tk->vmag = mcount > 0 ? msum / mcount : 21.;

    observation *first = &tk->olist[0];
    observation *last  = &tk->olist[n_obs - 1];

    if (last->mjd < first->mjd) {
        *status = D2_ERR_INPUT;
        free(tk->class);
        free(tk->olist);
        free(tk);
        return NULL;
    }

    if (first->ra == last->ra && first->dec == last->dec) {
        *status = D2_ERR_INPUT;
        free(tk->class);
        free(tk->olist);
        free(tk);
        return NULL;
    }

    *status = D2_OK;
    return tk;
}

static void lib_extract_scores(tracklet *tk, d2_result *result) {
    result->rms = tk->rms;
    result->rms_prime = tk->rmsPrime;

    int nCC = tk->classFilter ? tk->nClassFilter : nClassCompute;
    int *cC = tk->classFilter ? tk->classFilter : classCompute;

    for (int c = 0; c < nCC; c++) {
        int ci = cC[c];
        if (ci >= 0 && ci < D2CLASSES) {
            result->raw_scores[ci]  = tk->class[c].rawScore;
            result->noid_scores[ci] = tk->class[c].noIdScore;
        }
    }

    result->status = D2_OK;
}

static void lib_free_tracklet(tracklet *tk) {
    if (tk) {
        free(tk->classFilter);
        free(tk->class);
        free(tk->olist);
        free(tk);
    }
}

// --- Public scoring API ---

d2_result d2_score_observations(d2_observation *obs, int n_obs,
                                int *classes, int n_classes,
                                int is_ades) {
    d2_result result;
    memset(&result, 0, sizeof(result));
    result.n_classes = D2CLASSES;

    if (!lib_initialized) {
        result.status = D2_ERR_NOINIT;
        return result;
    }

    if (n_obs < 2) {
        result.status = D2_ERR_INPUT;
        return result;
    }

    if (lib_validate_classes(classes, n_classes) != D2_OK) {
        result.status = D2_ERR_INPUT;
        return result;
    }

    int status;
    tracklet *tk = lib_alloc_tracklet(obs, n_obs, classes, n_classes,
                                       is_ades, &status);
    if (!tk) {
        result.status = status;
        return result;
    }

    score(tk);
    lib_extract_scores(tk, &result);
    lib_free_tracklet(tk);

    return result;
}

d2_result_ext d2_score_observations_ext(d2_observation *obs, int n_obs,
                                         int *classes, int n_classes,
                                         int is_ades) {
    d2_result_ext ext;
    memset(&ext, 0, sizeof(ext));
    ext.base.n_classes = D2CLASSES;

    if (!lib_initialized) {
        ext.base.status = D2_ERR_NOINIT;
        return ext;
    }

    if (n_obs < 2) {
        ext.base.status = D2_ERR_INPUT;
        return ext;
    }

    if (lib_validate_classes(classes, n_classes) != D2_OK) {
        ext.base.status = D2_ERR_INPUT;
        return ext;
    }

    int status;
    tracklet *tk = lib_alloc_tracklet(obs, n_obs, classes, n_classes,
                                       is_ades, &status);
    if (!tk) {
        ext.base.status = status;
        return ext;
    }

    // Allocate orbit buffer and attach to tracklet
    d2_orbit_buffer *buf = (d2_orbit_buffer *)malloc(sizeof(d2_orbit_buffer));
    if (!buf) {
        lib_free_tracklet(tk);
        ext.base.status = D2_ERR_MEMORY;
        return ext;
    }
    buf->capacity = 1024;
    buf->count = 0;
    buf->orbits = (d2_trial_orbit *)malloc(buf->capacity * sizeof(d2_trial_orbit));
    if (!buf->orbits) {
        free(buf);
        lib_free_tracklet(tk);
        ext.base.status = D2_ERR_MEMORY;
        return ext;
    }
    tk->orbit_buf = buf;

    score(tk);
    lib_extract_scores(tk, &ext.base);

    // Transfer orbit data to result
    ext.orbits = buf->orbits;
    ext.n_orbits = buf->count;
    buf->orbits = NULL;  // prevent double-free
    free(buf);
    tk->orbit_buf = NULL;

    lib_free_tracklet(tk);

    return ext;
}

void d2_free_result_ext(d2_result_ext *result) {
    if (result && result->orbits) {
        free(result->orbits);
        result->orbits = NULL;
        result->n_orbits = 0;
    }
}

int d2_parse_obscode(const char *code3) {
    return parseCod3((char *)code3);
}

int d2_get_class_count(void) {
    return D2CLASSES;
}

const char *d2_get_class_abbr(int index) {
    if (index < 0 || index >= D2CLASSES) return NULL;
    return classAbbr[index];
}

const char *d2_get_class_name(int index) {
    if (index < 0 || index >= D2CLASSES) return NULL;
    return classHeading[index];
}

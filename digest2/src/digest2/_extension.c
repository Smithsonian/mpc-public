// _extension.c
//
// Public domain.
//
// CPython C extension module bridging the d2lib C library API to Python.
// Compiled as digest2._extension.

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "d2lib.h"

// --- Module state ---

static int module_initialized = 0;

// --- Python-callable functions ---

static PyObject *py_init(PyObject *self, PyObject *args) {
    const char *model_path;
    const char *obscodes_path;

    if (!PyArg_ParseTuple(args, "ss", &model_path, &obscodes_path))
        return NULL;

    int rc = d2_init(model_path, obscodes_path);
    if (rc != D2_OK) {
        const char *msg;
        switch (rc) {
            case D2_ERR_MODEL:    msg = "Failed to load population model CSV"; break;
            case D2_ERR_OBSCODES: msg = "Failed to load observatory codes file"; break;
            case D2_ERR_MEMORY:   msg = "Memory allocation failed"; break;
            default:              msg = "Unknown initialization error"; break;
        }
        PyErr_SetString(PyExc_RuntimeError, msg);
        return NULL;
    }

    module_initialized = 1;
    Py_RETURN_NONE;
}

static PyObject *py_cleanup(PyObject *self, PyObject *noargs) {
    d2_cleanup();
    module_initialized = 0;
    Py_RETURN_NONE;
}

static PyObject *py_is_initialized(PyObject *self, PyObject *noargs) {
    return PyBool_FromLong(d2_is_initialized());
}

static PyObject *py_score(PyObject *self, PyObject *args) {
    PyObject *obs_list;
    PyObject *classes_obj = Py_None;
    int is_ades = 0;

    if (!PyArg_ParseTuple(args, "O|Oi", &obs_list, &classes_obj, &is_ades))
        return NULL;

    if (!module_initialized) {
        PyErr_SetString(PyExc_RuntimeError,
                        "digest2 not initialized. Call init() first.");
        return NULL;
    }

    if (!PyList_Check(obs_list)) {
        PyErr_SetString(PyExc_TypeError, "observations must be a list");
        return NULL;
    }

    Py_ssize_t n_obs = PyList_Size(obs_list);
    if (n_obs < 2) {
        PyErr_SetString(PyExc_ValueError,
                        "At least 2 observations required");
        return NULL;
    }

    // Parse observations
    d2_observation *obs = (d2_observation *)calloc(n_obs, sizeof(d2_observation));
    if (!obs) {
        PyErr_NoMemory();
        return NULL;
    }

    for (Py_ssize_t i = 0; i < n_obs; i++) {
        PyObject *item = PyList_GetItem(obs_list, i);
        if (!PyTuple_Check(item) && !PyDict_Check(item)) {
            free(obs);
            PyErr_SetString(PyExc_TypeError,
                            "Each observation must be a tuple or dict");
            return NULL;
        }

        if (PyTuple_Check(item)) {
            // Tuple format: (mjd, ra_rad, dec_rad, vmag, site_int, rmsRA, rmsDec)
            // Optional 8th element: spacebased (int)
            Py_ssize_t tlen = PyTuple_Size(item);
            if (tlen < 5) {
                free(obs);
                PyErr_SetString(PyExc_ValueError,
                    "Observation tuple must have at least 5 elements: "
                    "(mjd, ra_rad, dec_rad, vmag, site_int)");
                return NULL;
            }
            obs[i].mjd  = PyFloat_AsDouble(PyTuple_GetItem(item, 0));
            obs[i].ra   = PyFloat_AsDouble(PyTuple_GetItem(item, 1));
            obs[i].dec  = PyFloat_AsDouble(PyTuple_GetItem(item, 2));
            obs[i].vmag = PyFloat_AsDouble(PyTuple_GetItem(item, 3));
            obs[i].site = (int)PyLong_AsLong(PyTuple_GetItem(item, 4));
            if (tlen > 5)
                obs[i].rmsRA = PyFloat_AsDouble(PyTuple_GetItem(item, 5));
            if (tlen > 6)
                obs[i].rmsDec = PyFloat_AsDouble(PyTuple_GetItem(item, 6));
            if (tlen > 7)
                obs[i].spacebased = (int)PyLong_AsLong(PyTuple_GetItem(item, 7));
        } else {
            // Dict format with keys: mjd, ra, dec, vmag, site, rmsRA, rmsDec, spacebased
            PyObject *val;
            val = PyDict_GetItemString(item, "mjd");
            if (!val) { free(obs); PyErr_SetString(PyExc_KeyError, "mjd"); return NULL; }
            obs[i].mjd = PyFloat_AsDouble(val);

            val = PyDict_GetItemString(item, "ra");
            if (!val) { free(obs); PyErr_SetString(PyExc_KeyError, "ra"); return NULL; }
            obs[i].ra = PyFloat_AsDouble(val);

            val = PyDict_GetItemString(item, "dec");
            if (!val) { free(obs); PyErr_SetString(PyExc_KeyError, "dec"); return NULL; }
            obs[i].dec = PyFloat_AsDouble(val);

            val = PyDict_GetItemString(item, "vmag");
            obs[i].vmag = val ? PyFloat_AsDouble(val) : 0.0;

            val = PyDict_GetItemString(item, "site");
            if (!val) { free(obs); PyErr_SetString(PyExc_KeyError, "site"); return NULL; }
            obs[i].site = (int)PyLong_AsLong(val);

            val = PyDict_GetItemString(item, "rmsRA");
            obs[i].rmsRA = val ? PyFloat_AsDouble(val) : 0.0;

            val = PyDict_GetItemString(item, "rmsDec");
            obs[i].rmsDec = val ? PyFloat_AsDouble(val) : 0.0;

            val = PyDict_GetItemString(item, "spacebased");
            obs[i].spacebased = val ? (int)PyLong_AsLong(val) : 0;
        }

        if (PyErr_Occurred()) {
            free(obs);
            return NULL;
        }
    }

    // Parse classes filter
    int *class_indices = NULL;
    int n_classes = 0;

    if (classes_obj != Py_None && PyList_Check(classes_obj)) {
        n_classes = (int)PyList_Size(classes_obj);
        if (n_classes > 0) {
            class_indices = (int *)malloc(n_classes * sizeof(int));
            if (!class_indices) {
                free(obs);
                PyErr_NoMemory();
                return NULL;
            }
            for (int i = 0; i < n_classes; i++) {
                class_indices[i] = (int)PyLong_AsLong(PyList_GetItem(classes_obj, i));
                if (PyErr_Occurred()) {
                    free(obs);
                    free(class_indices);
                    return NULL;
                }
            }
        }
    }

    // Call the C scoring function
    d2_result res = d2_score_observations(obs, (int)n_obs, class_indices, n_classes, is_ades);

    free(obs);
    if (class_indices) free(class_indices);

    if (res.status != D2_OK) {
        const char *msg;
        switch (res.status) {
            case D2_ERR_INPUT:  msg = "Invalid input (need >=2 obs with motion and time span)"; break;
            case D2_ERR_MEMORY: msg = "Memory allocation failed"; break;
            case D2_ERR_NOINIT: msg = "Library not initialized"; break;
            default:            msg = "Scoring error"; break;
        }
        PyErr_SetString(PyExc_RuntimeError, msg);
        return NULL;
    }

    // Build result dict
    PyObject *raw_list = PyList_New(D2CLASSES);
    PyObject *noid_list = PyList_New(D2CLASSES);
    if (!raw_list || !noid_list) {
        Py_XDECREF(raw_list);
        Py_XDECREF(noid_list);
        return PyErr_NoMemory();
    }

    for (int i = 0; i < D2CLASSES; i++) {
        PyList_SET_ITEM(raw_list, i, PyFloat_FromDouble(res.raw_scores[i]));
        PyList_SET_ITEM(noid_list, i, PyFloat_FromDouble(res.noid_scores[i]));
    }

    PyObject *result = Py_BuildValue("{sOsOsdsd}",
        "raw_scores", raw_list,
        "noid_scores", noid_list,
        "rms", res.rms,
        "rms_prime", res.rms_prime);

    Py_DECREF(raw_list);
    Py_DECREF(noid_list);

    return result;
}

static PyObject *py_configure(PyObject *self, PyObject *args, PyObject *kwargs) {
    static char *kwlist[] = {"obserr", "repeatable", "no_threshold",
                             "site_errors", NULL};
    double obserr = -1.0;
    int repeatable_flag = -1;
    int no_threshold_flag = -1;
    PyObject *site_errors = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|diiO", kwlist,
                                     &obserr, &repeatable_flag,
                                     &no_threshold_flag, &site_errors))
        return NULL;

    if (obserr >= 0.0) {
        d2_set_default_obserr(obserr);
    }

    if (repeatable_flag >= 0) {
        d2_set_repeatable(repeatable_flag);
    }

    if (no_threshold_flag >= 0) {
        d2_set_no_threshold(no_threshold_flag);
    }

    if (site_errors && PyDict_Check(site_errors)) {
        PyObject *key, *value;
        Py_ssize_t pos = 0;
        while (PyDict_Next(site_errors, &pos, &key, &value)) {
            int site_idx;
            if (PyUnicode_Check(key)) {
                const char *code = PyUnicode_AsUTF8(key);
                site_idx = d2_parse_obscode(code);
            } else {
                site_idx = (int)PyLong_AsLong(key);
            }
            if (site_idx < 0) {
                PyErr_SetString(PyExc_ValueError, "Invalid observatory code");
                return NULL;
            }
            double err = PyFloat_AsDouble(value);
            if (PyErr_Occurred()) return NULL;
            d2_set_site_obserr(site_idx, err);
        }
    }

    Py_RETURN_NONE;
}

static PyObject *py_parse_obscode(PyObject *self, PyObject *args) {
    const char *code;
    if (!PyArg_ParseTuple(args, "s", &code))
        return NULL;

    int idx = d2_parse_obscode(code);
    if (idx < 0) {
        PyErr_SetString(PyExc_ValueError, "Invalid observatory code");
        return NULL;
    }
    return PyLong_FromLong(idx);
}

static PyObject *py_get_classes(PyObject *self, PyObject *noargs) {
    int n = d2_get_class_count();
    PyObject *list = PyList_New(n);
    if (!list) return NULL;

    for (int i = 0; i < n; i++) {
        PyObject *tup = Py_BuildValue("(ss)",
            d2_get_class_abbr(i),
            d2_get_class_name(i));
        if (!tup) {
            Py_DECREF(list);
            return NULL;
        }
        PyList_SET_ITEM(list, i, tup);
    }
    return list;
}

// --- Module definition ---

static PyMethodDef methods[] = {
    {"init",           py_init,           METH_VARARGS,
     "init(model_csv_path, obscodes_path)\n"
     "Initialize digest2 with model and observatory data."},
    {"cleanup",        py_cleanup,        METH_NOARGS,
     "cleanup()\nRelease resources."},
    {"is_initialized", py_is_initialized, METH_NOARGS,
     "is_initialized() -> bool\nCheck if digest2 is initialized."},
    {"score",          py_score,          METH_VARARGS,
     "score(observations, classes=None, is_ades=0) -> dict\n"
     "Score a tracklet. observations is a list of tuples or dicts.\n"
     "Tuple format: (mjd, ra_rad, dec_rad, vmag, site_int[, rmsRA, rmsDec, spacebased])\n"
     "Returns dict with 'raw_scores', 'noid_scores', 'rms', 'rms_prime'."},
    {"configure",      (PyCFunction)py_configure, METH_VARARGS | METH_KEYWORDS,
     "configure(obserr=None, repeatable=None, no_threshold=None, site_errors=None)\n"
     "Set scoring configuration."},
    {"parse_obscode",  py_parse_obscode,  METH_VARARGS,
     "parse_obscode(code) -> int\nConvert 3-char MPC obscode to integer index."},
    {"get_classes",    py_get_classes,    METH_NOARGS,
     "get_classes() -> list of (abbr, name) tuples for all orbit classes."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "_extension",
    "Low-level C extension for digest2 orbit classification.",
    -1,
    methods
};

PyMODINIT_FUNC PyInit__extension(void) {
    return PyModule_Create(&moduledef);
}

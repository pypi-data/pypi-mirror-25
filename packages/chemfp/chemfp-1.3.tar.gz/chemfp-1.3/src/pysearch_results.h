#include <Python.h>
#include "chemfp.h"

typedef struct {
    PyObject_HEAD
    int num_results;
    int num_columns;
    chemfp_search_result *results;
    PyObject *target_ids;
} SearchResults;

extern PyTypeObject chemfp_py_SearchResultsType;

#include <Python.h>

#define MCACHE_SIZE_EXP 12
#define MCACHE_MAX_ATTR_SIZE 100
#define MCACHE_HASH(version, name_hash) \
    (((unsigned int)(version) ^ (unsigned int)(name_hash)) & ((1 << MCACHE_SIZE_EXP) - 1))

#define MCACHE_HASH_METHOD(type, name) \
    MCACHE_HASH((type)->tp_version_tag, ((Py_ssize_t)(name)) >> 3)
#define MCACHE_CACHEABLE_NAME(name) \
    PyUnicode_CheckExact(name) &&   \
        PyUnicode_IS_READY(name) && \
        (PyUnicode_GET_LENGTH(name) <= MCACHE_MAX_ATTR_SIZE)

static PyObject *
compute_hash(PyObject *self, PyObject *args)
{
    PyTypeObject *type = PyTuple_GetItem(args, 0);
    PyObject *name = PyTuple_GetItem(args, 1);

    unsigned int h = MCACHE_HASH_METHOD(type, name);
    return PyLong_FromLong((long)h);
}

static PyMethodDef HashModMethods[] = {
    {"compute_hash", compute_hash, METH_VARARGS, ""},
    {NULL, NULL, 0, NULL},
};

static struct PyModuleDef hashmodmodule = {
    PyModuleDef_HEAD_INIT,
    "typecachemod",
    "",
    -1,
    HashModMethods,
};

PyMODINIT_FUNC PyInit_hashmod(void)
{
    return PyModule_Create(&hashmodmodule);
}

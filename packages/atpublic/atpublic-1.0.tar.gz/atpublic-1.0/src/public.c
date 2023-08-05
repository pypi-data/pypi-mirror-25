/*
Copyright (C) 2016-2017 Barry Warsaw

This project is licensed under the terms of the Apache 2.0 License.  See
LICENSE.txt for details.
*/

#include <Python.h>


static PyObject *
public(PyObject *self, PyObject *args, PyObject *kwds)
{
    PyObject *arg = NULL;
    PyObject *globals = NULL;
    PyObject *all = NULL;
    PyObject *rtn = NULL;

    if (!PyArg_UnpackTuple(args, "public", 0, 1, &arg))
        return NULL;

    /* kwds can be empty, but the keys must be strings. */
    if (kwds != NULL && !PyArg_ValidateKeywordArguments(kwds))
        return NULL;

    if (!(globals = PyEval_GetGlobals())) {
        PyErr_Format(PyExc_TypeError,
                     "@public called with no active globals");
        return NULL;
    }
    if (!(all = PyDict_GetItemString(globals, "__all__"))) {
        if (!(all = PyList_New(0)))
            return NULL;
        if (PyDict_SetItemString(globals, "__all__", all) < 0)
            goto byebye;
    }
    else {
        /* Make sure __all__ is a list, raising an exception if not.  Bump
           all's reference count since it's currently borrowed, and this way
           we guarantee we own a reference for common exit cleanup.
        */
        if (!PyList_Check(all)) {
            PyErr_Format(PyExc_ValueError,
                         "__all__ must be a list not: %S",
                         all->ob_type);
            goto byebye;
        }
        Py_INCREF(all);
    }

    if (arg != NULL) {
        PyObject *name = NULL;

        /* There is a single positional argument.  This must have a "__name__"
           attribute, which we will put in __all__.  The keywords dictionary
           must be empty.
        */
        if (kwds != NULL && PyDict_Size(kwds) != 0) {
            PyErr_Format(PyExc_TypeError,
                         "Positional and keywords are mutually exclusive");
            goto byebye;
        }
        if (!PyObject_HasAttrString(arg, "__name__")) {
            PyErr_Format(PyExc_TypeError,
                         "Positional argument has no __name__");
            goto byebye;
        }
        if (!(name = PyObject_GetAttrString(arg, "__name__")) ||
            !PyUnicode_Check(name))
        {
            PyErr_Format(PyExc_TypeError, "Bad __name__ value");
            Py_XDECREF(name);
            goto byebye;
        }
        if (PyList_Append(all, name) < 0) {
            Py_DECREF(name);
            goto byebye;
        }
        Py_DECREF(name);
        rtn = arg;
    }
    else if (kwds == NULL || PyDict_Size(kwds) == 0) {
        PyErr_Format(
            PyExc_TypeError,
            "Either a single positional or keyword arguments required");
        goto byebye;
    }
    else {
        /* There are only keyword arguments, so for each of these, insert the
           key in __all__ *and* bind the name/key to the value in globals.  We
           force the use of globals here because we're modifying the global
           __all__ so it doesn't make sense to touch locals.
        */
        PyObject *key, *value;
        Py_ssize_t pos = 0;

        while (PyDict_Next(kwds, &pos, &key, &value)) {
            if (PyList_Append(all, key) < 0)
                goto byebye;
            if (PyDict_SetItem(globals, key, value) < 0)
                goto byebye;
        }
        rtn = Py_None;
    }

  byebye:
    Py_DECREF(all);
    Py_XINCREF(rtn);
    return rtn;
}

PyDoc_STRVAR(public_doc,
"public(named)\n\
public(**kws)\n\
\n\
May be used as a decorator or called directly.  When used as a decorator\n\
the thing being decorated must have an __name__ attribute.  The value of\n\
__name__ will be inserted in the global __all__ list.  In this use case\n\
it is an error to also include keyword arguments.\n\
\n\
When called directly, it is an error to pass a positional argument.  The\n\
keys must be strings, and are inserted into the global __all__ list. The\n\
mapping of keys to values is also inserted into the globals, thus creating\n\
name bindings for each key/value pair.");


static PyMethodDef public_methods[] = {
    {"public",  (PyCFunction)public, METH_VARARGS | METH_KEYWORDS, public_doc},
    {NULL,  NULL}
};


static struct PyModuleDef public_def = {
    PyModuleDef_HEAD_INIT,
    "public",
    NULL,
    0,                          /* size of module state */
    public_methods,
    NULL
};


PyObject *
PyInit__public(void)
{
    return PyModule_Create(&public_def);
}

/*
 * Local Variables:
 * c-file-style: "python3"
 * End:
 */

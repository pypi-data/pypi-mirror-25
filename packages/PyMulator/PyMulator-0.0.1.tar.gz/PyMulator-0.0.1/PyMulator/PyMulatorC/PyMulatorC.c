/* Mulator - An extensible {ARM} {e,si}mulator
 * Copyright 2011-2012  Pat Pannuto <pat.pannuto@gmail.com>
 * Copyright 2017  Andrew Lukefahr <lukefahr@indiana.edu>
 *
 * This file is part of Mulator.
 *
 * Mulator is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Mulator is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Mulator.  If not, see <http://www.gnu.org/licenses/>.
 */

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

#include <pthread.h>

#include <Python.h>

#include "core/common.h"
#include "csrc/interface.h"
#include "csrc/helpers.h"

//prototyping 
static PyObject * py_call_to_mulator (PyObject * self, PyObject * args);
static PyObject * py_register_callback( PyObject * dummy, PyObject * args);

//declares an exception class
static PyObject * PyMulatorCError;

//tells python our methods
static PyMethodDef PyMulatorCMethods[] = {
    {"call_to_mulator", py_call_to_mulator, METH_VARARGS,
        "a gdb-like wrapper for M-ulator in Python."},
    {"register_callback", py_register_callback, METH_VARARGS,
        "register a callback for Mulator" },
    {NULL, NULL, 0, NULL}
};

//pointer to the python callback function
static PyObject *py_callback = NULL;

/**
 * inializer for the PyMulatorC module 
 */
PyMODINIT_FUNC
initPyMulatorC(void)
{
    PyObject *m;

    m = Py_InitModule("PyMulatorC", PyMulatorCMethods);
    if (m == NULL)
        return;

    PyMulatorCError = PyErr_NewException("PyMulatorC.error", NULL, NULL);
    Py_INCREF(PyMulatorCError);
    PyModule_AddObject(m, "error", PyMulatorCError);
}

/**
 * called by python to register a callback function
 *
 * @dummy: a Python object of the class (not used)
 * @args: a single argument containing a Python function
 */
static PyObject * 
py_register_callback( PyObject * dummy, PyObject * args)
{
    PyObject *result = NULL;
    PyObject *temp;

    if (PyArg_ParseTuple(args, "O:set_callback", &temp)) {
        if (!PyCallable_Check(temp)) {
            PyErr_SetString(PyExc_TypeError, "parameter must be callable");
            return NULL;
        }
        Py_XINCREF(temp);         /* Add a reference to new callback */
        Py_XDECREF(py_callback);  /* Dispose of previous callback */
        py_callback = temp;       /* Remember new callback */

        /* Boilerplate to return "None" */
        Py_INCREF(Py_None);
        result = Py_None;
    }
    return result;
}

/**
 * called by python to start Mulator
 * 
 * @self: Python object to the class (not used)
 * @args:  a single string containing the command to be passed to Mulator
 */
static PyObject * py_call_to_mulator(PyObject * self, PyObject * args)
{
    int err = 0;
    char * input;
    PyObject * ret;

    // parse arguments
    if (!PyArg_ParseTuple(args, "s", &input)) {
        return NULL;
    }
    
    DBG2("T0: Start Mulator\n");
    call_to_mulator(input);
   

    // build the result into a Python object.
    ret = PyBool_FromLong(err); 

    return ret;
}

/**
 * called by Mulator to request more information
 * 
 * This will call back into Python to request that information
 *
 * @command:  a gdb-like request from Mulator
 * @result:  a pointer to where Mulator expects a gdb-like response to be placed
 */
void call_from_mulator( char * command, char ** result)
{

    PyObject *arglist;
    PyObject *pyresult;
    
    if (py_callback == NULL){
        printf("Found NULL py_callback function, aborting\n");
        UNIMPLIMENTED();
    } 

    /* Time to call the callback */
    DBG2("T0: passing request to python: %s\n", command); 
    arglist = Py_BuildValue("(s)", command);
    pyresult = PyObject_CallObject(py_callback, arglist);
    Py_DECREF(arglist);

    if (pyresult == NULL){
        printf("Found NULL pyresult, aborting\n");
        UNIMPLIMENTED();
    } else {
        const char * resp = PyString_AsString(pyresult);

        DBG2("T0: parsed response: %s\n", resp); 

        /* Here we can (finally) use the result */
        asprintf( result, "%s", resp); 

        Py_DECREF(pyresult);
    }

}



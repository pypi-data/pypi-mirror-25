/* -*- C -*-                                                             */
/* AsapPython.h: Includes Python.h and numarrays correctly               */
/*                                                                       */
/* Copyright (C) 2008 Jakob Schiotz and Center for Individual            */
/* Nanoparticle Functionality, Department of Physics, Technical          */
/* University of Denmark.  Email: schiotz@fysik.dtu.dk                   */
/*                                                                       */
/* This file is part of Asap version 3.                                  */
/*                                                                       */
/* This program is free software: you can redistribute it and/or         */
/* modify it under the terms of the GNU Lesser General Public License    */
/* version 3 as published by the Free Software Foundation.               */
/* Permission to use other versions of the GNU Lesser General Public     */
/* License may granted by Jakob Schiotz or the head of department of the */
/* Department of Physics, Technical University of Denmark, as described  */
/* in section 14 of the GNU General Public License.                      */
/*                                                                       */
/* This program is distributed in the hope that it will be useful,       */
/* but WITHOUT ANY WARRANTY; without even the implied warranty of        */
/* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         */
/* GNU General Public License for more details.                          */
/*                                                                       */
/* You should have received a copy of the GNU General Public License     */
/* along with this program.  If not, see <http://www.gnu.org/licenses/>. */


/* This file should be included by any file accessing Python objects,    */
/* except the AsapModule.cpp which should import the NumPy module.       */
/*                                                                       */
/* This file MUST remain valid C as well as valid C++ !                  */
/*                                                                       */
/* This file must be included BEFORE any other header file !             */


#ifndef _ASAPPYTHON_H
#define _ASAPPYTHON_H

#include <Python.h>
#define PY_ARRAY_UNIQUE_SYMBOL Asap_Array_API
#define NO_IMPORT_ARRAY
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <numpy/arrayobject.h>
#ifdef __cplusplus  // Allow inclusion from mpi.c
#include "Exception.h"

// Take a PyObject and check that it is a reasonable PyArrayObject
inline PyArrayObject *AsPyArray(PyObject *p) {
  if ((p != NULL) && !PyArray_Check(p))
    throw AsapError("Expected a NumPy array, got something else!");
  return (PyArrayObject *) p;
}
#endif // __cplusplus

#define CHECKREF(x) assert(Py_REFCNT(x) >= 1 && Py_REFCNT(x) <= 100);
#define XCHECKREF(x) assert((x) == NULL || (Py_REFCNT(x) >= 1 && Py_REFCNT(x) <= 100));
#define PRINTREF(x) cerr << __FILE__ << ":" << __LINE__ << " Refcount=" << Py_REFCNT(x) << endl;


/* Python 2 or Python 3 ? */
#if PY_MAJOR_VERSION >= 3
#define ASAP_PY3
#endif

#ifdef ASAP_PY3
#define PyAsapString_Check PyUnicode_Check
#define PyAsapString_Type PyUnicode_Type
#define PyAsapString_FromString PyUnicode_FromString
#define PyAsapString_AsString PyUnicode_AsUTF8
#define PyAsapInt_AsLong PyLong_AsLong
#define PyAsapInt_FromLong PyLong_FromLong
#define PyAsapInt_Check PyLong_Check
#else
#define PyAsapString_Check PyString_Check
#define PyAsapString_Type PyString_Type
#define PyAsapString_FromString PyString_FromString
#define PyAsapString_AsString PyString_AsString
#define PyAsapInt_AsLong PyInt_AsLong
#define PyAsapInt_FromLong PyInt_FromLong
#define PyAsapInt_Check PyInt_Check
#endif

#endif /* _ASAPPYTHON_H */

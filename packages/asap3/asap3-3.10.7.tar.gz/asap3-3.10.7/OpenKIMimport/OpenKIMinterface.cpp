// OpenKIMinterface.cpp - Python interface to OpenKIM models.
//
// This file is part of the optional Asap module to support OpenKIM
// models.  Defines the Python interface to the modules in the
// other files in OpenKIMimport.

// Copyright (C) 2014 Jakob Schiotz and Center for Individual
// Nanoparticle Functionality, Department of Physics, Technical
// University of Denmark.  Email: schiotz@fysik.dtu.dk
//
// This file is part of Asap version 3.
// Asap is released under the GNU Lesser Public License (LGPL) version 3.
// However, the parts of Asap distributed within the OpenKIM project
// (including this file) are also released under the Common Development
// and Distribution License (CDDL) version 1.0.
//
// This program is free software: you can redistribute it and/or
// modify it under the terms of the GNU Lesser General Public License
// version 3 as published by the Free Software Foundation.  Permission
// to use other versions of the GNU Lesser General Public License may
// granted by Jakob Schiotz or the head of department of the
// Department of Physics, Technical University of Denmark, as
// described in section 14 of the GNU General Public License.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// and the GNU Lesser Public License along with this program.  If not,
// see <http://www.gnu.org/licenses/>.

#include "AsapPython.h"
#include "OpenKIMinterface.h"
#include "OpenKIMinfo.h"
#include "OpenKIMcalculator.h"
#include "Templates.h"
#include "ExceptionInterface.h"
#include "PotentialInterface.h"
//#define ASAPDEBUG
#include "Debug.h"
#include "KIM_API.h"
#include "KIM_API_status.h"
#include <cstdlib>

#define KIMCHECKFAIL(m, x) PyErr_Format(PyAsap_ErrorObject, "KIM error %s at %s:%i", PyAsap_get_kimerror(m, x), __FILE__, __LINE__);

namespace ASAPSPACE {

//////////////////////////////
//
//  OpenKIMinfo object
//
//////////////////////////////

static PyTypeObject PyAsap_OpenKIMinfoType = {
  PyVarObject_HEAD_INIT(NULL, 0)
  "_asap.OpenKIMinfo",
  sizeof(PyAsap_OpenKIMinfoObject),
  // The rest are initialized by name for reliability.
};

char OpenKIMinfo_Docstring[] =
    "Informational about an OpenKIM model\n\n\
  Parameters:\n\
    name: The name of the model.\n\n";

PyObject *PyAsap_NewOpenKIMinfo(PyObject *noself, PyObject *args,
                                PyObject *kwargs)
{
  static char *kwlist[] = {"name", NULL};
  DEBUGPRINT;
  const char *name = NULL;
  if (!PyArg_ParseTupleAndKeywords(args, kwargs,  "s:NewOpenKIMinfo",
      kwlist, &name))
    return NULL;
  try {
      DEBUGPRINT;
      PyAsap_OpenKIMinfoObject *self = PyAsap_NewOpenKIMinfoObject(name);
      DEBUGPRINT;
      return (PyObject *) self;
  }
  CATCHEXCEPTION;
}

PyAsap_OpenKIMinfoObject *PyAsap_NewOpenKIMinfoObject(const char *name)
{
  DEBUGPRINT;
  PyAsap_OpenKIMinfoObject *self;

  self = PyObject_NEW(PyAsap_OpenKIMinfoObject,
                      &PyAsap_OpenKIMinfoType);
  if (self == NULL)
    throw AsapError("Failed to create OpenKIMinfo object ");

  self->weakrefs = NULL;
  self->cobj = new OpenKIMinfo(name);
  DEBUGPRINT;
  if (self->cobj == NULL)
    {
      CHECKREF(self);
      Py_DECREF(self);
      throw AsapError("Failed to create a new OpenKIMinfo object.");
    }
  DEBUGPRINT;
  return self;
}


static PyObject *PyAsap_OpenKIMinfoGetSupportedTypes(PyAsap_OpenKIMinfoObject
                                                     *self, PyObject *noargs)
{
  DEBUGPRINT;
  std::vector<const char *> symbols;
  self->cobj->GetSupportedSymbols(symbols);
  int num = symbols.size();
  PyObject *result = PyTuple_New(num);
  if (result == NULL)
    return NULL;
  for (int i = 0; i < num; i++)
    {
      PyTuple_SET_ITEM(result, i, PyUnicode_FromString(symbols[i]));
    }
  DEBUGPRINT;
  return result;
}

static PyObject *PyAsap_OpenKIMinfoGetSupportedNbList(PyAsap_OpenKIMinfoObject
                                                   *self, PyObject *noargs)
{
  DEBUGPRINT;
  PyObject *result;
  try {
      const std::vector<const char *> &pbc_types = self->cobj->GetSupportedNBC();

      int n = pbc_types.size();
      result = PyTuple_New(n);
      if (result == NULL)
        return NULL;
      for (int i = 0; i < n; i++)
        {
          PyTuple_SET_ITEM(result, i, PyUnicode_FromString(pbc_types[i]));
        }
  }
  CATCHEXCEPTION;
  DEBUGPRINT;
  return result;
}

static PyObject *PyAsap_OpenKIMinfoGetSupportedAccess(PyAsap_OpenKIMinfoObject
                                                     *self, PyObject *noargs)
{
  DEBUGPRINT;
  PyObject *result;
  try {
      const std::vector<const char *> &pbc_types = self->cobj->GetSupportedAccess();

      int n = pbc_types.size();
      result = PyTuple_New(n);
      if (result == NULL)
        return NULL;
      for (int i = 0; i < n; i++)
        {
          PyTuple_SET_ITEM(result, i, PyUnicode_FromString(pbc_types[i]));
        }
  }
  CATCHEXCEPTION;
  DEBUGPRINT;
  return result;
}

static PyObject *PyAsap_OpenKIMinfoGetAPIindex(PyAsap_OpenKIMinfoObject
                                               *self, PyObject *args,
                                               PyObject *kwargs)
{
  DEBUGPRINT;
  static char *kwlist[] = {"name", NULL};

  const char *name = NULL;
  if (!PyArg_ParseTupleAndKeywords(args, kwargs,  "s:get_API_index",
      kwlist, &name))
    return NULL;
  try {
      int result = self->cobj->GetAPIindex(name);
      return Py_BuildValue("i", result);
  }
  CATCHEXCEPTION;
  DEBUGPRINT;
}

static PyMethodDef PyAsap_OpenKIMinfoMethods[] = {
  {"get_supported_types", (PyCFunction) PyAsap_OpenKIMinfoGetSupportedTypes,
   METH_NOARGS, "Get the supported elements as a tuple of chemical symbols"},
  {"get_supported_nblist", (PyCFunction) PyAsap_OpenKIMinfoGetSupportedNbList,
   METH_NOARGS, "Get the supported boundary condition / neighbor list methods"},
  {"get_supported_access", (PyCFunction) PyAsap_OpenKIMinfoGetSupportedAccess,
    METH_NOARGS, "Get the supported neighbor list access methods"},
  {"get_API_index", (PyCFunction) PyAsap_OpenKIMinfoGetAPIindex,
   METH_VARARGS | METH_KEYWORDS, "Get API index of property - or -1 if not supported"},
  {NULL}
};



//////////////////////////////
//
//  OpenKIMcalculator object
//
//////////////////////////////

static PyTypeObject PyAsap_OpenKIMcalculatorType = {
  PyVarObject_HEAD_INIT(NULL, 0)
  "_asap.OpenKIMcalculator",
  sizeof(PyAsap_PotentialObject),
  // The rest are initialized by name for reliability.
};

char OpenKIMcalculator_Docstring[] =
    "Internal interface to an OpenKIM model\n\n\
  Parameters:\n\
    descr: OpenKIM descriptor string.\n\
    name: The name of the model.\n\n";


static int PyAsap_OpenKIMcalculatorInit(PyAsap_PotentialObject *self, PyObject *args,
                                        PyObject *kwargs)
{
  if (PyAsap_PotentialType.tp_init((PyObject *)self, args, kwargs) < 0)
    return -1;
  try
    {
      self->cobj = new OpenKIMcalculator((PyObject *) self);
      self->orig_cobj = self->cobj;
    }
  catch (AsapError &e)
    {
      string msg = e.GetMessage();
      PyErr_SetString(PyAsap_ErrorObject, msg.c_str());
      return -1;
    }
  catch (AsapPythonError &e)
    {
      return -1;
    }
  if (self->cobj == NULL)
    return -1;
  return 0;
}

static PyObject *PyAsap_OpenKIMcalcInitialize(PyAsap_PotentialObject *self, PyObject *args,
                                              PyObject *kwargs)
{
  static char *kwlist[] = {"descr", "name", NULL};
  const char *descr = NULL;
  const char *name = NULL;
  if (!PyArg_ParseTupleAndKeywords(args, kwargs,  "ss:NewOpenKIMcalculator",
                                   kwlist, &descr, &name))
    return NULL;
  OpenKIMcalculator *cobj = dynamic_cast<OpenKIMcalculator *>(self->orig_cobj);
  assert(cobj != NULL);
  try {
    cobj->Initialize(descr, name);
  }
  catch (AsapError &e)
    {
      string msg = e.GetMessage();
      PyErr_SetString(PyAsap_ErrorObject, msg.c_str());
      return NULL;
    }
  catch (AsapPythonError &e)
    {
      return NULL;
    }
  Py_RETURN_NONE;
}


static PyObject *PyAsap_OpenKIMcalcGetNBCmethod(PyAsap_PotentialObject
                                               *self, PyObject *noargs)
{
  OpenKIMcalculator *cobj = dynamic_cast<OpenKIMcalculator *>(self->orig_cobj);
  assert(cobj != NULL);
  const char *pbc;
  try {
      pbc = cobj->GetNBCmethod();
  }
  catch (AsapError &e)
    {
      string msg = e.GetMessage();
      PyErr_SetString(PyAsap_ErrorObject, msg.c_str());
      return NULL;
    }
  catch (AsapPythonError &e)
    {
      return NULL;
    }
  PyObject *result = Py_BuildValue("s", pbc);
  return result;
}

static PyObject *PyAsap_OpenKIMcalcPleaseAlloc(PyAsap_PotentialObject *self,
                                               PyObject *args, PyObject *kwargs)
{
  static char *kwlist[] = {"quantity", "alloc", NULL};
  const char *quantity = NULL;
  int alloc = 0;
  if (!PyArg_ParseTupleAndKeywords(args, kwargs,  "si:please_allocate", kwlist,
                                   &quantity, &alloc))
    return NULL;
  OpenKIMcalculator *cobj = dynamic_cast<OpenKIMcalculator *>(self->orig_cobj);
  assert(cobj != NULL);
  try
  {
    cobj->PleaseAllocate(quantity, alloc);
  }
  catch (AsapError &e)
    {
      string msg = e.GetMessage();
      PyErr_SetString(PyAsap_ErrorObject, msg.c_str());
      return NULL;
    }
  catch (AsapPythonError &e)
    {
      return NULL;
    }
  Py_RETURN_NONE;
}

static PyObject *PyAsap_OpenKIMcalcSetTranslation(PyAsap_PotentialObject *self,
                                                 PyObject *args, PyObject *kwargs)
{
  static char *kwlist[] = {"translation", NULL};
  PyObject *translation = NULL;
  if (!PyArg_ParseTupleAndKeywords(args, kwargs,  "O!:set_translation", kwlist,
                                   &PyDict_Type, &translation))
    return NULL;
  OpenKIMcalculator *cobj = dynamic_cast<OpenKIMcalculator *>(self->orig_cobj);
  assert(cobj != NULL);
  cobj->ClearTranslation();
  PyObject *key, *value;
  Py_ssize_t i = 0;
  while (PyDict_Next(translation, &i, &key, &value))
    {
      int z = PyAsapInt_AsLong(key);
      int code = PyAsapInt_AsLong(value);
      if (z == -1 || code == -1)
        return PyErr_Format(PyExc_ValueError,
            "Illegal translation %i -> %i (or non-integer type)", z, code);
      cobj->AddTranslation(z, code);
    }
  Py_RETURN_NONE;
}


static PyObject *PyAsap_OpenKIMcalcGetSupportedTypes(PyAsap_PotentialObject
                                                     *self, PyObject *noargs)
{
  DEBUGPRINT;
  std::vector<const char *> symbols;
  OpenKIMcalculator *cobj = dynamic_cast<OpenKIMcalculator *>(self->orig_cobj);
  assert(cobj != NULL);
  cobj->GetSupportedSymbols(symbols);
  int num = symbols.size();
  PyObject *result = PyTuple_New(num);
  if (result == NULL)
    return NULL;
  for (int i = 0; i < num; i++)
    {
      PyTuple_SET_ITEM(result, i, PyUnicode_FromString(symbols[i]));
    }
  DEBUGPRINT;
  return result;
}

static PyObject *PyAsap_OpenKIMcalcGetTypeCode(PyAsap_PotentialObject
                                               *self, PyObject *args,
                                               PyObject *kwargs)
{
  DEBUGPRINT;
  static char *kwlist[] = {"symbol", NULL};
  const char *symbol = NULL;
  if (!PyArg_ParseTupleAndKeywords(args, kwargs,  "s:get_type_code",
      kwlist, &symbol))
    return NULL;
  OpenKIMcalculator *cobj = dynamic_cast<OpenKIMcalculator *>(self->orig_cobj);
  assert(cobj != NULL);
  try {
      int result = cobj->GetParticleTypeCode(symbol);
      return Py_BuildValue("i", result);
  }
  CATCHEXCEPTION;
  DEBUGPRINT;
}

static PyObject *PyAsap_OpenKIMcalcGetFreeParamNames(PyAsap_PotentialObject
                                                     *self, PyObject *noargs)
{
  DEBUGPRINT;
  OpenKIMcalculator *cobj = dynamic_cast<OpenKIMcalculator *>(self->orig_cobj);
  assert(cobj != NULL);
  KIM_API_model *model = cobj->GetKimModel();
  int err;
  int n, maxstringlen;
  err = model->get_num_free_params(&n, &maxstringlen);
  if (err < KIM_STATUS_OK)
    return KIMCHECKFAIL(model, err);

  PyObject *result = PyTuple_New(n);
  if (result == NULL)
    return NULL;
  for (int i = 0; i < n; i++)
    {
      const char *name;
      err = model->get_free_parameter(i, &name);
      if (err < KIM_STATUS_OK)
        {
          Py_DECREF(result);
          return KIMCHECKFAIL(model, err);
        }
      PyTuple_SET_ITEM(result, i, PyUnicode_FromString(name));
    }
  return result;
}

static PyObject *PyAsap_OpenKIMcalcGetFixedParamNames(PyAsap_PotentialObject
                                                      *self, PyObject *noargs)
{
  DEBUGPRINT;
  OpenKIMcalculator *cobj = dynamic_cast<OpenKIMcalculator *>(self->orig_cobj);
  assert(cobj != NULL);
  KIM_API_model *model = cobj->GetKimModel();
  int err;
  int n, maxstringlen;
  err = model->get_num_fixed_params(&n, &maxstringlen);
  if (err < KIM_STATUS_OK)
    return KIMCHECKFAIL(model, err);

  PyObject *result = PyTuple_New(n);
  if (result == NULL)
    return NULL;
  for (int i = 0; i < n; i++)
    {
      const char *name;
      err = model->get_fixed_parameter(i, &name);
      if (err < KIM_STATUS_OK)
        {
          Py_DECREF(result);
          return KIMCHECKFAIL(model, err);
        }
      PyTuple_SET_ITEM(result, i, PyUnicode_FromString(name));
    }
  return result;
}


static PyObject *PyAsap_OpenKIMcalcGetParameter(PyAsap_PotentialObject
                                                *self, PyObject *args,
                                                PyObject *kwargs)
 {
   DEBUGPRINT;
   static char *kwlist[] = {"name", "is_integer", "info_only", NULL};
   const char *name = NULL;
   int is_integer = 0;
   int info_only = 0;
   if (!PyArg_ParseTupleAndKeywords(args, kwargs,  "s|ii:_get_parameter",
				    kwlist, &name, &is_integer, &info_only))
     return NULL;
   OpenKIMcalculator *cobj = dynamic_cast<OpenKIMcalculator *>(self->orig_cobj);
   assert(cobj != NULL);
   int err;
   KIM_API_model *model = cobj->GetKimModel();
   intptr_t rank = model->get_rank(name, &err);
   if (err < KIM_STATUS_OK || rank < 0)
     return KIMCHECKFAIL(model, err);
   intptr_t size = 1;
   vector<int> shape(rank);
   if (rank > 0)
     {
       size =  model->get_size(name, &err);
       if (err < KIM_STATUS_OK || size < 0)
	 return KIMCHECKFAIL(model, err);
       model->get_shape(name, &shape[0], &err);
       if (err < KIM_STATUS_OK)
         return KIMCHECKFAIL(model, err);
     }
   if (info_only)
     {
       // Return the shape of the data
       PyObject *result = PyTuple_New(rank);
       for (int i = 0; i < rank; i++)
         PyTuple_SET_ITEM(result, i, Py_BuildValue("l", shape[i]));
       return result;
     }
   // Return the actual data
   assert(size > 0);
   void *data = model->get_data(name, &err);
   if (err < KIM_STATUS_OK)
     return KIMCHECKFAIL(model, err);
   if (rank == 0)
     {
       // Return a scalar
       assert(size == 1);
       if (is_integer)
	 return Py_BuildValue("i", ((int *) data)[0] );
       else
	 return Py_BuildValue("d", ((double *) data)[0] );
     }
   else
     {
       // Build a numpy array, and return it.
       vector<npy_intp> numpyshape(rank);
       for (int i = 0; i < rank; i++)
         numpyshape[i] = shape[i];  // May involve type casting.
       if (is_integer)
	 {
	   PyObject *result = PyArray_SimpleNew(rank, &numpyshape[0],
						NPY_INT);
	   if (result == NULL)
	     return NULL;
	   int *npydata = (int *) PyArray_DATA((PyArrayObject *) result);
	   int *d = (int *) data;
	   for (int i = 0; i < size; i++)
	     npydata[i] = d[i];
	   return result;
	 }
       else
	 {
	   PyObject *result = PyArray_SimpleNew(rank, &numpyshape[0],
						NPY_DOUBLE);
	   if (result == NULL)
	     return NULL;
	   double *npydata = (double *) PyArray_DATA((PyArrayObject *) result);
	   double *d = (double *) data;
	   for (int i = 0; i < size; i++)
	     npydata[i] = d[i];
	   return result;
	 }
     }

}

static PyObject *PyAsap_OpenKIMcalcSetParamScal(PyAsap_PotentialObject
                                               *self, PyObject *args,
                                               PyObject *kwargs)
 {
   DEBUGPRINT;
   static char *kwlist[] = {"name", "value", NULL};
   const char *name = NULL;
   double value = 0.0;
   if (!PyArg_ParseTupleAndKeywords(args, kwargs,  "sd:_set_parameter_scalar",
       kwlist, &name, &value))
     return NULL;
   OpenKIMcalculator *cobj = dynamic_cast<OpenKIMcalculator *>(self->orig_cobj);
   assert(cobj != NULL);
   int err;
   KIM_API_model *model = cobj->GetKimModel();
   intptr_t rank = model->get_rank(name, &err);
   if (err < KIM_STATUS_OK || rank < 0)
     return KIMCHECKFAIL(model, err);
   if (rank != 0)
     {
       PyErr_SetString(PyExc_TypeError, "Trying to set an array parameter with a scalar");
       return NULL;
     }
   double *data = (double *) model->get_data(name, &err);
   if (err < KIM_STATUS_OK)
     return KIMCHECKFAIL(model, err);
   *data = value;
   Py_RETURN_NONE;
}

static PyObject *PyAsap_OpenKIMcalcSetParamArray(PyAsap_PotentialObject
                                                 *self, PyObject *args,
                                                 PyObject *kwargs)
 {
   DEBUGPRINT;
   static char *kwlist[] = {"name", "value", NULL};
   const char *name = NULL;
   PyObject *value;
   if (!PyArg_ParseTupleAndKeywords(args, kwargs,  "sO!:_set_parameter_array",
       kwlist, &name, &PyArray_Type, &value))
     return NULL;

   OpenKIMcalculator *cobj = dynamic_cast<OpenKIMcalculator *>(self->orig_cobj);
   assert(cobj != NULL);
   int err;
   KIM_API_model *model = cobj->GetKimModel();
   intptr_t size = model->get_size(name, &err);
   if (err < KIM_STATUS_OK || size < 0)
     return KIMCHECKFAIL(model, err);
   // Check that the size match (we don't care about the rank)
   double *data = (double *) model->get_data(name, &err);
   if (err < KIM_STATUS_OK)
     return KIMCHECKFAIL(model, err);

   // Make sure input array is contiguous and has the right type.
   PyObject *converted = PyArray_ContiguousFromAny(value, NPY_DOUBLE, 0, 0);
   if (converted == NULL)
     return NULL;

   // Check that the size matches
   npy_intp valuesize = PyArray_SIZE((PyArrayObject *) converted);
   if (valuesize != size)
     {
       Py_DECREF(converted);
       PyErr_SetString(PyExc_ValueError, "_set_parameter_array: Array size mismatch.");
       return NULL;
     }
   double *newdata = (double *) PyArray_DATA((PyArrayObject *) converted);
   for (npy_intp i = 0; i < size; i++)
     data[i] = newdata[i];
   Py_RETURN_NONE;
}

static PyObject *PyAsap_OpenKIMcalcReinit(PyAsap_PotentialObject
                                          *self, PyObject *noargs)
{
  DEBUGPRINT;
  OpenKIMcalculator *cobj = dynamic_cast<OpenKIMcalculator *>(self->orig_cobj);
  assert(cobj != NULL);
  KIM_API_model *model = cobj->GetKimModel();
  int err = model->model_reinit();
  if (err < KIM_STATUS_OK)
    return KIMCHECKFAIL(model, err);
  Py_RETURN_NONE;
}

static PyMethodDef PyAsap_OpenKIMcalculatorMethods[] = {
  {"_initialize", (PyCFunction) PyAsap_OpenKIMcalcInitialize,
    METH_VARARGS | METH_KEYWORDS, "Initialize the OpenKIM model by name and descriptor."},
  {"get_NBC_method", (PyCFunction) PyAsap_OpenKIMcalcGetNBCmethod,
   METH_NOARGS, "Get name of the neighborlist method"},
  {"please_allocate", (PyCFunction) PyAsap_OpenKIMcalcPleaseAlloc,
   METH_VARARGS | METH_KEYWORDS, "Enable specific property"},
  {"set_translation", (PyCFunction) PyAsap_OpenKIMcalcSetTranslation,
   METH_VARARGS | METH_KEYWORDS, "Set Z->typecode translation table."},
  {"_use_imageatoms", (PyCFunction) PyAsap_PotentialUseImageAtoms,
   METH_NOARGS, PyAsap_PotentialUseImageAtoms_Docstring},
  {"get_supported_types", (PyCFunction) PyAsap_OpenKIMcalcGetSupportedTypes,
   METH_NOARGS, "Get the supported elements as a tuple of chemical symbols"},
  {"get_type_code", (PyCFunction) PyAsap_OpenKIMcalcGetTypeCode,
   METH_VARARGS | METH_KEYWORDS, "Get type code of an element"},
  {"get_free_parameter_names", (PyCFunction) PyAsap_OpenKIMcalcGetFreeParamNames,
   METH_NOARGS, "Get the names of any free parameters supported by the model."},
  {"get_fixed_parameter_names", (PyCFunction) PyAsap_OpenKIMcalcGetFixedParamNames,
   METH_NOARGS, "Get the names of any fixed parameters supported by the model."},
  {"_get_parameter", (PyCFunction) PyAsap_OpenKIMcalcGetParameter,
   METH_VARARGS | METH_KEYWORDS, "Get a parameter or its shape."},
  {"_set_parameter_scalar", (PyCFunction) PyAsap_OpenKIMcalcSetParamScal,
   METH_VARARGS | METH_KEYWORDS, "Set a scalar parameter."},
  {"_set_parameter_array", (PyCFunction) PyAsap_OpenKIMcalcSetParamArray,
   METH_VARARGS | METH_KEYWORDS, "Set an array parameter."},
  {"_reinit", (PyCFunction) PyAsap_OpenKIMcalcReinit,
   METH_NOARGS, "Reinitialize the OpenKIM model."},
  {NULL}
};



//////////////////////////////
//
//  Module initialization
//
//////////////////////////////


int PyAsap_InitOpenKIMInterface(PyObject *module)
{

  InitPotentialType(PyAsap_OpenKIMcalculatorType);
  PyAsap_OpenKIMcalculatorType.tp_init = (initproc) PyAsap_OpenKIMcalculatorInit;
  PyAsap_OpenKIMcalculatorType.tp_doc = OpenKIMcalculator_Docstring;
  PyAsap_OpenKIMcalculatorType.tp_methods = PyAsap_OpenKIMcalculatorMethods;
  if (PyType_Ready(&PyAsap_OpenKIMcalculatorType) < 0)
    return -1;
  Py_INCREF(&PyAsap_OpenKIMcalculatorType);
  PyModule_AddObject(module, "OpenKIMcalculator", (PyObject *) &PyAsap_OpenKIMcalculatorType);

  PyAsap_OpenKIMinfoType.tp_new = NULL;  // Use factory functions
  PyAsap_OpenKIMinfoType.tp_dealloc =
    PyAsap_Dealloc<PyAsap_OpenKIMinfoObject>;
  PyAsap_OpenKIMinfoType.tp_flags = Py_TPFLAGS_DEFAULT;
  PyAsap_OpenKIMinfoType.tp_methods = PyAsap_OpenKIMinfoMethods;
  PyAsap_OpenKIMinfoType.tp_repr =
    PyAsap_Representation<PyAsap_OpenKIMinfoObject>;
  PyAsap_OpenKIMinfoType.tp_doc = OpenKIMinfo_Docstring;
  if (PyType_Ready(&PyAsap_OpenKIMinfoType) < 0)
    return -1;

  return 0;
}

} // namespace

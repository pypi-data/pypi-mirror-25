
#include "AsapPython.h"
#include "ParallelNeighborListInterface.h"
#include "NeighborLocatorInterface.h"
#include "ExceptionInterface.h"
#include "PythonConversions.h"
#include "Templates.h"
#include "SecondaryNeighborLocator.h"
#include "ParallelAtoms.h"
//#define ASAPDEBUG
#include "Debug.h"

// Note: in parallel simulations, the Python interface overrides
// PyAsap_NewNeighborCellLocator_Py with this function
PyObject *PyAsap_NewNeighborCellLocator_Parallel(PyObject *noself, PyObject *args,
                                           PyObject *kwargs)
{
  static char *kwlist[] = {"rCut", "atoms", "driftfactor", NULL};

  PyObject *atoms = Py_None;
  double rCut = 0.0;
  double driftfactor = 0.05;
  if (!PyArg_ParseTupleAndKeywords(args, kwargs,  "dO|d:NeighborCellLocator",
                                   kwlist, &rCut, &atoms, &driftfactor))
    return NULL;
  DEBUGPRINT;
  if (rCut <= 0.0)
    {
      PyErr_SetString(PyExc_ValueError,
                      "NeighborCellLocator: Cutoff must be greater than zero.");
      return NULL;
    }

  // Detect if the atoms have ghost atoms.  In that case a parallel access object
  // is used.
  DEBUGPRINT;
  Atoms *access = NULL;
  if (atoms != Py_None && PyObject_HasAttrString(atoms, "ghosts"))
    {
      DEBUGPRINT;
      access = new ParallelAtoms(atoms);
      DEBUGPRINT;
    }
  try {
    DEBUGPRINT;
    PyAsap_NeighborLocatorObject *self =
      PyAsap_NewSecondaryNeighborLocator(access, rCut, driftfactor);
    DEBUGPRINT;
    if (access != NULL)
      AsapAtoms_DECREF(access);
    DEBUGPRINT;
    if (atoms != Py_None)
      self->cobj->CheckAndUpdateNeighborList(atoms);
    DEBUGPRINT;
    return (PyObject *) self;
  }
  CATCHEXCEPTION;
}


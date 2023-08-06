// Copyright (C) 2008-2011 Jakob Schiotz and Center for Individual
// Nanoparticle Functionality, Department of Physics, Technical
// University of Denmark.  Email: schiotz@fysik.dtu.dk
//
// This file is part of Asap version 3.
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
#include "GetNeighborList.h"
#include "Atoms.h"
#include "Potential.h"
#include "NeighborCellLocator.h"
#include "NeighborLocatorInterface.h"
//#define ASAPDEBUG
#include "Debug.h"

namespace ASAPSPACE {
// Return a neighborlist object and an Atoms access object (either new
// or reused from the potential).  Begin() will have been called on the atoms.

void GetNbList_FromAtoms(PyObject *pyatoms, double rCut,
			      PyObject **pynblist, Atoms **atoms)
{
  PyObject *py_pot = NULL;
  NeighborLocator *nblist = NULL;
  *pynblist = NULL;  // Not found yet.
  py_pot = PyObject_CallMethod(pyatoms, "get_calculator", "");
  if (py_pot == NULL)
    PyErr_Clear();
  else
    {
      // Got a potential.
      DEBUGPRINT;
      *pynblist = PyObject_CallMethod(py_pot, "get_neighborlist", "");
      if (*pynblist == NULL)
        PyErr_Clear();
      else
        {
          if (PyAsap_NeighborLocatorCheck(*pynblist))
            {
              // Got an ASAP neighborlocator object.
              DEBUGPRINT;
               nblist = ((PyAsap_NeighborLocatorObject *)*pynblist)->cobj;
               if (nblist->GetCutoffRadius() >= rCut)
                 {
                   // Use this neighbor list
                   DEBUGPRINT;
                   *atoms = nblist->GetAtoms();
                   AsapAtoms_INCREF(*atoms);
                   (*atoms)->Begin(pyatoms);
                   nblist->CheckAndUpdateNeighborList();
                 }
               else
                 {
                   // Discard neighbor list
                   DEBUGPRINT;
                   nblist = NULL;
                   Py_CLEAR(*pynblist);
                 }
            }
          else
            {
              // Got a Python object that is not a real neighbor list.
              Py_CLEAR(*pynblist);
              throw AsapError("Got a strange object from the calculator instead of an Asap NeighborLocator.");
            }
        }
    }
  Py_XDECREF(py_pot);
  if (nblist == NULL)
    {
      DEBUGPRINT;
      assert(*pynblist == NULL);
      // Create interface object and neighborlist object
      *pynblist = GetSecondaryNeighborList(pyatoms, rCut);
      if (*pynblist == NULL)
        throw AsapPythonError();
      nblist = ((PyAsap_NeighborLocatorObject *)*pynblist)->cobj;
      *atoms = nblist->GetAtoms();
      assert(*atoms != NULL);
      AsapAtoms_INCREF(*atoms);
      (*atoms)->Begin(pyatoms);
    }
  assert(*atoms != NULL);
  assert(*pynblist != NULL);
}

PyObject *GetSecondaryNeighborList(PyObject *pyatoms, double rCut)
{
  // Create the neighor list by calling PyAsap_NewFullNeighborList, taking
  // python objects as arguments, rather than the usual C++ creation function
  // (in this case PyAsap_NewSecondaryNeighborLocator) taking C++ arguments.
  // This is because the Python function is wrapped in the outher Module
  // layer, so it works correctly also in parallel simulations (includes
  // ghost atoms correctly).
  PyObject *args = Py_BuildValue("(dOd)", rCut, pyatoms, 0.0);
  assert(args != NULL);  // How could this fail?
  PyObject *kwargs = PyDict_New();
  assert(kwargs != NULL);
  PyObject *nblist = PyAsap_NewNeighborCellLocator_Py(NULL, args, kwargs);
  Py_DECREF(args);
  Py_DECREF(kwargs);
  return nblist;
}


} // end namespace

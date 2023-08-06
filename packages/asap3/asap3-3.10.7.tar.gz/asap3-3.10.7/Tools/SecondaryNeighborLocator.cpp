// -*- C++ -*-
// SecondaryNeighborLocator.h:  Cell-based algorithm for finding neighbors.
//
// Copyright (C) 2008-2015 Jakob Schiotz and Center for Individual
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
//
// The SECONDARY neighbor locator is not intended to be used by a potential.
// It can be used for analysis in situations where there may already be a
// parallel potential having a (primary) neighbor locator.  The secondary
// neighbor locator then uses the primary locator to keep the ghost atoms
// updated.  It is thus an error if the secondary neighbor locator has
// longer range than the primary.  If no primary locator is present, the
// secondary will handle ghost atoms itself, until a primary locator appears
// when/if the user later adds a potential.

#include "SecondaryNeighborLocator.h"
//#define ASAPDEBUG
#include "Debug.h"

bool SecondaryNeighborLocator::CheckAndUpdateNeighborList(PyObject *atoms_obj)
{
  // Check if there is a master neighbor list.  If so, use its access object.
  py_master = atoms->GetPrimaryNbLocator(atoms_obj);
  if (py_master != NULL)
    {
      NeighborLocator *master = ((PyAsap_NeighborLocatorObject *) py_master)->cobj;
      Atoms *newatoms = master->GetAtoms();
      assert(newatoms != NULL);
      if (newatoms != atoms)
        {
          // Replace access object with this one.
          AsapAtoms_INCREF(newatoms);
          AsapAtoms_DECREF(atoms);
          atoms = newatoms;
        }
    }
  bool updated = NeighborCellLocator::CheckAndUpdateNeighborList(atoms_obj);
  Py_XDECREF(py_master);
  py_master = NULL;
  return updated;
}

bool SecondaryNeighborLocator::CheckNeighborList()
{
  DEBUGPRINT;
  if (py_master)
    {
      DEBUGPRINT;
      NeighborLocator *master = ((PyAsap_NeighborLocatorObject *) py_master)->cobj;
      assert(master != NULL);
      if (master->GetCutoffRadius() < this->GetCutoffRadiusWithDrift())
        throw AsapError("Attempting to create a secondary neighbor list with larger cutoff than the master list: ")
          <<  this->GetCutoffRadiusWithDrift() << " versus " << master->GetCutoffRadius();
      DEBUGPRINT;
      bool masterupdate = master->CheckNeighborList();
      // May communicate
      DEBUGPRINT;
      masterupdate = atoms->UpdateBeforeCalculation(masterupdate,
                                                    master->GetCutoffRadiusWithDrift());
      DEBUGPRINT;
      if (masterupdate)
        master->UpdateNeighborList();
      DEBUGPRINT;
      return NeighborCellLocator::CheckNeighborList();
    }
  else
    {
      // No master.  We must handle ghost atoms and migration here.
      DEBUGPRINT;
      bool update = NeighborCellLocator::CheckNeighborList();
      update = atoms->UpdateBeforeCalculation(update, rCut);
      DEBUGPRINT;
      return update;
    }
}

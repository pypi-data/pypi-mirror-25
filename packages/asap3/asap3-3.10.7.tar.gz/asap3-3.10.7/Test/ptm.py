#!/usr/bin/env python
"""
Tests that polyhedral template matching works on the simplest possible system.

Name: ptm.py

Description: Part of the Asap test suite.  Tests the analysis.ptm module

Usage: python ptm.py

Expected result: The output should end with 'ALL TESTS SUCCEEDED'.
"""
from __future__ import print_function

from ase.lattice.cubic import FaceCenteredCubic
from asap3.testtools import ReportTest
from asap3.analysis import PTM
import numpy as np

atoms = FaceCenteredCubic("Cu", size=(7,7,7), pbc=False)
x = atoms.get_positions()
#atoms.set_positions(x + 0.01 * np.random.standard_normal(x.shape))

data = PTM(atoms, rmsd_max=0.1, calculate_strains=True)
print("DONE")
cnt = np.bincount(data['structure'])
print(cnt)
print(data['info'])

ReportTest("Number of FCC atoms", cnt[1], 6*6*6*4, 0)
ReportTest("Number of non-classified atoms", cnt[0], len(atoms) - 6*6*6*4, 0)

data = PTM(atoms, rmsd_max=0.1, calculate_strains=True, quick=True)
cnt = np.bincount(data['structure'])
print(cnt)
print(data['info'])

ReportTest("Number of FCC atoms", cnt[1], 6*6*6*4, 0)
ReportTest("Number of non-classified atoms", cnt[0], len(atoms) - 6*6*6*4, 0)

data = PTM(atoms, rmsd_max=0.1, target_structures=('fcc', 'hcp'))
cnt = np.bincount(data['structure'])
print(cnt)
print(data['info'])

ReportTest("Number of FCC atoms", cnt[1], 6*6*6*4, 0)
ReportTest("Number of non-classified atoms", cnt[0], len(atoms) - 6*6*6*4, 0)


ReportTest.Summary()

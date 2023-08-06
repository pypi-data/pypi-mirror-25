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

#define PARALLEL
#include "mpimodule.h"
#include "ParallelAtomsInterface.h"
#include "ParallelPotentialInterface.h"
#include "ParallelNeighborListInterface.h"

// Now include the main code
#include "AsapModule.cpp"


#if PY_MAJOR_VERSION >= 3
#define AsapInitModule0 AsapInitModule
#else
void AsapInitModule0(void) {
  AsapInitModule();
}
#endif


int main(int argc, char **argv)
{
  int status;
  DEBUGPRINT;
  
#ifdef _OPENMP
  int provided = 0;
  MPI_Init_thread(&argc, &argv, MPI_THREAD_FUNNELED, &provided);
#if 0
  if (provided < MPI_THREAD_FUNNELED)
    {
      std::cerr << "Combined MPI / OpenMP parallelization not supported by MPI." << std::endl;
      std::cerr << "provided: " << provided << " requested: " << MPI_THREAD_FUNNELED << std::endl;
      return -1;
    }
#endif
#else
  MPI_Init(&argc, &argv);
#endif
  
#ifdef ASAP_PY3
  wchar_t* wargv[argc];
  //wchar_t* wargv2[argc];
  for (int i = 0; i < argc; i++) {
    int n = 1 + mbstowcs(NULL, argv[i], 0);
    wargv[i] = (wchar_t*)malloc(n * sizeof(wchar_t));
    //wargv2[i] = wargv[i];
    mbstowcs(wargv[i], argv[i], n);
  }
#else
  char** wargv = argv;
#endif

  DEBUGPRINT;
  Py_SetProgramName(wargv[0]);
  PyImport_AppendInittab("_asap", &AsapInitModule0);
  Py_Initialize();
  DEBUGPRINT;

  // Here, one could use PyImport_AppendInittab to handle loading the right module
  // instead of using logic in Python to choose the serial versus parallel module.
  status = Py_Main(argc, wargv);
  DEBUGPRINT;
  Py_Finalize();
  DEBUGPRINT;
  MPI_Finalize();
  return status;
}

  

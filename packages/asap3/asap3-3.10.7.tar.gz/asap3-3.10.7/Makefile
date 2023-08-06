#### This Makefile requires GNU make.  It is unlikely to work with other versions.
#### See installation instructions in the README file or at wiki.fysik.dtu.dk/asap
####
#### Important: All configuration should be done in the configuration files
#### named makefile-XXXX
####
#### This Makefile looks for configuration files in the following order
####   1.  makefile-local
####   2.  makefile-HOSTNAME
#### [ 3.  makefile-nifheim6   (ONLY if compiling on the Niflheim cluster) ]
####   4.  makefile-KERNELNAME-ARCH-COMPILER
####   5.  makefike-KERNELNAME-ARCH
####   6.  makefile-default
####
#### where HOSTNAME is the host name, KERNELNAME is e.g. Linux or Darwin,
#### ARCH is the architectur (e.g. x86_64), and COMPILER is "gnu" or "intel"
#### and reflects if the icc compiler is installed.
####
#### You can see the output of these variables by typing
####   make info
####
#### TO CUSTOMIZE THIS:
####
#### If you need to change an existing configuration, copy it to makefile-local
#### (or makefile-hostname) and edit it.
####
#### If you have an unsupported architecture, create a new makefike-KERNELNAME-ARCH
#### file, and edit it.  Please send it to me at schiotz@fysik.dtu.dk



# The version number is now defined in a single place
VERSION := $(shell python Python/asap3/version.py)

# ARCH is the machine architecture, used to select compiler flags etc
# On some weird machines (Macs!) uname -m returns a name with a space in it.
# It will be replaces with an underscore
ARCH := $(shell uname -m | sed -e 's/ /_/g')
HOSTNAME := $(shell uname -n | sed -e 's/ /_/g')
KERNELNAME := $(shell uname -s | sed -e 's/ /_/g')

# The Intel compiler (icc) can be used on Pentium 4 machines to gain at least
# a factor of two in performance.  A similar gain is obtained by using the
# PathScale compiler on and AMD processor.  The COMPILER variable indicates
# which compiler should be used.  It can take the values "pathscale",
# "intel" and "gnu" on i686 and x86_64 architectures, and at least the value
# "gnu" on other architectures.  If unset, it tries to auto-detect.
ifndef COMPILER
# Test for icc command if ARCH is i686 or x86_64
ifneq (,$(filter i686 x86_64,$(ARCH)))
HAS_ICC := $(shell which icc 2> /dev/null)
ifdef HAS_ICC
COMPILER = intel
else
COMPILER = gnu
endif
endif
endif

# Now include the right file for the specific architecture.
ifneq ("$(wildcard makefile-local)","")
MAKECONFIGURATION = makefile-local
else ifneq ("$(wildcard makefile-$(HOSTNAME))","")
MAKECONFIGURATION = makefile-$(HOSTNAME)
else ifneq ("$(wildcard makefile-$(FYS_PLATFORM))","")
MAKECONFIGURATION = makefile-$(FYS_PLATFORM)
else ifneq ("$(wildcard makefile-$(KERNELNAME)-$(ARCH)-$(COMPILER))","")
MAKECONFIGURATION = makefile-$(KERNELNAME)-$(ARCH)-$(COMPILER)
else ifneq ("$(wildcard makefile-$(KERNELNAME)-$(ARCH))","")
MAKECONFIGURATION = makefile-$(KERNELNAME)-$(ARCH)
else
MAKECONFIGURATION = makefile-default
endif

ifeq ($(MAKECONFIGURATION), makefile-default)
$(warning WARNING: No suitable configuration found.)
endif
$(info Getting configuration from $(MAKECONFIGURATION))
include $(MAKECONFIGURATION)

ifeq ($(shell $(CXX) -dumpversion), 15.0.1)
$(error ERROR: Cannot compile with Intel compiler version 15.0.1 due to optimization error)
endif


# The python executable.  May be overridden IN THE CONFIGURATION FILE for broken installations such
# as the former DTU databar systems, or to select Python 3.
ifndef PYTHON
PYTHON=python
endif

# PYVER is the Python version
PYVER := $(shell $(PYTHON) getconfig.py VERSION)

# MYMAJOR is the major Python version number (i.e. 2 or 3)
PYMAJOR := $(shell $(PYTHON) -c 'import sys; print(sys.version_info[0])')

# LINKFORSHARED, PYTHONLIBS snd PYTHONCLIBDIR are variables used for
# creating a custom Python interpreter for parallel Asap simulations.
ifndef LINKFORSHARED
LINKFORSHARED := $(shell $(PYTHON) getconfig.py LINKFORSHARED)
endif
ifndef PYTHONLIBS
PYTHONLIBS := $(shell $(PYTHON) getconfig.py LIBS) \
              $(shell $(PYTHON) getconfig.py LIBM)
endif
ifndef PYTHONCLIBDIR
PYTHONCLIBDIR := $(shell $(PYTHON) getconfig.py LIBPL)
endif
ifndef PYTHONBLDLIBRARY
PYTHONBLDLIBRARY := $(shell $(PYTHON) getconfig.py BLDLIBRARY)
endif
ifndef LDFLAGS
LDFLAGS =  $(shell $(PYTHON) getconfig.py LDFLAGS)
endif

# INSTALLATION.  
# "make install" will install .py files in the directory PYINSTALL,
# and compiled files in BININSTALL.
# DESTDIR is normally empty, used for relocation.
# THIS MAY BE CHANGED IN THE CONFIGURATION FILES (i.e. on 64 bit linux)
ifndef PYSITEPACKAGES
PYSITEPACKAGES := $(shell $(PYTHON) getconfig.py SITEPACKAGES)
endif
ifndef PYINSTALL
PYINSTALL := $(DESTDIR)/$(PYSITEPACKAGES)/asap3
endif
ifndef BININSTALL
BININSTALL:= $(DESTDIR)/$(PYSITEPACKAGES)
endif
ifndef EXECINSTALL
EXECINSTALL:= $(DESTDIR)/usr/local/bin
endif

# POSTFIX is used to select different object directories when compiling for 
# debugging, profiling etc.
#POSTFIX =

# Now get some include directories
ifndef PYTHON_INCLUDE
PYTHON_INCLUDE := $(shell $(PYTHON) -c 'import distutils.sysconfig as ds; print("-I"+ds.get_python_inc())')
endif
ifndef NUMPY_INCLUDE
NUMPY_INCLUDE:= $(shell $(PYTHON) -c 'import numpy; print("-I"+numpy.get_include())')
endif

# If ASAP_KIM_DIR is set, set ASAP_KIM_INC and ASAP_KIM_LIB
# This is intended for an in-place installation of OpenKIM
ifdef ASAP_KIM_DIR
ifndef ASAP_KIM_INC
ASAP_KIM_INC = $(ASAP_KIM_DIR)/src
endif
ifndef ASAP_KIM_LIB
ASAP_KIM_LIB = $(ASAP_KIM_DIR)/src
endif
endif

# If KIM_HOME is set, set ASAP_KIM_INC and ASAP_KIM_LIB
# This is intended for a system-wide installation of OpenKIM
ifdef KIM_HOME
ifndef ASAP_KIM_INC
ASAP_KIM_INC = $(KIM_HOME)/include/kim-api-v1
endif
ifndef ASAP_KIM_LIB
ASAP_KIM_LIB = $(KIM_HOME)/lib
endif
endif

# The object directories where object files are placed.
ifndef OBJDIR
OBJDIR = $(ARCH)-p$(PYMAJOR)$(POSTFIX)
endif
ifndef BINDIR
BINDIR = $(ARCH)
endif


# Source files

CXXSRC_BASICS = AsapObject.cpp NormalAtoms.cpp Vec.cpp Exception.cpp EMT.cpp \
	EMTDefaultParameterProvider.cpp EMTRasmussenParameterProvider.cpp \
	NeighborCellLocator.cpp NeighborList.cpp Matrix3x3.cpp \
	LennardJones.cpp EMTPythonParameterProvider.cpp MonteCarloEMT.cpp \
	MonteCarloAtoms.cpp Debug.cpp Morse.cpp \
	DynamicAtoms.cpp MolecularDynamics.cpp VelocityVerlet.cpp Timing.cpp \
	EMT2013.cpp NeighborList2013.cpp RGL.cpp Potential.cpp \
	Langevin.cpp RahmanStillingerLemberg.cpp  RandomNumbers.cpp \
	ImageAtoms.cpp ImagePotential.cpp MetalOxideInterface.cpp \
	MetalOxideInterface2.cpp

# Do not include autogenerated Basics/version.cpp on the list above, as that
# would cause superfluous compilations.

CXXSRC_INTERFACE = PotentialInterface.cpp \
	ExceptionInterface.cpp PythonConversions.cpp \
	EMTParameterProviderInterface.cpp NeighborLocatorInterface.cpp \
	RDFInterface.cpp ToolsInterface.cpp DynamicsInterface.cpp \
	OpenMPInterface.cpp PTMInterface.cpp

CXXSRC_TOOLS = RawRadialDistribution.cpp CoordinationNumbers.cpp CNA.cpp \
	GetNeighborList.cpp FullCNA.cpp SecondaryNeighborLocator.cpp

CXXSRC_PTM = canonical.cpp graph_data.cpp convex_hull_incremental.cpp \
	index_ptm.cpp alloy_types.cpp deformation_gradient.cpp \
	normalize_vertices.cpp polar_decomposition.cpp 	neighbour_ordering.cpp

CXXSRC_PTM_QC = qcprot/qcprot.cpp qcprot/quat.cpp

CXXSRC_PTM_V = voronoi/cell.cpp

CSRC_EXTRA =

CSRC_PARINTERFACE = mpi.c

CXXSRC_PARALLEL = RegularGridDecomposition.cpp ParallelAtoms.cpp \
	ParallelPotential.cpp

SERIAL_INTERFACE = AsapSerial.cpp

CXXSRC_PARINTERFACE = AsapParallel.cpp ParallelAtomsInterface.cpp \
	ParallelPotentialInterface.cpp ParallelNeighborListInterface.cpp

CXXSRC_BRENNER = BrennerPotential.cpp caguts.cpp expand.cpp inter2d_iv.cpp \
	mtable.cpp pibond.cpp radic.cpp radicdata.cpp sili_germ.cpp \
	spgch.cpp bcuint.cpp

CXXSRC_OPENKIM = OpenKIMinfo.cpp OpenKIMinterface.cpp OpenKIMcalculator.cpp \
    DummyNeighborLocator.cpp

TEMP_DOC_DIR = /tmp/Asap-documentation-$(USER)

# Default values
ifndef MPICC 
MPICC=env LAMMPICC='$(CC)' OMPI_MPICC='$(CC)' mpicc
endif
ifndef MPICXX
MPICXX=env LAMMPICXX='$(CXX)' OMPI_MPICXX='$(CXX)' mpicxx
endif
ifndef MPICFLAGS
MPICFLAGS = $(CFLAGS)
endif
ifndef MPICXXFLAGS
MPICXXFLAGS= $(CXXFLAGS)
endif
ifndef DEPENDCC
DEPENDCC = $(CC)
endif
ifndef DEPENDCXX
DEPENDCXX= $(CXX)
endif
ifndef DEPENDMPICC
DEPENDMPICC = $(MPICC)
endif
ifndef DEPENDMPICXX
DEPENDMPICXX = $(MPICXX)
endif
ifndef DEPENDFLAG
DEPENDFLAG = -MM
endif
ifndef DEPENDCLEAN
DEPENDCLEAN = sed -e 's@/usr/[^ ]*@@g' | sed -e '/^ *\\ *$$/d'
endif
ifndef LIBS
LIBS = -lm 
endif
ifndef CXXSHARED
CXXSHARED = $(CXX) -shared
endif

PAROBJDIR = $(OBJDIR)$(PARPOSTFIX)

COMMONOBJS := $(CXXSRC_BASICS:%.cpp=Basics/$(OBJDIR)/%.o) \
	$(CXXSRC_TOOLS:%.cpp=Tools/$(OBJDIR)/%.o) \
	$(CXXSRC_INTERFACE:%.cpp=Interface/$(OBJDIR)/%.o) \
	$(CXXSRC_BRENNER:%.cpp=Brenner/$(OBJDIR)/%.o) \
	$(CXXSRC_PTM:%.cpp=PTM/$(OBJDIR)/%.o) \
	$(CXXSRC_PTM_QC:qcprot/%.cpp=PTM/$(OBJDIR)/%.o) \
	$(CXXSRC_PTM_V:voronoi/%.cpp=PTM/$(OBJDIR)/%.o) \
	$(CSRC_EXTRA:%.c=Basics/$(OBJDIR)/%.o) 

ifdef ASAP_KIM_INC
COMMONOBJS += $(CXXSRC_OPENKIM:%.cpp=OpenKIMimport/$(OBJDIR)/%.o) 
endif

SERIALOBJS := $(COMMONOBJS) \
	$(SERIAL_INTERFACE:%.cpp=Interface/$(OBJDIR)/%.o)

PARALLELOBJS := $(CXXSRC_BASICS:%.cpp=Basics/$(PAROBJDIR)/%.o) \
	$(CXXSRC_TOOLS:%.cpp=Tools/$(PAROBJDIR)/%.o) \
	$(CXXSRC_INTERFACE:%.cpp=Interface/$(PAROBJDIR)/%.o) \
	$(CXXSRC_BRENNER:%.cpp=Brenner/$(PAROBJDIR)/%.o) \
	$(CXXSRC_PTM:%.cpp=PTM/$(PAROBJDIR)/%.o) \
	$(CXXSRC_PTM_QC:qcprot/%.cpp=PTM/$(PAROBJDIR)/%.o) \
	$(CXXSRC_PTM_V:voronoi/%.cpp=PTM/$(PAROBJDIR)/%.o) \
	$(CSRC_EXTRA:%.c=Basics/$(PAROBJDIR)/%.o) \
	$(CXXSRC_PARALLEL:%.cpp=Parallel/$(PAROBJDIR)/%.o) \
	$(CXXSRC_PARINTERFACE:%.cpp=ParallelInterface/$(PAROBJDIR)/%.o) \
	$(CSRC_PARINTERFACE:%.c=ParallelInterface/$(PAROBJDIR)/%.o) 

ifdef ASAP_KIM_INC
PARALLELOBJS += $(CXXSRC_OPENKIM:%.cpp=OpenKIMimport/$(PAROBJDIR)/%.o) 
endif

INCLUDES = -IBasics -ITools -IParallel -IInterface -IParallelInterface \
	 -IBrenner 
ifdef ASAP_KIM_INC
INCLUDES += -IOpenKIMimport -I$(ASAP_KIM_INC)
endif
INCLUDES += $(PYTHON_INCLUDE) $(NUMPY_INCLUDE)

ifdef ASAP_KIM_LIB
LIBS += -L$(ASAP_KIM_LIB) -lkim-api-v1 
EXTRA_LIBS += -L$(ASAP_KIM_LIB) -lkim-api-v1 
CXXFLAGS += -DWITH_OPENKIM
MPICXXFLAGS += -DWITH_OPENKIM
DEPENDFLAGS += -DWITH_OPENKIM
endif

# Name of binaries
BINSERIAL = _asap_p$(PYMAJOR).so
BINPARALLEL = asap-$(PYTHON)

.DEFAULT: help

help:
	@echo
	@echo "ASAP version $(VERSION) compilation:"
	@echo
	@echo "To compile the serial version:"
	@echo "    make depend"
	@echo "    make serial"
	@echo
	@echo "To compile both the serial and the parallel version:"
	@echo "    make depend"
	@echo "    make parallel         (or make all)"
	@echo
	@echo "To install the serial version:"
	@echo "    make install"
	@echo
	@echo "To install both the serial and the parallel version:"
	@echo "    make install-parallel"
	@echo
	@echo "To make a tar file for distribution:"
	@echo "    make tar"
	@echo
	@echo "To extract documentation from C++ source files, so it can be"
	@echo "built into the Python modules as docstrings."
	@echo "    make docs"
	@echo "(the information will persist until updated with 'make docs' or"
	@echo "deleted with 'make clean'.)"
	@echo
	@echo "To check the ASAP version number:"
	@echo "    make version"
	@echo
	@echo "To check configuration variables:"
	@echo "    make info"
	@echo

all: serial parallel

serial: $(BINDIR) Depend/$(OBJDIR)/depend.timestamp Basics/$(OBJDIR) Tools/$(OBJDIR) PTM/$(OBJDIR) Interface/$(OBJDIR) Brenner/$(OBJDIR) OpenKIMimport/$(OBJDIR) $(BINDIR)/$(BINSERIAL)

parallel: $(BINDIR) Depend/$(OBJDIR)/depend.timestamp Basics/$(PAROBJDIR) Tools/$(PAROBJDIR) PTM/$(PAROBJDIR) Interface/$(PAROBJDIR) Brenner/$(PAROBJDIR) OpenKIMimport/$(PAROBJDIR) Parallel/$(PAROBJDIR) ParallelInterface/$(PAROBJDIR)  $(BINDIR)/$(BINPARALLEL) 

$(BINDIR)/$(BINSERIAL): $(SERIALOBJS) Python/asap3/version.py scripts/asap-qsub scripts/asap-sbatch
	test -h $(BINDIR)/asap-qsub || (cd $(BINDIR) && ln -sf ../scripts/asap-qsub)
	test -h $(BINDIR)/asap-sbatch || (cd $(BINDIR) && ln -sf ../scripts/asap-sbatch)
	python recordversion.py "$(VERSION)" "serial" "$(CXX)" "$(CXXFLAGS)" > Basics/$(OBJDIR)/version.cpp
	$(CXX) -c $(CXXFLAGS) $(INCLUDES) Basics/$(OBJDIR)/version.cpp -o Basics/$(OBJDIR)/version.o 
	rm -f $@
	$(CXXSHARED) -g $(SERIALOBJS) Basics/$(OBJDIR)/version.o -o $@ $(LIBS)

$(BINDIR)/$(BINPARALLEL): $(PARALLELOBJS) Python/asap3/version.py scripts/asap-qsub asapmpiinfo-input.py
	cp asapmpiinfo-input.py $(BINDIR)/asapmpiinfo3.py
	echo "mpicc = '`which mpicc`'" >> $(BINDIR)/asapmpiinfo3.py
	test -h $(BINDIR)/asap-qsub || (cd $(BINDIR) && ln -sf ../scripts/asap-qsub)
	python recordversion.py "$(VERSION)" "parallel" "$(MPICXX)" "$(MPICXXFLAGS)" > Basics/$(PAROBJDIR)/version_p.cpp
	$(MPICXX) -c $(MPICXXFLAGS) $(INCLUDES) Basics/$(PAROBJDIR)/version_p.cpp -o Basics/$(PAROBJDIR)/version_p.o 
	rm -f $@
	$(MPICXX) $(LINKFORSHARED) $(ASAPLINKFORSHARED) $(LDFLAGS) -o $@ -g \
		$(PARALLELOBJS) Basics/$(PAROBJDIR)/version_p.o \
		-L$(PYTHONCLIBDIR) $(PYTHONBLDLIBRARY) $(PYTHONLIBS) $(EXTRA_LIBS)

# $(OBJDIR)/asap-python-serial: $(SERIALOBJS) Python/asap3/version.py
# 	python recordversion.py '$(VERSION)' 'static' '$(CXX)' '$(CXXFLAGS)' > Basics/$(OBJDIR)/version_st.cpp
# 	$(CXX) -c $(CXXFLAGS) $(INCLUDES) Basics/$(OBJDIR)/version_st.cpp -o Basics/$(OBJDIR)/version_st.o 
# 	rm -f $@
# 	$(CXX) $(LINKFORSHARED) $(ASAPLINKFORSHARED) -o $@ -g \
# 		$(SERIALOBJS) Basics/$(OBJDIR)/version_st.o \
# 		-L$(PYTHONCLIBDIR) -lpython$(PYVER) $(PYTHONLIBS) $(EXTRA_LIBS)

clean:
	rm -rf Basics/$(OBJDIR) Tools/$(OBJDIR) \
		Interface/$(OBJDIR) Parallel/$(PAROBJDIR) \
		ParallelInterface/$(PAROBJDIR) Brenner/$(OBJDIR) \
		OpenKIMimport/$(OBJDIR) PTM/$(OBJDIR) $(OBJDIR)
	rm -rf Basics/$(PAROBJDIR) Tools/$(PAROBJDIR) \
		Interface/$(PAROBJDIR) Brenner/$(PAROBJDIR) \
		OpenKIMimport/$(PAROBJDIR) PTM/$(PAROBJDIR)

cleanall:
	@echo "**** Removing .o files"
	find . -name '*.o' -print -delete
	@echo "**** Removing .a files"
	find . -name '*.a' -print -delete
	@echo "**** Removing .optrpt files (Intel optimization reports)"
	find . -name '*.optrpt' -print -delete
	@echo "**** Removing -pyc and .pyo files"
	find . -name '*.pyc' -print -delete
	find . -name '*.pyo' -print -delete
	@echo "**** Removing executables"
	find . -name 'asapserial3.so' -print -delete
	find . -name '_asap*.so' -print -delete
	find . -name 'asap-python*' -print -delete
	find . -name 'ptmmodule.so' -print -delete
	@echo "**** Removing special build targets."
	find . -name 'asapmpiinfo3.py' -print -delete
	find . -name 'asap-qsub' -type l -print -delete
	@echo "**** Removing empty directories"
	find . -name '.git' -prune -o \( -type d -empty -print -exec rmdir {} + \)
	@echo "**** Removing all dependencies"
	-rm -rf Depend
	@echo "**** Removing setup.py build folder"
	-rm -rf build


Depend/$(OBJDIR)/depend.timestamp: depend.CHANGES
	@echo ''
	@echo 'ERROR: The dependencies have changed. These are the last changes:'
	@echo ''
	@echo 'Date      Version    Description'
	@tail -n 3 depend.CHANGES
	@echo ''
	@echo ''
	@echo 'INSTRUCTIONS:'
	@echo ''
	@echo 'Please run'
	@echo '    make depend'
	@echo 'and then try compiling again.'
	@echo ''
	@echo ''
	exit 1


depend: Depend/$(OBJDIR) depend-serial depend-parallel
	touch Depend/$(OBJDIR)/depend.timestamp

depend-maybe:
	$(MAKE) -q "Depend/$(OBJDIR)/depend.timestamp" || $(MAKE) depend

depend-serial:
	@echo "Creating dependencies for serial version (hidden for clarity)"
	@($(DEPENDCXX) $(DEPENDFLAG) $(CXXSRC_BASICS:%=Basics/%) $(INCLUDES) \
		| sed -e 's@^\(.*\.o:\)@Basics/$(OBJDIR)/\1@'; \
	 $(DEPENDCXX) $(DEPENDFLAG) $(CXXSRC_TOOLS:%=Tools/%) $(INCLUDES) \
		| sed -e 's@^\(.*\.o:\)@Tools/$(OBJDIR)/\1@'; \
	 $(DEPENDCXX) $(DEPENDFLAG) $(CXXSRC_INTERFACE:%=Interface/%) $(INCLUDES) \
		| sed -e 's@^\(.*\.o:\)@Interface/$(OBJDIR)/\1@'; \
	 $(DEPENDCXX) $(DEPENDFLAG) $(CXXSRC_BRENNER:%=Brenner/%) $(INCLUDES) \
		| sed -e 's@^\(.*\.o:\)@Brenner/$(OBJDIR)/\1@'; \
	 $(DEPENDCXX) $(DEPENDFLAG) $(SERIAL_INTERFACE:%=Interface/%) $(INCLUDES) \
		| sed -e 's@^\(.*\.o:\)@Interface/$(OBJDIR)/\1@') \
	 | $(DEPENDCLEAN) > Depend/$(OBJDIR)/make.depend
ifdef ASAP_KIM_INC
	@$(DEPENDCXX) $(DEPENDFLAG) $(CXXSRC_OPENKIM:%=OpenKIMimport/%) $(INCLUDES) \
		| sed -e 's@^\(.*\.o:\)@OpenKIMimport/$(OBJDIR)/\1@' \
		| $(DEPENDCLEAN) >> Depend/$(OBJDIR)/make.depend
endif

depend-parallel: 
	@echo ""
	@echo ""
	@echo "PLEASE NOTE: If mpi is not installed, errors will be generated"
	@echo "when running the following commands.  They can be ignored."
	@echo ""
	@echo ""
	@sleep 2
	@echo "Creating dependencies for parallel version (hidden for clarity)"
	@($(DEPENDMPICXX) $(DEPENDFLAG) $(CXXSRC_PARALLEL:%=Parallel/%) $(INCLUDES) $(MPIINCLUDES)\
		| sed -e 's@^\(.*\.o:\)@Parallel/$(PAROBJDIR)/\1@'; \
	 $(DEPENDMPICXX) $(DEPENDFLAG) $(INCLUDES) $(MPIINCLUDES) \
		$(CXXSRC_PARINTERFACE:%=ParallelInterface/%) \
		| sed -e 's@^\(.*\.o:\)@ParallelInterface/$(PAROBJDIR)/\1@'; \
	 $(DEPENDMPICC) $(DEPENDFLAG) $(INCLUDES) $(MPIINCLUDES) \
		$(CSRC_PARINTERFACE:%=ParallelInterface/%) \
		| sed -e 's@^\(.*\.o:\)@ParallelInterface/$(PAROBJDIR)/\1@') \
	 | $(DEPENDCLEAN) > Depend/$(OBJDIR)/make.parallel.depend
ifneq ($(PAROBJDIR),$(OBJDIR))
	@echo "Creating dependencies for parallel version (part 2)."
	@($(DEPENDCXX) $(DEPENDFLAG) $(CXXSRC_BASICS:%=Basics/%) $(INCLUDES) \
		| sed -e 's@^\(.*\.o:\)@Basics/$(PAROBJDIR)/\1@'; \
	 $(DEPENDCXX) $(DEPENDFLAG) $(CXXSRC_TOOLS:%=Tools/%) $(INCLUDES) \
		| sed -e 's@^\(.*\.o:\)@Tools/$(PAROBJDIR)/\1@'; \
	 $(DEPENDCXX) $(DEPENDFLAG) $(CXXSRC_INTERFACE:%=Interface/%) $(INCLUDES) \
		| sed -e 's@^\(.*\.o:\)@Interface/$(PAROBJDIR)/\1@'; \
	 $(DEPENDCXX) $(DEPENDFLAG) $(CXXSRC_BRENNER:%=Brenner/%) $(INCLUDES) \
		| sed -e 's@^\(.*\.o:\)@Brenner/$(PAROBJDIR)/\1@'; \
	 $(DEPENDCXX) $(DEPENDFLAG) $(SERIAL_INTERFACE:%=Interface/%) $(INCLUDES) \
		| sed -e 's@^\(.*\.o:\)@Interface/$(PAROBJDIR)/\1@') \
	 | $(DEPENDCLEAN) >> Depend/$(OBJDIR)/make.parallel.depend
ifdef ASAP_KIM_INC
	@$(DEPENDCXX) $(DEPENDFLAG) $(CXXSRC_OPENKIM:%=OpenKIMimport/%) $(INCLUDES) \
		| sed -e 's@^\(.*\.o:\)@OpenKIMimport/$(PAROBJDIR)/\1@' \
		| $(DEPENDCLEAN) >> Depend/$(OBJDIR)/make.parallel.depend
endif
endif

$(BINDIR): 
	test -d $(BINDIR) || mkdir $(BINDIR)

Depend:
	test -d Depend || mkdir Depend

Depend/$(OBJDIR): Depend
	test -d Depend/$(OBJDIR) || mkdir Depend/$(OBJDIR)

-include Depend/$(OBJDIR)/make.depend
-include Depend/$(OBJDIR)/make.parallel.depend

Basics/$(OBJDIR)/%.o: Basics/%.cpp
	$(CXX) -c $(CXXFLAGS) $(INCLUDES) -o $@ $<

Basics/$(OBJDIR)/%.o: Basics/%.c
	$(CC) -c $(CFLAGS) $(INCLUDES) -o $@ $<

Tools/$(OBJDIR)/%.o: Tools/%.cpp
	$(CXX) -c $(CXXFLAGS) $(INCLUDES) -o $@ $<

Brenner/$(OBJDIR)/%.o: Brenner/%.cpp 
	$(CXX) -c $(CXXFLAGS) $(INCLUDES) -o $@ $<

PTM/$(OBJDIR)/%.o: PTM/%.cpp 
	$(CXX) -c $(CXXFLAGS) $(INCLUDES) -o $@ $<

PTM/$(OBJDIR)/%.o: PTM/qcprot/%.cpp 
	$(CXX) -c $(CXXFLAGS) $(INCLUDES) -o $@ $<

PTM/$(OBJDIR)/%.o: PTM/voronoi/%.cpp 
	$(CXX) -c $(CXXFLAGS) $(INCLUDES) -o $@ $<

Interface/$(OBJDIR)/%.o: Interface/%.cpp
	$(CXX) -c $(CXXFLAGS) $(IFACEFLAGS) $(INCLUDES) -o $@ $<

ifdef ASAP_KIM_INC
OpenKIMimport/$(OBJDIR)/%.o: OpenKIMimport/%.cpp
	$(CXX) -c $(CXXFLAGS) $(IFACEFLAGS) $(INCLUDES) -o $@ $<
endif

ifneq ($(PAROBJDIR),$(OBJDIR))
# If we need to compile the common object in a different way for
# the parallel version, this is handled here.
Basics/$(PAROBJDIR)/%.o: Basics/%.cpp
	$(MPICXX) -c $(MPICXXFLAGS) $(INCLUDES) -o $@ $<

Basics/$(PAROBJDIR)/%.o: Basics/%.c
	$(MPICC) -c $(MPICFLAGS) $(INCLUDES) -o $@ $<

Tools/$(PAROBJDIR)/%.o: Tools/%.cpp
	$(MPICXX) -c $(MPICXXFLAGS) $(INCLUDES) -o $@ $<

Brenner/$(PAROBJDIR)/%.o: Brenner/%.cpp 
	$(MPICXX) -c $(MPICXXFLAGS) $(BRENNERCFLAGS) $(INCLUDES) -o $@ $<

PTM/$(PAROBJDIR)/%.o: PTM/%.cpp 
	$(MPICXX) -c $(MPICXXFLAGS) $(INCLUDES) -o $@ $<

PTM/$(PAROBJDIR)/%.o: PTM/qcprot/%.cpp 
	$(MPICXX) -c $(MPICXXFLAGS) $(INCLUDES) -o $@ $<

PTM/$(PAROBJDIR)/%.o: PTM/voronoi/%.cpp 
	$(MPICXX) -c $(MPICXXFLAGS) $(INCLUDES) -o $@ $<

Interface/$(PAROBJDIR)/%.o: Interface/%.cpp
	$(MPICXX) -c $(MPICXXFLAGS) $(IFACEFLAGS) $(INCLUDES) -o $@ $<

ifdef ASAP_KIM_INC
OpenKIMimport/$(PAROBJDIR)/%.o: OpenKIMimport/%.cpp
	$(CXX) -c $(CXXFLAGS) $(IFACEFLAGS) $(INCLUDES) -o $@ $<
endif
endif

Parallel/$(PAROBJDIR)/%.o: Parallel/%.cpp 
	$(MPICXX) -c $(MPICXXFLAGS) $(INCLUDES) $(MPIINCLUDES) -o $@ $<

Parallel/$(PAROBJDIR)/%.o: Parallel/%.c 
	$(MPICC) -c $(MPICFLAGS) $(INCLUDES) $(MPIINCLUDES) -o $@ $<

ParallelInterface/$(PAROBJDIR)/%.o: ParallelInterface/%.cpp 
	$(MPICXX) -c $(MPICXXFLAGS) $(IFACEFLAGS) $(INCLUDES) $(MPIINCLUDES) -o $@ $<

ParallelInterface/$(PAROBJDIR)/%.o: ParallelInterface/%.c 
	$(MPICC) -c $(MPICFLAGS) $(IFACEFLAGS) $(INCLUDES) $(MPIINCLUDES) -o $@ $<

Basics/$(OBJDIR):
	mkdir Basics/$(OBJDIR)

Tools/$(OBJDIR):
	mkdir Tools/$(OBJDIR)

PTM/$(OBJDIR):
	mkdir PTM/$(OBJDIR)

Interface/$(OBJDIR):
	mkdir Interface/$(OBJDIR)

Brenner/$(OBJDIR):
	mkdir Brenner/$(OBJDIR)

OpenKIMimport/$(OBJDIR):
	mkdir OpenKIMimport/$(OBJDIR)

ifneq ($(PAROBJDIR),$(OBJDIR))
Basics/$(PAROBJDIR):
	mkdir Basics/$(PAROBJDIR)

Tools/$(PAROBJDIR):
	mkdir Tools/$(PAROBJDIR)

PTM/$(PAROBJDIR):
	mkdir PTM/$(PAROBJDIR)

Interface/$(PAROBJDIR):
	mkdir Interface/$(PAROBJDIR)

Brenner/$(PAROBJDIR):
	mkdir Brenner/$(PAROBJDIR)

OpenKIMimport/$(PAROBJDIR):
	mkdir OpenKIMimport/$(PAROBJDIR)
endif

Parallel/$(PAROBJDIR):
	mkdir Parallel/$(PAROBJDIR)

ParallelInterface/$(PAROBJDIR):
	mkdir ParallelInterface/$(PAROBJDIR)

install:	install-serial
	@echo 
	@echo 
	@echo 
	@echo SERIAL INSTALLATION SUCCESSFUL
	@echo
	@echo "IMPORTANT:  For parallel installation use $(MAKE) install-parallel"
	@echo 
	@echo 

install-serial: 	serial
	@echo ""
	@echo "Installing python files in $(PYINSTALL)"
	@echo "           binary python files in $(BININSTALL)"
	@echo "       and executables in $(EXECINSTALL)"
	@echo
	@sleep 3
	test -d $(PYINSTALL) || mkdir -p $(PYINSTALL)
	(cd Python/asap3 && find . -name '*.py' -print) | rsync -av --files-from=- Python/asap3 $(PYINSTALL)
	$(PYTHON) -c 'from compileall import *; compile_dir("'$(PYINSTALL)'")'
	test -d $(BININSTALL) || mkdir -p $(BININSTALL)
	@$(MAKE) -q $(OBJDIR)/_asap.so || (echo "ERROR: Serial version not up to date!"; exit 1)
	rm -f $(BININSTALL)/_asap.so
	cp $(OBJDIR)/_asap.so $(BININSTALL)

install-parallel: parallel install
	@$(MAKE) -q $(OBJDIR)/asap-python || (echo "WARNING: Parallel version not up to date or could not be built!" ; exit 1)
	rm -f $(EXECINSTALL)/asap-python
	cp $(OBJDIR)/asapmpiinfo3.py $(BININSTALL)
	test -d $(EXECINSTALL) || mkdir -p $(EXECINSTALL)
	cp $(OBJDIR)/asap-python $(OBJDIR)/asap-qsub $(EXECINSTALL)
	@echo 
	@echo 
	@echo 
	@echo SERIAL+PARALLEL INSTALLATION SUCCESSFUL
	@echo
	@echo 
	@echo 


########################################################
####
####  SPECIAL TARGETS:  Debugging, profiling etc
####
########################################################

distribution:
	$(PYTHON) check_distrib.py $(VERSION)

filelist: setup-filelist.txt

setup-filelist.txt: Makefile
	rm -f setup-filelist.txt
	touch setup-filelist.txt
	for i in $(CXXSRC_BASICS) ; do echo Basics/$$i >> setup-filelist.txt; done
	for i in $(CXXSRC_INTERFACE) ; do echo Interface/$$i >> setup-filelist.txt; done
	for i in $(SERIAL_INTERFACE) ; do echo Interface/$$i >> setup-filelist.txt; done
	for i in $(CXXSRC_BRENNER) ; do echo Brenner/$$i >> setup-filelist.txt; done
	for i in $(CXXSRC_TOOLS) ; do echo Tools/$$i >> setup-filelist.txt; done


tar:
	rm -rf tmp
	mkdir tmp
	svn export . tmp/Asap-$(VERSION)
	$(MAKE) -C tmp/Asap-$(VERSION) filelist
	tar -c -v -z -C tmp -f Asap-$(VERSION).tar.gz Asap-$(VERSION)
	rm -rf tmp
	@echo
	@echo "Tar file Asap-$(VERSION).tar.gz created."

version:
	@echo "ASAP version `python Python/asap3/version.py`"

info:
	@echo "COMPILER = $(COMPILER)"
	@echo "HAS_ICC = $(HAS_ICC)"
	@echo "PYTHON = $(PYTHON)"
	@echo "ARCH = $(ARCH)"
	@echo "HOSTNAME = $(HOSTNAME)"
	@echo "KERNELNAME = $(KERNELNAME)"
	@echo "PYVER = $(PYVER)"
	@echo "PYMAJOR = $(PYMAJOR)"
	@echo "OBJDIR = $(OBJDIR)"
	@echo "VERSION = $(VERSION)"

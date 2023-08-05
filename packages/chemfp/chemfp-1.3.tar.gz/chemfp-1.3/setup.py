#!/usr/bin/env python
from __future__ import print_function
import sys
import os

from distutils.core import setup, Extension
from distutils.command.build_ext import build_ext
from distutils.sysconfig import get_config_var

DESCRIPTION  = """\
chemfp is a set of command-lines tools for generating cheminformatics
fingerprints and searching those fingerprints by Tanimoto similarity,
as well as a Python library which can be used to build new tools.

These algorithms are designed for the dense, 100-10,000 bit
fingerprints which occur in small-molecule/pharmaceutical
chemisty. The Tanimoto search algorithms are implemented in C for
performance and support both threshold and k-nearest searches.

Fingerprint generation can be done either by extracting existing
fingerprint data from an SD file or by using an existing chemistry
toolkit. chemfp supports the Python libraries from Open Babel,
OpenEye, and RDKit toolkits.
"""

# chemfp has two compile-time options.
#  USE_OPENMP: Compile with OpenMP support
#  USE_SSSE3: Compile with compiler- and CPU-specific SSSE3 instructions

# These are available through the setup command-line as:
#   --with-openmp / --without-openmp
#   --with-ssse3 / --without-ssse3

# There doesn't seem to be a clean way to do this with distutils, so
# hack something together to make it work.

def getenv(name, default):
    value = os.environ.get(name, None)
    if value is None:
        return default
    if value == "1":
        return True
    if value == "0":
        return False
    if default:
        extra = "Must be '0' or '1' (default)."
    else:
        extra = "Must be '0' (default) or '1'."
    sys.stderr.write(
        "Warning: Environment variable %s has unsupported value %r."
        % (name, value))
    sys.stderr.write(" " + extra + "\n")
    return default

USE_OPENMP = getenv("CHEMFP_OPENMP", True)  # True means "enable", False means "disable"
USE_SSSE3 = getenv("CHEMFP_SSSE3", True)  # True means "enable", False means "disable"

argv = []
for arg in sys.argv:
    if arg == "--with-openmp":
        USE_OPENMP = True
    elif arg == "--without-openmp":
        USE_OPENMP = False
    elif arg == "--with-ssse3":
        USE_SSSE3 = True
    elif arg == "--without-ssse3":
        USE_SSSE3 = False
    else:
        # not one of the special command-line options; don't delete
        argv.append(arg)
sys.argv = argv



# chemfp uses OpenMP for parallelism.
def OMP(*args):
    if USE_OPENMP:
        return list(args)
    return []

def SSSE3(*args):
    if not USE_SSSE3:
        return []
    # Some Python installations on my Mac are compiled with "-arch ppc".
    # gcc doesn't like the -mssse3 option in that case.
    arch = get_config_var("ARCHFLAGS")
    if arch and "-arch ppc" in arch:
        return []

    return list(args)


# Set "USE_OPENMP" (above) to enable OpenMP support (disabled by default)
# Set "USE_SSSE3" (above) to enable SSSE3 support (enabled by default)
copt =  {
    "msvc": OMP("/openmp") + ["/Ox", "/GL"],
    "mingw32" : OMP("-fopenmp") + ["-O3", "-ffast-math", "-march=native"],

    "gcc-4.1": ["-O3"], # Doesn't support OpenMP, doesn't support -mssse3

    # I'm going to presume that everyone is using an Intel-like processor
    "gcc": OMP("-fopenmp") + SSSE3("-mssse3") + ["-O3"],
         #   Options to use before a release
         # ["-Wall", "-pedantic", "-Wunused-parameter", "-std=c99"],
    "clang-omp": OMP("-fopenmp") + SSSE3("-mssse3") + ["-O3"],
    }

lopt =  {
    "msvc": ["/LTCG", "/MANIFEST"],
    "mingw32" : OMP("-fopenmp"),

    "gcc-4.1": ["-O3"], # Doesn't support OpenMP
    "gcc": OMP("-fopenmp") + ["-O3"],

    "clang-omp": OMP("-fopenmp") + ["-O3"],
    }


def _is_gcc(compiler):
    return "gcc" in compiler or "g++" in compiler

class build_ext_subclass( build_ext ):
    def build_extensions(self):
        c = self.compiler.compiler_type
        if c == "unix":
            compiler_args = self.compiler.compiler
            c = compiler_args[0]  # get the compiler name (argv0)
            if _is_gcc(c):
                names = [c, "gcc"]
                # Fix up a problem on older Mac machines where Python
                # was compiled with clang-specific options:
                #  error: unrecognized command line option '-Wshorten-64-to-32'
                compiler_so_args = self.compiler.compiler_so
                for args in (compiler_args, compiler_so_args):
                    if "-Wshorten-64-to-32" in args:
                        del args[args.index("-Wshorten-64-to-32")]

            else:
                names = [c]
        else:
            names = [c]

        for c in names:
            if c in copt:
                for e in self.extensions:
                    e.extra_compile_args = copt[ c ]
                break

        for c in names:
            if c in lopt:
                for e in self.extensions:
                    e.extra_link_args = lopt[ c ]
                break
        
        build_ext.build_extensions(self)




setup(name = "chemfp",
      version = "1.3",
      description = "A set of command-line tools and a Python toolkit for cheminformatics fingerprint creation and similarity search.",
      long_description = DESCRIPTION,
      author = "Andrew Dalke",
      author_email = 'dalke@dalkescientific.com',
      url = "http://chemfp.com/",
      license = "MIT",
      classifiers = ["Development Status :: 5 - Production/Stable",
                     "Environment :: Console",
                     "License :: OSI Approved :: MIT License",
                     "Operating System :: Unix",
                     # chemfp 1.3 dropped support for Python 2.5 and Python 2.6.
                     # Python 3 for chemfp 3.0 took months to implement. I will
                     # not be back-porting it to the chemfp-1.x series.
                     "Programming Language :: Python :: 2.7",
                     "Programming Language :: Python :: 2 :: Only",
                     "Topic :: Scientific/Engineering :: Chemistry",
                     "Topic :: Software Development :: Libraries :: Python Modules"],
      
      packages = ["chemfp", "chemfp.commandline", "chemfp.futures", "chemfp.progressbar"],
      package_data = {"chemfp": ["rdmaccs.patterns", "rdmaccs2.patterns", "substruct.patterns"]},
      scripts = ["ob2fps", "oe2fps", "rdkit2fps", "sdf2fps", "simsearch"],

      ext_modules = [Extension("_chemfp",
                               ["src/bitops.c", "src/chemfp.c",
                                "src/heapq.c", "src/fps.c",
                                "src/searches.c", "src/hits.c",
                                "src/select_popcount.c", "src/popcount_popcnt.c",
                                "src/popcount_lauradoux.c", "src/popcount_lut.c",
                                "src/popcount_gillies.c", "src/popcount_SSSE3.c",
                                "src/python_api.c", "src/pysearch_results.c"],
                               )],
      cmdclass = {"build_ext": build_ext_subclass},
     )

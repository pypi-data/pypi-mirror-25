Installing
==========

Chemfp requires that Python and a C compiler be installed in your
machines. Since chemfp doesn't run on Microsoft Windows (for tedious
technical reasons), then your machine likely already has both Python
and a C compiler installed. In case you don't have Python, or you want
to install a newer version, you can download a copy of Python from
http://www.python.org/download/ . If you don't have a C
compiler, .. well, do I really need to give you a pointer for that?

Chemfp 1.3 only supports Python 2.7. It might work under Python 2.6
but that configuration hasn't been tested. It will not work under
Python 2.5.

The core chemfp functionality (e.g. similarity search) does not
depend on a third-party library but you will need a chemistry toolkit
in order to generate new fingerprints from structure files. chemfp
supports the free Open Babel and RDKit toolkits and the proprietary
OEChem toolkit. Make sure you install the Python libraries for the
toolkit(s) you select.

Chemfp 1.3 has been tested with Open Babel 2.4.1, RDKit 2013.03, RDKit
2016.09, RDKit 2017.03, RDKit 2017.09 (dev), OEChem/OEGraphSim
2014.07, OEChem/OEGraphSim 2016.10, and OEChem/OEGraphSim 2017.10
(beta).

The easiest way to install chemfp is with the `pip
<https://pip.pypa.io/>`_ installer. This comes with Python 2.7.9 or
later so it may already be installed. Chemfp 1.3 is available through
`PyPI (the Python Package Index)
<https://pypi.python.org/pypi/chemfp>`_ so you can install it
over the web as::

  pip install chemfp

To install the ``tar.gz`` file with pip::

  pip install chemfp-1.3.tar.gz

Otherwise you can use Python's standard "setup.py". Read
http://docs.python.org/install/index.html for details of how to use
it. The short version is to do the following::

  tar xf chemfp-1.3.tar.gz
  cd chemfp-1.3
  python setup.py build
  python setup.py install

The last step may need a ``sudo`` if you otherwise cannot write to your
Python site-package. Another option is to use a `virtual environment
<https://pypi.python.org/pypi/virtualenv>`_.

Configuration options
---------------------

The setup.py file has several compile-time options which can be set
either from the ``python setup.py build`` command-line or through
environment variables. The environment variable solution is the
easiest way to change the settings under pip.

.. option:: --with-openmp, --without-openmp

Chemfp uses OpenMP to parallelize multi-query searches. The default is
:option:`--with-openmp`. If you have a very old version of gcc, or an
older version of clang, or are on a Mac where the clang version
doesn't support OpenMP, then you will need to use
:option:`--without-openmp` to tell setup.py to compile without OpenMP::
   
   python setup.py build --without-openmp

You can also set the environment variable CHEMFP_OPENMP to "1" to
compile with OpenMP support, or to "0" to compile without OpenMP
support::
   
   CHEMFP_OPENMP=0 pip install chemfp-1.3.tar.gz 

Note: you can use the environment variable ``CC`` to change the C
compiler. For example, the clang compiler on Mac doesn't support
OpenMP so I installed gcc-7 and compile using::

   CC=gcc-7 pip install chemfp-1.3.tar.gz 

.. option:: --with-ssse3, --without-ssse3

Chemfp by default compiles with SSSE3 support, which was first
available in 2006 so almost certainly available on your Intel-like
processor. In case I'm wrong (are you compiling for ARM? If so, send
my any compiler patches), you can disable SSSE3 support using the
:option:`--without-ssse3`, or set the environment variable
``CHEMFP_SSSE3`` to "0".

Compiling with SSSE3 support has a very odd failure case. If you
compile with the SSSE3 flag enabled, then take the binary to a machine
without SSSE3 support, then it will crash because all of the code will
be compiled to expect the SSSE3 instruction set even though only one
file, popcount_SSSE3.c, should be compiledthat way.

The solution is to compile popcount_SSSE3.c with the SSSE3 flag
enabled and all of the other files without that flag. Unfortunately,
Python's setup.py doesn't make that easy to do. If this is a problem
for you, take a look at ``filter_gcc`` in the chemfp
distribution. It's used like this::

    CC=$PWD/filter_gcc python setup.py build

It's a bit of a hack so contact me if you have problems.

.. _intro:

========================
chemfp 1.3 documentation
========================

`chemfp <http://chemfp.com/>`_ is a set of tools for working with
cheminformatics fingerprints in the FPS format.

This is the documentation for the no-cost version of chemfp. To see
the documentation for the chemfp 3.1, the commercial version of chemfp, 
go to `http://chemfp.readthedocs.io/en/chemfp-3.1/
<http://chemfp.readthedocs.io/en/chemfp-3.1/>`_.

Most people will use the command-line programs to generate and search
fingerprint files. :ref:`ob2fps <ob2fps>`, :ref:`oe2fps <oe2fps>`, and
:ref:`rdkit2fps <rdkit2fps>` use respectively the `Open Babel
<http://openbabel.org/>`_, `OpenEye <http://www.eyesopen.com/>`_, and
`RDKit <http://www.rdkit.org/>`_ chemistry toolkits to convert
structure files into fingerprint files. :ref:`sdf2fps <sdf2fps>`
extracts fingerprints encoded in SD tags to make the fingerprint
file. :ref:`simsearch <simsearch>` finds targets in a fingerprint file
which are sufficiently similar to the queries.

The programs are built using the :ref:`chemfp Python library API <chemfp-api>`,
which in turn uses a C extension for the performance
critical sections. The parts of the library API documented here are
meant for public use, and include examples.


Remember: chemfp cannot generate fingerprints from a structure file
without a third-party chemistry toolkit.

Chemfp 1.3 was released on 18 September 2017. It supports Python 2.7
and can be used with any recent version of OEChem/OEGraphSim, Open
Babel, or RDKit. Python 3 support is available in the commerical
version of chemfp. If you are interested in paying for a copy, send an
email to sales@dalkescientific.com .

.. toctree::
   :maxdepth: 2

   installing
   using-tools
   tool-help
   using-api
   api
   

License and advertisement
=========================

This program was developed by Andrew Dalke
<dalke@dalkescientific.com>, Andrew Dalke Scientific, AB. It is
distributed free of charge under the "MIT" license, shown below.

Further chemfp development depends on funding from people like
you. Asking for voluntary contributions almost never works. Instead,
starting with chemfp 1.1, there are two development tracks. You can
download and use the no-cost version or you can pay money to get
access to the commercial version.

In both cases you get the software under the MIT license. I'll stress
that: even the commercial version of chemfp is open source
software. Once you have a copy there are very few restrictions on what
you can do with it. (The one exeception is we have signed a
non-disclosure agreement which lets you evaluate the commercial
version to decide if you want to pay for it.)

The current commercial version is 3.1. It can handle more than 4GB of
fingerprint data, it supports the FPB binary fingerprint format for
fast loading, it has an expanded API designed for web server
development (for example, reading and writing from strings, not just
files), and it supports both Python 2.7 and Python 3.5 or later.

If you pay for the commercial distribution then you will get the most
recent version of chemfp, free upgrades for one year, support, and a
discount on renewing participation in the incentive program.

If you have questions about or with to purchase the commercial
distribution, send an email to sales@dalkescientific.com .


.. highlight:: none

::

  Copyright (c) 2010-2017 Andrew Dalke Scientific, AB (Gothenburg, Sweden)
  
  Permission is hereby granted, free of charge, to any person obtaining
  a copy of this software and associated documentation files (the
  "Software"), to deal in the Software without restriction, including
  without limitation the rights to use, copy, modify, merge, publish,
  distribute, sublicense, and/or sell copies of the Software, and to
  permit persons to whom the Software is furnished to do so, subject to
  the following conditions:
  
  The above copyright notice and this permission notice shall be
  included in all copies or substantial portions of the Software.
  
  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
  NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
  LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
  OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
  WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Copyright to portions of the code are held by other people or
organizations, and may be under a different license. See the specific
code for details. These are:

 - OpenMP, cpuid, POPCNT, and Lauradoux implementations by Kim
   Walisch, <kim.walisch@gmail.com>, under the MIT license
 - SSSE3.2 popcount implementation by Stanford Univeristy (written by
   Imran S. Haque <ihaque@cs.stanford.edu>) under the BSD license
 - heapq by the Python Software Foundation under the Python license
 - TimSort code by Christopher Swenson under the MIT License
 - tests/unittest2 by Steve Purcell, the Python Software Foundation,
   and others, under the Python license
 - chemfp/rdmaccs.patterns and chemfp/rdmaccs2.patterns by Rational
   Discovery LLC, Greg Landrum, and Julie Penzotti, under the 3-Clause
   BSD License
 - chemfp/argparse.py by Steven J. Bethard under the Apache License 2.0 
 - chemfp/progressbar/ by Nilton Volpato under the LGPL 2.1 and/or BSD license
 - chemfp/futures/ by Brian Quinlan under the Python license

What's new in 1.3
=================

Released 18 September 2017

This release has dropped support for Python 2.5 and Python 2.6. It has
been over 7 years since Python 2.7 was released, so if you're using an
older Python, perhaps it's time to upgrade?

Toolkit changes
---------------

RDKit, OEGraphSim, Open Babel, and CDK did not implement MACCS key 44
("OTHER") because it wasn't defined. Then Accelrys published a white
paper which defined that term. All of the toolkits have updated their
implementations. The corresponding chemfp fingerprint types are
RDKit-MACCS166/2, OpenEye-MACCS166/3, and OpenBabel-MACCS/2. I have
also updated chemfp's own RDMACCS definitions to include key 44, and
changed the versions from /1 to /2.

This release supports OEChem v2 and OEGraphSim v2 and drops support
for OEGraphSim v1, which OpenEye replaced in 2010. It also drops
support for the old OEBinary format.

Several years ago, RDKit changed its hash fingerprint algorithm. The
new chemfp fingerprint type is "RDKit-Fingerprint/2". 

WARNING! In chemfp 1.1 the default for the RDKit-Fingerprint setting
nBitsPerHash was 4. It should have been 2 to match RDKit's own
default. I have changed the default to 2, but it means that your
fingerprints will likely change.

Chemfp now supports the experimental RDKit substructure
fingerprint. The chemfp type name is "RDKit-Pattern". There are four
known versions. RDKit-Pattern/1 is many years old, RDKit-Pattern/2 was
in place for several years up to 2017, RDKit-Pattern/3 was only in the
2017.3 release, and RDKit-Pattern/4 will be in the 2017.9
release.  The corresponding :ref:`rdkit2fps <rdkit2fps>` flag is :option:`--pattern`.

RDKit has an adapter to use the third-party Avalon chemistry toolkit
to create substructure fingerprints. Avalon support used to require
special configuration but it's now part of the standard RDKit build
process. Chemfp now supports the Avalon fingerprints, as the type
"RDKit-Avalon/1". The corresponding :ref:`rdkit2fps <rdkit2fps>` flag is
:option:`--avalon`.

Updated the #software line to include "chemfp/1.3" in addition to the
toolkit information. This helps distinguish between, say, two
different programs which generate RDKit Morgan fingerprints. It's also
possible that a chemfp bug can affect the fingerprint output, so the
extra term makes it easier to identify a bad dataset.


Performance
-----------

The k-nearest arena search, which is used in NxM searches, is now
parallelized.

The FPS reader is now much faster. As a result, simsearch for a single
query (which uses --scan mode) is about 40% faster, and the time for
chemfp.load_fingerprints() to create an areana is about 15% faster.

Similarity search performance for the MACCS keys, on a machine which
supports the POPCNT instruction, is now about 20-40% faster, depending
on the type of search.

Command-line tools
------------------

In chemfp 1.1 the default error handler for ob2fps, oe2fps, and
rdkit2fps was "strict". If chemfp detected that a toolkit could not
parse a structure, it would print an error message and stop
processing. This is not what most people wanted. They wanted the
processing to keep on going.

This was possible by specifying the :option:`--errors` values "report"
or "ignore", but that was extra work, and confusing.

In chemfp 1.3, the default :option:`--errors` value is "ignore", which
means chemfp will ignore any problems, not report a problem, and go on
to the next record.

However, if the record identifier is missing (for example, if the SD
title line is blank), then this will be always be reported to stderr
even under the "ignore" option. If :option:`--errors` is "strict" then
processing will stop if a record does not contain an identifier.

Added :option:`--version`. (Suggested by Noel O'Boyle.)

The ob2fps :option:`--help` now includes a description of the FP2,
FP3, FP4, and MACCS options.


API
---

Deprecated :func:`.read_structure_fingerprints`. Instead, call the
new function :func:`.read_molecule_fingerprints`. Chemfp 2.0 changed
the name to better fit its new toolkit API. This change in chemfp 1.3
helps improve forward compatibility.

The chemfp.search module implements two functions to help with
substructure fingerprint screening. The function :func:`.contains_fp`
takes a query fingerprint and finds all of the target fingerprints
which contain it. (A fingerprint x "contains" y if all the on-bits in
y are also on-bits in x.) The function :func:`.contains_arena` does the same screening for each fingerprint in a
query arena.

The new :attr:`.SearchResults.shape` attribute is a 2-element tuple
where the first is the size of the query arena and the second is the
size of the target arena. The new :meth:`.SearchResults.to_csr` method
converts the similarity scores in the SearchResults to a SciPy
compressed sparse row matrix. This can be passed to some of the
scikit-learn clustering algorithms.

Backported the FPS reader. This fixed a number of small bugs, like
reporting the wrong record line number when there was a missing
terminal newline. It also added some new features like a context
manager.

Backported the FPS writer from Python 3.0. While it is not hard to
write an FPS file yourself, the new API should make it even easier.
Among other things, it understands how to write the chemfp
:class:`.Metadata` as the header and it implements a context
manager. Here's an example of using it to find fingerprints with at
least 225 of the 881 bits set and save them in another file::

  import chemfp
  from chemfp import bitops
  with chemfp.open("pubchem_queries.fps") as reader:
    with chemfp.open_fingerprint_writer(
         "subset.fps", metadata=reader.metadata) as writer:
      for id, fp in reader:
        if bitops.byte_popcount(fp) >= 225:
          writer.write_fingerprint(id, fp)

The new FPS reader and writer, along with the chemistry toolkit
readers, support the :class:`Location` API as a way to get information
about the internal state in the readers or writers. This is another
backport from chemfp 3.0.

Backported bitops functions from chemfp 3.0. The new functions are:
:func:`.hex_contains`, :func:`.hex_contains_bit`, :func:`.hex_intersect`,
:func:`.hex_union`, :func:`.hex_difference`, :func:`.byte_hex_tanimoto`,
:func:`.byte_contains_bit`, :func:`.byte_to_bitlist`,
:func:`.byte_from_bitlist`, :func:`.hex_to_bitlist`,
:func:`.hex_from_bitlist`, :func:`.hex_encode`,
:func:`.hex_encode_as_bytes`, :func:`.hex_decode`.

The last three functions related to hex encoding and decoding are
important if you want to write code which is forward compatible for
Python 3. Under Python 3, the simple fp.encode("hex") is no longer
supported. Instead, use bitops.hex_encode("fp").

Note that the chemfp 1.x series is unlikely to become Python 3
compatible. For Python 3 support, consider purchasing a copy of chemfp
3.1.



Important bug fixes
-------------------

Fix: As described above, the RDKit-Fingerprint nBitsPerHash default changed
from 4 to 2 to match the RDKit default value.

Fix: Some of the Tanimoto calculations stored intermediate values as a
double. As a result of incorrectly ordered operations, some Tanimoto
scores were off by 1 ulp (the last bit in the double). They are now
exactly correct.

Fix: if the query fingerprint had 1 bit set and the threshold was 0.0
then the sublinear bounds for the Tanimoto searches (used when there
is a popcount index) failed to check targets with 0 bits set.

Fix: If a query had 0 bits then the k-nearest code for a symmetric
arena returned 0 matches, even when the threshold was 0.0. It now
returns the first k targets.

Fix: There was a bug in the sublinear range checks which only occurred
in the symmetric searches when the batch_size is larger than the
number of records and with a popcount just outside of the expected
range.

Configuration
-------------

The configuration of the --with-* or --without-* options (for OpenMP
and SSSE3) support, can now be specified via environment variables. In
the following, the value "0" means disable (same as "--without-\*") and
"1" means enable (same as "--with-\*")::

  CHEMFP_OPENMP -  compile for OpenMP (default: "1")
  CHEMFP_SSSE3  -  compile SSSE3 popcount support (default: "1")
  CHEMFP_AVX2   -  compile AVX2 popcount support (default: "0")

This makes it easier to do a "pip install" directly on the tar.gz file
or use chemfp under an automated testing system like tox, even when
the default options are not appropriate. For example, the default C
compiler on Mac OS X doesn't support OpenMP. If you want OpenMP
support then install gcc and specify it with the "CC". If you don't
want OpenMP support then you can do::

  CHEMFP_OPENMP=0 pip install chemfp-1.3.tar.gz



Future
======

The chemfp code base is solid and in use at many companies, some of
whom have paid for the commercial version. It has great support for
fingerprint generation, fast similarity search, and multiple
cheminformatics toolkits.

There are two tracks for improvements. Most of the new feature
development is done in the commerical version of chemfp. I make my
living in part by selling software, and few people will pay for
software they can get for free.

The chemfp 1.x series is primarily in maintenance mode. I will track
changes to the fingerprint types and add any new fingerprint types
which might come along. I'll also backport some of the features from
the commercial version. For example, I expect chemfp 1.4 will include
the text toolkit API from chemfp 2.1, and identifiers will be returned
as Unicode strings instead of byte strings.

I will also accept contributions to chemfp. These must be under the
MIT license or similarly unrestrictive license so I can include it in
both the no-cost and commercial versions of chemfp.


Thanks
======

In no particular order, the following contributed to chemfp in some
way: Noel O'Boyle, Geoff Hutchison, the Open Babel developers, Greg
Landrum, OpenEye, Roger Sayle, Phil Evans, Evan Bolton, Wolf-Dietrich
Ihlenfeldt, Rajarshi Guha, Dmitry Pavlov, Roche, Kim Walisch, Daniel
Lemire, Nathan Kurz, Chris Morely, Jörg Kurt Wegner, Phil Evans, Björn
Grüning, Andrew Henry, Brian McClain, Pat Walters, Brian Kelley, and
Lionel Uran Landaburu.

Thanks also to my wife, Sara Marie, for her many years of support.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


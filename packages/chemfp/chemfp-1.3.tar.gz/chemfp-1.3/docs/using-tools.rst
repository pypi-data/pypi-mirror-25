.. highlight:: none

===================================
Working with the command-line tools
===================================

The sections in this chapter describe examples of using the
command-line tools to generate fingerprint files and to do similarity
searches of those files.

.. _pubchem_fingerprints:

Generating fingerprint files from PubChem SD files
==================================================

In this section you'll learn how to create a fingerprint file from an
SD file which contains pre-computed CACTVS fingerprints. You do not
need a chemistry toolkit for this section.

`PubChem <http://pubchem.ncbi.nlm.nih.gov/>`_ is a great resource
of publically available chemistry information. The data is available
for `ftp download <ftp://ftp.ncbi.nlm.nih.gov>`_. We'll use some of
their `SD formatted
<http://en.wikipedia.org/wiki/Structure_Data_File#SDF>`_ files.
Each record has a PubChem/CACTVS fingerprint field, which we'll used.

Start by downloading the files 
Compound_027575001_027600000.sdf.gz
(from
ftp://ftp.ncbi.nlm.nih.gov/pubchem/Compound/CURRENT-Full/SDF/Compound_027575001_027600000.sdf.gz
)
and Compound_014550001_014575000.sdf.gz
(from
ftp://ftp.ncbi.nlm.nih.gov/pubchem/Compound/CURRENT-Full/SDF/Compound_014550001_014575000.sdf.gz
). At the time of writing they contain 213 and 5208 records,
respectively. (I chose smaller than average files so they would be
easier to open and review.)

Next, convert the files into fingerprint files. On the command line
do the following two commands::

    sdf2fps --pubchem Compound_027575001_027600000.sdf.gz -o pubchem_queries.fps
    sdf2fps --pubchem Compound_014550001_014575000.sdf.gz -o pubchem_targets.fps

Congratulations, that was it!

How does this work? Each PubChem record contains the precomputed
CACTVS substructure keys in the PUBCHEM_CACTVS_SUBSKEYS tag. The
:option:`--pubchem` flag tells sdf2fps to get the value of that tag and decode
it to get the fingerprint. It also adds a few metadata fields to the
fingerprint file header.

The order of the fingerprints are the same as the order of the
corresponding record in the SDF, although unconvertable records might
be skipped, depending on the :option:`--errors` flag.

If you store records in an SD file then you almost certainly don't use
the same fingerprint encoding as PubChem. sdf2ps can decode from a
number of encodings. Use :option:`--help` to see the list of available
decoders.


k-nearest neighbor search
=========================

In this section you'll learn how to search a fingerprint file to find
the k-nearest neighbors. You will need the fingerprint files generated
in :ref:`pubchem_fingerprints` but you do not need a chemistry
toolkit.

We'll use the pubchem_queries.fps as the queries for a k=2 nearest
neighor similarity search of the target file puchem_targets.gps::

   simsearch -k 2 -q pubchem_queries.fps pubchem_targets.fps

That's all! You should get output which starts::

    #Simsearch/1
    #num_bits=881
    #type=Tanimoto k=2 threshold=0.0
    #software=chemfp/1.3
    #queries=pubchem_queries.fps
    #targets=pubchem_targets.fps
    #query_sources=Compound_027575001_027600000.sdf.gz
    #target_sources=Compound_014550001_014575000.sdf.gz
    2	27575190	14555201	0.7236	14566941	0.7105
    2	27575192	14555203	0.7158	14555201	0.7114
    2	27575198	14555201	0.7286	14569555	0.7259
    2	27575208	14555201	0.7701	14566941	0.7584

How do you interpret the output? The lines starting with '#' are
header lines. It contains metadata information describing that this is
a similarity search report. You can see the search parameters, the
name of the tool which did the search, and the filenames which went
into the search.

After the '#' header lines come the search results, with one result
per line. There are in the same order as the query fingerprints. Each
result line contains tab-delimited columns. The first column is the
number of hits. The second column is the query identifier used. The
remaining columns contain the hit data, with alternating target id and
its score.

For example, the first result line contains the 2 hits for the
query 27575190. The first hit is the target id 1455201 with score
0.7236 and the second hit is 14566941 with score 0.7105. Since this is
a k-nearest neighor search, the hits are sorted by score, starting
with the highest score. Do be aware that ties are broken arbitrarily.


Threshold search
================

In this section you'll learn how to search a fingerprint file to find
all of the neighbors at or above a given threshold. You will need the
fingerprint files generated in :ref:`pubchem_fingerprints` but you do
not need a chemistry toolkit.

Let's do a threshold search and find all hits which are at least 0.738
similar to the queries::

    simsearch --threshold 0.738 -q pubchem_queries.fps pubchem_targets.fps

The first 20 lines of output from this are::

    #Simsearch/1
    #num_bits=881
    #type=Tanimoto k=all threshold=0.738
    #software=chemfp/1.3
    #queries=pubchem_queries.fps
    #targets=pubchem_targets.fps
    #query_sources=Compound_027575001_027600000.sdf.gz
    #target_sources=Compound_014550001_014575000.sdf.gz
    0	27575190
    0	27575192
    0	27575198
    3	27575208	14566941	0.7584	14566938	0.7542	14555201	0.7701
    0	27575240
    0	27575250
    1	27575257	14572463	0.7468
    1	27575282	14555201	0.7656
    0	27575284
    0	27575295
    0	27575318
    0	27575419
    
Take a look at the fourth result line, which contains the 3 hits for
the query id 27575208. As before, the hit information alternates
between the target ids and the target scores, but unlike the k-nearest
search, the hits are not in a particular order. You can see that here
where the scores are 0.7584, 0.7542, and 0.7701 .

You might be wondering why I chose the 0.738 threshold. Query id
27575208 has 10 hits with a threshold of 0.7 or higher. That requires
22 columns to show, which is a bit overwhelming.

Combined k-nearest and threshold search
=======================================

In this section you'll learn how to search a fingerprint file to find
the k-nearest neighbors, where all of the hits must be at or above
given threshold. You will need the fingerprint files generated in
:ref:`pubchem_fingerprints` but you do not need a chemistry toolkit.


You can combine the :option:`-k` and :option:`--threshold` queries to
find the k-nearest neighbors which are all above a given threshold::

    simsearch -k 3 --threshold 0.7 -q pubchem_queries.fps pubchem_targets.fps

This find the nearest 3 structures, which all must be at least 0.7
similar to the query fingerprint. The output from the above starts::

    #Simsearch/1
    #num_bits=881
    #type=Tanimoto k=3 threshold=0.7
    #software=chemfp/1.3
    #queries=pubchem_queries.fps
    #targets=pubchem_targets.fps
    #query_sources=Compound_027575001_027600000.sdf.gz
    #target_sources=Compound_014550001_014575000.sdf.gz
    3	27575190	14555201	0.7236	14566941	0.7105	14566938	0.7068
    2	27575192	14555203	0.7158	14555201	0.7114
    3	27575198	14555201	0.7286	14569555	0.7259	14553070	0.7065
    3	27575208	14555201	0.7701	14566941	0.7584	14566938	0.7542
    2	27575240	14555201	0.7150	14566941	0.7016
    2	27575250	14555203	0.7128	14555201	0.7085
    3	27575257	14572463	0.7468	14563588	0.7250	14561245	0.7219
    3	27575282	14555201	0.7656	14555198	0.7317	14566941	0.7166
    0	27575284
    0	27575295
    0	27575318
    3	27575419	14570951	0.7339	14570934	0.7265	14570935	0.7232

The output format is identical to the previous two search examples,
and because this is a k-nearest search, the hits are sorted from
higest score to lowest.

NxN (self-similar) searches
===========================

Use the --NxN option if you want to use the same fingerprints as both
the queries and targets::

    simsearch -k 3 --threshold 0.7 --NxN pubchem_queries.fps

This is about twice as fast and uses half as much memory compared to::

    simsearch -k 3 --threshold 0.7 -q pubchem_queries.fps pubchem_queries.fps

Plus, the --NxN option excludes matching a fingerprint to itself (the
diagonal term).

.. _chebi_fingerprints:

Using a toolkit to process the ChEBI dataset
============================================

In this section you'll learn how to create a fingerprint file from a
structure file. The structure processing and fingerprint generation
are done with a third-party chemisty toolkit. chemfp supports Open
Babel, OpenEye, and RDKit. (OpenEye users please note that you will
need an OEGraphSim license to use the OpenEye-specific
fingerprinters.)


We'll work with data from ChEBI http://www.ebi.ac.uk/chebi/ which
contains "Chemical Entities of Biological Interest". They distribute
their structures in several formats, including as an SD file. For this
section, download the "lite" version from
ftp://ftp.ebi.ac.uk/pub/databases/chebi/SDF/ChEBI_lite.sdf.gz . It
contains the same structure data as the complete version but many
fewer tag data fields.  For ChEBI 155 this file contains 95,955 records
and the compressed file is 28MB.

Unlike the PubChem data set, the ChEBI data set does not contain
fingerprints so we'll need to generate them using a toolkit.

ChEBI record titles don't contain the id
----------------------------------------

Strangely, the ChEBI dataset does not use the title line of the SD
file to store the record id. A simple examination shows that 47,376 of
the title lines are empty, 39,615 have the title "null", 4,499 have
the title " ", 2,033 have the title "ChEBI", 45 of them are labeled
"Structure #1", and the others are usually compound names.

(I've asked ChEBI to fix this, to no success. Perhaps you have more
influence?)

Instead, the id is stored as the value of the "ChEBI ID" tag, which
in the SD file looks like::

    > <ChEBI ID>
    CHEBI:776

By default the toolkit-based fingerprint generation tools use the
title as the identifier, and print a warning and skip the record if
the identifier is missing. Here's an example with :ref:`rdkit2fps
<rdkit2fps>`::

    #FPS1
    #num_bits=2048
    #type=RDKit-Fingerprint/2 minPath=1 maxPath=7 fpSize=2048 nBitsPerHash=2 useHs=1
    #software=RDKit/2017.09.1.dev1 chemfp/1.3
    #source=ChEBI_lite.sdf.gz
    #date=2017-09-14T21:22:01
    ERROR: Missing title in SD record, file 'ChEBI_lite.sdf.gz', line 1, record #1. Skipping.
    ERROR: Missing title in SD record, file 'ChEBI_lite.sdf.gz', line 62, record #2. Skipping.
    ERROR: Missing title in SD record, file 'ChEBI_lite.sdf.gz', line 100, record #3. Skipping.
    ERROR: Missing title in SD record, file 'ChEBI_lite.sdf.gz', line 135, record #4. Skipping.
    ERROR: Missing title in SD record, file 'ChEBI_lite.sdf.gz', line 201, record #5. Skipping.
    ERROR: Missing title in SD record, file 'ChEBI_lite.sdf.gz', line 236, record #6. Skipping.
    [23:22:01]  S group MUL ignored on line 103
    ERROR: Missing title in SD record, file 'ChEBI_lite.sdf.gz', line 264, record #7. Skipping.
    [23:22:01]  Unhandled CTAB feature: S group SRU on line: 31. Molecule skipped.
    ERROR: Missing title in SD record, file 'ChEBI_lite.sdf.gz', line 435, record #9. Skipping.
    ERROR: Missing title in SD record, file 'ChEBI_lite.sdf.gz', line 519, record #10. Skipping.
    ERROR: Missing title in SD record, file 'ChEBI_lite.sdf.gz', line 581, record #11. Skipping.
    031087be231150242e714400920000a193c1080c02858a1116a68100a58806342840405253004080c8cc3c4811
    4101b25081a10c025e634c08a1c00088102c0400121040a2080505188a9c0a150000028211219c1001000981c4
    804417180aca0401408500180182210716db1580708a0b8a0802820532854411200c1101040404001118600d0a
    518402385dc00011290602205a070480c148f240421000c321801922c7808740cd0b10ea4c40000403dc180121
    94d8d120020150b3d00043a24370000201042881d15018c0e0901442881d68604c4a83808110c772a824051948
    003c801360600221040010e20418381668404b0424ec130f05a090c94960e0	ChEBI
    00008000000000000000002880000000000000000200000004008000000000000000200040000002000c000000
    000000000080080000000200400100000000000000001000000400001000000000000000800000000000000100
    00000801002000000001000000400004c000000000000000800004000000001102000000200004000000100300
    08000000000000000000000000000000000820000404000000800000400000200c000008040000000000000000
    200101008000000000000000000202000002008000000000000002000000000008000400000000000000000100
    40000100020080000001000300280000002002000000000000000000000000	ChEBI

That output contains only two fingerprint records, both with the id
"ChEBI". The other records had no title and were skipped, with a
message sent to stderr describing the problem and the location of the
record containing the problem.

(If the first 100 records have no identifiers then the command-line
tools will exit even if :option:`--errors` is ignore. This is a safety
mechanism. Let me know if it's a problem.)

Instead, use the :option:`--id-tag` option to specify of the name of
the data tag containing the id. For this data set you'll need to write
it as::

    --id-tag "ChEBI ID"

The quotes are important because of the space in the tag name.

Here's what that looks like::

    [23:25:17]  S group MUL ignored on line 103
    [23:25:17]  Unhandled CTAB feature: S group SRU on line: 31. Molecule skipped.
    #FPS1
    #num_bits=2048
    #type=RDKit-Fingerprint/2 minPath=1 maxPath=7 fpSize=2048 nBitsPerHash=2 useHs=1
    #software=RDKit/2017.09.1.dev1 chemfp/1.3
    #source=ChEBI_lite.sdf.gz
    #date=2017-09-14T21:25:17
    10208220141258c184490038b4124609db0030024a0765883c62c9e1288a1dc224de62f445743b8b
    30ad542718468104d521a214227b29ba3822fbf20e15491802a051532cd10d902c39b02b51648981
    9c87eb41142811026d510a890a711cb02f2090ddacd990c5240cc282090640103d0a0a8b460184f5
    11114e2a8060200804529804532313bb03912d5e2857a6028960189e370100052c63474748a1c000
    8079f49c484ca04c0d0bcb2c64b72401042a1f82002b097e852830e5898302021a1203e412064814
    a598741c014e9210bc30ab180f0162029d4c446aa01c34850071e4ff037a60e732fd85014344f82a
    344aa98398654481b003a84f201f518f	CHEBI:90
    00000000080200412008000008000004000010100022008000400002000020100020006000800001
    01000100080001000010000002002200000200000008000000400002100000000080000004401000
    80200020800200002000001400022064000004244810000000000080000a80012002020004198002
    00080200020020120040203001000802010100024211000004400000000100200003000001000100
    0100021000a200601080002a00002020048004030000884084000008000002040200010800000000
    2000010022000800002000020001400020800100025040000000200a080244000060008000000802
    8100c801108000000041c00200800002	CHEBI:165

In addition to "ChEBI ID" there's also a "ChEBI Name" tag which
includes data values like "tropic acid" and
"(+)-guaia-6,9-diene". Every ChEBI record has a unique name so the
names could also be used as the primary identifier.

The FPS fingerprint file format allows identifiers with a space, or
comma, or anything other tab, newline, and a couple of other special
bytes, so it's no problem using those names directly.

To use the ChEBI Name as the primary chemfp identifier, specify::

    --id-tag "ChEBI Name"


Generating fingerprints with Open Babel
---------------------------------------

If you have the Open Babel Python library installed then you can use
:ref:`ob2fps <ob2fps>` to generate fingerprints::

    ob2fps --id-tag "ChEBI ID" ChEBI_lite.sdf.gz -o ob_chebi.fps

This takes just under 3 minutes on my 7 year old desktop to process
all of the records.

The default uses the FP2 fingerprints, so the above is the same as::

    ob2fps --FP2 --id-tag "ChEBI ID" ChEBI_lite.sdf.gz -o ob_chebi.fps

ob2fps can generate several other types of fingerprints. (Use
:option:`--help` for a list.) For example, to generate the Open Babel
implementation of the MACCS definition use::

    ob2fps --MACCS --id-tag "ChEBI ID" ChEBI_lite.sdf.gz -o chebi_maccs.fps


Generating fingerprints with OpenEye
------------------------------------

If you have the OEChem Python library installed, with licenses for
OEChem and OEGraphSim, then you can use :ref:`oe2fps <oe2fps>` to
generate fingerprints::

    oe2fps --id-tag "ChEBI ID" ChEBI_lite.sdf.gz -o oe_chebi.fps

This takes about 40 seconds on my desktop and generates a number of
warnings like "Stereochemistry corrected on atom number 17 of",
"Unsupported Sgroup information ignored", and "Invalid stereochemistry
specified for atom number 9 of". Normally the record title comes after
the "... of", but the title is blank for most of the records.

OEChem could not parse 7 of the 95,955 records. I looked at the
failing records and noticed that all of them had 0 atoms and 0 bonds.

The default settings produce OEGraphSim path fingerprint with the
values::

    numbits=4096 minbonds=0 maxbonds=5
       atype=Arom|AtmNum|Chiral|EqHalo|FCharge|HvyDeg|Hyb btype=Order|Chiral 

Each of these can be changed through command-line options.

oe2fps can generate several other types of fingerprints. For example,
to generate the OpenEye implementation of the MACCS definition specify::

   oe2fps --maccs166 --id-tag "ChEBI ID" ChEBI_lite.sdf.gz -o chebi_maccs.fps

Use :option:`--help` for a list of available oe2fps fingerprints or to
see more configuration details.

Generating fingerprints with RDKit
----------------------------------

If you have the RDKit Python library installed then you can use
:ref:`rdkit2fps <rdkit2fps>` to generate fingerprints. Based on the
previous examples you probably guessed that the command-line is::

    rdkit2fps --id-tag "ChEBI ID" ChEBI_lite.sdf.gz -o rdkit_chebi.fps

This takes just under 6 minutes on my desktop, and RDKit did not
generate fingerprints for 1,101 of the 95,955 records.
    
You can see some of the RDKit error messages in the output, like::

    [00:47:02] Explicit valence for atom # 12 N, 4, is greater than permitted
    [00:47:02]  S group DAT ignored on line 102

These come from RDKit's error log. RDKit is careful to check that
structures make chemical sense, and in this case it didn't like the
4-valent nitrogen. It refuses to process this molecule.


The default generates RDKit's path fingerprints with parameters::

    minPath=1 maxPath=7 fpSize=2048 nBitsPerHash=2 useHs=1  

(NOTE! In chemfp 1.1 the default nBitsPerHash was 4. The RDKit default
nBitsPerHash is 2.)

Each of those can be changed through command-line options. See rdkit2fps
:option:`--help` for details, where you'll also see a list of the
other available fingerprint types.

For example, to generate the RDKit implementation of the MACCS
definition use::

  rdkit2fps --maccs166 --id-tag "ChEBI ID" ChEBI_lite.sdf.gz -o chebi_maccs.fps

while the following generates the Morgan/circular fingerprint with
radius 3::

  rdkit2fps --morgan --radius 3 --id-tag "ChEBI ID" ChEBI_lite.sdf.gz

Alternate error handlers
========================

In this section you'll learn how to change the error handler for
rdkit2fps using the :option:`--errors` option.

By default the "<toolkit>2fps" programs "ignore" structures which
could not be parsed into a molecule option. There are two other
options. They can "report" more information about the failure case and
keep on processing, or they can be "strict" and exit after reporting
the error.

This is configured with the :option:`--errors` option.

Here's the rdkit2fps output using :option:`--errors report`::

    [00:52:39]  S group MUL ignored on line 103
    [00:52:39]  Unhandled CTAB feature: S group SRU on line: 36. Molecule skipped.
    ERROR: Could not parse molecule block, file 'ChEBI_lite.sdf.gz', line 12036, record #179. Skipping.
    [00:52:39] Explicit valence for atom # 12 N, 4, is greater than permitted
    ERROR: Could not parse molecule block, file 'ChEBI_lite.sdf.gz', line 16213, record #265. Skipping.

The first two lines come from RDKit. The third line is from chemfp,
reporting which record could not be parsed. (The record starts at line
12036 of the file and the SRU is on line 36 of the record, so the SRU
is at line 12072.) The fourth line is another RDKit error message, and
the last line is another chemfp error message.

Here's the rdkit2fps output using :option:`--errors strict`::

    [00:54:30]  S group MUL ignored on line 103
    [00:54:30]  Unhandled CTAB feature: S group SRU on line: 36. Molecule skipped.
    ERROR: Could not parse molecule block, file 'ChEBI_lite.sdf.gz', line 12036, record #179. Exiting.

Because this is strict mode, processing exits at the first failure.

The ob2fps and oe2fps tools implement the :option:`--errors` option,
but they aren't as useful as rdkit2fps because the underlying APIs
don't give useful feedback to chemfp about which records failed. For
example, the standard OEChem file reader automatically skips records
that it cannot parse. Chemfp can't report anything when it doesn't
know there was a failure.

The default error handler in chemfp 1.1 was "strict". In practice this
proved more annoying than useful because most people want to skip the
records which could not be processed. They would then contact me
asking what was wrong, or doing some pre-processing to remove the
failure cases.

One of the few times when it is useful is for records which contain no
identifier. When I changed the default from "strict" to "ignore" and
tried to process ChEBI, I was confused at first about why the output
file was so small. Then I realized that it's because the many records
without a title were skipped, and there was no feedback about skipping
those records.

I changed the code so missing identifiers are always reported, even if
the error setting is "ignore". Missing identifiers will still stop
processing if the error setting is "strict".


chemfp's two cross-toolkit substructure fingerprints
====================================================

In this section you'll learn how to generate the two
substructure-based fingerprints which come as part of chemfp. These
are based on cross-toolkit SMARTS pattern definitions and can be used
with Open Babel, OpenEye, and RDKit. (For OpenEye users, these
fingerprints use the base OEChem library and not the separately licensed
OEGraphSim add-on.)

Chemfp implements two platform-independent fingerprints where were
originally designed for substructure filters but which are also used
for similarity searches. One is based on the 166-bit MACCS
implementation in RDKit and the other is derived from the 881-bit
PubChem/CACTVS substructure fingerprints.

The chemfp MACCS definition is called "rdmaccs" because it closely
derives from the MACCS SMARTS patterns used in RDKit. (These pattern
definitions are also used in Open Babel and the CDK, but are
completely independent from the OpenEye implementation.)

Here are example of the respective rdmaccs fingerprint for phenol
using each of the toolkits.

Open Babel::

    % echo "c1ccccc1O phenol" | ob2fps --in smi --rdmaccs 
    #FPS1
    #num_bits=166
    #type=RDMACCS-OpenBabel/2
    #software=OpenBabel/2.4.1 chemfp/1.3
    #date=2017-09-12T23:16:00
    00000000000000000000000000000140004480101e	phenol

OpenEye::

    % echo "c1ccccc1O phenol" | oe2fps --in smi --rdmaccs
    #FPS1
    #num_bits=166
    #type=RDMACCS-OpenEye/2
    #software=OEChem/2.1.3 (20170828) chemfp/1.3
    #date=2017-09-12T23:19:19
    00000000000000000000000000000140004480101e	phenol

RDKit::

    % echo "c1ccccc1O phenol" | rdkit2fps --in smi --rdmaccs
    #FPS1
    #num_bits=166
    #type=RDMACCS-RDKit/2
    #software=RDKit/2017.09.1 chemfp/1.3
    #date=2017-09-12T23:20:30
    00000000000000000000000000000140004480101e	phenol


For more complex molecules it's possible that different toolkits
produce different fingerprint rdmaccs, even though the toolkits use
the same SMARTS definitions. Each toolkit has a different
understanding of chemistry. The most notable is the different
definition of aromaticity, so the bit for "two or more aromatic rings"
will be toolkit dependent.


substruct fingerprints
----------------------

chemp also includes a "substruct" substructure fingerprint. This is an
881 bit fingerprint derived from the PubChem/CACTVS substructure
keys. They do not match the CACTVS fingerprints exactly, in part due
to differences in ring perception. Some of the substruct bits will
always be 0. With that caution in mind, if you want to try them out,
use the :option:`--substruct` option.

The term "substruct" is a horribly generic name, but I couldn't think
of a better one. Until chemfp 3.0 I said these fingerprints were
"experimental", in that I hadn't fully validated them against
PubChem/CACTVS and could not tell you the error rate. I still haven't
done that.

What's changed is that I've found out over the years that people are
using the substruct fingerprints, even without full validatation. That
surprised me, but use is its own form of validation. I still would
like to validate the fingerprints, but it's slow, tedious work which I
am not really interested in doing. Nor does it earn me any
money. Plus, if the validation does lead to any changes, it's easy to
simply change the version number.

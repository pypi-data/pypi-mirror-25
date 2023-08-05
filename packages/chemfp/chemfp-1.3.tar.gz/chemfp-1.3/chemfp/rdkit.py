"Create RDKit fingerprints"

# Copyright (c) 2010-2017 Andrew Dalke Scientific, AB
# See the contents of "__init__.py" for full license details.

from __future__ import absolute_import, print_function

import os
import sys
import gzip

import rdkit
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors
import rdkit.rdBase
from rdkit.Chem.MACCSkeys import GenMACCSKeys

try:
    from rdkit.Avalon import pyAvalonTools
    HAS_AVALON = True
except ImportError:
    pyAvalonTools = None
    HAS_AVALON = False

from . import sdf_reader
from .encodings import from_binary_lsb as _from_binary_lsb
from . import io
from . import types

# These are the things I consider to be public
__all__ = ["read_structures", "iter_smiles_molecules", "iter_sdf_molecules"]


# If the attribute doesn't exist then this is an unsupported pre-2010 RDKit distribution
SOFTWARE = "RDKit/" + getattr(rdkit.rdBase, "rdkitVersion", "unknown")

EXTERNAL_NAME = "RDKit"

# Used to check for version-dependent fingerprints
_VERSION_PROBE_MOL = Chem.MolFromSmiles(r"CC1=CC(=NN1CC(=O)NNC(=O)\C=C\C2=C(C=CC=C2Cl)F)C")

#########

# Helper function to convert a fingerprint to a sequence of bytes.

from rdkit import DataStructs
if getattr(DataStructs, "BitVectToBinaryText", None):
    _fp_to_bytes = DataStructs.BitVectToBinaryText
else:
    # Support for pre-2012 releases of RDKit
    def _fp_to_bytes(fp):
        return _from_binary_lsb(fp.ToBitString())[1]

#########
_allowed_formats = ["sdf", "smi"]
_format_extensions = {
    "sdf": "sdf",
    "mol": "sdf",
    "sd": "sdf",
    "mdl": "sdf",

    "smi": "smi",
    "can": "smi",
    "smiles": "smi",
    "ism": "smi",  # This does not exist in 2.0 or later
    "usm": "smi",  # Added in 2.0. Following OEChem's lead.
}


# While RDKit has a SMILES file parser, it doesn't handle reading from
# stdin or from compressed files. I wanted to support those as well, so
# ended up not using Chem.SmilesMolSupplier.

def iter_smiles_molecules(fileobj, close, errors="strict", location=None):
    """Iterate over the SMILES file records, returning (title, RDKit.Chem.Mol) pairs

    Each line of the input must at least one whitespace separated
    fields.  The first field is the SMILES. If there is a second field
    then it is used as the title, otherwise the title is the current
    record number, starting with "1".

    """
    name = getattr(fileobj, "name", None)
    error_handler = io.get_parse_error_handler(errors)
    if location is None:
        location = io.Location.from_source(name)

    
    it = _iter_smiles_molecules(fileobj, close, error_handler, location)
    next(it)
    return it

def _iter_smiles_molecules(fileobj, close, error_handler, location):
    recno = lineno = start_offset = end_offset = 0
    line = None
    mol = None
    def get_lineno():
        return lineno
    def get_offsets():
        return start_offset, end_offset
    def get_record():
        return line
    def get_mol():
        return mol
    location.register(get_lineno = get_lineno,
                      get_recno = get_lineno,
                      get_offsets = get_offsets,
                      get_mol = get_mol,
        )
    yield "Ready!"
    try:
        for lineno, line in enumerate(fileobj, 1):
            start_offset = end_offset
            end_offset += len(line)
            
            words = line.split()
            if len(words) < 2:
                if not words:
                    mol = None
                    error_handler.error("Unexpected blank line", location)
                    continue
                id = None
            else:
                id = words[1]

            mol = Chem.MolFromSmiles(words[0])
            if mol is None:
                error_handler.error("Cannot parse the SMILES %r" % (words[0],), location)
                continue

            yield id, mol
    finally:
        if close is not None:
            close()
        location.save(lineno = get_lineno(),
                      recno = get_lineno(),
                      offsets = None,
                      record = None,
                      mol = None,
            )
    
        
def iter_sdf_molecules(fileobj, close, id_tag, errors="strict", location=None):
    """Iterate over the SD file records, returning (id, Chem.Mol) pairs

    """
    # If there's no explicit filename, see if fileobj has one
    name = getattr(fileobj, "name", None)
    error_handler = io.get_parse_error_handler(errors)
    if location is None:
        location = io.Location.from_source(name)

    return _iter_sdf_molecules(fileobj, close, id_tag, error_handler, location)

def _iter_sdf_molecules(fileobj, close, id_tag, error_handler, location):
    mol = None
    def get_mol():
        return mol
    location.register(get_mol=get_mol)
    try:
        if id_tag is None:
            for i, text in enumerate(sdf_reader.iter_sdf_records(fileobj, close, error_handler, location)):
                mol = Chem.MolFromMolBlock(text)
                if mol is None:
                    # This was not a molecule?
                    error_handler.error("Could not parse molecule block", location)
                    continue
                title = mol.GetProp("_Name")
                id = title
                ## id = io.cleanup_ids(title)
                ## if not id:
                ##     error_handler.error("Missing title", location)
                ##     continue
                yield id, mol
        else:
            # According to
            #   http://www.mail-archive.com/rdkit-discuss@lists.sourceforge.net/msg01436.html
            # I can make a new SDMolSupplier, then SetData(), get the first record, and
            # get its property names. That's ... crazy.
            sdf_iter = sdf_reader.iter_sdf_records(fileobj, close, error_handler, location)
            for i, (id, text) in enumerate(sdf_reader.iter_tag_and_record(sdf_iter, id_tag)):
                mol = Chem.MolFromMolBlock(text)
                if mol is None:
                    # This was not a molecule?
                    error_handler.error("Could not parse molecule block", location)
                    continue
                ## if id is None:
                ##     error_handler.error("Missing id tag %r" % (id_tag,), location)
                ##     continue
                ## id = io.remove_special_characters_from_id(id)
                ## if not id:
                ##     error_handler.error("Empty id tag %r" % (id_tag,), location)
                ##     continue
                yield id, mol
    finally:
        location.save(mol=None)
        
            
# this class helps the case when someone is entering structure
# by-hand. (Most likely to occur with SMILES input). They would like
# to see the result as soon as a record is entered. But normal
# interation reader grabs a buffer of input to process, and not a
# line. It's faster that way. The following adapter supports the
# iterator protocol but turns it into simple readlines(). This will be
# slower but since do it only if stdin is a tty, there shouldn't be a
# problem.
## class _IterUsingReadline(object):
##     "Internal class for iterating a line at a time from tty input"
##     def __init__(self, fileobj):
##         self.fileobj = fileobj
##     def __iter__(self):
##         return iter(self.fileobj.readline, "")

## def _open(filename, compressed):
##     "Internal function to open the given filename, which might be compressed"
##     if filename is None:
##         if compressed:
##             return gzip.GzipFile(fileobj=sys.stdin, mode="r")
##         else:
##             # Python's iter reads a block.
##             # When someone types interactively, read only a line.
##             if sys.stdin.isatty():
##                 return _IterUsingReadline(sys.stdin)
##             else:
##                 return sys.stdin

##     if compressed:
##         return gzip.GzipFile(filename, "r")
##     return open(filename, "rU")

def is_valid_format(format):
    if format is None:
        return True
    try:
        format_name, compression = io.normalize_input_format(None, format, ("smi", None))
    except ValueError:
        return False
    format_name = _format_extensions.get(format_name, format_name)
    return format_name in ("sdf", "smi")
    

def read_structures(source, format=None, id_tag=None, reader_args=None, errors="strict", location=None):
    """Iterate the records in the input source as (title, RDKit.Chem.Mol) pairs

    'source' is a filename, a file object, or None for stdin
    'format' is either "sdf" or "smi" with optional ".gz" or ".bz2" extensions.
        If None then the format is inferred from the source extension
    'errors' is one of "strict" (default), "log", or "ignore" (other values are experimental)
    """
    format_name, compression = io.normalize_input_format(source, format, default=("smi", None))
    format_name = _format_extensions.get(format_name, format_name)
    if location is None:
        location = io.Location.from_source(source)
    location.save(record_format=format_name)
    
    error_handler = io.get_parse_error_handler(errors)
    if format_name == "sdf":
        # When chemfp-1.1 came out, it was faster for chemfp to parse the
        # records and have RDKit parse each record than to have RDKit handle
        # it. Here are the numbers:
        # """
        # I have an old PubChem file Compound_09425001_09450000.sdf .
        #   num. lines = 5,041,475   num. bytes = 159,404,037
        # 
        # Parse times for iter_sdf_records (parsing records in Python)
        #   37.6s (best of 37.6, 38.3, 37.8)
        # Parse times for the RDKit implementation (parsing records in C++)
        #   40.2s (best of 41.7, 41.33, 40.2)
        # 
        # The native RDKit reader is slower than the Python one and does
        # not have (that I can tell) support for compressed files, so
        # I'll go with the Python one. For those interested, here's the
        # RDKit version.
        # """
        
        # I re-ran a similar test for the chemfp-1.3 release. The
        # timing numbers are now about the same. The tradeoff now is
        # the improved error reporting in chemfp vs. the more accurate
        # parsing in RDKit. Since no one has complained, I'll stick
        # with using chemfp to identify the records.
        
        ## if (not compression) and (source is not None):
        ##     supplier = Chem.SDMolSupplier(source)
        ##     def native_sdf_reader():
        ##         for mol in supplier:
        ##             if mol is None:
        ##                 print >>sys.stderr, "Missing? after", title
        ##             else:
        ##                 title = mol.GetProp("_Name")
        ##                 yield title, mol
        ##     return native_sdf_reader()

        fileobj, close = io.open_compressed_input(source, compression, EXTERNAL_NAME)
        # fileobj should always have the .name attribute set.
        return iter_sdf_molecules(fileobj, close, id_tag=id_tag,
                                  errors=error_handler, location=location)

    elif format_name == "smi":
        # I timed the native reader at 31.6 seconds (best of 31.6, 31.7, 31.7)
        # and the Python reader at 30.8 seconds (best of 30.8, 30.9, and 31.0)
        # Yes, the Python reader is faster and using it gives me better consistency
        #
        #if (not compressed) and (source is not None):
        #    supplier = Chem.SmilesMolSupplier(source, delimiter=" \t", titleLine=False)
        #    def native_smiles_reader():
        #        for mol in supplier:
        #            yield mol.GetProp("_Name"), mol
        #    return native_smiles_reader()
        fileobj, close = io.open_compressed_input(source, compression, EXTERNAL_NAME)
        return iter_smiles_molecules(fileobj, close,
                                     errors=error_handler, location=location)

    else:
        raise ValueError("%s does not support the %r format"
                         % (EXTERNAL_NAME, format_name))
        

########### The topological fingerprinter

# Some constants shared by the fingerprinter and the command-line code.

NUM_BITS = 2048
MIN_PATH = 1
MAX_PATH = 7
BITS_PER_HASH = 2
USE_HS = 1
assert USE_HS == 1, "Don't make this 0 unless you know what you are doing"

# Not supporting the tgtDensity and minSize options.
# This program generates fixed-length fingerprints.

def make_rdk_fingerprinter(minPath=MIN_PATH, maxPath=MAX_PATH, fpSize=NUM_BITS,
                           nBitsPerHash=BITS_PER_HASH, useHs=USE_HS):
    if not (fpSize > 0):
        raise ValueError("fpSize must be positive")
    if not (minPath > 0):
        raise ValueError("minPath must be positive")
    if not (maxPath >= minPath):
        raise ValueError("maxPath must not be smaller than minPath")
    if not (nBitsPerHash > 0):
        raise ValueError("nBitsPerHash must be positive")

    def rdk_fingerprinter(mol):
        fp = Chem.RDKFingerprint(
            mol, minPath=minPath, maxPath=maxPath, fpSize=fpSize,
            nBitsPerHash=nBitsPerHash, useHs=useHs)
        return _fp_to_bytes(fp)
    return rdk_fingerprinter

########### The MACCS fingerprinter


def maccs166_fingerprinter(mol):
    fp = GenMACCSKeys(mol)
    # In RDKit the first bit is always bit 1 .. bit 0 is empty (?!?!)
    bitstring_with_167_bits = fp.ToBitString()
    # I want the bits to start at 0, so I do a manual left shift
    return _from_binary_lsb(bitstring_with_167_bits[1:])[1]

def make_maccs166_fingerprinter():
    return maccs166_fingerprinter


########### The Morgan fingerprinter

# Some constants shared by the fingerprinter and the command-line code.

RADIUS = 2
USE_FEATURES = 0
USE_CHIRALITY = 0
USE_BOND_TYPES = 1

def make_morgan_fingerprinter(fpSize=NUM_BITS,
                              radius=RADIUS,
                              useFeatures=USE_FEATURES,
                              useChirality=USE_CHIRALITY,
                              useBondTypes=USE_BOND_TYPES):
    if not (fpSize > 0):
        raise ValueError("fpSize must be positive")
    if not (radius >= 0):
        raise ValueError("radius must be positive or zero")

    def morgan_fingerprinter(mol):
        fp = rdMolDescriptors.GetMorganFingerprintAsBitVect(
            mol, radius, nBits=fpSize, useChirality=useChirality,
            useBondTypes=useBondTypes,useFeatures=useFeatures)
        return _fp_to_bytes(fp)
    return morgan_fingerprinter


########### Torsion fingerprinter

TARGET_SIZE = 4

def make_torsion_fingerprinter(fpSize=NUM_BITS,
                               targetSize=TARGET_SIZE):
    if not (fpSize > 0):
        raise ValueError("fpSize must be positive")
    if not (targetSize >= 0):
        raise ValueError("targetSize must be positive or zero")

    def torsion_fingerprinter(mol):
        fp = rdMolDescriptors.GetHashedTopologicalTorsionFingerprintAsBitVect(
            mol, nBits=fpSize, targetSize=targetSize)
        return _fp_to_bytes(fp)
    return torsion_fingerprinter

TORSION_VERSION = {
    "\xc2\x10@\x83\x010\x18\xa4,\x00\x80B\xc0\x00\x08\x00": "1",
    "\x13\x11\x103\x00\x007\x00\x00p\x01\x111\x0107": "2",
    }[make_torsion_fingerprinter(128)(_VERSION_PROBE_MOL)]

########### Atom Pair fingerprinter

MIN_LENGTH = 1
MAX_LENGTH = 30

def make_atom_pair_fingerprinter(fpSize=NUM_BITS,
                                 minLength=MIN_LENGTH,
                                 maxLength=MAX_LENGTH):
    if not (fpSize > 0):
        raise ValueError("fpSize must be positive")
    if not (minLength >= 0):
        raise ValueError("minLength must be positive or zero")
    if not (maxLength >= minLength):
        raise ValueError("maxLength must not be less than minLength")

    def pair_fingerprinter(mol):
        fp = rdMolDescriptors.GetHashedAtomPairFingerprintAsBitVect(
            mol, nBits=fpSize, minLength=minLength, maxLength=maxLength)
        return _fp_to_bytes(fp)
    return pair_fingerprinter

try:
    ATOM_PAIR_VERSION = {
        "\xfdB\xfe\xbd\xfa\xdd\xff\xf5\xff\x05\xdf?\xe3\xc3\xff\xfb": "1",
        "w\xf7\xff\xf7\xff\x17\x01\x7f\x7f\xff\xff\x7f\xff?\xff\xff": "2",
        }[make_atom_pair_fingerprinter(128)(_VERSION_PROBE_MOL)]
except Exception, err:
    # RDKit 2011.06 contained a bug
    if "Boost.Python.ArgumentError" in str(type(err)):
        ATOM_PAIR_VERSION = None
    else:
        raise


####################

from .types import FingerprintFamilyConfig, positive_int, nonnegative_int, zero_or_one

def _read_structures(metadata, source, format, id_tag, reader_args, errors, location):
    if metadata.aromaticity is not None:
        raise ValueError("RDKit does not support alternate aromaticity models "
                         "(want aromaticity=%r)" % metadata.aromaticity)
    return read_structures(source, format, id_tag, reader_args, errors, location)

# This configuration system is complicated because the design expected
# that all parameters will have the same defaults. Unfortunately,
# Avalon uses an fpSize default of 512 while the other fingerprints
# with an fpSize use 2048. Thus, I have a _base_fpsize used for the
# command-line args, which is able to figure out the correct default;
# a _base_avalon used for Avalon fingerprints; and _base_2048 used for
# everything else.

# This has been improved in chemfp 2.0.


_base = FingerprintFamilyConfig(
    software = SOFTWARE,
    read_structures = _read_structures,
    )

# Only used for the command-line "--fpSize" option.
_base_fpsize = _base.clone()
_base_fpsize.add_argument(
    "fpSize", decoder=positive_int, metavar="INT", default=None, help=
        "number of bits in the fingerprint. Default of 2048 for RDK, Morgan, "
        "topological torsion, atom pair, and pattern fingerprints, and "
        "512 for Avalon fingerprints")

# Only used by Avalon
_base_avalon = _base.clone()
_base_avalon.add_argument(
    "fpSize", decoder=positive_int, metavar="INT", default=512, help=
        "number of bits in the fingerprint. Default of 2048 for RDK, Morgan, "
        "topological torsion, atom pair, and pattern fingerprints, and "
        "512 for Avalon fingerprints")

# Used by everything except Avalon
_base_2048 = _base.clone()
_base_2048.add_argument(
    "fpSize", decoder=positive_int, metavar="INT", default=2048, help=
        "number of bits in the fingerprint. Default of 2048 for RDK, Morgan, "
        "topological torsion, atom pair, and pattern fingerprints, and "
        "512 for Avalon fingerprints")


_base_2048.add_argument("minPath", decoder=positive_int, metavar="INT", default=MIN_PATH,
                   help = "minimum number of bonds to include in the subgraph")

_base_2048.add_argument("maxPath", decoder=positive_int, metavar="INT", default=MAX_PATH,
                   help = "maximum number of bonds to include in the subgraph")

_base_2048.add_argument("nBitsPerHash", decoder=positive_int, metavar="INT",
                   default=BITS_PER_HASH, help = "number of bits to set per path")

_base_2048.add_argument("useHs", decoder=zero_or_one, metavar="0|1", default=USE_HS,
                   help = "include information about the number of hydrogens on each atom")
# Morgan
_base_2048.add_argument("radius", decoder=nonnegative_int, metavar="INT", default=RADIUS,
                   help = "radius for the Morgan algorithm")

_base_2048.add_argument("useFeatures", decoder=zero_or_one, metavar="0|1",
                   default=USE_FEATURES, help = "use chemical-feature invariants")

_base_2048.add_argument("useChirality", decoder=zero_or_one, metavar="0|1",
                   default=USE_CHIRALITY, help = "include chirality information")

_base_2048.add_argument("useBondTypes", decoder=zero_or_one, metavar="0|1",
                   default=USE_BOND_TYPES, help = "include bond type information")


# torsion
_base_2048.add_argument("targetSize", decoder=positive_int, metavar="INT",
                   default=TARGET_SIZE, help = "number of bits in the fingerprint")

# pair
_base_2048.add_argument("minLength", decoder=nonnegative_int, metavar="INT",
                   default=MIN_LENGTH, help = "minimum bond count for a pair")

_base_2048.add_argument("maxLength", decoder=nonnegative_int, metavar="INT",
                   default=MAX_LENGTH, help = "maximum bond count for a pair")

# Avalon
IS_QUERY = 0
BIT_FLAGS = 15761407
_base_avalon.add_argument("isQuery", decoder=zero_or_one, metavar="0|1", default=IS_QUERY,
                   help="is the fingerprint for a query structure? (1 if yes, 0 if no)")

_base_avalon.add_argument("bitFlags", decoder=positive_int, metavar="INT", default=BIT_FLAGS,
                   help="bit flags, SSSBits are 32767 and similarity bits are 15761407")

#########

_MACCS_PROBE_MOL = Chem.MolFromSmiles("[He]")
_has_key_44 = GenMACCSKeys(_MACCS_PROBE_MOL)[44] != 0
MACCS_VERSION = {False: "1", True: "2"}[_has_key_44]

def _check_maccs_version(version):
    def make_fingerprinter(*args, **kwargs):
        if MACCS_VERSION != version:
            raise TypeError("This version of RDKit does not support the RDKit-MACCS/%s fingerprint" % (version,))
        return make_maccs166_fingerprinter(*args, **kwargs)
    return make_fingerprinter
            

RDKitMACCSFingerprintFamily_v1 = _base_2048.clone(
    name = "RDKit-MACCS166/1",
    num_bits = 166,
    make_fingerprinter = _check_maccs_version("1"),
    )
RDKitMACCSFingerprintFamily_v2 = _base_2048.clone(
    name = "RDKit-MACCS166/2",
    num_bits = 166,
    make_fingerprinter = _check_maccs_version("2"),
    )


# The number of bits depends on the parameters
def _get_num_bits(d):
    return d["fpSize"]

# Figure out the RDKit version
RDK_VERSION = {
    b"~\x89\x90\x04\xdb\xe9t\xc5\x87\xfe\xfc\xbf\xf8r\x01\xd6\xe9\xd7\xbbZv\xfeM\xc9\xfb\xf7{\xb7\xbd\xacl\xc9\xff\xb6s\xd5\x84\xf2\x8e\xdb\xcf\xcc\xb7\x02\xfa-\xa6\xee2\x1c\x19\x11\xe8q;\x08\x96NTN\xb2\xd7\x99\xa9\xca\xe7\xc3\x0c\x9bqP!\xd5\xe6\xf5\xff\x92\xf6\xed\xfa\xc4\xb4x\xf5\xd6\xde~\xfb\xcdp\xefv\xfb\xcd\xbb\x7f\xb9\xda\xf8?\xad\xd9\xf6\xe4\x94\xc3\xfb\xbf\xefv9\xff\xfe\x9bd\xf3\x15\x9d\x9bm\xeb\x0f\xaa$\xf5\x01\xef\xb7": "1",
    b"""\xcd\xd7\xb9\xc7\xd8\xa7\x18\n\xff\x90R\xc2\xfbS\xf5\xba\xd1\xf5\xf6F\x0f\x8d\xf1\x07\xbf\t_\x995`\xcaH\xf1>\x045q\'5\xce>\x8f\xf5\x18L\xb6\xae\xca\xde\xd5\xbd\xcd\xff/K"m\xdc\xec\xd3\x02\xb9\xf5\xc0\xb6_\xe2nv\xe36\xf5\xd5j\x1f\x90\xc6\xd1/\xb3]"=[\xbd\xb0F\xb9\xcfd\x96[e\xf7x\xafQ\xc7\xfa\xb3\xbf\xf3\xdfb\xb7]\xd7\xfe\xb7\xd6\xfd\x1f{\xd7\xbd\xf1\'P\xfaU\x89l^f\xde\xb5}\xaf""": "2",
}[make_rdk_fingerprinter(fpSize=1024)(_VERSION_PROBE_MOL)]


def _check_rdkit_fingerprint_version(version):
    def make_fingerprinter(*args, **kwargs):
        if RDK_VERSION != version:
            raise TypeError("This version of RDKit does not support the RDKit-Fingerprint/%s fingerprint" % (version,))
        return make_rdk_fingerprinter(*args, **kwargs)
    return make_fingerprinter

RDKitFingerprintFamily_v1 = _base_2048.clone(
    name = "RDKit-Fingerprint/1",
    format_string = ("minPath=%(minPath)s maxPath=%(maxPath)s fpSize=%(fpSize)s "
                     "nBitsPerHash=%(nBitsPerHash)s useHs=%(useHs)s"),
    num_bits = _get_num_bits,
    make_fingerprinter = _check_rdkit_fingerprint_version("1"),
    )

RDKitFingerprintFamily_v2 = _base_2048.clone(
    name = "RDKit-Fingerprint/2",
    format_string = ("minPath=%(minPath)s maxPath=%(maxPath)s fpSize=%(fpSize)s "
                     "nBitsPerHash=%(nBitsPerHash)s useHs=%(useHs)s"),
    num_bits = _get_num_bits,
    make_fingerprinter = _check_rdkit_fingerprint_version("2"),
    )

###

RDKitMorganFingerprintFamily_v1 = _base_2048.clone(
    name = "RDKit-Morgan/1",
    format_string = (
             "radius=%(radius)d fpSize=%(fpSize)s useFeatures=%(useFeatures)d "
             "useChirality=%(useChirality)d useBondTypes=%(useBondTypes)d"),
    num_bits = _get_num_bits,
    make_fingerprinter = make_morgan_fingerprinter,
    )

###

def _check_torsion_version(version):
    def make_fingerprinter(*args, **kwargs):
        if TORSION_VERSION != version:
            raise TypeError("This version of RDKit does not support the RDKit-Torsion/%s fingerprint" % (version,))
        return make_torsion_fingerprinter(*args, **kwargs)
    return make_fingerprinter

RDKitTorsionFingerprintFamily_v1 = _base_2048.clone(
    name = "RDKit-Torsion/1",
    format_string = "fpSize=%(fpSize)s targetSize=%(targetSize)d",
    num_bits = _get_num_bits,
    make_fingerprinter = _check_torsion_version("1"),
    )

RDKitTorsionFingerprintFamily_v2 = _base_2048.clone(
    name = "RDKit-Torsion/2",
    format_string = "fpSize=%(fpSize)s targetSize=%(targetSize)d",
    num_bits = _get_num_bits,
    make_fingerprinter = _check_torsion_version("2"),
    )

###

def _check_atom_pair_version(version):
    def make_fingerprinter(*args, **kwargs):
        if ATOM_PAIR_VERSION != version:
            raise TypeError("This version of RDKit does not support the RDKit-AtomPair/%s fingerprint" % (version,))
        return make_atom_pair_fingerprinter(*args, **kwargs)
    return make_fingerprinter

RDKitAtomPairFingerprintFamily_v1 = _base_2048.clone(
    name = "RDKit-AtomPair/1",
    format_string = "fpSize=%(fpSize)s minLength=%(minLength)d maxLength=%(maxLength)d",
    num_bits = _get_num_bits,
    make_fingerprinter = _check_atom_pair_version("1"),
    )

RDKitAtomPairFingerprintFamily_v2 = _base_2048.clone(
    name = "RDKit-AtomPair/2",
    format_string = "fpSize=%(fpSize)s minLength=%(minLength)d maxLength=%(maxLength)d",
    num_bits = _get_num_bits,
    make_fingerprinter = _check_atom_pair_version("2"),
    )

########### Pattern fingerprinter

# PatternFingerprint((Mol) mol, (int) fpSize=2048, (list) atomCounts=[], (ExplicitBitVect) setOnlyBits=None)
# "NOTE: This function is experimental. The API or results may change from release to release."

def make_pattern_fingerprinter(fpSize=NUM_BITS):
    if not (fpSize > 0):
        raise ValueError("fpSize must be positive")
    def pattern_fingerprinter(mol):
        fp = Chem.PatternFingerprint(mol, fpSize=fpSize)
        return DataStructs.BitVectToBinaryText(fp)
    return pattern_fingerprinter

def _check_pattern_version():
    _pattern = make_pattern_fingerprinter(fpSize=256)(_VERSION_PROBE_MOL)
    if _pattern == b'\xfb\xce\xfe\xfd\xf8\xdb{l\x97\xfb\xfa\xf3\xfb\xff\xf4Y\xfc\x7f\xb9m\xff\xf7\xff\xff\xfe\x1fw\xef\xd3\xcfRy':
        return "1"

    _pattern2 = make_pattern_fingerprinter(fpSize=256)(Chem.MolFromSmiles("O"))
    
    if _pattern == b'{\xde\xfe\xfd\xfa\xdbsl\x97i\xfa\xb2\xfb\xff\xf49\xfd\x7f\xb9m\xff\xf3\xff\xff\xfe\x7fwo\xd3\x8f\xd2y':
        # The probe molecule isn't able to distinguish between v2 and v3
        if _pattern2 == b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00":
            return "2"
        if _pattern2 == b"\x00\x02\x00\x00 \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00":
            return "3"

    if _pattern == b'{\xdf\xfe\xfd\xfa\xdfs|\x97i\xfa\xb2\xfb\xff\xf49\xfd\x7f\xb9o\xff\xf3\xff\xff\xfe\x7fwo\xdb\x8f\xd2y':
        # Might as well double-check _pattern2
        if _pattern2 == b"\x00\x02\x00\x00 \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00":
            return "4"

    return "unknown"
    

if hasattr(Chem, "PatternFingerprint"):
    PATTERN_VERSION = _check_pattern_version()
else:
    PATTERN_VERSION = "unknown"


def _check_pattern_fingerprint(version):
    def make_fingerprinter(*args, **kwargs):
        if PATTERN_VERSION != version:
            raise TypeError("This version of RDKit does not support the RDKit-Pattern/%s fingerprint" % (version,))
        return make_pattern_fingerprinter(*args, **kwargs)
    return make_fingerprinter

RDKitPatternFingerprint_v1 = _base_2048.clone(
    name = "RDKit-Pattern/1",
    format_string = "fpSize=%(fpSize)s",
    num_bits = _get_num_bits,
    make_fingerprinter = _check_pattern_fingerprint("1")
    )
    
RDKitPatternFingerprint_v2 = _base_2048.clone(
    name = "RDKit-Pattern/2",
    format_string = "fpSize=%(fpSize)s",
    num_bits = _get_num_bits,
    make_fingerprinter = _check_pattern_fingerprint("2")
    )

# Added in RDKit version 2017.03.1.
RDKitPatternFingerprint_v3 = _base_2048.clone(
    name = "RDKit-Pattern/3",
    format_string = "fpSize=%(fpSize)s",
    num_bits = _get_num_bits,
    make_fingerprinter = _check_pattern_fingerprint("3")
    )

# Added in RDKit version 2017.09.1.
RDKitPatternFingerprint_v4 = _base_2048.clone(
    name = "RDKit-Pattern/4",
    format_string = "fpSize=%(fpSize)s",
    num_bits = _get_num_bits,
    make_fingerprinter = _check_pattern_fingerprint("4")
    )


########### Avalon fingerprinter

# GetAvalonFP( (object)mol [, (int)nBits=512 [, (bool)isQuery=False [, (bool)resetVect=False [, (int)bitFlags=15761407]]]])

# I don't know what the bitFlags do.
# avalonSSSBits        =    32767 = 0x007fff
# avalonSimilarityBits = 15761407 = 0xf07fff

AVALON_NBITS = 512

if HAS_AVALON:
    AVALON_VERSION = "1"
else:
    AVALON_VERSION = None

def make_avalon_fingerprinter(fpSize=AVALON_NBITS, isQuery=IS_QUERY, bitFlags=BIT_FLAGS):
    if not (fpSize > 0):
        raise ValueError("fpSize must be positive")
    isQuery = 1 if isQuery else 0
    def avalon_fingerprinter(mol):
        fp = pyAvalonTools.GetAvalonFP(mol, nBits=fpSize, isQuery=isQuery, bitFlags=bitFlags)
        return DataStructs.BitVectToBinaryText(fp)
    return avalon_fingerprinter

def _check_avalon_fingerprinter(version):
    def make_fingerprinter(*args, **kwargs):
        if not HAS_AVALON:
            raise TypeError("This version of RDKit is not compiled for Avalon support")
        if AVALON_VERSION != version:
            raise TypeError("This version of RDKit does not support the RDKit-Avalon/%s fingerprint" % (version,))
        return make_avalon_fingerprinter(*args, **kwargs)
    return make_fingerprinter

RDKitAvalonFingerprint_v1 = _base_avalon.clone(
    name = "RDKit-Avalon/1",
    format_string = "fpSize=%(fpSize)d isQuery=%(isQuery)s bitFlags=%(bitFlags)s",
    num_bits = _get_num_bits,
    make_fingerprinter = _check_avalon_fingerprinter("1"),
    )


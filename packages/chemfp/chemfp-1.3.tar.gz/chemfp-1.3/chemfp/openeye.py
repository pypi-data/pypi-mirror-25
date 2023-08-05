"""Create OpenEye fingerprints


"""

# Copyright (c) 2010-2017 Andrew Dalke Scientific, AB (Sweden)
# See the contents of "chemfp/__init__.py" for full license details.

from __future__ import absolute_import

import sys
import os
import errno
import ctypes
import warnings

from openeye.oechem import *
from openeye.oegraphsim import *

from . import ParseError
from . import types
from . import io
from . import argparse

__all__ = ["read_structures", "get_path_fingerprinter", "get_maccs_fingerprinter"]


class UnknownFormat(KeyError):
    def __str__(self):
        return "Unknown format %r" % (self.args[0],)

############# Used when generate the FPS header

SOFTWARE = "OEGraphSim/%(release)s (%(version)s)" % dict(
    # There can be spaces in the beta releases
    release = OEGraphSimGetRelease().replace(" ", "_"),
    version = OEGraphSimGetVersion())


_is_licensed = OEGraphSimIsLicensed()

def is_licensed():
    return _is_licensed

def _get_num_bits(d):
    return d["numbits"]
    
##### Handle the atom and bond type flags for path fingerprints

# The atom and bond type flags can be specified on the command-line
# 
#   --atype=DefaultAtom --btype=BondOrder,InRing
#   --atype AtomicNumber,InRing  --btype DefaultBond,InRing
#
# The type fields may be separated by either a "," or a "|".
# The relevant OpenEye function (OEGetFPAtomType() and
# OEGetFPBondType()) use a "|" but that requires escaping for
# the shell, so I support "," as well.

# There's another conversion of the integer type values into a string
# representation, used when generating the canonical form of the
# generation parameters for the FPS output. That case uses "|"
# (and not ",") and omits the DefaultAtom and DefaultBond name.
# The result is easier to parse with the OpenEye API functions.


# Note: Version 1.0 of OEGraphSim uses different names than 2.0 (Grr!)
# OpenEye says these names will not change again. We'll see.

_atype_flags = [(OEGetFPAtomType(atype), atype) for atype in ( 
                    OEFPAtomType_Aromaticity,   # Arom
                    OEFPAtomType_AtomicNumber,  # AtmNum
                    OEFPAtomType_Chiral,        # Chiral
                    OEFPAtomType_EqHalogen,     # EqHalo
                    OEFPAtomType_FormalCharge,  # FCharge
                    OEFPAtomType_HvyDegree,     # HvyDeg
                    OEFPAtomType_Hybridization, # Hyb
                    OEFPAtomType_InRing,        # InRing
                    OEFPAtomType_EqAromatic,    # EqArom
                    OEFPAtomType_HCount,           # HCount
                    OEFPAtomType_EqHBondAcceptor,  # EqHBAcc
                    OEFPAtomType_EqHBondDonor,     # EqHBDon
                    )]
    
_btype_flags = [(OEGetFPBondType(btype), btype) for btype in
                (OEFPBondType_BondOrder,
                OEFPBondType_Chiral,
                 OEFPBondType_InRing)]

# I support the DefaultAtom and DefaultBond special values.
# (Note: complex bitflags go first; it simplifies the flag->description code)

_atype_default_flags = [("DefaultPathAtom", OEFPAtomType_DefaultPathAtom),
                        ("DefaultCircularAtom", OEFPAtomType_DefaultCircularAtom),
                        ("DefaultTreeAtom", OEFPAtomType_DefaultTreeAtom),
                        ("DefaultAtom", OEFPAtomType_DefaultAtom)]
_btype_default_flags = [("DefaultPathBond", OEFPBondType_DefaultPathBond),
                        ("DefaultCircularBond", OEFPBondType_DefaultCircularBond),
                        ("DefaultTreeBond", OEFPBondType_DefaultTreeBond),
                        ("DefaultBond", OEFPBondType_DefaultBond)]
    
_path_atype_flags = _atype_flags + _atype_default_flags + [("Default", OEFPAtomType_DefaultPathAtom)]
_path_btype_flags = _btype_flags + _btype_default_flags + [("Default", OEFPBondType_DefaultPathBond)]

_circular_atype_flags = _atype_flags + _atype_default_flags + [
    ("Default", OEFPAtomType_DefaultCircularAtom)]
_circular_btype_flags = _btype_flags + _btype_default_flags + [
    ("Default", OEFPBondType_DefaultCircularBond)]

_tree_atype_flags = _atype_flags + _atype_default_flags + [("Default", OEFPAtomType_DefaultTreeAtom)]
_tree_btype_flags = _btype_flags + _btype_default_flags + [("Default", OEFPBondType_DefaultTreeBond)]

_path_atypes = dict(_path_atype_flags)
_path_btypes = dict(_path_btype_flags)
_circular_atypes = dict(_circular_atype_flags)
_circular_btypes = dict(_circular_btype_flags)
_tree_atypes = dict(_tree_atype_flags)
_tree_btypes = dict(_tree_btype_flags)


## Go from a "," or "|" separated text field to an integer value
# Removes extra whitespace, but none should be present.

def _get_type_value(a_or_b, table, description):
    value = 0
    # Allow both "|" and "," as separators
    # (XXX OEGraphSim 2.0.0 only allows "|")
    description = description.replace("|", ",")
    for word in description.split(","):
        word = word.strip()
        try:
            value |= table[word]
        except KeyError:
            if not word:
                raise ValueError("Missing %s flag" % (a_or_b,))
            raise ValueError("Unknown %s type %r (expecting one of: %s)" % (
                a_or_b, word, ", ".join(sorted(table))))
    return value

def path_atom_description_to_value(description):
    """path_atom_description_to_value(description) -> integer

    Convert an atom description like FormalCharge,EqHalogen
    or FormalCharge|EqHalogen into its atom type value.

    This is similar to OEGetFPAtomType except both "|" and "," are
    allowed seperators and "AtomDefault" is an allowed term.
    """
    return _get_type_value("path atom", _path_atypes, description)

def path_bond_description_to_value(description):
    """bond_description_to_value(description) -> integer

    Convert an bond description like BondOrder,Chiral
    or BondOrder|Chiral into its bond type value.

    This is similar to OEGetFPBondType except both "|" and "," are
    allowed seperators and "BondDefault" is an allowed term.
    """
    return _get_type_value("path bond", _path_btypes, description)

def circular_atom_description_to_value(description):
    return _get_type_value("circular atom", _circular_atypes, description)
def circular_bond_description_to_value(description):
    return _get_type_value("circular bond", _circular_btypes, description)
def tree_atom_description_to_value(description):
    return _get_type_value("tree atom", _tree_atypes, description)
def tree_bond_description_to_value(description):
    return _get_type_value("tree bond", _tree_btypes, description)

## Go from an integer value into a canonical description

# I could use OEGetFPAtomType() and OEGetFPBondType() but I wanted
# something which has a fixed sort order even for future releases,
# which isn't part of those functions.

def _get_type_description(a_or_b, flags, value):
    words = []
    for (word, flag) in flags:
        if flag & value == flag:
            # After over 12 years of full-time use of Python,
            # I finally have a chance to use the xor operator.
            value = value ^ flag
            words.append(word)
    if value != 0:
        raise AssertionError("Unsupported %s value %d" % (a_or_b, value))
    return "|".join(words)


def path_atom_value_to_description(value):
    """atom_value_to_description(value) -> string

    Convert from an atom type string into its text description,
    separated by "|"s. The result are compatible with
    OEGetFPAtomType and are in canonical order.
    """
    return _get_type_description("path atom", _path_atype_flags, value)

def path_bond_value_to_description(value):
    """bond_value_to_description(value) -> string

    Convert from a bond type string into its text description,
    separated by "|"s. The result are compatible with
    OEGetFPBontType and are in canonical order.
    """
    return _get_type_description("path bond", _path_btype_flags, value)

def circular_atom_value_to_description(value):
    return _get_type_description("circular atom", _circular_atype_flags, value)
def circular_bond_value_to_description(value):
    return _get_type_description("circular bond", _circular_btype_flags, value)
def tree_atom_value_to_description(value):
    return _get_type_description("tree atom", _tree_atype_flags, value)
def tree_bond_value_to_description(value):
    return _get_type_description("tree bond", _tree_btype_flags, value)

    
##### Create a function which generate fingerprints

# I use functions which return functions because it was a nice way to
# hide the differences between the two fingerprinters. I also found
# that I can save a bit of time by not creating a new fingerprint each
# time. The measured speedup is about 2% for MACCS166 and 6% for path
# fingerprints.

# Just like the OEGraphMol, these fingerprints must not be reused or
# stored. They are mutated EVERY TIME. They are NOT thread-safe.
# If you need to use these in multiple threads, then make multiple
# fingerprinters.

# Believe it or not, reusing the preallocated fingerprint measurably
# helps the performance.

def get_path_fingerprinter(numbits, minbonds, maxbonds, atype, btype):
    # Extra level of error checking since I expect people will think
    # of this as part of the public API.
    if not (16 <= numbits <= 65536):
        raise ValueError("numbits must be between 16 and 65536 (inclusive)")
    if not (0 <= minbonds):
        raise ValueError("minbonds must be 0 or greater")
    if not (minbonds <= maxbonds):
        raise ValueError("maxbonds must not be smaller than minbonds")

    # XXX validate the atype and type values?
    # It's a simple mask against the | of all possible value, then test for 0.
    # However, I'm not sure what to report as the error message.
    
    fp = OEFingerPrint()
    fp.SetSize(numbits)
    data_location = int(fp.GetData())
    num_bytes = (numbits+7)//8

    def path_fingerprinter(mol):
        OEMakePathFP(fp, mol, numbits, minbonds, maxbonds, atype, btype)
        return ctypes.string_at(data_location, num_bytes)

    return path_fingerprinter

def get_maccs_fingerprinter():
    fp = OEFingerPrint()
    # Call SetSize() now to force space allocation, so I only need one GetData()
    fp.SetSize(166)
    data_location = int(fp.GetData())
    num_bytes = (166+7)//8
    
    def maccs_fingerprinter(mol):
        OEMakeMACCS166FP(fp, mol)
        return ctypes.string_at(data_location, num_bytes)

    return maccs_fingerprinter

def get_circular_fingerprinter(numbits, minradius, maxradius, atype, btype):
    # Extra level of error checking since I expect people will think
    # of this as part of the public API.
    if not (16 <= numbits <= 65536):
        raise ValueError("numbits must be between 16 and 65536 (inclusive)")
    if not (0 <= minradius):
        raise ValueError("minradius must be 0 or greater")
    if not (minradius <= maxradius):
        raise ValueError("maxradius must not be smaller than minradius")

    fp = OEFingerPrint()
    fp.SetSize(numbits)
    data_location = int(fp.GetData())
    num_bytes = (numbits+7)//8

    def circular_fingerprinter(mol):
        OEMakeCircularFP(fp, mol, numbits, minradius, maxradius, atype, btype)
        return ctypes.string_at(data_location, num_bytes)

    return circular_fingerprinter


def get_tree_fingerprinter(numbits, minbonds, maxbonds, atype, btype):
    # Extra level of error checking since I expect people will think
    # of this as part of the public API.
    if not (16 <= numbits <= 65536):
        raise ValueError("numbits must be between 16 and 65536 (inclusive)")
    if not (0 <= minbonds):
        raise ValueError("minbonds must be 0 or greater")
    if not (minbonds <= maxbonds):
        raise ValueError("maxbonds must not be smaller than minbonds")

    fp = OEFingerPrint()
    fp.SetSize(numbits)
    data_location = int(fp.GetData())
    num_bytes = (numbits+7)//8

    def tree_fingerprinter(mol):
        OEMakeTreeFP(fp, mol, numbits, minbonds, maxbonds, atype, btype)
        return ctypes.string_at(data_location, num_bytes)

    return tree_fingerprinter
        

### A note on fingerprints and ctypes.string_at

# The FPS format and OEFingerPrint.GetData() values used identical bit
# and byte order. Bytes are in little-endian order and bits are in
# big-endian order. That means I can use GetData() to get the
# underlying C storage area, use ctypes to turn that into a Python
# string, which I then hex encode.

# The other option is to use OEFingerPrint.ToHexString(). But that's
# pure little endian, so I would need a transposition to make the bits
# be what I want them to be. OEChem's hex strings also end with a flag
# which says how many extra bits to trim, which I don't need since I
# handle it a different way.

# Here's some info about the bit order, which I tested by setting a
# few bits though the API then seeing what changed in the hex string
# and in the underlying GetData() field.

# The bit pattern
#   01234567 89ABCDEF  pure little endian
#   10011100 01000011
#   
#         93 2C    using ToHexString()  (pure little endian)
#       0x39 c2    using hex(ord(GetData())) (litle endian byte, big endian bit)
#
#   76543210 FEDCBA98
#   00111001 11000010   little endian byte, big endian bit


################ Handle formats

# Make format names to OEChem format types
_formats = {
    "smi": OEFormat_SMI,
    "ism": OEFormat_ISM,  # old format, don't use
    "usm": OEFormat_USM,
    "can": OEFormat_CAN,

    "sdf": OEFormat_SDF,
    "mol": OEFormat_SDF,

    "skc": OEFormat_SKC,
    "mol2": OEFormat_MOL2,
    "mmod": OEFormat_MMOD,
    "oeb": OEFormat_OEB,
}

# Some trickiness to verify that the format specification is
# supported, but without doing anything (yet) to set those flags.

# I return a function which will set the file stream parameters
# correctly.

def _do_nothing(ifs):
    pass

# Return a function which can be use to set the ifs format, flavor, and compression properties
    
def get_format_setter(format, compression):
    if compression:
        if compression == "gz":
            is_compressed = True
        else:
            raise ValueError("OEChem does not support compression type %r" % (compression,))
    else:
        is_compressed = False

    oeformat = _formats.get(format.lower(), None)
    if oeformat is None:
        raise ValueError("OEChem does not support the %r format" % (format,))
        
    def set_format(ifs):
        ifs.SetFormat(oeformat)
        # OEChem 20170208 has a bug where Setgz(True) on a file where
        # Getgz()==True causes data loss and Setgz(False) causes a
        # segmentation fault. I can work around the first case by
        # not setting 'gz' when 'gz' is already set. I can't work
        # around the second problem. I classify it as a vendor bug,
        # and let the segmentation fault percolate through.
        # Reported to OpenEye on 2017-04-25 in an email titled
        #   'can't use Setgz() to change the gz state of an oemolostream'
        if is_compressed and ifs.Getgz():
            pass
        else:
            ifs.Setgz(is_compressed)
        
    return set_format

def _open_stdin(set_format, aromaticity_flavor):
    ifs = oemolistream()
    ifs.open()
    set_format(ifs)
    
    if aromaticity_flavor is not None:
        flavor = ifs.GetFlavor(ifs.GetFormat())
        flavor |= aromaticity_flavor
        ifs.SetFlavor(ifs.GetFormat(), flavor)

    return ifs

def _open_ifs(filename, set_format, aromaticity_flavor):
    ifs = oemolistream()

    if not ifs.open(filename):
        # Let Python try to do better error reporting.
        open(filename).close()
        # If that didn't work, give up and fake it.
        # (Did manual coverage testing for this. The test cases I can
        # think of, like tricky timing, are too tricky.)
        raise IOError(errno.EIO, "OEChem cannot open the file", filename)

    set_format(ifs)

    if aromaticity_flavor is not None:
        flavor = ifs.GetFlavor(ifs.GetFormat())
        flavor |= aromaticity_flavor
        ifs.SetFlavor(ifs.GetFormat(), flavor)
    
    return ifs

# This code is a bit strange. It needs to do eager error checking but
# lazy parsing. That is, it needs to check right away that the file
# can be opened (if it exists) and the format is understood. But it
# can wait until later to actually parse the files.

_aromaticity_sorted = (
#    ("default", None),
    ("openeye", OEIFlavor_Generic_OEAroModelOpenEye),
    ("daylight", OEIFlavor_Generic_OEAroModelDaylight),
    ("tripos", OEIFlavor_Generic_OEAroModelTripos),
    ("mdl", OEIFlavor_Generic_OEAroModelMDL),
    ("mmff", OEIFlavor_Generic_OEAroModelMMFF),
    )
_aromaticity_flavors = dict(_aromaticity_sorted)
_aromaticity_flavor_names = [pair[0] for pair in _aromaticity_sorted]
_aromaticity_flavors[None] = OEIFlavor_Generic_OEAroModelOpenEye
del _aromaticity_sorted, pair

# If unspecified, use "openeye" (this is what OEChem does internally)
_aromaticity_flavors[None] = _aromaticity_flavors["openeye"]   # Allow "None"

def is_valid_format(filename, format):
    format_name, compression = io.normalize_input_format(filename, format,
                                                         default=("smi", ""))
    if compression not in ("", "gz"):
        return False
    try:
        get_format_setter(format_name, compression)
        return True
    except ValueError:
        return False

def is_valid_aromaticity(aromaticity):
    return aromaticity in _aromaticity_flavors

# Part of the code (parameter checking, opening the file) are eager.
# Actually reading the structures is lazy.

def read_structures(source, format=None, id_tag=None, reader_args=None, errors="strict", location=None):
    if reader_args is None:
        aromaticity = None
    else:
        aromaticity = reader_args.get("aromaticity", None)
    try:
        aromaticity_flavor = _aromaticity_flavors[aromaticity]
    except KeyError:
        raise ValueError("Unsupported aromaticity model %r" % (aromaticity,))
    error_handler = io.get_parse_error_handler(errors)

    # Check that that the format is known
    format_name, compression = io.normalize_input_format(source, format,
                                                         default=("smi", ""))

    if compression not in ("", "gz"):
        raise ValueError("OEChem does not support compression type %r for %r" % (compression, source))
    if location is None:
        location = io.Location.from_source(source)
    location.save(record_format=format_name)

    set_format = get_format_setter(format_name, compression)

    # Input is from a file
    if source is None:
        ifs = _open_stdin(set_format, aromaticity_flavor)
    else:
        ifs = _open_ifs(source, set_format, aromaticity_flavor)

    # Only SD files can take the id_tag
    if ifs.GetFormat() != OEFormat_SDF:
        id_tag = None

    # Lazy structure reader
    return _iter_structures(ifs, id_tag, error_handler, location)

def _iter_structures(ifs, id_tag, error_handler, location):
    recno = 0
    mol = None

    def get_recno():
        return recno
    def get_mol():
        return mol
    location.register(get_recno = get_recno,
                      get_mol = get_mol)
    try:
        if id_tag is None:
            for recno, mol in enumerate(ifs.GetOEGraphMols(), 1):
                title = mol.GetTitle()
                yield title, mol
        else:
            for recno, mol in enumerate(ifs.GetOEGraphMols(), 1):
                id = OEGetSDData(mol, id_tag)
                if not id:
                    # Either it's empty or missing
                    if not OEHasSDData(mol, id_tag):
                        # Missing.
                        id = None
                yield id, mol
    finally:
        ifs.close()
        location.save(recno = get_recno(),
                      mol = None)


def _read_fingerprints(structure_reader, fingerprinter):
    for (id, mol) in structure_reader:
        yield id, fingerprinter(mol)

from .types import FingerprintFamilyConfig, nonnegative_int

def _read_structures(metadata, source, format, id_tag, reader_args, errors, location):
    return read_structures(source, format, id_tag=id_tag, reader_args=reader_args,
                           errors=errors, location=location)

def _correct_numbits(s):
    try:
        if not s.isdigit():
            raise ValueError
        i = int(s)
        if not (16 <= i <= 65536):
            raise ValueError
    except ValueError:
        raise ValueError("must be between 16 and 65536 bits")
    return i

_base = FingerprintFamilyConfig(
    software = SOFTWARE,
    read_structures = _read_structures)


######### These are appropriate for OEGraphSim 2.0  #############

_path_ff = OpenEyePathFingerprintFamily_v2 = _base.clone(
    name = "OpenEye-Path/2",
    format_string = ("numbits=%(numbits)s minbonds=%(minbonds)s "
                     "maxbonds=%(maxbonds)s atype=%(atype)s btype=%(btype)s"),
    make_fingerprinter = get_path_fingerprinter,
    num_bits = _get_num_bits,
    )
_path_ff.add_argument("numbits", decoder=_correct_numbits, metavar="INT", default=4096,
                      help="number of bits in the path fingerprint")

_path_ff.add_argument("minbonds", decoder=nonnegative_int, metavar="INT", default=0,
                      help="minimum number of bonds in the path fingerprint")

_path_ff.add_argument("maxbonds", decoder=nonnegative_int, metavar="INT", default=5,
                      help="maximum number of bonds in the path fingerprint")

_path_ff.add_argument("atype", decoder=path_atom_description_to_value,
                      encoder=path_atom_value_to_description,
                      help="atom type", default=OEFPAtomType_DefaultPathAtom)
_path_ff.add_argument("btype", decoder=path_bond_description_to_value,
                      encoder=path_bond_value_to_description,
                      help="bond type", default=OEFPBondType_DefaultPathBond)


if _is_licensed:
    _PROBE_MOL = OEGraphMol()
    _PROBE_FP = OEFingerPrint()
    _PROBE_MOL.NewAtom(2)
    OEMakeMACCS166FP(_PROBE_FP, _PROBE_MOL)
    _maccs_version = {
        "2.0.0": "2",
        "2.2.0": "3",
        }.get(_PROBE_FP.GetFPTypeBase().GetFPVersionString(), "unknown")
else:
    _maccs_version = "unknown"

def _check_maccs_version(version):
    def make_fingerprinter(*args, **kwargs):
        if _maccs_version != version:
            raise TypeError("This version of OEChem does not support the RDKit-MACCS/%s fingerprint" % (version,))
        return get_maccs_fingerprinter(*args, **kwargs)
    return make_fingerprinter

    
OpenEyeMACCSFingerprintFamily_v2 = _base.clone(
    name = "OpenEye-MACCS166/2",
    make_fingerprinter = _check_maccs_version("2"),
    num_bits = 166,
    )

OpenEyeMACCSFingerprintFamily_v3 = _base.clone(
    name = "OpenEye-MACCS166/3",
    make_fingerprinter = _check_maccs_version("3"),
    num_bits = 166,
    )

_circular_ff = OpenEyeCircularFingerprintFamily_v2 = _base.clone(
    name = "OpenEye-Circular/2",
    format_string = ("numbits=%(numbits)s minradius=%(minradius)s "
                     "maxradius=%(maxradius)s atype=%(atype)s btype=%(btype)s"),
    num_bits = _get_num_bits,
    make_fingerprinter = get_circular_fingerprinter)
_circular_ff.add_argument("numbits", decoder=_correct_numbits, metavar="INT", default=4096,
                          help="number of bits in the circular fingerprint")
_circular_ff.add_argument("minradius", decoder=nonnegative_int, metavar="INT", default=0,
                          help="minimum radius for the circular fingerprint")
_circular_ff.add_argument("maxradius", decoder=nonnegative_int, metavar="INT", default=5,
                          help="maximum radius for the circular fingerprint")
_circular_ff.add_argument("atype", decoder=circular_atom_description_to_value,
                          encoder=circular_atom_value_to_description,
                          help="atom type", default=OEFPAtomType_DefaultCircularAtom)
_circular_ff.add_argument("btype", decoder=circular_bond_description_to_value,
                 encoder=circular_bond_value_to_description,
                 help="bond type", default=OEFPBondType_DefaultCircularBond)

_tree_ff = OpenEyeTreeFingerprintFamily_v2 = _base.clone(
    name = "OpenEye-Tree/2",
    format_string = ("numbits=%(numbits)s minbonds=%(minbonds)s "
                     "maxbonds=%(maxbonds)s atype=%(atype)s btype=%(btype)s"),
    num_bits = _get_num_bits,
    make_fingerprinter = get_tree_fingerprinter)
_tree_ff.add_argument("numbits", decoder=_correct_numbits, metavar="INT", default=4096,
                      help="number of bits in the tree fingerprint")
_tree_ff.add_argument("minbonds", decoder=nonnegative_int, metavar="INT", default=0,
                      help="minimum number of bonds in the tree fingerprint")
_tree_ff.add_argument("maxbonds", decoder=nonnegative_int, metavar="INT", default=4,
                      help="maximum number of bonds in the tree fingerprint")
_tree_ff.add_argument("atype", decoder=tree_atom_description_to_value,
                      encoder=tree_atom_value_to_description,
                      help="atom type", default=OEFPAtomType_DefaultTreeAtom)
_tree_ff.add_argument("btype", decoder=tree_bond_description_to_value,
                      encoder=tree_bond_value_to_description,
                      help="bond type", default=OEFPBondType_DefaultTreeBond)


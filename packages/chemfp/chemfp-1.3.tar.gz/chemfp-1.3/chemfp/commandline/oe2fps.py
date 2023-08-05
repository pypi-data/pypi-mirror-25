from __future__ import absolute_import
import sys
import itertools
import textwrap

from .. import ChemFPError, open_fingerprint_writer
from .. import argparse, types, io
from .. import openeye as oe
from . import cmdsupport

##### Handle command-line argument parsing

# Build up some help text based on the atype and btype fields
atype_options = "\n  ".join(textwrap.wrap(" ".join(sorted(dict(oe._atype_flags)))))
btype_options = "\n  ".join(textwrap.wrap(" ".join(sorted(dict(oe._btype_flags)))))
from openeye.oegraphsim import (
    OEGetFPAtomType, OEFPAtomType_DefaultPathAtom,
    OEFPAtomType_DefaultCircularAtom, OEFPAtomType_DefaultTreeAtom,
    OEGetFPBondType, OEFPBondType_DefaultPathBond,
    OEFPBondType_DefaultCircularBond, OEFPBondType_DefaultTreeBond,
    )
type_help = """\
ATYPE is one or more of the following, separated by the '|' character
  %(atype_options)s
The following shorthand terms and expansions are also available:
 DefaultPathAtom = %(defaultpathatom)s
 DefaultCircularAtom = %(defaultcircularatom)s
 DefaultTreeAtom = %(defaulttreeatom)s
and 'Default' selects the correct value for the specified fingerprint.
Examples:
  --atype Default
  --atype Arom|AtmNum|FCharge|HCount

BTYPE is one or more of the following, separated by the '|' character
  %(btype_options)s
The following shorthand terms and expansions are also available:
 DefaultPathBond = %(defaultpathbond)s
 DefaultCircularBond = %(defaultcircularbond)s
 DefaultTreeBond = %(defaulttreebond)s
and 'Default' selects the correct value for the specified fingerprint.
Examples:
   --btype Default
   --btype Order|InRing

To simplify command-line use, a comma may be used instead of a '|' to
separate different fields. Example:
  --atype AtmNum,HvyDegree
""" % dict(atype_options=atype_options,
           btype_options=btype_options,
           defaultpathatom=OEGetFPAtomType(OEFPAtomType_DefaultPathAtom),
           defaultcircularatom=OEGetFPAtomType(OEFPAtomType_DefaultCircularAtom),
           defaulttreeatom=OEGetFPAtomType(OEFPAtomType_DefaultTreeAtom),
           defaultpathbond=OEGetFPBondType(OEFPBondType_DefaultPathBond),
           defaultcircularbond=OEGetFPBondType(OEFPBondType_DefaultCircularBond),
           defaulttreebond=OEGetFPBondType(OEFPBondType_DefaultTreeBond),

)


# Extra help text after the parameter descriptions
epilog = type_help + """\

OEChem guesses the input structure format based on the filename
extension and assumes SMILES for structures read from stdin.
Use "--in FORMAT" to select an alternative, where FORMAT is one of:
 
  File Type      Valid FORMATs (use gz if compressed)
  ---------      ------------------------------------
   SMILES        smi, ism, usm, can, smi.gz, ism.gz, can.gz
   SDF           sdf, mol, sdf.gz, mol.gz
   SKC           skc, skc.gz
   CDK           cdk, cdk.gz
   MOL2          mol2, mol2.gz
   PDB           pdb, ent, pdb.gz, ent.gz
   MacroModel    mmod, mmod.gz
   OEBinary v2   oeb, oeb.gz
"""

parser = argparse.ArgumentParser(
    description="Generate FPS fingerprints from a structure file using OEChem",
    epilog=epilog,
    formatter_class=argparse.RawDescriptionHelpFormatter,    
    )

CircularFamily = oe.OpenEyeCircularFingerprintFamily_v2
path_group = parser.add_argument_group("path, circular, and tree fingerprints")
path_group.add_argument(
    "--path", action="store_true", help="generate path fingerprints (default)")
path_group.add_argument(
    "--circular", action="store_true", help="generate circular fingerprints")
path_group.add_argument(
    "--tree", action="store_true", help="generate tree fingerprints")

path_group.add_argument(
    "--numbits", action="store", type=int, metavar="INT", default=4096,
    help="number of bits in the fingerprint (default=4096)")
path_group.add_argument(
    "--minbonds", action="store", type=int, metavar="INT", default=0,
    help="minimum number of bonds in the path or tree fingerprint (default=0)")
path_group.add_argument(
    "--maxbonds", action="store", type=int, metavar="INT", default=None,
    help="maximum number of bonds in the path or tree fingerprint (path default=5, tree default=4)")
CircularFamily.add_argument_to_argparse("minradius", path_group)
CircularFamily.add_argument_to_argparse("maxradius", path_group)

# The expansion of 'Default' differs based on the fingerprint type
path_group.add_argument(
    "--atype", metavar="ATYPE", default="Default",
    help="atom type flags, described below (default=Default)")
path_group.add_argument(
    "--btype", metavar="BTYPE", default="Default",
    help="bond type flags, described below (default=Default)")

maccs_group = parser.add_argument_group("166 bit MACCS substructure keys")
maccs_group.add_argument(
    "--maccs166", action="store_true", help="generate MACCS fingerprints")

substruct_group = parser.add_argument_group("881 bit ChemFP substructure keys")
substruct_group.add_argument(
    "--substruct", action="store_true", help="generate ChemFP substructure fingerprints")

rdmaccs_group = parser.add_argument_group("ChemFP version of the 166 bit RDKit/MACCS keys")
rdmaccs_group.add_argument(
    "--rdmaccs", "--rdmaccs/2", action="store_true", help="generate 166 bit RDKit/MACCS fingerprints (version 2)")
rdmaccs_group.add_argument(
    "--rdmaccs/1", dest="rdmaccs/1", action="store_true", help="use the version 1 definition for --rdmaccs")

parser.add_argument(
    "--aromaticity", metavar="NAME", choices=oe._aromaticity_flavor_names,
    default="openeye",
    help="use the named aromaticity model")

parser.add_argument(
    "--id-tag", metavar="NAME",
    help="tag name containing the record id (SD files only)")

parser.add_argument(
    "--in", metavar="FORMAT", dest="format",
    help="input structure format (default guesses from filename)")
parser.add_argument(
    "-o", "--output", metavar="FILENAME",
    help="save the fingerprints to FILENAME (default=stdout)")
parser.add_argument(
    "--out", metavar="FORMAT", dest="output_format", choices=("fps", "fps.gz"),
    help="output structure format (default guesses from output filename, or is 'fps')")

parser.add_argument(
    "--errors", choices=["strict", "report", "ignore"], default="ignore",
    help="how should structure parse errors be handled? (default=ignore)")

cmdsupport.add_version(parser)

parser.add_argument(
    "filenames", nargs="*", help="input structure files (default is stdin)")

def _get_atype_and_btype(args, atom_description_to_value, bond_description_to_value):
    try:
        atype = atom_description_to_value(args.atype)
    except ValueError, err:
        parser.error("--atype must contain '|' separated atom terms: %s" % (err,))
    try:
        btype = bond_description_to_value(args.btype)
    except ValueError, err:
        parser.error("--btype must contain '|' separated atom terms: %s" % (err,))
    return atype, btype

#######

def main(args=None):
    args = parser.parse_args(args)

    supported_fingerprints = ("maccs166", "path", "substruct", "rdmaccs", "rdmaccs/1",
                              "circular", "tree")
    cmdsupport.mutual_exclusion(parser, args, "path", supported_fingerprints)

    if args.maccs166:
        # Create the MACCS keys fingerprinter
        opener = types.get_fingerprint_family("OpenEye-MACCS166")()
    elif args.path:
        if not (16 <= args.numbits <= 65536):
            parser.error("--numbits must be between 16 and 65536 bits")

        if not (0 <= args.minbonds):
            parser.error("--minbonds must be 0 or greater")
        if args.maxbonds is None:
            args.maxbonds = 5
        if not (args.minbonds <= args.maxbonds):
            parser.error("--maxbonds must not be smaller than --minbonds")
        atype, btype = _get_atype_and_btype(args, oe.path_atom_description_to_value,
                                            oe.path_bond_description_to_value)
        opener = types.get_fingerprint_family("OpenEye-Path")(
            numbits = args.numbits,
            minbonds = args.minbonds,
            maxbonds = args.maxbonds,
            atype = atype,
            btype = btype)
    elif args.circular:
        if not (16 <= args.numbits <= 65536):
            parser.error("--numbits must be between 16 and 65536 bits")

        if not (0 <= args.minradius):
            parser.error("--minradius must be 0 or greater")
        if not (args.minradius <= args.maxradius):
            parser.error("--maxradius must not be smaller than --minradius")
        atype, btype = _get_atype_and_btype(args, oe.circular_atom_description_to_value,
                                            oe.circular_bond_description_to_value)

        opener = types.get_fingerprint_family("OpenEye-Circular")(
            numbits = args.numbits,
            minradius = args.minradius,
            maxradius = args.maxradius,
            atype = atype,
            btype = btype)
    elif args.tree:
        if not (16 <= args.numbits <= 65536):
            parser.error("--numbits must be between 16 and 65536 bits")

        if not (0 <= args.minbonds):
            parser.error("--minbonds must be 0 or greater")
        if args.maxbonds is None:
            args.maxbonds = 4
        if not (args.minbonds <= args.maxbonds):
            parser.error("--maxbonds must not be smaller than --minbonds")
        atype, btype = _get_atype_and_btype(args, oe.tree_atom_description_to_value,
                                            oe.tree_bond_description_to_value)

        opener = types.get_fingerprint_family("OpenEye-Tree")(
            numbits = args.numbits,
            minbonds = args.minbonds,
            maxbonds = args.maxbonds,
            atype = atype,
            btype = btype)
        
    elif args.substruct:
        opener = types.get_fingerprint_family("ChemFP-Substruct-OpenEye")()
    elif args.rdmaccs:
        opener = types.get_fingerprint_family("RDMACCS-OpenEye")()
    elif getattr(args, "rdmaccs/1"):
        opener = types.get_fingerprint_family("RDMACCS-OpenEye/1")()
    else:
        parser.error("ERROR: fingerprint not specified?")

    if args.format is not None:
        if args.filenames:
            filename = args.filenames[0]
        else:
            filename = None
        if not oe.is_valid_format(filename, args.format):
            parser.error("Unsupported format specifier: %r" % (args.format,))

    if not oe.is_valid_aromaticity(args.aromaticity):
        parser.error("Unsupported aromaticity specifier: %r" % (args.aromaticity,))

    if not cmdsupport.is_valid_tag(args.id_tag):
        parser.error("Invalid id tag: %r" % (args.id_tag,))

    missing = cmdsupport.check_filenames(parser, None, args.format, args.filenames)

    # Ready the input reader/iterator
    metadata, reader = cmdsupport.read_multifile_structure_fingerprints(
        opener, args.filenames, format = args.format, id_tag = args.id_tag,
        reader_args = {"aromaticity": args.aromaticity}, errors = args.errors)
    
    location = io.Location.from_destination(args.output)
    try:
        writer = open_fingerprint_writer(args.output, metadata, format=args.output_format)
    except (IOError, ValueError) as err:
        msg = "Cannot open output fingerprint file: %s" % (err,)
        if isinstance(err, ValueError) and "Unable to determine fingerprint format" in str(err):
            msg += ".\nUse --out to specify 'fps' or 'fps.gz'."
        parser.error(msg)
        
    try:
        with writer:
            writer.write_fingerprints(reader)
    except (ChemFPError, IOError, EOFError) as err:
        sys.stderr.write("ERROR: %s. Exiting.\n" % (err,))
        raise SystemExit(1)
    
if __name__ == "__main__":
    main()

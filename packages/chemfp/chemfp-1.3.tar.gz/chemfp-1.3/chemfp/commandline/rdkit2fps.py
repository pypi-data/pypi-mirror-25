# Copyright (c) 2010-2017 Andrew Dalke Scientific, AB (Sweden)
# See the contents of "chemfp/__init__.py" for full license details.

from __future__ import with_statement, print_function

import sys

from .. import ChemFPError, open_fingerprint_writer
from .. import argparse, io, rdkit, types
from . import cmdsupport

########### Configure the command-line parser

epilog = ""

if rdkit.PATTERN_VERSION is None:
    epilog += """\
    
This version of RDKit does not support the 'Pattern' fingerprints.
"""

if not rdkit.HAS_AVALON:
    epilog += """\
    
This version of RDKit does not support the Avalon fingerprints. To use them,
reinstall RDKit with pyAvalonTools.
"""

    
epilog = """\

This program guesses the input structure format based on the filename
extension. If the data comes from stdin, or the extension name us
unknown, then use "--in" to change the default input format. The
supported format extensions are:

  File Type      Valid FORMATs (use gz if compressed)
  ---------      ------------------------------------
   SMILES        smi, ism, usm, can, smi.gz, ism.gz, usm.gz, can.gz
   SDF           sdf, mol, sd, mdl, sdf.gz, mol.gz, sd.gz, mdl.gz
"""

parser = argparse.ArgumentParser(
    description="Generate FPS fingerprints from a structure file using RDKit",
    epilog=epilog,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    conflict_handler="resolve",
    )

_base = rdkit._base_2048

# --RDK and --morgan both have fpSize but argparse doesn't allow the
# same option in different groups. Especially with different defaults.

rdkit._base_fpsize.add_argument_to_argparse("fpSize", parser)

rdk_group = parser.add_argument_group("RDKit topological fingerprints")
rdk_group.add_argument("--RDK", action="store_true",
                       help="generate RDK fingerprints (default)")
_base.add_argument_to_argparse("minPath", rdk_group)
_base.add_argument_to_argparse("maxPath", rdk_group)
_base.add_argument_to_argparse("nBitsPerHash", rdk_group)
_base.add_argument_to_argparse("useHs", rdk_group)


morgan_group = parser.add_argument_group("RDKit Morgan fingerprints")

morgan_group.add_argument("--morgan", action="store_true",
                          help="generate Morgan fingerprints")

_morgan = rdkit.RDKitMorganFingerprintFamily_v1
_morgan.add_argument_to_argparse("radius", morgan_group)
_morgan.add_argument_to_argparse("useFeatures", morgan_group)
_morgan.add_argument_to_argparse("useChirality", morgan_group)
_morgan.add_argument_to_argparse("useBondTypes", morgan_group)

torsion_group = parser.add_argument_group("RDKit Topological Torsion fingerprints")
torsion_group.add_argument("--torsions", action="store_true",
                           help="generate Topological Torsion fingerprints")
rdkit.RDKitTorsionFingerprintFamily_v1.add_argument_to_argparse(
    "targetSize", torsion_group)

pair_group = parser.add_argument_group("RDKit Atom Pair fingerprints")
pair_group.add_argument("--pairs", action="store_true",
                        help="generate Atom Pair fingerprints")
rdkit.RDKitTorsionFingerprintFamily_v1.add_argument_to_argparse(
    "minLength", pair_group)
rdkit.RDKitTorsionFingerprintFamily_v1.add_argument_to_argparse(
    "maxLength", pair_group)



maccs_group = parser.add_argument_group("166 bit MACCS substructure keys")
maccs_group.add_argument(
    "--maccs166", action="store_true", help="generate MACCS fingerprints")

avalon_help = "generate Avalon fingerprints"
if rdkit.HAS_AVALON:
    has_avalon = True
else:
    has_avalon = False
    avalon_help += " (not available for this RDKit install)"
avalon_group = parser.add_argument_group("Avalon fingerprints")
avalon_group.add_argument(
    "--avalon", action="store_true", help=avalon_help)
rdkit._base_avalon.add_argument_to_argparse("isQuery", avalon_group)
rdkit._base_avalon.add_argument_to_argparse("bitFlags", avalon_group)

pattern_group = parser.add_argument_group("RDKit Pattern fingerprints")
pattern_group.add_argument("--pattern", action="store_true",
                           help="generate (substructure) pattern fingerprints")


substruct_group = parser.add_argument_group("881 bit substructure keys")
substruct_group.add_argument(
    "--substruct", action="store_true", help="generate ChemFP substructure fingerprints")


rdmaccs_group = parser.add_argument_group("ChemFP version of the 166 bit RDKit/MACCS keys")
rdmaccs_group.add_argument(
    "--rdmaccs", "--rdmaccs/2", action="store_true", help="generate 166 bit RDKit/MACCS fingerprints (version 2)")
rdmaccs_group.add_argument(
    "--rdmaccs/1", dest="rdmaccs/1", action="store_true", help="use the version 1 definition for --rdmaccs")


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


def main(args=None):
    args = parser.parse_args(args)
    cmdsupport.mutual_exclusion(parser, args, "RDK",
                                ("maccs166", "RDK", "substruct", "rdmaccs", "rdmaccs/1", "morgan",
                                 "torsions", "pairs", "pattern", "avalon"))
    # If size isn't specified, use the appropriate size that fingerprint
    if args.fpSize is None:
        if args.avalon:
            args.fpSize = rdkit.AVALON_NBITS
        else:
            args.fpSize = rdkit.NUM_BITS

    if args.maccs166:
        opener = types.get_fingerprint_family("RDKit-MACCS166")()
    elif args.RDK:
        fpSize = args.fpSize or rdkit.NUM_BITS
        minPath = args.minPath
        maxPath = args.maxPath
        nBitsPerHash = args.nBitsPerHash
        if maxPath < minPath:
            parser.error("--minPath must not be greater than --maxPath")

        useHs = args.useHs

        opener = types.get_fingerprint_family("RDKit-Fingerprint")(
            minPath=minPath,
            maxPath=maxPath,
            fpSize=fpSize,
            nBitsPerHash=nBitsPerHash,
            useHs=useHs)

    elif args.substruct:
        opener = types.get_fingerprint_family("ChemFP-Substruct-RDKit")()
    elif args.rdmaccs:
        opener = types.get_fingerprint_family("RDMACCS-RDKit")()
    elif getattr(args, "rdmaccs/1"):
        opener = types.get_fingerprint_family("RDMACCS-RDKit/1")()
    elif args.morgan:
        opener = types.get_fingerprint_family("RDKit-Morgan")(
            radius=args.radius,
            fpSize=args.fpSize,
            useFeatures=args.useFeatures,
            useChirality=args.useChirality,
            useBondTypes=args.useBondTypes)

    elif args.torsions:
        opener = types.get_fingerprint_family("RDKit-Torsion")(
            fpSize=args.fpSize,
            targetSize=args.targetSize)
    elif args.pairs:
        minLength = args.minLength
        maxLength = args.maxLength
        if maxLength < minLength:
            parser.error("--minLength must not be greater than --maxLength")
        opener = types.get_fingerprint_family("RDKit-AtomPair")(
            fpSize=args.fpSize,
            minLength=minLength,
            maxLength=maxLength)
    elif args.pattern:
        opener = types.get_fingerprint_family("RDKit-Pattern")(
            fpSize=args.fpSize)
    elif args.avalon:
        if rdkit.HAS_AVALON:
            opener = types.get_fingerprint_family("RDKit-Avalon")(
                fpSize=args.fpSize,
                isQuery=args.isQuery,
                bitFlags=args.bitFlags)
        else:
            parser.error("Cannot generate --avalon fingerprints. The RDKit toolkit was not compiled with Avalon support.")
        
    else:
        raise AssertionError("Unknown fingerprinter")

    if not rdkit.is_valid_format(args.format):
        parser.error("Unsupported format specifier: %r" % (args.format,))

    if not cmdsupport.is_valid_tag(args.id_tag):
        parser.error("Invalid id tag: %r" % (args.id_tag,))

    cmdsupport.check_filenames(parser, None, args.format, args.filenames)

    # Ready the input reader/iterator
    metadata, reader = cmdsupport.read_multifile_structure_fingerprints(
        opener, args.filenames, format = args.format, id_tag = args.id_tag, 
        reader_args = {}, errors = args.errors)

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


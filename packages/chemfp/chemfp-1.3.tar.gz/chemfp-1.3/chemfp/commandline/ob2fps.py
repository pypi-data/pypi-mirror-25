import sys
from chemfp import openbabel as ob
from chemfp import argparse, io, types

from .. import ChemFPError
from . import cmdsupport
from .. import open_fingerprint_writer

############ Command-line parser definition

epilog = """\

Open Babel autodetects the input structure format based on the filename
extension. The default format for structures read from stdin is
SMILES. Use"--in FORMAT" to select an alternative, where FORMAT is
one of the extensions at http://openbabel.org/wiki/List_of_extensions .
For a short list of some common formats:


  File Type      Valid FORMATs
  ---------      -------------
   SMILES        smi, can, smiles
   SDF           sdf, mol, sd, mdl
   MOL2          mol2, ml2
   PDB           pdb, ent
   MacroModel    mmod

If Open Babel is compiled with zlib support then it will automatically
handle gzip'ed input data if the filename ends with ".gz". You may
optionally include that suffix in the format name.

"""

parser = argparse.ArgumentParser(
    description="Generate FPS fingerprints from a structure file using Open Babel",
    )
group = parser.add_mutually_exclusive_group()
group.add_argument("--FP2", action="store_true",
                   help="linear fragments up to 7 atoms",
                   )
group.add_argument("--FP3", action="store_true",
                   help="SMARTS patterns specified in the file patterns.txt",
                   )
group.add_argument("--FP4", action="store_true",
                   help="SMARTS patterns specified in the file SMARTS_InteLigand.txt",
                   )

if ob.HAS_MACCS:
    # Added in Open Babel 2.3
    group.add_argument("--MACCS", action="store_true",
                       help="Open Babel's implementation of the MACCS 166 keys",
                       )
else:
    group.add_argument("--MACCS", action="store_true",
                       help="(Not available using your version of Open Babel)")

group.add_argument(
    "--substruct", action="store_true", help="generate ChemFP substructure fingerprints")

group.add_argument(
    "--rdmaccs", "--rdmaccs/2", action="store_true", help="166 bit RDKit/MACCS fingerprints (version 2)")
group.add_argument(
    "--rdmaccs/1", dest="rdmaccs/1", action="store_true", help="use the version 1 definition for --rdmaccs")

parser.add_argument(
    "--id-tag", metavar="NAME",
    help="tag name containing the record id  (SD files only)")

parser.add_argument(
    "--in", metavar="FORMAT", dest="format",
    help="input structure format (default autodetects from the filename extension)")
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


#########

def main(args=None):
    args = parser.parse_args(args)
    outfile = sys.stdout

    cmdsupport.mutual_exclusion(parser, args, "FP2",
                                ("FP2", "FP3", "FP4", "MACCS", "substruct", "rdmaccs", "rdmaccs/1"))

    if args.FP2:
        opener = types.get_fingerprint_family("OpenBabel-FP2")()
    elif args.FP3:
        opener = types.get_fingerprint_family("OpenBabel-FP3")()
    elif args.FP4:
        opener = types.get_fingerprint_family("OpenBabel-FP4")()
    elif args.MACCS:
        if not ob.HAS_MACCS:
            parser.error(
                "--MACCS is not supported in your Open Babel installation (%s)" % (
                    ob.GetReleaseVersion(),))
        opener = types.get_fingerprint_family("OpenBabel-MACCS")()
    elif args.substruct:
        opener = types.get_fingerprint_family("ChemFP-Substruct-OpenBabel")()
    elif args.rdmaccs:
        opener = types.get_fingerprint_family("RDMACCS-OpenBabel")()
    elif getattr(args, "rdmaccs/1"):
        opener = types.get_fingerprint_family("RDMACCS-OpenBabel/1")()
    else:
        parser.error("should not get here")

    if not ob.is_valid_format(args.format):
        parser.error("Unsupported format specifier: %r" % (args.format,))

    if not cmdsupport.is_valid_tag(args.id_tag):
        parser.error("Invalid id tag: %r" % (args.id_tag,))

    missing = cmdsupport.check_filenames(parser, None, args.format, args.filenames)

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

# Copyright (c) 2010-2017 Andrew Dalke Scientific, AB (Sweden)
# See the contents of "chemfp/__init__.py" for full license details.

from __future__ import absolute_import, print_function
import os
import sys
import itertools

from .. import argparse
from .. import __version__ as chemfp_version
from .. import ChemFPError, ParseError
from .. import io

######
# Code extracted from Python's argparse.py. Distributed under the Python license.
# Before Python 3.4, argparse --version sent the message to stderr, not stdout.
# The bug was fixed in https://bugs.python.org/issue18920 .
# chemfp supports Python 2.7 and Python 3.5+.
# This is a back-port to version 2.7

version_action = "version"
#if sys.version_info.major == 2:
if sys.version_info[0] == 2: # Support Python 2.6
    class ChemfpVersionAction(argparse._VersionAction):
        def __call__(self, parser, namespace, values, option_string=None):
            version = self.version
            if version is None:
                version = parser.version
            formatter = parser._get_formatter()
            formatter.add_text(version)
            parser._print_message(formatter.format_help(), sys.stdout)
            parser.exit()

    version_action = ChemfpVersionAction
    
def add_version(parser):
    parser.add_argument("--version", action=version_action,
                        version="%(prog)s " + chemfp_version)
    

######

def mutual_exclusion(parser, args, default, groups):
    true_groups = []
    for g in groups:
        if getattr(args, g):
            true_groups.append(g)

    if not true_groups:
        setattr(args, default, True)
    elif len(true_groups) == 1:
        pass
    else:
        parser.error("Cannot specify both --%s and --%s" % (true_groups[0], true_groups[1]))

class AbortHandler(object):
    def error(self, msg, location):
        raise ParseError("Each of the first 100 records contained errors. Final error: %s" % (msg,), location)

def cleanup_ids(reader, id_tag, error_handler, location):
    err_count = 0
    for recno, (id, fp) in enumerate(reader):
        if not id:
            if recno == err_count == 99:
                error_handler = AbortHandler()
            err_count += 1
                
            if location.record_format == "sdf":
                if id_tag is None:
                    error_handler.error("Missing title in SD record", location)
                else:
                    error_handler.error("Missing id tag %r in SD record" % (id_tag,), location)
            elif location.record_format == "smi":
                error_handler.error("Missing SMILES identifier (second column)", location)
            else:
                error_handler.error("Missing identifier", location)
            continue
                    
        else:
            # This assumes that these characters are rare
            if "\n" in id:
                id = id.partition("\n")[0]  # get up to the newline
            if "\r" in id:
                id = id.replace("\r", "")
            if "\t" in id:
                id = id.replace("\t", "")
            if "\0" in id:
                id = id.replace("\0", "")
            if " " in id:
                id = id.strip()

            if not id:
                if recno == err_count == 99:
                    error_handler = AbortHandler()
                err_count += 1
                if location.record_format == "sdf":
                    if id_tag is None:
                        error_handler.error("Empty title in SD record after cleanup", location)
                    else:
                        error_handler.error("Empty id tag %r in SD record after cleanup"
                                            % (id_tag,), location)
                elif location.record_format == "smi":
                    error_handler.error("Empty SMILES identifier (second column) after cleanup", location)
                else:
                    error_handler.error("Empty identifier after cleanup", location)
                continue
            else:
                yield id, fp
    

def sys_exit_opener(opener, source, format, id_tag, error_handler, reader_args, location):
    try:
        return opener.read_molecule_fingerprints(source, format, id_tag, reader_args=reader_args,
                                                 errors=error_handler, location=location)
    except (IOError, ChemFPError, ValueError) as err:
        sys.stderr.write("Problem reading structure fingerprints: %s. Exiting.\n" % err)
        raise SystemExit(1)

## def iter_all_sources(fptype, filenames, format, id_tag, errors):
##     for filename in filenames:
##         reader = sys_exit_opener(fptype, filename, format, id_tag, errors)
##         for id, fp in reader:
##             yield id, fp

def read_multifile_structure_fingerprints(opener, filenames, format, id_tag, reader_args, errors):
    error_handler = io.get_parse_error_handler(errors)
    if errors == "strict":
        id_error_handler = error_handler
    else:
        id_error_handler = io.get_parse_error_handler("report")
    
    if not filenames:
        location = io.Location.from_source(None)
        reader = sys_exit_opener(opener, None, format, id_tag, error_handler, reader_args, location)
        cleanup_reader = cleanup_ids(reader, id_tag, id_error_handler, location)
        return reader.metadata, cleanup_reader

    if len(filenames) == 1:
        location = io.Location.from_source(filenames[0])
        reader = sys_exit_opener(opener, filenames[0], format, id_tag, error_handler, reader_args, location)
        cleanup_reader = cleanup_ids(reader, id_tag, id_error_handler, location)
        return reader.metadata, cleanup_reader

    location = io.Location.from_source(filenames[0])
    reader = sys_exit_opener(opener, filenames[0], format, id_tag, error_handler, reader_args, location)
    reader.metadata.sources = filenames

    def multifile_reader(reader):
        # This is very annoying. The gzip reader fails if the file
        # isn't in the correct format but the check doesn't occur
        # until someone tries to read a byte. The error message is the
        # un-helpful generic "Not a gzipped file", without the
        # filename. I want to report that error, but do so carefully.

        
        try:
            # Handle the first filename
            filename = filenames[0]
            
            for id, fp in cleanup_ids(reader, id_tag, id_error_handler, location):
                yield id, fp
        
            # Handle the remaining filenames
            for filename in filenames[1:]:
                location.filename = filename
                reader = sys_exit_opener(opener, filename, format, id_tag,
                                         error_handler, reader_args, location)
                for id, fp in cleanup_ids(reader, id_tag, id_error_handler, location):
                    yield id, fp

        except IOError as err:
            if err.filename is None:
                raise IOError("%s: %r" % (err, filename))
            raise
        except EOFError as err:
            raise EOFError("%s: %r" % (err, filename))
            

    return reader.metadata, multifile_reader(reader)

def is_valid_tag(tag):
    if tag is None:
        return True
    for c in "<>\r\n":
        if c in tag:
            return False
    return True

def check_filenames(parser, toolkit, format, filenames):
    if not filenames:
        # Read from stdin.
        return None
    for filename in filenames:
        if not os.path.exists(filename):
            parser.error("Structure file %r does not exist" % (filename,))
        ## try:
        ##     toolkit.get_input_format_from_source(source=filename, format=format)
        ## except ValueError as err:
        ##     parser.error(str(err))

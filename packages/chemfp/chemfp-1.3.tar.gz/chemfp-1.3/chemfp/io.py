# Copyright (c) 2010-2017 Andrew Dalke Scientific, AB (Sweden)
# See the contents of "chemfp/__init__.py" for full license details.

from __future__ import with_statement

import re
import os
import sys
import binascii

from datetime import datetime

from . import ParseError

DEV_STDIN = "/dev/stdin"


def utcnow():
    return datetime.utcnow().isoformat().split(".", 1)[0]
############ error handlers
def _get_text(msg, location):
    if location is None:
        return str(msg)
    return "%s, %s" % (msg, location.where())

class ErrorHandler(object):
    ## def warning(self, msg, location=None, extra=None):
    ##     sys.stderr.write("WARNING: %s\n" % _get_text(msg, location))

    def error(self, msg, location=None, extra=None):
        raise NotImplementedError("error() must be implemented in the subclass")
    

class IgnoreHandler(ErrorHandler):
    ## def warning(self, msg, location=None, extra=None):
    ##     pass
    
    def error(self, msg, location=None, extra=None):
        pass

class ReportHandler(ErrorHandler):
    ## def warning(self, msg, location=None, extra=None):
    ##     sys.stderr.write("WARNING: %s\n" % _get_text(msg, location))

    def error(self, msg, location=None, extra=None):
        sys.stderr.write("ERROR: %s. Skipping.\n" % _get_text(msg, location))

class LogHandler(ErrorHandler):
    def __init__(self, logger="chemfp"):
        if isinstance(logger, basestring):
            import logging
            logger = logging.getLogger(logger)
        self._logger = logger

    ## def warning(self, msg, location=None, extra=None):
    ##     self._logger.warning(_get_text(msg, location))

    def error(self, msg, location=None, extra=None):
        self._logger.error(_get_text(msg, location))

class StrictHandler(ErrorHandler):
    ## def warning(self, msg, location=None, extra=None):
    ##     pass

    def error(self, msg, location=None, extra=None):
        raise ParseError(msg, location), None, None


_error_handlers = {
    "ignore": IgnoreHandler(),
    "report": ReportHandler(),
    "strict": StrictHandler(),
}

def get_parse_error_handler(errors):
    if isinstance(errors, basestring):
        try:
            return _error_handlers[errors]
        except KeyError:
            pass
        if "log" not in _error_handlers:
            _error_handlers["log"] = handler = LogHandler("chemfp")
        if errors == "log":
            return handler
            
        raise ValueError("'errors' value must be an ErrorHandler or one of %s, not %r"
                         % (", ".join(map(repr, sorted(_error_handlers))), errors))

    return errors


############
    
_compression_extensions = {
    ".gz": "gz",
    ".gzip": "gz",
    ".bz2": "bz2",
    ".bzip": "bz2",
    ".bzip2": "bz2",
    ".xz": "xz",
    }

def _determine_format_from_filename(filename, default):
    # The filename could have 0, 1 or 2 extensions
    base, ext = os.path.splitext(filename)
    if ext == "":
        # No extensions, use the default
        return default
    ext = ext.lower()

    # If it's not a compression extension then it's a format indicator
    if ext not in _compression_extensions:
        # the [1:] is to remove the leading "."
        return (ext[1:], "")

    # Found a compression, now look for the format
    compression = _compression_extensions[ext]

    base, ext = os.path.splitext(base)
    if ext == "":
        # compression found but not the actual format type
        return (default[0], compression)

    # The [1:] is to remove the leading "."
    format_name = ext[1:].lower()
    
    return (format_name, compression)


    
def normalize_input_format(source, format, default=("fps", "")):
    if format is not None:
        # Either 0 or 1 dots
        terms = format.split(".")
        if terms:
            if len(terms) == 1:
                return terms[0], ""
            elif len(terms) == 2:
                return terms[0], terms[1]
        raise ValueError("Could not understand format specification %r" % (format,))
        
    if source is None:
        # Read from stdin
        filename = None
    elif isinstance(source, basestring):
        # This is a filename
        filename = source
    elif hasattr(source, "read"):
        # This is a Python file object
        filename = getattr(source, "name", None)
    else:
        raise ValueError("Unsupported source type %r" % (source,))

    if filename is None:
        # Reading from stdin or an unnamed file-like object with no
        # specified format. Not going to sniff the input. Instead, just
        return default

    return _determine_format_from_filename(filename, default)
        


def normalize_output_format(destination, format, default=("fps", "")):
    if format is not None:
        # Either 0 or 1 dots
        terms = format.split(".")
        if terms:
            if len(terms) == 1:
                return terms[0], ""
            elif len(terms) == 2:
                return terms[0], terms[1]
        raise ValueError("Could not understand format specification %r" % (format,))
    
    if destination is None:
        # Write to stdout
        filename = None
    elif isinstance(destination, (str, unicode)):
        # This is a filename
        filename = destination
    elif hasattr(destination, "write"):
        # This is a Python file object
        filename = getattr(destination, "name", None)
    else:
        raise ValueError("Unknown destination type %r" % (destination,))

    if filename is None:
        # Writing to stdout or an unnamed file-like object with no
        # specified format.
        return default
        
    return _determine_format_from_filename(filename, default)


def get_filename(source):
    if source is None:
        return None
    elif isinstance(source, basestring):
        return source
    else:
        return getattr(source, "name", None)

####

def _do_nothing():
    pass

def open_binary_output(destination, blame_name=None):
    if destination is None:
        return sys.stdout, _do_nothing
    if not isinstance(destination, basestring):
        return destination, _do_nothing
    base, ext = os.path.splitext(destination)
    ext = ext.lower()
    if ext not in _compression_extensions:
        f = open(destination, "wb")
        close = f.close
    else:
        f, close = open_compressed_output(destination, _compression_extensions[ext], blame_name)
    return f, close

def open_compressed_output(destination, compression, blame_name):
    # Raises a ValueError if the compression isn't supported
    if not compression:
        if destination is None:
            return sys.stdout, _do_nothing
        elif isinstance(destination, basestring):
            f = open(destination, "wb")
            return f, f.close
        else:
            return destination, _do_nothing

    if compression == "gz":
        import gzip
        if destination is None:
            f = gzip.GzipFile(mode="wb", fileobj=sys.stdout)
        elif isinstance(destination, basestring):
            f = gzip.open(destination, "wb")
        else:
            f = gzip.GzipFile(mode="wb", fileobj=destination)
        return f, f.close

    if compression == "bz2":
        try:
            import bz2
        except ImportError as err:
            raise ValueError("Please install the bz2 module for bzip2 compression support")
        
        if destination is None:
            if not os.path.exists("/dev/stdout"):
                raise ValueError("Python's bz2 library cannot write compressed data to stdout "
                               "on this platform")
            f = bz2.BZ2File("/dev/stdout", "wb")
        elif isinstance(destination, basestring):
            f = bz2.BZ2File(destination, "wb")
        else:
            raise ValueError("Python's bz2 library does not support writing to a file object")
        return f, f.close

    if compression == "xz":
        raise ValueError("chemfp does not yet support xz compression")

    if blame_name is None:
        raise ValueError("Unsupported compression type %r" % (compression,))
    else:
        raise ValueError("%s does not support compression type %r" % (blame_name, compression))

# The chemfp-1.1 release used 'open_compressed_input_universal' for all text input.
# This lets Python normalize "\n" or "\r\n" to "\n".
#
# However, the chemfp C extension for FPS parsing handles both newline
# conventions, and there's overhead for double-conversion. On my
# benchmark of 1M PubChem fingerprints.
#
# simsearch using --memory: 11% faster
#   Universal: 5.34, 5.22, 5.22  (chemfp-1.1)
#        byte: 4.72, 4.67, 4.79  (chemfp-1.3)
# simsearch using --scan: 40% faster
#   Universal: 1.35, 1.46, 1.45  (chemfp-1.1)
#        byte: 0.90, 0.81, 0.93  (chemfp-1.3)
# Using sum(1 for _ in chemfp.open("pubchem_million.fps")): 20% faster
#   Universal: 2.36, 2.35, 2.58  (chemfp-1.1)
#        byte: 1.87, 2.02, 2.02  (chemfp-1.3)
# Using chemfp.load_fingerprints("pubchem_million.fps"): 14% faster
#   Universal: 5.30, 5.18, 5.25  (chemfp-1.1)
#        byte: 4.43, 4.65, 4.67  (chemfp-1.3)

def open_compressed_input(source, compression, blame_name):
    if not compression:
        if source is None:
            return sys.stdin, _do_nothing
        elif isinstance(source, basestring):
            f = open(source, "rb")
            return f, f.close
        else:
            return source, _do_nothing

    if compression == "gz":
        import gzip
        if source is None:
            f = gzip.GzipFile(fileobj=sys.stdin)
        elif isinstance(source, basestring):
            f = gzip.open(source, "rb")
        else:
            f = gzip.GzipFile(mode="rb", fileobj=source)
        return f, f.close

    if compression == "bz2":
        try:
            import bz2
        except ImportError as err:
            raise ValueError("Please install the bz2 module for bzip2 compression support")
        if source is None:
            # bz2 doesn't support Python objects. On some platforms
            # I can work around the problem
            if not os.path.exists("/dev/stdin"):
                raise NotImplementedError("Cannot compressed bzip2 data from stdin on this platform")
            f = bz2.BZ2File("/dev/stdin", "rb")
        elif isinstance(source, basestring):
            f = bz2.BZ2File(source, "rb")
        else:
            # Well, I could emulate it, but I'm not going to
            raise NotImplementedError("bzip decompression from file-like objects is not supported")
        return f, f.close

    if compression == "xz":
        raise NotImplementedError("xz decompression is not supported")

    if blame_name is None:
        raise ValueError("Unsupported compression type %r" % (compression,))
    else:
        raise ValueError("%s does not support compression type %r" % (blame_name, compression))


def write_fps1_magic(outfile):
    outfile.write("#FPS1\n")

def write_fps1_header(outfile, metadata):
    if metadata is None:
        return 0
    lines = []
    if metadata.num_bits is not None:
        lines.append("#num_bits=%d\n" % metadata.num_bits)

    if metadata.type is not None:
        assert "\n" not in metadata.type
        lines.append("#type=" + metadata.type.encode("ascii")+"\n") # type cannot contain non-ASCII characters

    if metadata.software is not None:
        assert "\n" not in metadata.software
        lines.append("#software=" + metadata.software.encode("utf8")+"\n")

    if metadata.aromaticity is not None:
        lines.append("#aromaticity=" + metadata.aromaticity.encode("ascii") + "\n")

    for source in metadata.sources:
        # Ignore newlines in the source filename, if present
        source = source.replace("\n", "")
        lines.append("#source=" + source.encode("utf8")+"\n")

    if metadata.date is not None:
        lines.append("#date=" + metadata.date.encode("ascii")+"\n") # date cannot contain non-ASCII characters

    outfile.writelines(lines)
    return len(lines)

def write_fps1_fingerprint(outfile, fp, id):
    if "\t" in id:
        raise ValueError("Fingerprint ids must not contain a tab: %r" % (id,))
    if "\n" in id:
        raise ValueError("Fingerprint ids must not contain a newline: %r" % (id,))
    if not id:
        raise ValueError("Fingerprint ids must not be the empty string")
    
    outfile.write("%s\t%s\n" % (binascii.hexlify(fp), id))


# This is a bit of a hack. If I open a file then I want to close it,
# but if I use stdout then I don't want to close it.

## class _closing_output(object):
##     def __init__(self, destination):
##         self.destination = destination
##         self.output = open_output(destination)
##     def __enter__(self):
##         return self.output
##     def __exit__(self, *exec_info):
##         if isinstance(self.destination, basestring):
##             self.output.close()

## def write_fps1_output(reader, destination, metadata=None):
##     if metadata is None:
##         metadata = reader.metadata
##     hexlify = binascii.hexlify
##     with _closing_output(destination) as outfile:
##         with ignore_pipe_errors:
##             write_fps1_magic(outfile)
##             write_fps1_header(outfile, metadata)

##             for i, (id, fp) in enumerate(reader):
##                 if "\t" in id:
##                     raise ValueError("Fingerprint ids must not contain a tab: %r in record %d" %
##                                      (id, i+1))
##                 if "\n" in id:
##                     raise ValueError("Fingerprint ids must not contain a newline: %r in record %d" %
##                                      (id, i+1))
##                 if not id:
##                     raise ValueError("Fingerprint ids must not be the empty string in record %d" %
##                                      (i+1,))
##                 outfile.write("%s\t%s\n" % (hexlify(fp), id))


_where_template = {
    (0, 0, 0): "<unknown position>",
    (0, 0, 1): "record #%(recno)d",
    (0, 1, 0): "line %(lineno)d",
    (0, 1, 1): "line %(lineno)d, record #%(recno)d",
    (1, 0, 0): "file %(filename)r",
    (1, 0, 1): "file %(filename)r, record #%(recno)d",
    (1, 1, 0): "file %(filename)r, line %(lineno)d",
    (1, 1, 1): "file %(filename)r, line %(lineno)d, record #%(recno)d",
    }

class Location(object):
    """Get location and other internal reader and writer state information

    A Location instance gives a way to access information like
    the current record number, line number, and molecule object.::

      >>> import chemfp
      >>> with chemfp.read_molecule_fingerprints("RDKit-MACCS166",
      ...                        "ChEBI_lite.sdf.gz", id_tag="ChEBI ID") as reader:
      ...   for id, fp in reader:
      ...     if id == "CHEBI:3499":
      ...         print("Record starts at line", reader.location.lineno)
      ...         print("Record byte range:", reader.location.offsets)
      ...         print("Number of atoms:", reader.location.mol.GetNumAtoms())
      ...         break
      ... 
      [08:18:12]  S group MUL ignored on line 103
      Record starts at line 3599
      Record byte range: (138171, 141791)
      Number of atoms: 36

    The supported properties are:

      * filename - a string describing the source or destination
      * lineno - the line number for the start of the file
      * mol - the toolkit molecule for the current record
      * offsets - the (start, end) byte positions for the current record
      * output_recno - the number of records written successfully
      * recno - the current record number
      * record - the record as a text string
      * record_format - the record format, like "sdf" or "can"
       

    Most of the readers and writers do not support all of the properties.
    Unsupported properties return a None. The *filename* is a read/write
    attribute and the other attributes are read-only.
    
    If you don't pass a location to the readers and writers then they will
    create a new one based on the source or destination, respectively.
    You can also pass in your own Location, created as ``Location(filename)``
    if you have an actual filename, or ``Location.from_source(source)`` or
    ``Location.from_destination(destination)`` if you have a more generic
    source or destination.

    """
    _get_recno = None
    _get_output_recno = None
    _get_lineno = None
    _get_offsets = None
    _get_mol = None
    _get_record = None
    _record_format = None
    
    def __init__(self, filename=None):
        """Use *filename* as the location's filename"""
        self.filename = filename

    def __repr__(self):
        """Return a string like 'Location("<stdout>")'"""
        return "Location(%r)" % (self.filename,)

    def where(self):
        """Return a human readable description about the current reader or writer state.

        The description will contain the filename, line number, record
        number, and up to the first 40 characters of the first line of
        the record, if those properties are available.
        """
        filename = self.filename
        lineno = self.lineno
        recno = self.recno

        template = _where_template[ (filename is not None, lineno is not None, recno is not None) ]
        s = template % {"filename": filename, "lineno": lineno, "recno": recno}

        first_line = self.first_line

        if first_line:  # Don't show None and don't show blank lines
            if len(first_line) > 40:
                t = repr(first_line[:40])
                t = t[:-1] + " ..." + t[-1]
                s += ": first line starts %s" % (t,)
            else:
                s += ": first line is %s" % (repr(first_line),)
        return s

    @classmethod
    def from_source(cls, source):
        """Create a Location instance based on the source

        If *source* is a string then it's used as the filename.
        If *source* is None then the location filename is "<stdin>".
        If *source* is a file object then its ``name`` attribute
        is used as the filename, or None if there is no attribute.
        """
        if source is None:
            return cls("<stdin>")
        if isinstance(source, basestring):
            return cls(source)
        return cls(getattr(source, "name", None))

    @classmethod
    def from_destination(cls, destination):
        """Create a Location instance based on the destination
        
        If *destination* is a string then it's used as the filename.
        If *destination* is None then the location filename is "<stdout>".
        If *destination* is a file object then its ``name`` attribute
        is used as the filename, or None if there is no attribute.
        """
        if destination is None:
            return cls("<stdout>")
        if isinstance(destination, basestring):
            return cls(destination)
        return cls(getattr(destination, "name", None))


    def clear_registry(self):
        """Part of the internal API, and subject to change."""
        self._get_recno = None
        self._get_output_recno = None
        self._get_lineno = None
        self._get_offsets = None
        self._get_mol = None
        self._get_record = None

    def register(self, **kwargs):
        """Part of the internal API, and subject to change."""
        for k, v in kwargs.items():
            if k in ("get_recno", "get_output_recno", "get_lineno", "get_offsets", "get_mol", "get_record"):
                setattr(self, "_" + k, v)
            else:
                raise KeyError(k)

    def save(self, **kwargs):
        """Part of the internal API, and subject to change."""
        for k, v in kwargs.items():
            if k in ("recno", "output_recno", "lineno", "offsets", "mol", "record"):
                def recall_value(value=v):
                    return value
                setattr(self, "_get_" + k, recall_value)
            elif k == "record_format":
                self._record_format = v
            else:
                raise KeyError(k)

    def get_registry(self):
        """Part of the internal API, and subject to change."""
        return {"get_recno": self._get_recno,
                "get_output_recno": self._get_output_recno,
                "get_lineno": self._get_lineno,
                "get_offsets": self._get_offsets,
                "get_mol": self._get_mol,
                "get_record": self._get_record,
                }

    @property
    def recno(self):
        """The current record number

        For writers this is the number of records sent to
        the writer, and output_recno is the number of records
        sucessfully written to the file or string.
        """
        _get_recno = self._get_recno
        if _get_recno is None:
            return None
        return _get_recno()

    @property
    def output_recno(self):
        """The number of records actually written to the file or string.

        The value ``recno - output_recno`` is the number of records
        sent to the writer but which had an error and could not be
        written to the output.
        """
        _get_output_recno = self._get_output_recno
        if _get_output_recno is None:
            return None
        return _get_output_recno()

    @property
    def lineno(self):
        """The current line number, starting from 1"""
        _get_lineno = self._get_lineno
        if _get_lineno is None:
            return None
        return _get_lineno()

    @property
    def offsets(self):
        """The (start, end) byte offsets, starting from 0

        *start* is the record start byte position and *end* is
        one byte past the last byte of the record.
        """
        _get_offsets = self._get_offsets
        if _get_offsets is None:
            return None
        return _get_offsets()

    @property
    def mol(self):
        """The molecule object for the current record"""
        _get_mol = self._get_mol
        if _get_mol is None:
            return None
        return _get_mol()

    @property
    def record(self):
        """The current record as an uncompressed text string"""
        _get_record = self._get_record
        if _get_record is None:
            return None
        return _get_record()

    @property
    def record_format(self):
        """The record format name"""
        return self._record_format

    @property
    def first_line(self):
        """The first line of the current record"""
        _get_record = self._get_record
        if _get_record is None:
            return None
        record = _get_record()
        if record is None:
            return None
        first_line, _, _ = record.partition(b"\n")
        return first_line
        #return first_line.rstrip(b"\r").decode("utf8", errors="replace")

    @property
    def first_line_bytes(self):
        """The first line of the current record"""
        _get_record = self._get_record
        if _get_record is None:
            return None
        record = _get_record()
        if record is None:
            return None
        first_line, _, _ = record.partition(b"\n")
        return first_line.rstrip(b"\r")
        

    def get_info(self):
        """Part of the internal API, and subject to change."""
        d = {}
        for k, v in self.get_registry().items():
            if v is not None:
                d[k] = v
        return d


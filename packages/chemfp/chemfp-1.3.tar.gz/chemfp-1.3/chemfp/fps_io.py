# Copyright (c) 2010-2017 Andrew Dalke Scientific, AB (Sweden)
# See the contents of "chemfp/__init__.py" for full license details.

from __future__ import absolute_import, print_function

from cStringIO import StringIO
from __builtin__ import open as _builtin_open
import binascii
import _chemfp
import re
import sys
import heapq
import itertools
from binascii import hexlify as _hexlify

from . import Metadata, ParseError, FingerprintReader, FingerprintWriter
from . import fps_search
from . import io

# I tried a wide range of sizes for my laptop, with both compressed
# and uncompressed files, and found that the best size was around
# 2**17. Actually, 2**16.8 was the absolute best, which gives
BLOCKSIZE=11400
# (BTW, the compressed time took 1.3x the uncompressed time)

def open_fps(source, format_name, compression, location=None):
    if format_name != "fps":
        raise ValueError("Unknown format %r" % (format_name,))

    infile, close = io.open_compressed_input(source, compression, "chemfp")
    if location is None:
        location = io.Location.from_source(source)
    #filename = io.get_filename(source)
    metadata, block = read_header(infile, location)
    return FPSReader(infile, close, metadata, location, block)


# This never buffers
def _read_blocks(infile):
    while 1:
        block = infile.read(BLOCKSIZE)
        if not block:
            break
        if block[-1:] == "\n":
            yield block
            continue
        line = infile.readline()
        if not line:
            # Note: this might not end with a newline!
            yield block
            break
        yield block + line

            

class FPSReader(FingerprintReader):
    """FPS file reader

    This class implements the :class:`chemfp.FingerprintReader` API. It
    is also its own a context manager, which automatically closes the
    file when the manager exists.

    The public attributes are:

    .. py:attribute:: metadata

       a :class:`chemfp.Metadata` instance with information about the fingerprint type
       
    .. py:attribute:: location

       a :class:`chemfp.io.Location` instance with parser location and state information
       
    .. py:attribute:: closed

       True if the file is open, else False
    
    The FPSReader.location only tracks the "lineno" variable.
    """
    _search = fps_search
    def __init__(self, infile, close, metadata, location, first_fp_block):
        self._infile = infile
        self._close = close
        self._filename = getattr(infile, "name", "<unknown>")
        self.metadata = metadata
        self.location = location
        self._first_fp_block = first_fp_block
        if metadata.num_bytes is None:
            self._expected_hex_len = 0
        else:
            self._expected_hex_len = 2*metadata.num_bytes
        self._hex_len_source = "size in header"

        self._at_start = True
        self._it = None
        self._block_reader = None
        self._iter = None

        self._record_iter = None

        self.closed = False

    def close(self):
        """Close the file"""
        if self._close is not None:
            self._close()
        self.closed = True

    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.close()
    
    def iter_blocks(self):
        """This is not part of the public API"""
        if self._block_reader is None:
            self._block_reader = iter(self._iter_blocks())
        return self._block_reader

    def _iter_blocks(self):
        if not self._at_start:
            raise TypeError("Already iterating")
        
        self._at_start = False

        if self._first_fp_block is None:
            return
        
        block_stream = _read_blocks(self._infile)
        yield self._first_fp_block
        for block in block_stream:
            yield block

    def iter_rows(self):
        """This is not part of the public API"""
        unhexlify = binascii.unhexlify
        expected_hex_len = self._expected_hex_len
        
        location = self.location
        lineno = location.lineno
        def get_lineno():
            return lineno
        location.register(get_lineno=get_lineno)
            
        try:
            for block in self.iter_blocks():
                for line in block.splitlines(True):
                    lineno += 1
                    err = _chemfp.fps_line_validate(expected_hex_len, line)
                    if err:
                        raise ParseError(_chemfp.strerror(err), location)
                    yield line[:-1].split(b"\t")
        finally:
            location.save(lineno=lineno)

    def __next__(self):
        if self._record_iter is None:
            self._record_iter = self._make_record_iter()
        return next(self._record_iter)

    def next(self):
        "Return the next (id, fp) pair"
        if self._record_iter is None:
            self._record_iter = self._make_record_iter()
        return next(self._record_iter)
        

    def __iter__(self):
        "Iterate through the (id, fp) pairs"
        if self._record_iter is None:
            self._record_iter = iter(self._make_record_iter())
        return self._record_iter

    def _make_record_iter(self):
        unhexlify = binascii.unhexlify
        expected_hex_len = self._expected_hex_len
        
        location = self.location
        lineno = location.lineno
        def get_lineno():
            return lineno
        location.register(get_lineno=get_lineno)

        try:
            for block in self.iter_blocks():
                for line in block.splitlines(True):
                    lineno += 1
                    err, id_fp = _chemfp.fps_parse_id_fp(expected_hex_len, line)
                    if err:
                        # Include the line?
                        raise ParseError(_chemfp.strerror(err), location)
                    yield id_fp
        finally:
            location.save(lineno=lineno)

    def _check_at_start(self):
        if not self._at_start:
            raise TypeError("FPS file is not at the start of the file; cannot search")


    def count_tanimoto_hits_fp(self, query_fp, threshold=0.7):
        """Count the fingerprints which are sufficiently similar to the query fingerprint

        Return the number of fingerprints in the reader which are
        at least *threshold* similar to the query fingerprint *query_fp*.

        :param query_fp: query fingerprint
        :type query_fp: byte string
        :param threshold: minimum similarity threshold (default: 0.7)
        :type threshold: float between 0.0 and 1.0, inclusive
        :returns: integer count
        """
        self._check_at_start()
        return fps_search.count_tanimoto_hits_fp(query_fp, self, threshold)

    def count_tanimoto_hits_arena(self, queries, threshold=0.7):
        """Count the fingerprints which are sufficiently similar to each query fingerprint

        Returns a list containing a count for each query fingerprint
        in the *queries* arena. The count is the number of
        fingerprints in the reader which are at least *threshold*
        similar to the query fingerprint.

        The order of results is the same as the order of the queries.
        
        :param queries: query fingerprints
        :type queries: a :class:`.FingerprintArena`
        :param threshold: minimum similarity threshold (default: 0.7)
        :type threshold: float between 0.0 and 1.0, inclusive
        :returns: list of integer counts, one for each query
        """
        self._check_at_start()
        return fps_search.count_tanimoto_hits_arena(queries, self, threshold)

    def threshold_tanimoto_search_fp(self, query_fp, threshold=0.7):
        """Find the fingerprints which are sufficiently similar to the query fingerprint

        Find all of the fingerprints in this reader which are at least
        *threshold* similar to the query fingerprint *query_fp*.  The
        hits are returned as a :class:`.SearchResult`, in arbitrary
        order.
        
        :param query_fp: query fingerprint
        :type query_fp: byte string
        :param threshold: minimum similarity threshold (default: 0.7)
        :type threshold: float between 0.0 and 1.0, inclusive
        :returns: a :class:`.SearchResult`
        """
        self._check_at_start()
        return fps_search.threshold_tanimoto_search_fp(query_fp, self, threshold)

    def threshold_tanimoto_search_arena(self, queries, threshold=0.7):
        """Find the fingerprints which are sufficiently similar to each of the query fingerprints

        For each fingerprint in the *queries* arena, find all of the
        fingerprints in this arena which are at least *threshold*
        similar. The hits are returned as a :class:`.SearchResults`,
        where the hits in each :class:`.SearchResult` is in arbitrary
        order.

        :param queries: query fingerprints
        :type queries: a :class:`.FingerprintArena`
        :param threshold: minimum similarity threshold (default: 0.7)
        :type threshold: float between 0.0 and 1.0, inclusive
        :returns: a :class:`.SearchResults`
        """
        self._check_at_start()
        return fps_search.threshold_tanimoto_search_arena(queries, self, threshold)

    def knearest_tanimoto_search_fp(self, query_fp, k=3, threshold=0.7):
        """Find the k-nearest fingerprints which are sufficiently similar to the query fingerprint

        Find all of the fingerprints in this reader which are at least
        *threshold* similar to the query fingerprint, and of those, select
        the top *k* hits. The hits are returned as a :class:`.SearchResult`,
        sorted from highest score to lowest.

        :param queries: query fingerprints
        :type queries: a :class:`.FingerprintArena`
        :param threshold: minimum similarity threshold (default: 0.7)
        :type threshold: float between 0.0 and 1.0, inclusive
        :returns: a :class:`.SearchResult`
        """
        self._check_at_start()
        return fps_search.knearest_tanimoto_search_fp(query_fp, self, k, threshold)

    def knearest_tanimoto_search_arena(self, queries, k=3, threshold=0.7):
        """Find the k-nearest fingerprints which are sufficiently similar to each of the query fingerprints

        For each fingerprint in the *queries* arena, find the
        fingerprints in this reader which are at least *threshold*
        similar to the query fingerprint, and of those, select the top
        *k* hits. The hits are returned as a :class:`.SearchResults`,
        where the hits in each :class:`.SearchResult` are sorted by
        similarity score.

        :param queries: query fingerprints
        :type queries: a :class:`.FingerprintArena`
        :param threshold: minimum similarity threshold (default: 0.7)
        :type threshold: float between 0.0 and 1.0, inclusive
        :returns: a :class:`.SearchResults`
        """
        self._check_at_start()
        return fps_search.knearest_tanimoto_search_arena(queries, self, k, threshold)

def open_output(destination, metadata, compression="", errors="strict", location=None):
    output, close = io.open_compressed_output(destination, compression, "chemfp")
    io.write_fps1_magic(output)
    initial_lineno = 1 + io.write_fps1_header(output, metadata)
    error_handler = io.get_parse_error_handler(errors)

    if location is None:
        location = io.Location.from_destination(destination)
    writer = _fps_writer_gen(output, close, error_handler, location, initial_lineno)
    assert next(writer) == "Ready!" # prime the generator
    
    return FPSWriter(output, writer, metadata, location)

def _fps_writer_gen(output, close, error_handler, location, initial_lineno):
    hexlify = _hexlify
    recno = 0
    output_recno = 0
    def get_recno():
        return recno
    def get_output_recno():
        return output_recno
    def get_lineno():
        return initial_lineno + output_recno
    location.register(get_recno=get_recno, get_output_recno=get_output_recno, get_lineno=get_lineno)
    errno = 0
    try:
        yield_value = "Ready!"
        num_fp_bytes = -1
        while 1:
            id_fp_pairs = (yield yield_value)
            try:
                for id, fp in id_fp_pairs:
                    recno += 1
                    ### Check for illegal characters.
                    if "\t" in id:
                        error_handler.error("Unable to write an identifier containing a tab: %r" % (id,),
                                            location)
                        continue
                    if "\n" in id:
                        error_handler.error("Unable to write an identifier containing a newline: %r" % (id,),
                                            location)
                        continue
                    if not id:
                        error_handler.error("Unable to write a fingerprint with an empty identifier",
                                            location)
                        continue
                    
                    output.write(_hexlify(fp) + "\t" + id + "\n")
                    
                    output_recno += 1
            except Exception as err:
                yield_value = err, sys.exc_info()[2]
            else:
                yield_value = None
                
    finally:
        location.save(recno=get_recno(), output_recno=get_output_recno(), lineno=get_lineno())
        if close is not None:
            try:
                close()
            finally:
                close = None
        
class FPSWriter(FingerprintWriter):
    """Write fingerprints in FPS format.

    This is a subclass of :class:`chemfp.FingerprintWriter`.

    Instances have the following attributes:

    * metadata - a :class:`chemfp.Metadata` instance
    * closed - False when the file is open, else True
    * location - a :class:`chemfp.io.Location` instance

    An FPSWriter is its own context manager, and will close the
    output file on context exit.

    The Location instance supports the "recno", "output_recno",
    and "lineno" properties.
    """
    def __init__(self, output, writer, metadata, location=None):
        "The constructor is not part of the public API"
        self._output = output # Should this be public?
        self._writer = writer
        self.metadata = metadata
        self.location = location
        self.closed = False

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        """Close the writer

        This will set self.closed to False.
        """
        if not self.closed:
            self.closed = True
            self._writer.close()


    def write_fingerprint(self, id, fp):
        """Write a single fingerprint record with the given id and fp

        :param string id: the record identifier
        :param bytes fp: the fingerprint
        """
        if self.closed:
            raise ValueError("Cannot write a fingerprint after calling close()")
        err = self._writer.send( [(id, fp)] )
        if err is not None:
            raise err[0], None, err[1]

    def write_fingerprints(self, id_fp_pairs):
        """Write a sequence of fingerprint records

        :param id_fp_pairs: An iterable of (id, fingerprint) pairs.
        """
        if self.closed:
            raise ValueError("Cannot write fingerprints after calling close()")
        err = self._writer.send(id_fp_pairs)
        if err is not None:
            raise err[0], None, err[1]



def read_header(f, location):
    #metadata = Metadata()
    num_bits = None
    num_bytes = None
    software = None
    type = None
    sources = []
    date = None
    aromaticity = None

    location.save(lineno=0)

    def error(errmsg):
        location.save(lineno=lineno+1)
        return ParseError(errmsg, location=location)

    lineno = 0
    for block in _read_blocks(f):
        # A block must be non-empty
        start = 0
        while 1:
            c = block[start:start+1]
            if c == b"":
                # End of the block; get the next one
                break
            if c != b'#':
                # End of the header. This block contains the first fingerprint line
                block = block[start:]
                if num_bits is None:
                    if num_bytes is None:
                        # We can figure this out from the fingerprint on the first line
                        err = _chemfp.fps_line_validate(-1, block)
                        if err:
                            if err == -36: # CHEMFP_MISSING_NEWLINE
                                # The block does not end with a newline.
                                # Figure out the correct line number for that line.
                                lineno += block.count(b"\n")
                            raise error(_chemfp.strerror(err))
                        i = block.index(b"\t")
                        # If you don't specify the number of bits then I'll do it for you.
                        num_bits = i * 4
                        num_bytes = i // 2
                    else:
                        num_bits = num_bytes * 8
                else:
                    if num_bytes is None:
                        num_bytes = (num_bits+7) // 8
                    else:
                        # Already validated this case when the values were set.
                        pass

                location.save(lineno=lineno)
                return Metadata(num_bits, num_bytes, type, aromaticity, software,
                                sources, date), block

            start += 1 # Skip the '#'
            end = block.find(b"\n", start)
            if end == -1:
                raise error(_chemfp.strerror(-36)) # CHEMFP_MISSING_NEWLINE
                ## # Only happens when the last line of the file contains
                ## # no newlines. In that case, we're at the last block.
                ## line = block[start:]
                ## start = len(block)
            else:
                line = block[start:end]
                start = end+1

            # Right! We've got a line. Check if it's magic
            # This is the only line which cannot contain a '='
            if lineno == 0:
                if line == b"FPS1" or line == b"#FPS1\r":
                    lineno += 1
                    continue

            if line.startswith(b"x-") or line.startswith(b"X-"):
                # Completely ignore the contents of 'experimental' lines
                continue

            if b"=" not in line:
                raise error("header line must contain an '=': %r" % (line,))
            key, value = line.split(b"=", 1)
            key = key.strip()
            value = value.strip()
            if key == b"num_bits":
                if num_bits is not None:
                    raise error("Only one num_bits header is allowed")
                try:
                    num_bits = int(value)
                    if num_bits <= 0:
                        raise ValueError
                except ValueError:
                    raise error("num_bits header must be a positive integer, not %r" % (value,))

                if num_bytes is not None:
                    n = (num_bits+7)//8
                    if n != num_bytes:
                        raise error(
                            "The num_bits header of %d requires %d bytes, which is "
                            "incompatible with the earlier num_bytes header of %d"
                            %  (num_bits, n, num_bytes))
                                        
            elif key == b"num_bytes":
                if num_bytes is not None:
                    raise error("Only one num_bytes header is allowed")
                try:
                    num_bytes = int(value)
                    if num_bytes <= 0:
                        raise ValueError
                except ValueError:
                    raise error(
                        "num_bytes header must be a positive integer, not %r" % (value,))
                if num_bits is not None:
                    n = (num_bits+7)//8
                    if n != num_bytes:
                        raise error(
                            "The num_bytes header of %d is incompatible with the "
                            "earlier num_bits header of %d, which requires %d bytes"
                            % (num_bytes, num_bits, n))
                            
            elif key == b"software":
                if software is not None:
                    raise error("Only one software header is allowed")
                try:
                    software = value.decode("utf8")
                except UnicodeDecodeError as err:
                    raise error("software header must be utf8 encoded: %r (%s)" % (value, err))
            elif key == b"type":
                if type is not None:
                    raise error("Only one type header is allowed")
                # Should I have an auto-normalization step here which
                # removes excess whitespace?
                #type = normalize_type(value)
                try:
                    type = value.decode("ascii")
                except UnicodeDecodeError as err:
                    raise error("type header must be ASCII encoded: %r (%s)" % (value, err))
            elif key == b"source":
                sources.append(value.decode("utf8", "surrogateescape"))
            elif key == b"date":
                if date is not None:
                    raise error("Only one date header is allowed")
                try:
                    date = value.decode("ascii")
                except UnicodeDecodeError as err:
                    raise error("date header must be ASCII encoded: %r (%s)" % (value, err))
            elif key == b"aromaticity":
                if aromaticity is not None:
                    raise error("Only one aromaticity header is allowed")
                try:
                    aromaticity = value.decode("ascii")
                except UnicodeDecodeError as err:
                    raise error("aromaticity header must be ASCII encoded: %r (%s)" % (value, err))
            elif key.startswith(b"x-"):
                pass
            else:
                # In the interests of forward compatibility, I ignore unknown headers.
                # XXX Should I give a warning? A log message? How does someone help
                # figure out if there's a typo?
                #print "UNKNOWN", repr(line), repr(key), repr(value)
                #warn(filename, lineno, "Unknown header %r" % (value,))
                pass
            lineno += 1

    # Reached the end of file. No fingerprint lines and nothing left to process.
    if num_bits is None:
        if num_bytes is None:
            num_bits = None
            num_bytes = None
        else:
            num_bits = num_bytes*8
    else:
        if num_bytes is None:
            num_bytes = (num_bits+7)//8
        else:
            # Already verified this case when the values were first set.
            pass

    location.save(lineno=lineno)
    return Metadata(num_bits, num_bytes, type, aromaticity, software,
                    sources, date), None


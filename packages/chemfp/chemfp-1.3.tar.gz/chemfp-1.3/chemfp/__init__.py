# Library for working with cheminformatics fingerprints

# All chemfp software is distributed with the following license:

# Copyright (c) 2010-2017 Andrew Dalke Scientific, AB (Sweden)
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

__version__ = "1.3"
__version_info = (1, 3, 0)
SOFTWARE = "chemfp/" + __version__

import os
import itertools

__all__ = [
        "ChemFPError",
        "ChemFPProblem",
        "FingerprintIterator",
        "FingerprintReader",
        "Fingerprints",
        "Metadata",
        "ParseError",
        "check_fingerprint_problems",
        "check_metadata_problems",
        "count_tanimoto_hits",
        "count_tanimoto_hits_symmetric",
        "get_max_threads",
        "get_num_threads",
        "knearest_tanimoto_search",
        "knearest_tanimoto_search_symmetric",
        "load_fingerprints",
        "open",
        "open_fingerprint_writer",
        "set_num_threads",
        "threshold_tanimoto_search",
        "threshold_tanimoto_search_symmetric",
        ]
           

class ChemFPError(Exception):
    """Base class for all of the chemfp exceptions"""
    pass

class ParseError(ChemFPError, ValueError):
    """Exception raised by the molecule and fingerprint parsers and writers

    The public attributes are:

    .. py:attribute:: msg

       a string describing the exception

    .. py:attribute:: location

       a :class:`chemfp.io.Location` instance, or None
    
    """
    def __init__(self, msg, location=None):
        self.msg = msg
        self.location = location
        
    def __str__(self):
        if self.location is None:
            return str(self.msg)
        else:
            return "%s, %s" % (self.msg, self.location.where())

def read_structure_fingerprints(type, source=None, format=None, id_tag=None, reader_args=None, errors="strict"):
    """Deprecated function. Please call read_molecule_fingerprints() instead

    The function named changed in chemfp 2.0 to read_molecule_fingerprints()
    because it was a better fit to the toolkit API. Chemfp-1.3 maintains
    backwards compatibility with chemfp-1.1, so the function remains.
    It forwards the call the correct function.
    
    :param type: information about how to convert the input structure into a fingerprint
    :type type: string or Metadata
    :param source: The structure data source.
    :type source: A filename (as a string), a file object, or None to read from stdin
    :param format: The file format and optional compression.
            Examples: 'smi' and 'sdf.gz'
    :type format: string, or None to autodetect based on the source
    :param id_tag: The tag containing the record id. Example: 'ChEBI ID'.
            Only valid for SD files.
    :type id_tag: string, or None to use the default title for the given format
    :returns: a FingerprintReader
    """
    import warnings
    warnings.warn("chemfp.read_structure_fingerprints() has been renamed to read_molecule_fingerprints()")
    return read_molecule_fingerprints(type, source, format, id_tag, reader_args, errors="strict")
    
    
def read_molecule_fingerprints(type, source=None, format=None, id_tag=None, reader_args=None, errors="strict"):
    """Read structures from 'source' and return the corresponding ids and fingerprints

    This returns a FingerprintReader which can be iterated over to get
    the id and fingerprint for each read structure record. The
    fingerprint generated depends on the value of 'type'. Structures
    are read from 'source', which can either be the structure
    filename, or None to read from stdin.

    'type' contains the information about how to turn a structure
    into a fingerprint. It can be a string or a metadata instance.
    String values look like "OpenBabel-FP2/1", "OpenEye-Path", and
    "OpenEye-Path/1 min_bonds=0 max_bonds=5 atype=DefaultAtom btype=DefaultBond".
    Default values are used for unspecified parameters. Use a
    Metadata instance with 'type' and 'aromaticity' values set
    in order to pass aromaticity information to OpenEye.

    If 'format' is None then the structure file format and compression
    are determined by the filename's extension(s), defaulting to
    uncompressed SMILES if that is not possible. Otherwise 'format' may
    be "smi" or "sdf" optionally followed by ".gz" or "bz2" to indicate
    compression. The OpenBabel and OpenEye toolkits also support
    additional formats.
    
    If 'id_tag' is None, then the record id is based on the title
    field for the given format. If the input format is "sdf" then 'id_tag'
    specifies the tag field containing the identifier. (Only the first
    line is used for multi-line values.) For example, ChEBI omits the
    title from the SD files and stores the id after the ">  <ChEBI ID>"
    line. In that case, use id_tag = "ChEBI ID".

    'aromaticity' specifies the aromaticity model, and is only appropriate for
    OEChem. It must be a string like "openeye" or "daylight".

    Here is an example of using fingerprints generated from structure file::
    
        fp_reader = read_molecule_fingerprints("OpenBabel-FP4/1", "example.sdf.gz")
        print "Each fingerprint has", fps.metadata.num_bits, "bits"
        for (id, fp) in fp_reader:
           print id, fp.encode("hex")


    :param type: information about how to convert the input structure into a fingerprint
    :type type: string or Metadata
    :param source: The structure data source.
    :type source: A filename (as a string), a file object, or None to read from stdin
    :param format: The file format and optional compression.
            Examples: 'smi' and 'sdf.gz'
    :type format: string, or None to autodetect based on the source
    :param id_tag: The tag containing the record id. Example: 'ChEBI ID'.
            Only valid for SD files.
    :type id_tag: string, or None to use the default title for the given format
    :returns: a FingerprintReader

    """ # ' # emacs cruft
    from . import types
    if isinstance(type, basestring):
        metadata = None
    else:
        metadata = type
        if metadata.type is None:
            raise ValueError("Missing fingerprint type information in metadata")
        type = metadata.type

    structure_fingerprinter = types.parse_type(type)
    return structure_fingerprinter.read_molecule_fingerprints(
        source, format, id_tag=id_tag, reader_args=reader_args, errors=errors, metadata=metadata)
    
# Low-memory, forward-iteration, or better
def open(source, format=None, location=None):
    """Read fingerprints from a fingerprint file

    Read fingerprints from *source*, using the given format. If
    *source* is a string then it is treated as a filename. If *source*
    is None then fingerprints are read from stdin. Otherwise, *source*
    must be a Python file object supporting the ``read`` and
    ``readline`` methods.

    If *format* is None then the fingerprint file format and
    compression type are derived from the source filename, or from the
    ``name`` attribute of the source file object. If the source is None
    then the stdin is assumed to be uncompressed data in "fps" format.

    The supported format strings are "fps", "fps.gz" for fingerprints
    in FPS format and compressed FPS format, respectively.

    This version of chemfp does not support the FPB format. Trying
    to use the "fpb" format will raise a NotImplementedError.

    The optional *location* is a :class:`chemfp.io.Location` instance.
    It will only be used if the source is in FPS format.

    If the source is in FPS format then ``open`` will return a
    :class:`chemfp.fps_io.FPSReader`, which will use the *location*
    if specified.

    Here's an example of printing the contents of the file::
    
        from chemfp.bitops import hex_encode
        reader = chemfp.open("example.fps.gz")
        for id, fp in reader:
            print(id, hex_encode(fp))
        
    :param source: The fingerprint source.
    :type source: A filename string, a file object, or None
    :param format: The file format and optional compression.
    :type format: string, or None

    :returns: a :class:`chemfp.fps_io.FPSReader`
    """
    from . import io
    format_name, compression = io.normalize_input_format(source, format)

    if format_name == "fps":
        from . import fps_io
        return fps_io.open_fps(source, format_name, compression, location)

    if format_name == "fpb":
        raise NotImplementedError("fpb format support not implemented")
    if format is None:
        raise ValueError("Unable to determine fingerprint format type from %r" % (source,))
    else:
        raise ValueError("Unsupported fingerprint format %r" % (format,))

def open_fingerprint_writer(destination, metadata=None, format=None, alignment=8, reorder=True,
                            tmpdir=None, max_spool_size=None, errors="strict", location=None):
    """Create a fingerprint writer for the given destination

    The fingerprint writer is an object with methods to write fingerprints
    to the given *destination*. The output format is based on the `format`.
    If that's None then the format depends on the *destination*, or is
    "fps" if the attempts at format detection fail.

    The *metadata*, if given, is a :class:`Metadata` instance, and used to
    fill the header of an FPS file.
    
    If the output format is "fps" or "fps.gz" then *destination* may be
    a filename, a file object, or None for stdout. The "fpb" format is
    not available for this version of chemfp, and function will raise
    a NotImplementedError in that case.

    The parameters *alignment*, *reorder*, *tmpdir*, and *max_spool_size*
    are for FPB output and are ignored. The parameters are listed for
    better forwards-compatibility.

    The *errors* specifies how to handle recoverable write errors. The
    value "strict" raises an exception if there are any detected
    errors. The value "report" sends an error message to stderr and
    skips to the next record. The value "ignore" skips to the next
    record.

    The *location* is a :class:`Location` instance. It lets the caller
    access state information such as the number of records that have
    been written.

    :param destination: the output destination
    :type destination: a filename, file object, or None
    :param metadata: the fingerprint metadata
    :type metadata: a Metadata instance, or None
    :param format: the output format
    :type format: None, "fps", "fps.gz", or "fpb"
    :param alignment: arena byte alignment for FPB files
    :type alignment: positive integer
    :param reorder: True reorders the fingerprints by popcount, False leaves them in input order
    :type reorder: True or False
    :param tmpdir: the directory to use for temporary files, when max_spool_size is specified
    :type tmpdir: string or None
    :param max_spool_size: number of bytes to store in memory before using a temporary file. If None, use memory for everything.
    :type max_spool_size: integer, or None
    :param location: a location object used to access output state information
    :type location: a Location instance, or None
    :returns: a :class:`chemfp.FingerprintWriter`
    """
    from . import io
    format_name, compression = io.normalize_output_format(destination, format, ("fps", ""))

    if format_name == "fps":
        from . import fps_io
        #outfile = io.open_compressed_output(destination, compression)
        return fps_io.open_output(destination, metadata, compression, errors=errors, location=location)

    if format_name == "fpb":
        raise NotImplementedError("This version of chemfp does not support FPB output.")

    # Unknown format name.
    if format is None:
        raise ValueError("Unable to determine fingerprint format type from %r" % (destination,))
    else:
        raise ValueError("Unsupported output fingerprint format %r" % (format,))
    

def load_fingerprints(reader, metadata=None, reorder=True, alignment=None, format=None):
    """Load all of the fingerprints into an in-memory FingerprintArena data structure
    
    The FingerprintArena data structure reads all of the fingerprints and
    identifers from 'reader' and stores them into an in-memory data
    structure which supports fast similarity searches.
    
    If 'reader' is a string or implements "read" then the contents will be
    parsed with the 'chemfp.open' function. Otherwise it must support
    iteration returning (id, fingerprint) pairs. 'metadata' contains the
    metadata the arena. If not specified then 'reader.metadata' is used.
    
    The loader may reorder the fingerprints for better search performance.
    To prevent ordering, use reorder=False.

    The 'alignment' option specifies the alignment data alignment and
    padding size for each fingerprint. A value of 8 means that each
    fingerprint will start on a 8 byte alignment, and use storage
    space which a multiple of 8 bytes long. The default value of None
    determines the best alignment based on the fingerprint size and
    available popcount methods.

    :param reader: An iterator over (id, fingerprint) pairs
    :type reader: a string, file object, or (id, fingerprint) iterator
    :param metadata: The metadata for the arena, if other than reader.metadata
    :type metadata: Metadata
    :param reorder: Specify if fingerprints should be reordered for better performance
    :type reorder: True or False
    :param alignment: Alignment size in bytes (both data alignment and padding); None
       autoselects the best alignment.
    :type alignment: a positive integer, or None
    :param format: The file format name if the reader is a string
    :type format: None, "fps", or "fps.gz". "fpb" will raise a NotImplementedError
    :returns: FingerprintArena
    """
    from .arena import FingerprintArena
    
    if (isinstance(reader, basestring)  # Read from a file
        or reader is None               # Read from stdin
        or hasattr(reader, "read")      # Read from a file object
        ):
        reader = open(reader, format=format)
        
        # Can I use the existing reader?
        if isinstance(reader, FingerprintArena):
            # If so, I can set the metadata directly (if needed) and return it.
            if metadata is not None:
                reader.metadata = metadata
            return reader
        else:
            # Otherwise I need to convert to arena
            pass
    else:
        # Was I passed in an arena that I might reuse directly?
        if isinstance(reader, FingerprintArena):
            # If there's no metadata then I can use it directly.
            if metadata is None:
                return reader
            # Need a new arena with the same parameters except for a new metadata
            return FingerprintArena(
                metadata, reader.alignment,
                reader.start_padding, reader.end_padding, reader.storage_size, reader.arena,
                reader.popcount_indices, reader.arena_ids, reader.start, reader.end,
                reader._id_lookup, reader.num_bits, reader.num_bytes)

    from . import arena
    return arena.fps_to_arena(reader, metadata=metadata, reorder=reorder,
                              alignment=alignment)

##### High-level search interfaces

def count_tanimoto_hits(queries, targets, threshold=0.7, arena_size=100):
    """Count the number of targets within 'threshold' of each query term

    For each query in 'queries', count the number of targets in 'targets'
    which are at least 'threshold' similar to the query. This function
    returns an iterator containing the (query_id, count) pairs.

    Example::

        queries = chemfp.open("queries.fps")
        targets = chemfp.load_fingerprints("targets.fps.gz")
        for (query_id, count) in chemfp.count_tanimoto_hits(queries, targets, threshold=0.9):
            print query_id, "has", count, "neighbors with at least 0.9 similarity"

    Internally, queries are processed in batches of size 'arena_size'.
    A small batch size uses less overall memory and has lower
    processing latency, while a large batch size has better overall
    performance. Use arena_size=None to process the input as a single batch.

    Note: the FPSReader may be used as a target but it can only process
    one batch, and searching a FingerprintArena is faster if you have more
    than a few queries.

    :param queries: The query fingerprints.
    :type queries: any fingerprint container
    :param targets: The target fingerprints.
    :type targets: FingerprintArena or the slower FPSReader
    :param threshold: The minimum score threshold.
    :type threshold: float between 0.0 and 1.0, inclusive
    :param arena_size: The number of queries to process in a batch
    :type arena_size: a positive integer, or None
    :returns:
       An iterator containing (query_id, score) pairs, one for each query
    """
    from . import fps_io
    if isinstance(targets, fps_io.FPSReader):
        from . import fps_search
        count_hits = fps_search.count_tanimoto_hits_arena
    else:
        from . import search
        count_hits = search.count_tanimoto_hits_arena

    ### Start the search now so compatibility errors are raised eagerly

    # Start iterating through the subarenas, and get the first of those
    subarenas = queries.iter_arenas(arena_size)
    try:
        first_query_arena = subarenas.next()
    except StopIteration:
        # There are no subarenas; return an empty iterator
        return iter([])

    # Get the first result, and hold on to it for the generator
    first_counts = count_hits(first_query_arena, targets, threshold=threshold)
    
    def count_tanimoto_hits():
        # Return results for the first arena
        for query_id, count in zip(first_query_arena.ids, first_counts):
            yield query_id, count
        # Return results for the rest of the arenas
        for query_arena in subarenas:
            counts = count_hits(query_arena, targets, threshold=threshold)
            for query_id, count in zip(query_arena.ids, counts):
                yield query_id, count
    return count_tanimoto_hits()


def threshold_tanimoto_search(queries, targets, threshold=0.7, arena_size=100):
    """Find all targets within 'threshold' of each query term

    For each query in 'queries', find all the targets in 'targets' which
    are at least 'threshold' similar to the query. This function returns
    an iterator containing the (query_id, hits) pairs. The hits are stored
    as a list of (target_id, score) pairs.

    Example::

      queries = chemfp.open("queries.fps")
      targets = chemfp.load_fingerprints("targets.fps.gz")
      for (query_id, hits) in chemfp.id_threshold_tanimoto_search(queries, targets, threshold=0.8):
          print query_id, "has", len(hits), "neighbors with at least 0.8 similarity"
          non_identical = [target_id for (target_id, score) in hits if score != 1.0]
          print "  The non-identical hits are:", non_identical

    Internally, queries are processed in batches of size 'arena_size'.
    A small batch size uses less overall memory and has lower
    processing latency, while a large batch size has better overall
    performance. Use arena_size=None to process the input as a single batch.

    Note: the FPSReader may be used as a target but it can only process
    one batch, and searching a FingerprintArena is faster if you have more
    than a few queries.

    :param queries: The query fingerprints.
    :type queries: any fingerprint container
    :param targets: The target fingerprints.
    :type targets: FingerprintArena or the slower FPSReader
    :param threshold: The minimum score threshold.
    :type threshold: float between 0.0 and 1.0, inclusive
    :param arena_size: The number of queries to process in a batch
    :type arena_size: positive integer, or None
    :returns:
      An iterator containing (query_id, hits) pairs, one for each query.
      'hits' contains a list of (target_id, score) pairs.
    """
    from . import fps_io
    if isinstance(targets, fps_io.FPSReader):
        from . import fps_search
        threshold_search = fps_search.threshold_tanimoto_search_arena
    else:
        from . import search
        threshold_search = search.threshold_tanimoto_search_arena

    ### Start the search now so compatibility errors are raised eagerly

    # Start iterating through the subarenas, and get the first of those
    subarenas = queries.iter_arenas(arena_size)
    try:
        first_query_arena = subarenas.next()
    except StopIteration:
        # There are no subarenas; return an empty iterator
        return iter([])

    # Get the first result, and hold on to it for the generator
    first_results = threshold_search(first_query_arena, targets, threshold=threshold)
    ## Here's a thought; allow a 'result_order' parameter so I can do:
    # if result_order is not None:
    #    first_results.reorder(reorder)

    def threshold_tanimoto_search():
        # Return results for the first arena
        for query_id, row in zip(first_query_arena.ids, first_results):
            yield query_id, row
        
        for query_arena in subarenas:
            results = threshold_search(query_arena, targets, threshold=threshold)
            ## I would also need to do
            #if result_order is not None:
            #    first_results.reorder(reorder)
                
            for query_id, row in zip(query_arena.ids, results):
                yield (query_id, row)
    return threshold_tanimoto_search()

def knearest_tanimoto_search(queries, targets, k=3, threshold=0.7, arena_size=100):
    """Find the 'k'-nearest targets within 'threshold' of each query term

    For each query in 'queries', find the 'k'-nearest of all the targets
    in 'targets' which are at least 'threshold' similar to the query. Ties
    are broken arbitrarily and hits with scores equal to the smallest value
    may have been omitted.
    
    This function returns an iterator containing the (query_id, hits) pairs,
    where hits is a list of (target_id, score) pairs, sorted so that the
    highest scores are first. The order of ties is arbitrary.

    Example::

      # Use the first 5 fingerprints as the queries 
      queries = next(chemfp.open("pubchem_subset.fps").iter_arenas(5))
      targets = chemfp.load_fingerprints("pubchem_subset.fps")
      
      # Find the 3 nearest hits with a similarity of at least 0.8
      for (query_id, hits) in chemfp.id_knearest_tanimoto_search(queries, targets, k=3, threshold=0.8):
          print query_id, "has", len(hits), "neighbors with at least 0.8 similarity"
          if hits:
              target_id, score = hits[-1]
              print "    The least similar is", target_id, "with score", score

    Internally, queries are processed in batches of size 'arena_size'.
    A small batch size uses less overall memory and has lower
    processing latency, while a large batch size has better overall
    performance. Use arena_size=None to process the input as a single batch.

    Note: the FPSReader may be used as a target but it can only process
    one batch, and searching a FingerprintArena is faster if you have more
    than a few queries.

    :param queries: The query fingerprints.
    :type queries: any fingerprint container
    :param targets: The target fingerprints.
    :type targets: FingerprintArena or the slower FPSReader
    :param k: The maximum number of nearest neighbors to find.
    :type k: positive integer
    :param threshold: The minimum score threshold.
    :type threshold: float between 0.0 and 1.0, inclusive
    :param arena_size: The number of queries to process in a batch
    :type arena_size: positive integer, or None
    :returns:
      An iterator containing (query_id, hits) pairs, one for each query.
      'hits' contains a list of (target_id, score) pairs, sorted by score.
    """
    from . import fps_io
    if isinstance(targets, fps_io.FPSReader):
        from . import fps_search
        knearest_search = fps_search.knearest_tanimoto_search_arena
    else:
        from . import search
        knearest_search = search.knearest_tanimoto_search_arena
        
    ### Start the search now so compatibility errors are raised eagerly

    # Start iterating through the subarenas, and get the first of those
    subarenas = queries.iter_arenas(arena_size)
    try:
        first_query_arena = subarenas.next()
    except StopIteration:
        # There are no subarenas; return an empty iterator
        return iter([])

    # Get the first result, and hold on to it for the generator
    first_results = knearest_search(first_query_arena, targets, k=k, threshold=threshold)

    def knearest_tanimoto_search():
        # Return results for the first arena
        for query_id, row in zip(first_query_arena.ids, first_results):
            yield query_id, row

        # and for the subarenas
        for query_arena in subarenas:
            results = knearest_search(query_arena, targets, k=k, threshold=threshold)
            for query_id, row in zip(query_arena.ids, results):
                yield (query_id, row)
        
    return knearest_tanimoto_search()

def count_tanimoto_hits_symmetric(fingerprints, threshold=0.7):
    """Find the number of other fingerprints within `threshold` of each fingerprint
    
    For each fingerprint in the `fingerprints` arena, find the number
    of other fingerprints in the same arena which are at least
    `threshold` similar to it. The arena must have pre-computed
    popcounts. A fingerprint never matches itself.

    This function returns an iterator of (fingerprint_id, count) pairs.

    Example::

      arena = chemfp.load_fingerprints("targets.fps.gz")
      for (fp_id, count) in chemfp.count_tanimoto_hits_symmetric(arena, threshold=0.6):
          print fp_id, "has", count, "neighbors with at least 0.6 similarity"
    
    :param fingerprints: The arena containing the fingerprints.
    :type fingerprints: a FingerprintArena with precomputed popcount_indices
    :param threshold: The minimum score threshold.
    :type threshod: float between 0.0 and 1.0, inclusive
    :returns:
      An iterator of (fp_id, count) pairs, one for each fingerprint
    """
    from . import fps_io, search
    if (isinstance(fingerprints, fps_io.FPSReader) or
        not getattr(fingerprints, "popcount_indices", None)):
        raise ValueError("`fingerprints` must be a FingerprintArena with pre-computed popcount indices")

    # Start the search now so the errors are caught early
    results = search.count_tanimoto_hits_symmetric(fingerprints, threshold)
    def count_tanimoto_hits_symmetric_internal():
        for id, count in zip(fingerprints.ids, results):
            yield id, count
    return count_tanimoto_hits_symmetric_internal()

def threshold_tanimoto_search_symmetric(fingerprints, threshold=0.7):
    """Find the other fingerprints within `threshold` of each fingerprint

    For each fingerprint in the `fingerprints` arena, find the other
    fingerprints in the same arena which hare at least `threshold`
    similar to it. The arena must have pre-computed popcounts. A
    fingerprint never matches itself.

    This function returns an iterator of (fingerprint, SearchResult) pairs.
    The SearchResult hit order is arbitrary.

    Example::
    
      arena = chemfp.load_fingerprints("targets.fps.gz")
      for (fp_id, hits) in chemfp.threshold_tanimoto_search_symmetric(arena, threshold=0.75):
          print fp_id, "has", len(hits), "neighbors:"
          for (other_id, score) in hits.get_ids_and_scores():
              print "   %s  %.2f" % (other_id, score)

    :param fingerprints: The arena containing the fingerprints.
    :type fingerprints: a FingerprintArena with precomputed popcount_indices
    :param threshold: The minimum score threshold.
    :type threshod: float between 0.0 and 1.0, inclusive
    :returns: An iterator of (fp_id, SearchResult) pairs, one for each fingerprint
    """
    from . import fps_io, search
    if (isinstance(fingerprints, fps_io.FPSReader) or
        not getattr(fingerprints, "popcount_indices", None)):
        raise ValueError("`fingerprints` must be a FingerprintArena with pre-computed popcount indices")

    # Start the search now so the errors are caught early
    results = search.threshold_tanimoto_search_symmetric(fingerprints, threshold)
    def threshold_tanimoto_search_symmetric_internal():
        for id, hits in zip(fingerprints.ids, results):
            yield id, hits
    return threshold_tanimoto_search_symmetric_internal()

def knearest_tanimoto_search_symmetric(fingerprints, k=3, threshold=0.7):
    """Find the nearest `k` fingerprints within `threshold` of each fingerprint

    For each fingerprint in the `fingerprints` arena, find the nearest
    `k` fingerprints in the same arena which hare at least `threshold`
    similar to it. The arena must have pre-computed popcounts. A
    fingerprint never matches itself.

    This function returns an iterator of (fingerprint, SearchResult) pairs.
    The SearchResult hits are ordered from highest score to lowest, with
    ties broken arbitrarily.

    Example::
    
      arena = chemfp.load_fingerprints("targets.fps.gz")
      for (fp_id, hits) in chemfp.knearest_tanimoto_search_symmetric(arena, k=5, threshold=0.5):
          print fp_id, "has", len(hits), "neighbors, with scores", 
          print ", ".join("%.2f" % x for x in hits.get_scores())

    :param fingerprints: The arena containing the fingerprints.
    :type fingerprints: a FingerprintArena with precomputed popcount_indices
    :param k: The maximum number of nearest neighbors to find.
    :type k: positive integer
    :param threshold: The minimum score threshold.
    :type threshod: float between 0.0 and 1.0, inclusive
    :returns: An iterator of (fp_id, SearchResult) pairs, one for each fingerprint
    """
    from . import fps_io, search
    if (isinstance(fingerprints, fps_io.FPSReader) or
        not getattr(fingerprints, "popcount_indices", None)):
        raise ValueError("`fingerprints` must be a FingerprintArena with pre-computed popcount indices")

    # Start the search now so the errors are caught early
    results = search.knearest_tanimoto_search_symmetric(fingerprints, k, threshold)
    def knearest_tanimoto_search_symmetric_internal():
        for id, hits in zip(fingerprints.ids, results):
            yield id, hits
    return knearest_tanimoto_search_symmetric_internal()
        

_error_levels = {"info": 5, "warning": 10, "error": 20}
class ChemFPProblem(ChemFPError):
    """Information about a compatibility problem between a query and target.

    Instances are generated by :func:`chemfp.check_fingerprint_problems`
    and :func:`chemfp.check_metadata_problems`.

    The public attributes are:
    
    .. py:attribute:: severity

        one of "info", "warning", or "error"
        
    .. py:attribute:: error_level

        5 for "info", 10 for "warning", and 20 for "error"
        
    .. py:attribute:: category

        a string used as a category name. This string will not change over time.
        
    .. py:attribute:: description

        a more detailed description of the error, including details of the mismatch.
        The description depends on *query_name* and *target_name* and may change over time.

    The current category names are:
      * "num_bits mismatch" (error)
      * "num_bytes_mismatch" (error)
      * "type mismatch" (warning)
      * "aromaticity mismatch" (info)
      * "software mismatch" (info)
    """
    def __init__(self, severity, category, description):
        "The constructor is not part of the public API"
        self.severity = severity  # one of 'info', 'warning', or 'error'
        self.error_level = _error_levels[severity]
        self.category = category
        self.description = description
        
    def __str__(self):
        return "%s: %s" % (self.severity.upper(), self.description)
    
    def __repr__(self):
        return "ChemFPProblem(%r, %r, %r)" % (self.severity, self.category, self.description)

def check_fingerprint_problems(query_fp, target_metadata, query_name="query", target_name="target"):
    """Return a list of compatibility problems between a fingerprint and a metadata

    If there are no problems then this returns an empty list. If there is a
    bit length or byte length mismatch between the *query_fp* byte string
    and the *target_metadata* then it will return a list containing a
    :class:`ChemFPProblem` instance, with a severity level "error" and
    category "num_bytes mismatch".

    This function is usually used to check if a query fingerprint is
    compatible with the target fingerprints. In case of a problem, the
    default message looks like::

        >>> problems = check_fingerprint_problems("A"*64, Metadata(num_bytes=128))
        >>> problems[0].description
        'query contains 64 bytes but target has 128 byte fingerprints'

    You can change the error message with the *query_name* and *target_name*
    parameters::

        >>> import chemfp
        >>> problems = check_fingerprint_problems("z"*64, chemfp.Metadata(num_bytes=128),
        ...      query_name="input", target_name="database")
        >>> problems[0].description
        'input contains 64 bytes but database has 128 byte fingerprints'

    :param query_fp: a fingerprint (usually the query fingerprint)
    :type query_fp: byte string
    :param target_metadata: the metadata to check against (usually the target metadata)
    :type target_metadata: Metadata instance
    :param query_name: the text used to describe the fingerprint, in case of problem
    :type query_name: string
    :param target_name: the text used to describe the metadata, in case of problem
    :type target_name: string
    :return: a list of :class:`ChemFPProblem` instances
    """
    if len(query_fp) != target_metadata.num_bytes:
        if target_metadata.num_bytes is None:
            msg = ("%s contains %d bytes but %s has no specified byte size" %
                   (query_name, len(query_fp), target_name))
        else:
            msg = ("%s contains %d bytes but %s has %d byte fingerprints" %
                   (query_name, len(query_fp), target_name, target_metadata.num_bytes))
        return [ChemFPProblem("error", "num_bytes mismatch", msg)]
    return []

def check_metadata_problems(query_metadata, target_metadata, query_name="query", target_name="target"):
    """Return a list of compatibility problems between two metadata instances.
    
    If there are no probelms then this returns an empty list. Otherwise it
    returns a list of :class:`ChemFPProblem` instances, with a severity level
    ranging from "info" to "error".

    Bit length and byte length mismatches produce an "error". Fingerprint type
    and aromaticity mismatches produce a "warning". Software version mismatches
    produce an "info".

    This is usually used to check if the query metadata is incompatible with
    the target metadata. In case of a problem the messages look like::

      >>> import chemfp
      >>> m1 = chemfp.Metadata(num_bytes=128, type="Example/1")
      >>> m2 = chemfp.Metadata(num_bytes=256, type="Counter-Example/1")
      >>> problems = chemfp.check_metadata_problems(m1, m2)
      >>> len(problems)
      2
      >>> print(problems[1].description)
      query has fingerprints of type 'Example/1' but target has fingerprints of type 'Counter-Example/1'

    You can change the error message with the *query_name* and *target_name*
    parameters::

      >>> problems = chemfp.check_metadata_problems(m1, m2, query_name="input", target_name="database")
      >>> print(problems[1].description)
      input has fingerprints of type 'Example/1' but database has fingerprints of type 'Counter-Example/1'

    :param fp: a fingerprint
    :type fp: byte string
    :param metadata: the metadata to check against
    :type metadata: Metadata instance
    :param query_name: the text used to describe the fingerprint, in case of problem
    :type query_name: string
    :param target_name: the text used to describe the metadata, in case of problem
    :type target_name: string
    :return: a list of :class:`ChemFPProblem` instances
    """
    messages = []
    if (query_metadata.num_bits is not None and target_metadata.num_bits is not None):
        if query_metadata.num_bits != target_metadata.num_bits:
            msg = ("%s has %d bit fingerprints but %s has %d bit fingerprints" %
                   (query_name, query_metadata.num_bits, target_name, target_metadata.num_bits))
            messages.append(ChemFPProblem("error", "num_bits mismatch", msg))

    elif (query_metadata.num_bytes is not None and
          target_metadata.num_bytes is not None and
          query_metadata.num_bytes != target_metadata.num_bytes):
        
        msg = ("%s has %d byte fingerprints but %s has %d byte fingerprints" %
               (query_name, query_metadata.num_bytes, target_name, target_metadata.num_bytes))
        messages.append(ChemFPProblem("error", "num_bytes mismatch", msg))


    if (query_metadata.type is not None and
        target_metadata.type is not None and
        query_metadata.type != target_metadata.type):
        
        msg = ("%s has fingerprints of type %r but %s has fingerprints of type %r" %
               (query_name, query_metadata.type, target_name, target_metadata.type))
        messages.append(ChemFPProblem("warning", "type mismatch", msg))

    if (query_metadata.aromaticity is not None and
        target_metadata.aromaticity is not None and
        query_metadata.aromaticity != target_metadata.aromaticity):

        msg = ("%s uses aromaticity %r but %s uses aromaticity %r" %
               (query_name, query_metadata.aromaticity, target_name, target_metadata.aromaticity))
        messages.append(ChemFPProblem("warning", "aromaticity mismatch", msg))

    if (query_metadata.software is not None and
        target_metadata.software is not None and
        query_metadata.software != target_metadata.software):

        msg = ("%s comes from software %r but %s comes from software %r" %
               (query_name, query_metadata.software, target_name, target_metadata.software))
        messages.append(ChemFPProblem("info", "software mismatch", msg))

    return messages

class Metadata(object):
    """Store information about a set of fingerprints

    The public attributes are:

    .. py:attribute:: num_bits

       the number of bits in the fingerprint

    .. py:attribute:: num_bytes

       the number of bytes in the fingerprint

    .. py:attribute:: type

       the fingerprint type string

    .. py:attribute:: aromaticity

       aromaticity model (only used with OEChem, and now deprecated)

    .. py:attribute:: software

       software used to make the fingerprints

    .. py:attribute:: sources

       list of sources used to make the fingerprint

    .. py:attribute:: date

       a `datetime <https://docs.python.org/2/library/datetime.html#module-datetime>`_
       timestamp of when the fingerprints were made
    """
    def __init__(self, num_bits=None, num_bytes=None, type=None, aromaticity=None,
                 software=None, sources=None, date=None):
        if num_bytes is None:
            if num_bits is None:
                pass
            else:
                num_bytes = (num_bits + 7)//8
        elif num_bits is None:
            num_bits = num_bytes * 8
        else:
            if (num_bits + 7)//8 != num_bytes:
                raise ValueError("num_bits of %d is incompatible with num_bytes of %d" %
                                (num_bits, num_bytes))
            
        self.num_bits = num_bits
        self.num_bytes = num_bytes
        self.type = type
        self.aromaticity = aromaticity
        self.software = software
        if sources is None:
            self.sources = []
        elif isinstance(sources, basestring):
            self.sources = [sources]
            #raise TypeError("sources must be a list, not a string")
        else:
            self.sources = sources
        self.date = date

    def __repr__(self):
        """Return a string like ``Metadata(num_bits=1024, num_bytes=128, type='OpenBabel/FP2', ....)``"""
        return "Metadata(num_bits=%(num_bits)r, num_bytes=%(num_bytes)r, type=%(type)r, aromaticity=%(aromaticity)r, sources=%(sources)r, software=%(software)r, date=%(date)r)" % self.__dict__

    def __str__(self):
        """Show the metadata in FPS header format"""
        from cStringIO import StringIO
        from . import io
        f = StringIO()
        io.write_fps1_header(f, self)
        return f.getvalue()

    def copy(self, num_bits=None, num_bytes=None, type=None, aromaticity=None,
             software=None, sources=None, date=None):
        """Return a new Metadata instance based on the current attributes and optional new values

        When called with no parameter, make a new Metadata instance with the
        same attributes as the current instance.

        If a given call parameter is not None then it will be used instead of
        the current value. If you want to change a current value to None then
        you will have to modify the new Metadata after you created it.

        :param num_bits: the number of bits in the fingerprint
        :type num_bits: an integer, or None
        :param num_bytes: the number of bytes in the fingerprint
        :type num_bytes: an integer, or None
        :param type: the fingerprint type description
        :type type: string or None
        :param aromaticity: obsolete
        :type aromaticity: None
        :param software: a description of the software
        :type software: string or None
        :param sources: source filenames
        :type sources: list of strings, a string (interpreted as a list with one string), or None
        :param date: creation or processing date for the contents
        :type date: a datetime instance, or None
        :returns: a new Metadata instance
        """
        if num_bits is None:
            num_bits = self.num_bits
        if num_bytes is None:
            num_bytes = self.num_bytes
        if type is None:
            type = self.type
        if aromaticity is None:
            aromaticity = self.aromaticity
        if software is None:
            software = self.software
        if sources is None:
            sources = self.sources
        if date is None:
            date = self.date
        return Metadata(num_bits=num_bits, num_bytes=num_bytes,
                        type=type, aromaticity=aromaticity, software=software,
                        sources=sources, date=date)

class FingerprintReader(object):
    """Base class for all chemfp objects holding fingerprint records

    All FingerprintReader instances have a ``metadata`` attribute
    containing a Metadata and can be iteratated over to get the (id,
    fingerprint) for each record.
    
    """
    def __init__(self, metadata):
        """Initialize with a :class:`Metadata` instance"""
        self.metadata = metadata

    def __iter__(self):
        """iterate over the (id, fingerprint) pairs"""
        raise NotImplementedError
    
    def iter_arenas(self, arena_size=1000):
        """iterate through *arena_size* fingerprints at a time, as subarenas

        Iterate through *arena_size* fingerprints  at a time, returned
        as :class:`chemfp.arena.FingerprintArena` instances. The arenas are in input
        order and not reordered by popcount.

        This method helps trade off between performance and memory
        use. Working with arenas is often faster than processing one
        fingerprint at a time, but if the file is very large then you
        might run out of memory, or get bored while waiting to process
        all of the fingerprint before getting the first answer.

        If *arena_size* is None then this makes an iterator which
        returns a single arena containing all of the fingerprints.
        
        :param arena_size: The number of fingerprints to put into each arena.
        :type arena_size: positive integer, or None
        :returns: an iterator of :class:`chemfp.arena.FingerprintArena` instances
        """
        from itertools import islice

        if arena_size is None:
            yield load_fingerprints(self, self.metadata, reorder=False)
            return

        if arena_size < 1:
            raise ValueError("arena_size cannot be zero")
            return
        
        it = iter(self)
        while 1:
            slice = islice(it, 0, arena_size)
            arena = load_fingerprints(slice, self.metadata, reorder=False)
            if not arena:
                break
            yield arena

    def save(self, destination, format=None):
        """Save the fingerprints to a given destination and format

        The output format is based on the *format*. If the format
        is None then the format depends on the *destination* file
        extension. If the extension isn't recognized then the
        fingerprints will be saved in "fps" format.

        If the output format is "fps" or "fps.gz" then *destination*
        may be a filename, a file object, or None; None writes
        to stdout.

        If the output format is "fpb" then *destination* must be
        a filename.

        :param destination: the output destination
        :type destination: a filename, file object, or None
        :param format: the output format
        :type format: None, "fps", "fps.gz", or "fpb"
        :returns: None
        """
        with open_fingerprint_writer(destination, format=format, metadata=self.metadata) as writer:
                writer.write_fingerprints(self)

    def get_fingerprint_type(self):
        """Get the fingerprint type object based on the metadata's type field

        This uses ``self.metadata.type`` to get the fingerprint type
        string then calls :func:`chemfp.get_fingerprint_type` to get and return
        a :class:`chemfp.types.FingerprintType` instance.
        
        This will raise a TypeError if there is no metadata, and
        a ValueError if the type field was invalid or the fingerprint
        type isn't available.

        :returns: a :class:`chemfp.types.FingerprintType`
        """
        metadata = self.metadata
        if metadata is None:
            raise TypeError("No metadata available")
        type_string = metadata.type
        return get_fingerprint_type(type_string)

class FingerprintIterator(FingerprintReader):
    """A :class:`chemfp.FingerprintReader` for an iterator of (id, fingerprint) pairs

    This is often used as an adapter container to hold the metadata
    and (id, fingerprint) iterator. It supports an optional location,
    and can call a close function when the iterator has completed.

    A FingerprintIterator is a context manager which will close the
    underlying iterator if it's given a close handler.
    
    Like all iterators you can use next() to get the next
    (id, fingerprint) pair.
    """
    def __init__(self, metadata, id_fp_iterator, location=None, close=None):
        """Initialize with a Metadata instance and the (id, fingerprint) iterator
        
        The *metadata* is a :class:`Metadata` instance. The *id_fp_iterator*
        is an iterator which returns (id, fingerprint) pairs.
        
        The optional *location* is a :class:`chemfp.io.Location`. The optional
        *close* callable is called (as ``close()``) whenever ``self.close()``
        is called and when the context manager exits.
        """
        super(FingerprintIterator, self).__init__(metadata)
        self.location = location
        self._id_fp_iterator = id_fp_iterator
        self._at_start = True
        self._close = close

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        """Close the iterator

        The call will be forwarded to the ``close`` callable passed to the
        constructor. If that ``close`` is None then this does nothing.
        """
        if self._close is not None:
            self._close()

    def __iter__(self):
        """Iterate over the (id, fingerprint) pairs"""
        for x in self._id_fp_iterator:
            self._at_start = False
            yield x

    def next(self):
        """Return the next (id, fingerprint) pair"""
        return next(self._id_fp_iterator)

    def __next__(self):
        """Return the next (id, fingerprint) pair"""
        return next(self._id_fp_iterator)


class Fingerprints(FingerprintReader):
    """A :class:`chemf.FingerprintReader` containing a metadata and a list of (id, fingerprint) pairs.

    This is typically used as an adapater when you have a list of (id, fingerprint)
    pairs and you want to pass it (and the metadata) to the rest of the chemfp API.

    This implements a simple list-like collection of fingerprints. It supports:
      - for (id, fingerprint) in fingerprints: ...
      - id, fingerprint = fingerprints[1]
      - len(fingerprints)

    More features, like slicing, will be added as needed or when requested.
    """
    def __init__(self, metadata, id_fp_pairs):
        """Initialize with a Metadata instance and the (id, fingerprint) pair list

        The *metadata* is a :class:`Metadata` instance. The *id_fp_iterator*
        is an iterator which returns (id, fingerprint) pairs.
        """
        super(Fingerprints, self).__init__(metadata)
        self._id_fp_pairs = id_fp_pairs
    def __len__(self):
        """Return the number of available (id, fingerprint) pairs"""
        return len(self._id_fp_pairs)
    def __iter__(self):
        """iterate over the (id, fingerprint) pairs"""
        return iter(self._id_fp_pairs)
    
    def __repr__(self):
        return "FingerprintList(%r, %r)" % (self.metadata, self._id_fp_pairs)
    
    def __getitem__(self, i):
        """return the given (id, fingerprint) pair"""
        return self._id_fp_pairs[i]

    # Question: should I support other parts of the list API?
    # I almost certainly want to support slice syntax like x[:5]

class FingerprintWriter(object):
    """Base class for the fingerprint writers

    The only concrete fingerprint writer class in chemfp 1.3 is:

    * :class:`chemfp.fps_io.FPSWriter` - write an FPS file

    Chemfp 2.0 and later also implement OrderedFPBWriter and InputOrderFPBWriter.

    Use :func:`chemfp.open_fingerprint_writer` to create a fingerprint
    writer class; do not create them directly.

    All classes have the following attributes:

    * metadata - a :class:`chemfp.Metadata` instance
    * closed - False when the file is open, else True

    Fingerprint writers are also their own context manager, and
    close the writer on context exit.
    """
    def close(self):
        """Close the writer

        This will set self.closed to False.
        """
        raise NotImplementedError("Must be implemented in the subclass")

    def write_fingerprint(self, id, fp):
        """Write a single fingerprint record with the given id and fp to the destination

        :param string id: the record identifier
        :param fp: the fingerprint
        :type fp: byte string
        """
        raise NotImplementedError("Must be implemented in the subclass")

    def write_fingerprints(self, id_fp_pairs):
        """Write a sequence of (id, fingerprint) pairs to the destination

        :param id_fp_pairs: An iterable of (id, fingerprint) pairs. *id* is a string
          and *fingerprint* is a byte string.
        """
        raise NotImplementedError("Must be implemented in the subclass")

def get_num_threads():
    """Return the number of OpenMP threads to use in searches

    Initially this is the value returned by omp_get_max_threads(),
    which is generally 4 unless you set the environment variable
    OMP_NUM_THREADS to some other value. 
    
    It may be any value in the range 1 to get_max_threads(), inclusive.
    """
    # I don't want the top-level chemfp module import to import a submodule.
    import _chemfp

    return _chemfp.get_num_threads()

def set_num_threads(num_threads):
    """Set the number of OpenMP threads to use in searches

    If `num_threads` is less than one then it is treated as one, and a
    value greater than get_max_threads() is treated as get_max_threads().
    """
    # I don't want the top-level chemfp module import to import a submodule.
    import _chemfp

    return _chemfp.set_num_threads(num_threads)

def get_max_threads():
    """Return the maximum number of threads available.

    If OpenMP is not available then this will return 1. Otherwise it
    returns the maximum number of threads available, as reported by
    omp_get_num_threads().
    
    """
    # I don't want the top-level chemfp module import to import a submodule.
    import _chemfp

    return _chemfp.get_max_threads()



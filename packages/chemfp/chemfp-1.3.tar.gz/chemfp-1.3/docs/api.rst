

.. py:module:: chemfp 

.. _chemfp-api:

==========
chemfp API
==========

This chapter contains the docstrings for the public portion of the
chemfp API.

=======================
chemfp top-level module
=======================

The following functions and classes are in the top-level chemfp module.



.. py:function:: open(source, format=None, location=None)

   Read fingerprints from a fingerprint file
   
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




.. py:function:: load_fingerprints(reader, metadata=None, reorder=True, alignment=None, format=None)

   Load all of the fingerprints into an in-memory FingerprintArena data structure
   
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




.. py:function:: read_structure_fingerprints(type, source=None, format=None, id_tag=None, reader_args=None, errors="strict")

   Deprecated function. Please call read_molecule_fingerprints() instead
   
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



.. py:function:: read_molecule_fingerprints(type, source=None, format=None, id_tag=None, reader_args=None, errors="strict")

   Read structures from 'source' and return the corresponding ids and fingerprints
   
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




.. py:function:: open_fingerprint_writer(destination, metadata=None, format=None, alignment=8, reorder=True, tmpdir=None, max_spool_size=None, errors="strict", location=None)

   Create a fingerprint writer for the given destination
   
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



ChemFPError
===========

.. py:class:: ChemFPError

   Base class for all of the chemfp exceptions



ParseError
==========

.. py:class:: ParseError

   Exception raised by the molecule and fingerprint parsers and writers
   
   The public attributes are:
   
   .. py:attribute:: msg
   
      a string describing the exception
   
   .. py:attribute:: location
   
      a :class:`chemfp.io.Location` instance, or None



Metadata
========

.. py:class:: Metadata

   Store information about a set of fingerprints
   
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



  .. py:method:: __repr__()

     Return a string like ``Metadata(num_bits=1024, num_bytes=128, type='OpenBabel/FP2', ....)``



  .. py:method:: __str__()

     Show the metadata in FPS header format



  .. py:method:: copy(num_bits=None, num_bytes=None, type=None, aromaticity=None, software=None, sources=None, date=None)

     Return a new Metadata instance based on the current attributes and optional new values
     
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



FingerprintReader
=================

.. py:class:: FingerprintReader

   Base class for all chemfp objects holding fingerprint records
   
   All FingerprintReader instances have a ``metadata`` attribute
   containing a Metadata and can be iteratated over to get the (id,
   fingerprint) for each record.



  .. py:method:: __iter__()

     iterate over the (id, fingerprint) pairs



  .. py:method:: iter_arenas(arena_size=1000)

     iterate through *arena_size* fingerprints at a time, as subarenas
     
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



  .. py:method:: save(destination, format=None)

     Save the fingerprints to a given destination and format
     
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



  .. py:method:: get_fingerprint_type()

     Get the fingerprint type object based on the metadata's type field
     
     This uses ``self.metadata.type`` to get the fingerprint type
     string then calls :func:`chemfp.get_fingerprint_type` to get and return
     a :class:`chemfp.types.FingerprintType` instance.
     
     This will raise a TypeError if there is no metadata, and
     a ValueError if the type field was invalid or the fingerprint
     type isn't available.
     
     :returns: a :class:`chemfp.types.FingerprintType`



FingerprintIterator
===================

.. py:class:: FingerprintIterator

   A :class:`chemfp.FingerprintReader` for an iterator of (id, fingerprint) pairs
   
   This is often used as an adapter container to hold the metadata
   and (id, fingerprint) iterator. It supports an optional location,
   and can call a close function when the iterator has completed.
   
   A FingerprintIterator is a context manager which will close the
   underlying iterator if it's given a close handler.
   
   Like all iterators you can use next() to get the next
   (id, fingerprint) pair.



  .. py:method:: __init__(metadata, id_fp_iterator, location=None, close=None)

     Initialize with a Metadata instance and the (id, fingerprint) iterator
     
     The *metadata* is a :class:`Metadata` instance. The *id_fp_iterator*
     is an iterator which returns (id, fingerprint) pairs.
     
     The optional *location* is a :class:`chemfp.io.Location`. The optional
     *close* callable is called (as ``close()``) whenever ``self.close()``
     is called and when the context manager exits.



  .. py:method:: __iter__()

     Iterate over the (id, fingerprint) pairs



  .. py:method:: close()

     Close the iterator
     
     The call will be forwarded to the ``close`` callable passed to the
     constructor. If that ``close`` is None then this does nothing.



Fingerprints
============

.. py:class:: Fingerprints

   A :class:`chemf.FingerprintReader` containing a metadata and a list of (id, fingerprint) pairs.
   
   This is typically used as an adapater when you have a list of (id, fingerprint)
   pairs and you want to pass it (and the metadata) to the rest of the chemfp API.
   
   This implements a simple list-like collection of fingerprints. It supports:
     - for (id, fingerprint) in fingerprints: ...
     - id, fingerprint = fingerprints[1]
     - len(fingerprints)
   
   More features, like slicing, will be added as needed or when requested.



  .. py:method:: __init__(metadata, id_fp_pairs)

     Initialize with a Metadata instance and the (id, fingerprint) pair list
     
     The *metadata* is a :class:`Metadata` instance. The *id_fp_iterator*
     is an iterator which returns (id, fingerprint) pairs.



FingerprintWriter
=================

.. py:class:: FingerprintWriter

   Base class for the fingerprint writers
   
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



  .. py:method:: write_fingerprint(id, fp)

     Write a single fingerprint record with the given id and fp to the destination
     
     :param string id: the record identifier
     :param fp: the fingerprint
     :type fp: byte string



  .. py:method:: write_fingerprints(id_fp_pairs)

     Write a sequence of (id, fingerprint) pairs to the destination
     
     :param id_fp_pairs: An iterable of (id, fingerprint) pairs. *id* is a string
       and *fingerprint* is a byte string.



  .. py:method:: close()

     Close the writer
     
     This will set self.closed to False.



ChemFPProblem
=============

.. py:class:: ChemFPProblem

   Information about a compatibility problem between a query and target.
   
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



.. py:function:: check_fingerprint_problems(query_fp, target_metadata, query_name="query", target_name="target")

   Return a list of compatibility problems between a fingerprint and a metadata
   
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



.. py:function:: check_metadata_problems(query_metadata, target_metadata, query_name="query", target_name="target")

   Return a list of compatibility problems between two metadata instances.
   
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




.. py:function:: count_tanimoto_hits(queries, targets, threshold=0.7, arena_size=100)

   Count the number of targets within 'threshold' of each query term
   
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



.. py:function:: count_tanimoto_hits_symmetric(fingerprints, threshold=0.7)

   Find the number of other fingerprints within `threshold` of each fingerprint
   
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



.. py:function:: threshold_tanimoto_search(queries, targets, threshold=0.7, arena_size=100)

   Find all targets within 'threshold' of each query term
   
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



.. py:function:: threshold_tanimoto_search_symmetric(fingerprints, threshold=0.7)

   Find the other fingerprints within `threshold` of each fingerprint
   
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



.. py:function:: knearest_tanimoto_search(queries, targets, k=3, threshold=0.7, arena_size=100)

   Find the 'k'-nearest targets within 'threshold' of each query term
   
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



.. py:function:: knearest_tanimoto_search_symmetric(fingerprints, k=3, threshold=0.7)

   Find the nearest `k` fingerprints within `threshold` of each fingerprint
   
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





.. py:function:: get_max_threads()

   Return the maximum number of threads available.
   
   If OpenMP is not available then this will return 1. Otherwise it
   returns the maximum number of threads available, as reported by
   omp_get_num_threads().



.. py:function:: get_num_threads()

   Return the number of OpenMP threads to use in searches
   
   Initially this is the value returned by omp_get_max_threads(),
   which is generally 4 unless you set the environment variable
   OMP_NUM_THREADS to some other value. 
   
   It may be any value in the range 1 to get_max_threads(), inclusive.



.. py:function:: set_num_threads(num_threads)

   Set the number of OpenMP threads to use in searches
   
   If `num_threads` is less than one then it is treated as one, and a
   value greater than get_max_threads() is treated as get_max_threads().



Open Babel fingerprints
=======================

Open Babel implements four fingerprints families and chemfp implements
two fingerprint families using the Open Babel toolkit. These are:

* OpenBabel-FP2 - Indexes linear fragments up to 7 atoms.
* OpenBabel-FP3 - SMARTS patterns specified in the file patterns.txt
* OpenBabel-FP4 - SMARTS patterns specified in the file SMARTS_InteLigand.txt
* OpenBabel-MACCS - SMARTS patterns specified in the file MACCS.txt, which
  implements nearly all of the 166 MACCS keys
* RDMACCS-OpenBabel - a chemfp implementation of nearly all of the
  MACCS keys
* ChemFP-Substruct-OpenBabel - an experimental chemfp implementation
  of the PubChem keys

Most people use FP2 and MACCS.

Note: chemfp 1.3 implements both RDMACCS-OpenBabel/1 and
RDMACCS-OpenBabel/2. Version 1.1 did not have a definition for key 44.


OpenEye fingerprints
====================

OpenEye's OEGraphSim library implements four bitstring-based
fingerprint families, and chemfp implements two fingerprint families
based on OEChem. These are:

* OpenEye-Path - exhaustive enumeration of all linear fragments
  up to a given size
* OpenEye-Circular - exhaustive enumeration of all circular
  fragments grown radially from each heavy atom up to a given radius
* OpenEye-Tree - exhaustive enumeration of all trees up to
  a given size
* OpenEye-MACCS166 - an implementation of the 166 MACCS keys
* RDMACCS-OpenEye - a chemfp implementation of the 166 MACCS keys
* ChemFP-Substruct-OpenEye - an experimental chemfp implementation
  of the PubChem keys

Note: chemfp 1.3 implements both RDMACCS-OpenEye/1 and
RDMACCS-OpenEye/2. Version 1.1 did not have a definition for key 44.


RDKit fingerprints
==================

RDKit implements nine fingerprint families, and chemfp implements two
fingerprint families based on RDKit. These are:

* RDKit-Fingerprint - exhaustive enumeration of linear and branched trees
* RDKit-MACCS166 - The RDKit implementation of the MACCS keys
* RDKit-Morgan - EFCP-like circular fingerprints
* RDKit-AtomPair - atom pair fingerprints
* RDKit-Torsion - topological-torsion fingerprints
* RDKit-Pattern - substructure screen fingerprint 
* RDKit-Avalon - RDKit's interface to the Avalon toolkit fingerprints
* RDMACCS-RDKit - a chemfp implementation of the 166 MACCS keys
* ChemFP-Substruct-RDKit - an experimental chemfp implementation
  of the PubChem keys

Note: chemfp 1.3 implements both RDMACCS-RDKit/1 and
RDMACCS-RDKit/2. Version 1.1 did not have a definition for key 44.

===================
chemfp.arena module
===================

There should be no reason for you to import this module yourself. It
contains the :class:`.FingerprintArena`
implementation. FingerprintArena instances are returns part of the
public API but should not be constructed directly.

.. py:module:: chemfp.arena


FingerprintArena
================

.. py:class:: FingerprintArena

   Store fingerprints in a contiguous block of memory for fast searches
   
   A fingerprint arena implements the :class:`chemfp.FingerprintReader` API.
   
   A fingerprint arena stores all of the fingerprints in a continuous
   block of memory, so the per-molecule overhead is very low.
   
   The fingerprints can be sorted by popcount, so the fingerprints
   with no bits set come first, followed by those with 1 bit, etc.
   If ``self.popcount_indices`` is a non-empty string then the string
   contains information about the start and end offsets for all the
   fingerprints with a given popcount. This information is used for
   the sublinear search methods.
   
   The public attributes are:
   
   .. py:attribute:: metadata
   
      :class:`chemfp.Metadata` about the fingerprints
   
   .. py:attribute:: ids
   
      list of identifiers, in index order
   
   Other attributes, which might be subject to change, and which I won't fully explain, are:
     * arena - a contiguous block of memory, which contains the fingerprints
     * start_padding - number of bytes to the first fingerprint in the block
     * end_padding - number of bytes after the last fingerprint in the block
     * storage_size - number of bytes used to store a fingerprint
     * num_bytes - number of bytes in each fingerprint (must be <= storage_size)
     * num_bits - number of bits in each fingerprint
     * alignment - the fingerprint alignment
     * start - the index for the first fingerprint in the arena/subarena
     * end - the index for the last fingerprint in the arena/subarena
     * arena_ids - all of the identifiers for the parent arena
   
   The FingerprintArena is its own context manager, but it does
   nothing on context exit.



  .. py:method:: __len__()

     Number of fingerprint records in the FingerprintArena



  .. py:method:: __getitem__(i)

     Return the (id, fingerprint) pair at index i



  .. py:method:: __iter__()

     Iterate over the (id, fingerprint) contents of the arena



  .. py:method:: get_fingerprint_type()

     Get the fingerprint type object based on the metadata's type field
     
     This uses ``self.metadata.type`` to get the fingerprint type
     string then calls :func:`chemfp.get_fingerprint_type` to get and return
     a :class:`chemfp.types.FingerprintType` instance.
     
     This will raise a TypeError if there is no metadata, and
     a ValueError if the type field was invalid or the fingerprint
     type isn't available.
     
     :returns: a :class:`chemfp.types.FingerprintType`



  .. py:method:: get_fingerprint(i)

     Return the fingerprint at index *i*
     
     Raises an IndexError if index *i* is out of range.



  .. py:method:: get_by_id(id)

     Given the record identifier, return the (id, fingerprint) pair,
     
     If the *id* is not present then return None.



  .. py:method:: get_index_by_id(id)

     Given the record identifier, return the record index
     
     If the *id* is not present then return None.



  .. py:method:: get_fingerprint_by_id(id)

     Given the record identifier, return its fingerprint
     
     If the *id* is not present then return None



  .. py:method:: save(destination, format=None)

     Save the fingerprints to a given destination and format
     
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



  .. py:method:: iter_arenas(arena_size = 1000)

     Base class for all chemfp objects holding fingerprint records
     
     All FingerprintReader instances have a ``metadata`` attribute
     containing a Metadata and can be iteratated over to get the (id,
     fingerprint) for each record.



  .. py:method:: copy(indices=None, reorder=None)

     Create a new arena using either all or some of the fingerprints in this arena
     
     By default this create a new arena. The fingerprint data block and ids may
     be shared with the original arena, which makes this a shallow copy. If the
     original arena is a slice, or "sub-arena" of an arena, then the copy will
     allocate new space to store just the fingerprints in the slice and use its
     own list for the ids.
     
     The *indices* parameter, if not None, is an iterable which contains the
     indicies of the fingerprint records to copy. Duplicates are allowed, though
     discouraged.
     
     If *indices* are specified then the default *reorder* value of None, or
     the value True, will reorder the fingerprints for the new arena by popcount.
     This improves overall search performance. If *reorder* is False then the
     new arena will preserve the order given by the indices.
     
     If *indices* are not specified, then the default is to preserve the order
     type of the original arena. Use ``reorder=True`` to always reorder the
     fingerprints in the new arena by popcount, and ``reorder=False`` to always
     leave them in the current ordering.
     
         >>> import chemfp
         >>> arena = chemfp.load_fingerprints("pubchem_queries.fps")
         >>> arena.ids[1], arena.ids[5], arena.ids[10], arena.ids[18]
         (b'9425031', b'9425015', b'9425040', b'9425033')
         >>> len(arena)
         19
         >>> new_arena = arena.copy(indices=[1, 5, 10, 18])
         >>> len(new_arena)
         4
         >>> new_arena.ids
         [b'9425031', b'9425015', b'9425040', b'9425033']
         >>> new_arena = arena.copy(indices=[18, 10, 5, 1], reorder=False)
         >>> new_arena.ids
         [b'9425033', b'9425040', b'9425015', b'9425031']
     
     :param indices: indicies of the records to copy into the new arena
     :type indices: iterable containing integers, or None
     :param reorder: describes how to order the fingerprints
     :type reorder: True to reorder, False to leave in input order, None for default action




  .. py:method:: count_tanimoto_hits_fp(query_fp, threshold=0.7)

     Count the fingerprints which are sufficiently similar to the query fingerprint
     
     Return the number of fingerprints in the arena which are
     at least *threshold* similar to the query fingerprint *query_fp*.
     
     :param query_fp: query fingerprint
     :type query_fp: byte string
     :param threshold: minimum similarity threshold (default: 0.7)
     :type threshold: float between 0.0 and 1.0, inclusive
     :returns: integer count



  .. py:method:: threshold_tanimoto_search_fp(query_fp, threshold=0.7)

     Find the fingerprints which are sufficiently similar to the query fingerprint
     
     Find all of the fingerprints in this arena which are at least
     *threshold* similar to the query fingerprint *query_fp*.  The
     hits are returned as a :class:`.SearchResult`, in arbitrary
     order.
     
     :param query_fp: query fingerprint
     :type query_fp: byte string
     :param threshold: minimum similarity threshold (default: 0.7)
     :type threshold: float between 0.0 and 1.0, inclusive
     :returns: a :class:`.SearchResult`



  .. py:method:: knearest_tanimoto_search_fp(query_fp, k=3, threshold=0.7)

     Find the k-nearest fingerprints which are sufficiently similar to the query fingerprint
     
     Find all of the fingerprints in this arena which are at least
     *threshold* similar to the query fingerprint, and of those, select
     the top *k* hits. The hits are returned as a :class:`.SearchResult`,
     sorted from highest score to lowest.
     
     :param queries: query fingerprints
     :type queries: a :class:`.FingerprintArena`
     :param threshold: minimum similarity threshold (default: 0.7)
     :type threshold: float between 0.0 and 1.0, inclusive
     :returns: a :class:`.SearchResult`



====================
chemfp.search module
====================

.. _chemfp_search:
.. py:module:: chemfp.search


The following functions and classes are in the chemfp.search module.

There are three main classes of functions. The ones ending with
``*_fp`` use a query fingerprint to search a target arena. The ones
ending with ``*_arena`` use a query arena to search a target
arena. The ones ending with ``*_symmetric`` use arena to search
itself, except that a fingerprint is not tested against itself.


These functions share the same name with very similar functions in the
top-level :mod:`chemfp` module. My apologies for any confusion. The
top-level functions are designed to work with both arenas and
iterators as the target. They give a simple search API, and
automatically process in blocks, to give a balanced trade-off between
performance and response time for the first results.

The functions in this module only work with arena as the target. By
default it searches the entire arena before returning. If you want to
process portions of the arena then you need to specify the range
yourself.




.. py:function:: count_tanimoto_hits_fp(query_fp, target_arena, threshold=0.7)

   Count the number of hits in *target_arena* at least *threshold* similar to the *query_fp*
   
   Example::
   
       query_id, query_fp = chemfp.load_fingerprints("queries.fps")[0]
       targets = chemfp.load_fingerprints("targets.fps")
       print chemfp.search.count_tanimoto_hits_fp(query_fp, targets, threshold=0.1)
       
   
   :param query_fp: the query fingerprint
   :type query_fp: a byte string
   :param target_arena: the target arena
   :type target_fp: a :class:`FingerprintArena`
   :param threshold: The minimum score threshold.
   :type threshold: float between 0.0 and 1.0, inclusive
   :returns: an integer count



.. py:function:: count_tanimoto_hits_arena(query_arena, target_arena, threshold=0.7)

   For each fingerprint in *query_arena*, count the number of hits in *target_arena* at least *threshold* similar to it
   
   Example::
   
       queries = chemfp.load_fingerprints("queries.fps")
       targets = chemfp.load_fingerprints("targets.fps")
       counts = chemfp.search.count_tanimoto_hits_arena(queries, targets, threshold=0.1)
       print counts[:10]
   
   The result is implementation specific. You'll always be able to
   get its length and do an index lookup to get an integer
   count. Currently it's a `ctypes array of longs <https://docs.python.org/2/library/ctypes.html#arrays>`_,
   but it could be an `array.array <https://docs.python.org/2/library/array.html>`_
   or Python list in the future.
   
   :param query_arena: The query fingerprints.
   :type query_arena: a :class:`chemfp.arena.FingerprintArena`
   :param target_arena: The target fingerprints.
   :type target_arena: a :class:`chemfp.arena.FingerprintArena`
   :param threshold: The minimum score threshold.
   :type threshold: float between 0.0 and 1.0, inclusive
   :returns: an array of counts



.. py:function:: count_tanimoto_hits_symmetric(arena, threshold=0.7, batch_size=100)

   For each fingerprint in the *arena*, count the number of other fingerprints at least *threshold* similar to it
   
   A fingerprint never matches itself.
   
   The computation can take a long time. Python won't check check for
   a ``^C`` until the function finishes. This can be irritating. Instead,
   process only *batch_size* rows at a time before checking for a ``^C``.
   
   Note: the *batch_size* may disappear in future versions of chemfp.
   I can't detect any performance difference between the current value
   and a larger value, so it seems rather pointless to have. Let me
   know if it's useful to keep as a user-defined parameter.
   
   Example::
   
       arena = chemfp.load_fingerprints("targets.fps")
       counts = chemfp.search.count_tanimoto_hits_symmetric(arena, threshold=0.2)
       print counts[:10]
   
   The result object is implementation specific. You'll always be able to
   get its length and do an index lookup to get an integer
   count. Currently it's a ctype array of longs, but it could be an
   array.array or Python list in the future.
   
   :param arena: the set of fingerprints
   :type arena: a :class:`chemfp.arena.FingerprintArena`
   :param threshold: The minimum score threshold.
   :type threshold: float between 0.0 and 1.0, inclusive
   :param batch_size: the number of rows to process before checking for a ``^C``
   :type batch_size: integer
   :returns: an array of counts
 


.. py:function:: partial_count_tanimoto_hits_symmetric(counts, arena, threshold=0.7, query_start=0, query_end=None, target_start=0, target_end=None)

   Compute a portion of the symmetric Tanimoto counts
   
   For most cases, use :func:`chemfp.search.count_tanimoto_hits_symmetric`
   instead of this function!
   
   This function is only useful for thread-pool implementations. In
   that case, set the number of OpenMP threads to 1.
   
   *counts* is a contiguous array of integers. It should be
   initialized to zeros, and reused for successive calls.
   
   The function adds counts for counts[*query_start*:*query_end*] based
   on computing the upper-triangle portion contained in the rectangle
   *query_start*:*query_end* and *target_start*:target_end* and using
   symmetry to fill in the lower half.
   
   You know, this is pretty complicated. Here's the bare minimum
   example of how to use it correctly to process 10 rows at a time
   using up to 4 threads::
   
       import chemfp
       import chemfp.search
       from chemfp import futures
       import array
       
       chemfp.set_num_threads(1)  # Globally disable OpenMP
       
       arena = chemfp.load_fingerprints("targets.fps")  # Load the fingerprints
       n = len(arena)
       counts = array.array("i", [0]*n)
       
       with futures.ThreadPoolExecutor(max_workers=4) as executor:
           for row in xrange(0, n, 10):
               executor.submit(chemfp.search.partial_count_tanimoto_hits_symmetric,
                               counts, arena, threshold=0.2,
                               query_start=row, query_end=min(row+10, n))
       
       print counts
   
   :param counts: the accumulated Tanimoto counts
   :type counts: a contiguous block of integer
   :param arena: the fingerprints.
   :type arena: a :class:`chemfp.arena.FingerprintArena`
   :param threshold: The minimum score threshold.
   :type threshold: float between 0.0 and 1.0, inclusive
   :param query_start: the query start row
   :type query_start: an integer
   :param query_end: the query end row
   :type query_end: an integer, or None to mean the last query row
   :param target_start: the target start row
   :type target_start: an integer
   :param target_end: the target end row
   :type target_end: an integer, or None to mean the last target row
   :returns: None




.. py:function:: threshold_tanimoto_search_fp(query_fp, target_arena, threshold=0.7)

   Search for fingerprint hits in *target_arena* which are at least *threshold* similar to *query_fp*
   
   The hits in the returned :class:`chemfp.search.SearchResult` are in arbitrary order.
   
   Example::
   
       query_id, query_fp = chemfp.load_fingerprints("queries.fps")[0]
       targets = chemfp.load_fingerprints("targets.fps")
       print list(chemfp.search.threshold_tanimoto_search_fp(query_fp, targets, threshold=0.15))
   
   :param query_fp: the query fingerprint
   :type query_fp: a byte string
   :param target_arena: the target arena
   :type target_arena: a :class:`chemfp.arena.FingerprintArena`
   :param threshold: The minimum score threshold.
   :type threshold: float between 0.0 and 1.0, inclusive
   :returns: a :class:`chemfp.search.SearchResult`



.. py:function:: threshold_tanimoto_search_arena(query_arena, target_arena, threshold=0.7)

   Search for the hits in the *target_arena* at least *threshold* similar to the fingerprints in *query_arena*
   
   The hits in the returned :class:`chemfp.search.SearchResults` are in arbitrary order.
   
   Example::
   
       queries = chemfp.load_fingerprints("queries.fps")
       targets = chemfp.load_fingerprints("targets.fps")
       results = chemfp.search.threshold_tanimoto_search_arena(queries, targets, threshold=0.5)
       for query_id, query_hits in zip(queries.ids, results):
           if len(query_hits) > 0:
               print query_id, "->", ", ".join(query_hits.get_ids())
   
   :param query_arena: The query fingerprints.
   :type query_arena: a :class:`chemfp.arena.FingerprintArena`
   :param target_arena: The target fingerprints.
   :type target_arena: a :class:`chemfp.arena.FingerprintArena`
   :param threshold: The minimum score threshold.
   :type threshold: float between 0.0 and 1.0, inclusive
   :returns: a :class:`chemfp.search.SearchResults`



.. py:function:: threshold_tanimoto_search_symmetric(arena, threshold=0.7, include_lower_triangle=True, batch_size=100)

   Search for the hits in the *arena* at least *threshold* similar to the fingerprints in the arena
   
   When *include_lower_triangle* is True, compute the upper-triangle
   similarities, then copy the results to get the full set of
   results. When *include_lower_triangle* is False, only compute the
   upper triangle.
   
   The hits in the returned :class:`chemfp.search.SearchResults` are in arbitrary order.
   
   The computation can take a long time. Python won't check check for
   a ``^C`` until the function finishes. This can be irritating. Instead,
   process only *batch_size* rows at a time before checking for a ``^C``.
   
   Note: the *batch_size* may disappear in future versions of chemfp. Let
   me know if it really is useful for you to have as a user-defined parameter.
   
   Example::
   
       arena = chemfp.load_fingerprints("queries.fps")
       full_result = chemfp.search.threshold_tanimoto_search_symmetric(arena, threshold=0.2)
       upper_triangle = chemfp.search.threshold_tanimoto_search_symmetric(
                 arena, threshold=0.2, include_lower_triangle=False)
       assert sum(map(len, full_result)) == sum(map(len, upper_triangle))*2
                 
   :param arena: the set of fingerprints
   :type arena: a :class:`chemfp.arena.FingerprintArena`
   :param threshold: The minimum score threshold.
   :type threshold: float between 0.0 and 1.0, inclusive
   :param include_lower_triangle:
       if False, compute only the upper triangle, otherwise use symmetry to compute the full matrix
   :type include_lower_triangle: boolean
   :param batch_size: the number of rows to process before checking for a ^C
   :type batch_size: integer
   :returns: a :class:`chemfp.search.SearchResults`
 


.. py:function:: partial_threshold_tanimoto_search_symmetric(results, arena, threshold=0.7, query_start=0, query_end=None, target_start=0, target_end=None, results_offset=0)

   Compute a portion of the symmetric Tanimoto search results
   
   For most cases, use :func:`chemfp.search.threshold_tanimoto_search_symmetric`
   instead of this function!
   
   This function is only useful for thread-pool implementations. In
   that case, set the number of OpenMP threads to 1.
   
   *results* is a :class:`chemfp.search.SearchResults` instance which is at
   least as large as the arena. It should be reused for successive updates.
   
   The function adds hits to results[*query_start*:*query_end*], based
   on computing the upper-triangle portion contained in the rectangle
   *query_start*:*query_end* and *target_start*:*target_end*.
   
   It does not fill in the lower triangle. To get the full matrix,
   call *fill_lower_triangle*.
   
   You know, this is pretty complicated. Here's the bare minimum
   example of how to use it correctly to process 10 rows at a time
   using up to 4 threads::
   
       import chemfp
       import chemfp.search
       from chemfp import futures
       import array
   
       chemfp.set_num_threads(1)
   
       arena = chemfp.load_fingerprints("targets.fps")
       n = len(arena)
       results = chemfp.search.SearchResults(n, n, arena.ids)
   
       with futures.ThreadPoolExecutor(max_workers=4) as executor:
           for row in xrange(0, n, 10):
               executor.submit(chemfp.search.partial_threshold_tanimoto_search_symmetric,
                               results, arena, threshold=0.2,
                               query_start=row, query_end=min(row+10, n))
   
       chemfp.search.fill_lower_triangle(results)
   
   The hits in the :class:`chemfp.search.SearchResults` are in arbitrary order.
   
   :param results: the intermediate search results
   :type results: a :class:`chemfp.search.SearchResults` instance
   :param arena: the fingerprints.
   :type arena: a :class:`chemfp.arena.FingerprintArena`
   :param threshold: The minimum score threshold.
   :type threshold: float between 0.0 and 1.0, inclusive
   :param query_start: the query start row
   :type query_start: an integer
   :param query_end: the query end row
   :type query_end: an integer, or None to mean the last query row
   :param target_start: the target start row
   :type target_start: an integer
   :param target_end: the target end row
   :type target_end: an integer, or None to mean the last target row
   :param results_offset: use results[results_offset] as the base for the results
   :param results_offset: an integer
   :returns: None



.. py:function:: fill_lower_triangle(results)

   Duplicate each entry of *results* to its transpose
   
   This is used after the symmetric threshold search to turn the
   upper-triangle results into a full matrix.
   
   :param results: search results
   :type results: a :class:`chemfp.search.SearchResults`




.. py:function:: knearest_tanimoto_search_fp(query_fp, target_arena, k=3, threshold=0.7)

   Search for *k*-nearest hits in *target_arena* which are at least *threshold* similar to *query_fp*
   
   The hits in the :class:`chemfp.search.SearchResults` are ordered by
   decreasing similarity score.
   
   Example::
   
       query_id, query_fp = chemfp.load_fingerprints("queries.fps")[0]
       targets = chemfp.load_fingerprints("targets.fps")
       print list(chemfp.search.knearest_tanimoto_search_fp(query_fp, targets, k=3, threshold=0.0))
   
   :param query_fp: the query fingerprint
   :type query_fp: a byte string
   :param target_arena: the target arena
   :type target_arena: a :class:`chemfp.arena.FingerprintArena`
   :param k: the number of nearest neighbors to find.
   :type k: positive integer
   :param threshold: The minimum score threshold.
   :type threshold: float between 0.0 and 1.0, inclusive
   :returns: a :class:`chemfp.search.SearchResult`



.. py:function:: knearest_tanimoto_search_arena(query_arena, target_arena, k=3, threshold=0.7)

   Search for the *k* nearest hits in the *target_arena* at least *threshold* similar to the fingerprints in *query_arena*
   
   The hits in the :class:`chemfp.search.SearchResults` are ordered by
   decreasing similarity score.
   
   Example::
   
       queries = chemfp.load_fingerprints("queries.fps")
       targets = chemfp.load_fingerprints("targets.fps")
       results = chemfp.search.knearest_tanimoto_search_arena(queries, targets, k=3, threshold=0.5)
       for query_id, query_hits in zip(queries.ids, results):
           if len(query_hits) >= 2:
               print query_id, "->", ", ".join(query_hits.get_ids())
   
   :param query_arena: The query fingerprints.
   :type query_arena: a :class:`chemfp.arena.FingerprintArena`
   :param target_arena: The target fingerprints.
   :type target_arena: a :class:`chemfp.arena.FingerprintArena`
   :param k: the number of nearest neighbors to find.
   :type k: positive integer
   :param threshold: The minimum score threshold.
   :type threshold: float between 0.0 and 1.0, inclusive
   :returns: a :class:`chemfp.search.SearchResults`



.. py:function:: knearest_tanimoto_search_symmetric(arena, k=3, threshold=0.7, batch_size=100)

   Search for the *k*-nearest hits in the *arena* at least *threshold* similar to the fingerprints in the arena
   
   The hits in the :class:`SearchResults` are ordered by decreasing similarity score.
   
   The computation can take a long time. Python won't check check for
   a ``^C`` until the function finishes. This can be irritating. Instead,
   process only *batch_size* rows at a time before checking for a ``^C.``
   
   Note: the *batch_size* may disappear in future versions of chemfp. Let
   me know if it really is useful for you to keep as a user-defined parameter.
   
   Example::
   
       arena = chemfp.load_fingerprints("queries.fps")
       results = chemfp.search.knearest_tanimoto_search_symmetric(arena, k=3, threshold=0.8)
       for (query_id, hits) in zip(arena.ids, results):
           print query_id, "->", ", ".join(("%s %.2f" % hit) for hit in  hits.get_ids_and_scores())
   
   :param arena: the set of fingerprints
   :type arena: a :class:`chemfp.arena.FingerprintArena`
   :param k: the number of nearest neighbors to find.
   :type k: positive integer
   :param threshold: The minimum score threshold.
   :type threshold: float between 0.0 and 1.0, inclusive
   :param include_lower_triangle:
       if False, compute only the upper triangle, otherwise use symmetry to compute the full matrix
   :type include_lower_triangle: boolean
   :param batch_size: the number of rows to process before checking for a ^C
   :type batch_size: integer
   :returns: a :class:`chemfp.search.SearchResults`




.. py:function:: contains_fp(query_fp, target_arena)

   Find the target fingerprints which contain the query fingerprint bits as a subset
   
   A target fingerprint contains a query fingerprint if all of the on
   bits of the query fingerprint are also on bits of the target
   fingerprint. This function returns a :class:`chemfp.search.SearchResult`
   containing all of the target fingerprints in *target_arena* that contain
   the *query_fp*.
   
   The SearchResult scores are all 0.0. 
   
   There is currently no direct way to limit the arena search range.
   Instead create a subarena by using Python's slice notation on the
   arena then search the subarena.
   
   :param query_fp: the query fingerprint
   :type query_fp: a byte string
   :param target_arena: The target fingerprints.
   :type target_arena: a :class:`chemfp.arena.FingerprintArena`
   :returns: a SearchResult instance



.. py:function:: contains_arena(query_arena, target_arena)

   Find the target fingerprints which contain the query fingerprints as a subset
   
   A target fingerprint contains a query fingerprint if all of the on
   bits of the query fingerprint are also on bits of the target
   fingerprint. This function returns a :class:`chemfp.search.SearchResults`
   where SearchResults[i] contains all of the target fingerprints in
   *target_arena* that contain the fingerprint for entry
   *query_arena* [i].
   
   The SearchResult scores are all 0.0.
   
   There is currently no direct way to limit the arena search range,
   though you can create and search a subarena by using Python's
   slice notation.
   
   :param query_arena: the query fingerprints
   :type query_arena: a :class:`chemfp.arena.FingerprintArena`
   :param target_arena: the target fingerprints
   :type target_arena: a :class:`chemfp.arena.FingerprintArena`
   :returns: a :class:`chemfp.search.SearchResults` instance, of the same size as query_arena




SearchResults
=============

.. py:class:: SearchResults

   Search results for a list of query fingerprints against a target arena
   
   This acts like a list of SearchResult elements, with the ability
   to iterate over each search results, look them up by index, and
   get the number of scores.
   
   In addition, there are helper methods to iterate over each hit and
   to get the hit indicies, scores, and identifiers directly as Python
   lists, sort the list contents, and more.



  .. py:method:: __len__()

     The number of rows in the SearchResults



  .. py:method:: __iter__()

     Iterate over each SearchResult hit



  .. py:method:: __getitem__(i)

     Get the *i*-th SearchResult




  .. py:attribute:: SearchResults.shape

     Read-only attribute.

     the tuple (number of rows, number of columns)
     
     The number of columns is the size of the target arena.



  .. py:method:: iter_indices()

     For each hit, yield the list of target indices



  .. py:method:: iter_ids()

     For each hit, yield the list of target identifiers



  .. py:method:: iter_scores()

     For each hit, yield the list of target scores



  .. py:method:: iter_indices_and_scores()

     For each hit, yield the list of (target index, score) tuples



  .. py:method:: iter_ids_and_scores()

     For each hit, yield the list of (target id, score) tuples



  .. py:method:: clear_all()

     Remove all hits from all of the search results



  .. py:method:: count_all(min_score=None, max_score=None, interval="[]")

     Count the number of hits with a score between *min_score* and *max_score*
     
     Using the default parameters this returns the number of
     hits in the result.
     
     The default *min_score* of None is equivalent to -infinity.
     The default *max_score* of None is equivalent to +infinity.
     
     The *interval* parameter describes the interval end
     conditions. The default of "[]" uses a closed interval,
     where min_score <= score <= max_score. The interval "()"
     uses the open interval where min_score < score < max_score.
     The half-open/half-closed intervals "(]" and "[)" are
     also supported.
     
     :param min_score: the minimum score in the range.
     :type min_score: a float, or None for -infinity
     :param max_score: the maximum score in the range.
     :type max_score: a float, or None for +infinity
     :param interval: specify if the end points are open or closed.
     :type interval: one of "[]", "()", "(]", "[)"
     :returns: an integer count



  .. py:method:: cumulative_score_all(min_score=None, max_score=None, interval="[]")

     The sum of all scores in all rows which are between *min_score* and *max_score*
     
     Using the default parameters this returns the sum of all of
     the scores in all of the results. With a specified range this
     returns the sum of all of the scores in that range. The
     cumulative score is also known as the raw score.
     
     The default *min_score* of None is equivalent to -infinity.
     The default *max_score* of None is equivalent to +infinity.
     
     The *interval* parameter describes the interval end
     conditions. The default of "[]" uses a closed interval,
     where min_score <= score <= max_score. The interval "()"
     uses the open interval where min_score < score < max_score.
     The half-open/half-closed intervals "(]" and "[)" are
     also supported.
     
     :param min_score: the minimum score in the range.
     :type min_score: a float, or None for -infinity
     :param max_score: the maximum score in the range.
     :type max_score: a float, or None for +infinity
     :param interval: specify if the end points are open or closed.
     :type interval: one of "[]", "()", "(]", "[)"
     :returns: a floating point count



  .. py:method:: reorder_all(order="decreasing-score")

     Reorder the hits for all of the rows based on the requested *order*.
     
     The available orderings are:
     
     * increasing-score - sort by increasing score
     * decreasing-score - sort by decreasing score
     * increasing-index - sort by increasing target index
     * decreasing-index - sort by decreasing target index
     * move-closest-first - move the hit with the highest score to the first position
     * reverse - reverse the current ordering
     
     :param ordering: the name of the ordering to use



  .. py:method:: to_csr(dtype=None)

     Return the results as a SciPy compressed sparse row matrix.
     
     The returned matrix has the same shape as the SearchResult
     instance and can be passed into, for example, a scikit-learn
     clustering algorithm.
     
     By default the scores are stored with the `dtype` is "float64".
     
     This method requires that SciPy (and NumPy) be installed.
     
     :param dtype: a NumPy numeric data type
     :type dtype: string or NumPy type



SearchResult
============

.. py:class:: SearchResult

   Search results for a query fingerprint against a target arena.
   
   The results contains a list of hits. Hits contain a target index,
   score, and optional target ids. The hits can be reordered based on
   score or index.



  .. py:method:: __len__()

     The number of hits



  .. py:method:: __iter__()

     Iterate through the pairs of (target index, score) using the current ordering



  .. py:method:: clear()

     Remove all hits from this result



  .. py:method:: get_indices()

     The list of target indices, in the current ordering.



  .. py:method:: get_ids()

     The list of target identifiers (if available), in the current ordering



  .. py:method:: iter_ids()

     Iterate over target identifiers (if available), in the current ordering



  .. py:method:: get_scores()

     The list of target scores, in the current ordering



  .. py:method:: get_ids_and_scores()

     The list of (target identifier, target score) pairs, in the current ordering
     
     Raises a TypeError if the target IDs are not available.



  .. py:method:: get_indices_and_scores()

     The list of (target index, score) pairs, in the current ordering



  .. py:method:: reorder(ordering="decreasing-score")

     Reorder the hits based on the requested ordering.
     
     The available orderings are:
       * increasing-score - sort by increasing score
       * decreasing-score - sort by decreasing score
       * increasing-index - sort by increasing target index
       * decreasing-index - sort by decreasing target index
       * move-closest-first - move the hit with the highest score to the first position
       * reverse - reverse the current ordering
     
     :param string ordering: the name of the ordering to use



  .. py:method:: count(min_score=None, max_score=None, interval="[]")

     Count the number of hits with a score between *min_score* and *max_score*
     
     Using the default parameters this returns the number of
     hits in the result.
     
     The default *min_score* of None is equivalent to -infinity.
     The default *max_score* of None is equivalent to +infinity.
     
     The *interval* parameter describes the interval end
     conditions. The default of "[]" uses a closed interval,
     where min_score <= score <= max_score. The interval "()"
     uses the open interval where min_score < score < max_score.
     The half-open/half-closed intervals "(]" and "[)" are
     also supported.
     
     :param min_score: the minimum score in the range.
     :type min_score: a float, or None for -infinity
     :param max_score: the maximum score in the range.
     :type max_score: a float, or None for +infinity
     :param interval: specify if the end points are open or closed.
     :type interval: one of "[]", "()", "(]", "[)"
     :returns: an integer count



  .. py:method:: cumulative_score(min_score=None, max_score=None, interval="[]")

     The sum of the scores which are between *min_score* and *max_score*
     
     Using the default parameters this returns the sum of all of
     the scores in the result. With a specified range this returns
     the sum of all of the scores in that range. The cumulative
     score is also known as the raw score.
     
     The default *min_score* of None is equivalent to -infinity.
     The default *max_score* of None is equivalent to +infinity.
     
     The *interval* parameter describes the interval end
     conditions. The default of "[]" uses a closed interval,
     where min_score <= score <= max_score. The interval "()"
     uses the open interval where min_score < score < max_score.
     The half-open/half-closed intervals "(]" and "[)" are
     also supported.
     
     :param min_score: the minimum score in the range.
     :type min_score: a float, or None for -infinity
     :param max_score: the maximum score in the range.
     :type max_score: a float, or None for +infinity
     :param interval: specify if the end points are open or closed.
     :type interval: one of "[]", "()", "(]", "[)"
     :returns: a floating point value


.. _chemfp.bitops:

=====================
chemfp.bitops module
=====================

.. py:module:: chemfp.bitops

The following functions from the chemfp.bitops module provide
low-level bit operations on byte and hex fingerprints.



.. py:function:: byte_contains(super_fp, sub_fp)

   Return 1 if the on bits of sub_fp are also 1 bits in super_fp



.. py:function:: byte_contains_bit(fp, bit_index)

   Return True if the the given bit position is on, otherwise False



.. py:function:: byte_difference(fp1, fp2)

   Return the absolute difference (xor) between the two byte strings, fp1 ^ fp2



.. py:function:: byte_from_bitlist(fp[, num_bits=1024])

   Convert a list of bit positions into a byte fingerprint, including modulo folding



.. py:function:: byte_hex_tanimoto(fp1, fp2)

   Compute the Tanimoto similarity between the byte fingerprint *fp1* and the hex fingerprint *fp2*.
   Return a float between 0.0 and 1.0, or raise a ValueError if *fp2* is not a hex fingerprint



.. py:function:: byte_intersect(fp1, fp2)

   Return the intersection of the two byte strings, *fp1* & *fp2*



.. py:function:: byte_intersect_popcount(fp1, fp2)

   Return the number of bits set in the instersection of the two byte fingerprints



.. py:function:: byte_popcount(fp)

   Return the number of bits set in a byte fingerprint



.. py:function:: byte_tanimoto(fp1, fp2)

   Compute the Tanimoto similarity between two byte fingerprints



.. py:function:: byte_to_bitlist(bitlist)

   Return a sorted list of the on-bit positions in the byte fingerprint



.. py:function:: byte_union(fp1, fp2)

   Return the union of the two byte strings, *fp1* | *fp2*



.. py:function:: hex_contains(sub_fp, super_fp)

   Return 1 if the on bits of sub_fp are also on bits in super_fp, otherwise 0.
   Return -1 if either string is not a hex fingerprint



.. py:function:: hex_contains_bit(fp, bit_index)

   Return True if the the given bit position is on, otherwise False.
   
   This function does not validate that the hex fingerprint is actually in hex.



.. py:function:: hex_difference(fp1, fp2)

   Return the absolute difference (xor) between the two hex strings, *fp1* ^ *fp2*.
   Raises a ValueError for non-hex fingerprints.



.. py:function:: hex_from_bitlist(fp[, num_bits=1024])

   Convert a list of bit positions into a hex fingerprint, including modulo folding



.. py:function:: hex_intersect(fp1, fp2)

   Return the intersection of the two hex strings, *fp1* & *fp2*.
   Raises a ValueError for non-hex fingerprints.



.. py:function:: hex_intersect_popcount(fp1, fp2)

   Return the number of bits set in the intersection of the two hex fingerprint,
   or -1 if either string is a non-hex string



.. py:function:: hex_isvalid(s)

   Return 1 if the string is a valid hex fingerprint, otherwise 0



.. py:function:: hex_popcount(fp)

   Return the number of bits set in a hex fingerprint, or -1 for non-hex strings



.. py:function:: hex_tanimoto(fp1, fp2)

   Compute the Tanimoto similarity between two hex fingerprints.
   Return a float between 0.0 and 1.0, or -1.0 if either string is not a hex fingerprint



.. py:function:: hex_to_bitlist(bitlist)

   Return a sorted list of the on-bit positions in the hex fingerprint



.. py:function:: hex_union(fp1, fp2)

   Return the union of the two hex strings, *fp1* | *fp2*.
   Raises a ValueError for non-hex fingerprints.



.. py:function:: hex_encode(s)

   Encode the byte string or ASCII string to hex. Returns a text string.



.. py:function:: hex_encode_as_bytes(s)

   Encode the byte string or ASCII string to hex. Returns a byte string.



.. py:function:: hex_decode(s)

   Decode the hex-encoded value to a byte string


================
chemfp.encodings
================

.. py:module:: chemfp.encodings

Decode different fingerprint representations into chemfp
form. (Currently only decoders are available. Future released may
include encoders.)

The chemfp fingerprints are stored as byte strings, with the bytes in
least-significant bit order (bit #0 is stored in the first/left-most
byte) and with the bits in most-significant bit order (bit #0 is
stored in the first/right-most bit of the first byte).

Other systems use different encodings. These include:
  - the '0 and '1' characters, as in '00111101'
  - hex encoding, like '3d'
  - base64 encoding, like 'SGVsbG8h'
  - CACTVS's variation of base64 encoding

plus variations of different LSB and MSB orders.

This module decodes most of the fingerprint encodings I have come
across. The fingerprint decoders return a 2-ple of the bit length and
the chemfp fingerprint. The bit length is None unless the bit length
is known exactly, which currently is only the case for the binary and
CACTVS fingerprints. (The hex and other encoders must round the
fingerprints up to a multiple of 8 bits.)



.. py:function:: from_binary_lsb(text)

   Convert a string like '00010101' (bit 0 here is off) into '\xa8'
   
   The encoding characters '0' and '1' are in LSB order, so bit 0 is the left-most field.
   The result is a 2-ple of the fingerprint length and the decoded chemfp fingerprint
   
   >>> from_binary_lsb('00010101')
   (8, '\xa8')
   >>> from_binary_lsb('11101')
   (5, '\x17')
   >>> from_binary_lsb('00000000000000010000000000000')
   (29, '\x00\x80\x00\x00')
   >>>



.. py:function:: from_binary_msb(text)

   Convert a string like '10101000' (bit 0 here is off) into '\xa8'
   
   The encoding characters '0' and '1' are in MSB order, so bit 0 is the right-most field.
   
   >>> from_binary_msb('10101000')
   (8, '\xa8')
   >>> from_binary_msb('00010101')
   (8, '\x15')
   >>> from_binary_msb('00111')
   (5, '\x07')
   >>> from_binary_msb('00000000000001000000000000000')
   (29, '\x00\x80\x00\x00')
   >>>



.. py:function:: from_base64(text)

   Decode a base64 encoded fingerprint string
   
   The encoded fingerprint must be in chemfp form, with the bytes in
   LSB order and the bits in MSB order.
   
   >>> from_base64("SGk=")
   (None, 'Hi')
   >>> from_base64("SGk=")[1].encode("hex")
   '4869'
   >>> 



.. py:function:: from_hex(text)

   Decode a hex encoded fingerprint string
   
   The encoded fingerprint must be in chemfp form, with the bytes in
   LSB order and the bits in MSB order.
   
   >>> from_hex('10f2')
   (None, '\x10\xf2')
   >>>
   
   Raises a ValueError if the hex string is not a multiple of 2 bytes long
   or if it contains a non-hex character.



.. py:function:: from_hex_msb(text)

   Decode a hex encoded fingerprint string where the bits and bytes are in MSB order
   
   >>> from_hex_msb('10f2')
   (None, '\xf2\x10')
   >>>
   
   Raises a ValueError if the hex string is not a multiple of 2 bytes long
   or if it contains a non-hex character.



.. py:function:: from_hex_lsb(text)

   Decode a hex encoded fingerprint string where the bits and bytes are in LSB order
   
   >>> from_hex_lsb('102f')
   (None, '\x08\xf4')
   >>> 
   
   Raises a ValueError if the hex string is not a multiple of 2 bytes long
   or if it contains a non-hex character.



.. py:function:: from_cactvs(text)

   Decode a 881-bit CACTVS-encoded fingerprint used by PubChem
   
   >>> from_cactvs("AAADceB7sQAEAAAAAAAAAAAAAAAAAWAAAAAwAAAAAAAAAAABwAAAHwIYAAAADA" +
   ...             "rBniwygJJqAACqAyVyVACSBAAhhwIa+CC4ZtgIYCLB0/CUpAhgmADIyYcAgAAO" +
   ...             "AAAAAAABAAAAAAAAAAIAAAAAAAAAAA==")
   (881, '\x07\xde\x8d\x00 \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x06\x00\x00\x00\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x80\x03\x00\x00\xf8@\x18\x00\x00\x000P\x83y4L\x01IV\x00\x00U\xc0\xa4N*\x00I \x00\x84\xe1@X\x1f\x04\x1df\x1b\x10\x06D\x83\xcb\x0f)%\x10\x06\x19\x00\x13\x93\xe1\x00\x01\x00p\x00\x00\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00@\x00\x00\x00\x00\x00\x00\x00\x00')
   >>>
   
   For format details, see
     ftp://ftp.ncbi.nlm.nih.gov/pubchem/specifications/pubchem_fingerprints.txt



.. py:function:: from_daylight(text)

   Decode a Daylight ASCII fingerprint
   
   >>> from_daylight("I5Z2MLZgOKRcR...1")
   (None, 'PyDaylight')
   
   See the implementation for format details.



.. py:function:: from_on_bit_positions(text, num_bits=1024, separator=" ")

   Decode from a list of integers describing the location of the on bits
   
   >>> from_on_bit_positions("1 4 9 63", num_bits=32)
   (32, '\x12\x02\x00\x80')
   >>> from_on_bit_positions("1,4,9,63", num_bits=64, separator=",")
   (64, '\x12\x02\x00\x00\x00\x00\x00\x80')
   
   The text contains a sequence of non-negative integer values
   separated by the `separator` text. Bit positions are folded modulo
   num_bits. 
   
   This is often used to convert sparse fingerprints into a dense
   fingerprint.



.. py:module:: chemfp.fps_io

==================== 
chemfp.fps_io module
====================

This module is part of the private API. Do not import it directly.

The function :func:`chemfp.open` returns an FPSReader if the source is
an FPS file. The function :func:`chemfp.open_fingerprint_writer`
returns an FPSWriter if the destination is an FPS file.


FPSReader
=========

.. py:class:: FPSReader

   FPS file reader
   
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




  .. py:method:: __iter__()

     Iterate through the (id, fp) pairs



  .. py:method:: iter_arenas(arena_size=1000)

     iterate through *arena_size* fingerprints at a time, as subarenas
     
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



  .. py:method:: save(destination, format=None)

     Save the fingerprints to a given destination and format
     
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



  .. py:method:: get_fingerprint_type()

     Get the fingerprint type object based on the metadata's type field
     
     This uses ``self.metadata.type`` to get the fingerprint type
     string then calls :func:`chemfp.get_fingerprint_type` to get and return
     a :class:`chemfp.types.FingerprintType` instance.
     
     This will raise a TypeError if there is no metadata, and
     a ValueError if the type field was invalid or the fingerprint
     type isn't available.
     
     :returns: a :class:`chemfp.types.FingerprintType`



  .. py:method:: close()

     Close the file




  .. py:method:: count_tanimoto_hits_fp(query_fp, threshold=0.7)

     Count the fingerprints which are sufficiently similar to the query fingerprint
     
     Return the number of fingerprints in the reader which are
     at least *threshold* similar to the query fingerprint *query_fp*.
     
     :param query_fp: query fingerprint
     :type query_fp: byte string
     :param threshold: minimum similarity threshold (default: 0.7)
     :type threshold: float between 0.0 and 1.0, inclusive
     :returns: integer count



  .. py:method:: count_tanimoto_hits_arena(queries, threshold=0.7)

     Count the fingerprints which are sufficiently similar to each query fingerprint
     
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



  .. py:method:: threshold_tanimoto_search_fp(query_fp, threshold=0.7)

     Find the fingerprints which are sufficiently similar to the query fingerprint
     
     Find all of the fingerprints in this reader which are at least
     *threshold* similar to the query fingerprint *query_fp*.  The
     hits are returned as a :class:`.SearchResult`, in arbitrary
     order.
     
     :param query_fp: query fingerprint
     :type query_fp: byte string
     :param threshold: minimum similarity threshold (default: 0.7)
     :type threshold: float between 0.0 and 1.0, inclusive
     :returns: a :class:`.SearchResult`



  .. py:method:: threshold_tanimoto_search_arena(queries, threshold=0.7)

     Find the fingerprints which are sufficiently similar to each of the query fingerprints
     
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



  .. py:method:: knearest_tanimoto_search_fp(query_fp, k=3, threshold=0.7)

     Find the k-nearest fingerprints which are sufficiently similar to the query fingerprint
     
     Find all of the fingerprints in this reader which are at least
     *threshold* similar to the query fingerprint, and of those, select
     the top *k* hits. The hits are returned as a :class:`.SearchResult`,
     sorted from highest score to lowest.
     
     :param queries: query fingerprints
     :type queries: a :class:`.FingerprintArena`
     :param threshold: minimum similarity threshold (default: 0.7)
     :type threshold: float between 0.0 and 1.0, inclusive
     :returns: a :class:`.SearchResult`



  .. py:method:: knearest_tanimoto_search_arena(queries, k=3, threshold=0.7)

     Find the k-nearest fingerprints which are sufficiently similar to each of the query fingerprints
     
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




FPSWriter
=========

.. py:class:: FPSWriter

   Write fingerprints in FPS format.
   
   This is a subclass of :class:`chemfp.FingerprintWriter`.
   
   Instances have the following attributes:
   
   * metadata - a :class:`chemfp.Metadata` instance
   * closed - False when the file is open, else True
   * location - a :class:`chemfp.io.Location` instance
   
   An FPSWriter is its own context manager, and will close the
   output file on context exit.
   
   The Location instance supports the "recno", "output_recno",
   and "lineno" properties.



  .. py:method:: write_fingerprint(id, fp)

     Write a single fingerprint record with the given id and fp
     
     :param string id: the record identifier
     :param bytes fp: the fingerprint



  .. py:method:: write_fingerprints(id_fp_pairs)

     Write a sequence of fingerprint records
     
     :param id_fp_pairs: An iterable of (id, fingerprint) pairs.
 


  .. py:method:: close()

     Close the writer
     
     This will set self.closed to False.
 


================
chemfp.io module
================

.. py:module:: chemfp.io

This module implements a single public class, :class:`Location`, which
tracks parser state information, including the location of the current
record in the file. The other functions and classes are undocumented,
should not be used, and may change in future releases.


Location
========

.. py:class:: Location

   Get location and other internal reader and writer state information
   
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



  .. py:method:: __init__(filename=None)

     Use *filename* as the location's filename



  .. py:method:: from_source(cls, source)

     Create a Location instance based on the source
     
     If *source* is a string then it's used as the filename.
     If *source* is None then the location filename is "<stdin>".
     If *source* is a file object then its ``name`` attribute
     is used as the filename, or None if there is no attribute.



  .. py:method:: from_destination(cls, destination)

     Create a Location instance based on the destination
     
     If *destination* is a string then it's used as the filename.
     If *destination* is None then the location filename is "<stdout>".
     If *destination* is a file object then its ``name`` attribute
     is used as the filename, or None if there is no attribute.



  .. py:method:: __repr__()

     Return a string like 'Location("<stdout>")'




  .. py:attribute:: Location.first_line

     Read-only attribute.

     The first line of the current record
 

  .. py:attribute:: Location.filename

     Read/write attribute.

     A string which describes the source or destination. This is usually
     the source or destination filename but can be a string like "<stdin>"
     or "<stdout>".




  .. py:attribute:: Location.mol

     Read-only attribute.

     The molecule object for the current record
 



  .. py:attribute:: Location.offsets

     Read-only attribute.

     The (start, end) byte offsets, starting from 0
     
     *start* is the record start byte position and *end* is
     one byte past the last byte of the record.
 



  .. py:attribute:: Location.output_recno

     Read-only attribute.

     The number of records actually written to the file or string.
     
     The value ``recno - output_recno`` is the number of records
     sent to the writer but which had an error and could not be
     written to the output.
 



  .. py:attribute:: Location.recno

     Read-only attribute.

     The current record number
     
     For writers this is the number of records sent to
     the writer, and output_recno is the number of records
     sucessfully written to the file or string.
 



  .. py:attribute:: Location.record

     Read-only attribute.

     The current record as an uncompressed text string
 



  .. py:attribute:: Location.record_format

     Read-only attribute.

     The record format name
 


  .. py:method:: where()

     Return a human readable description about the current reader or writer state.
     
     The description will contain the filename, line number, record
     number, and up to the first 40 characters of the first line of
     the record, if those properties are available.

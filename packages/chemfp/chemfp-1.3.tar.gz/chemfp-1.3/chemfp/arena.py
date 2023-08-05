"""Algorithms and data structure for working with a FingerprintArena.

NOTE: This module should not be used directly.

A FingerprintArena stores the fingerprints as a contiguous byte
string, called the `arena`. Each fingerprint takes `storage_size`
bytes, which may be larger than `num_bytes` if the fingerprints have a
specific memory alignment. The bytes for fingerprint i are
  arena[i*storage_size:i*storage_size+num_bytes]
Additional bytes must contain NUL bytes.

The lookup for `ids[i]` contains the id for fingerprint `i`.

A FingerprintArena has an optional `indices` attribute. When
available, it means that the arena fingerprints and corresponding ids
are ordered by population count, and the fingerprints with popcount
`p` start at index indices[p] and end just before indices[p+1].

"""

# Copyright (c) 2010-2017 Andrew Dalke Scientific, AB (Sweden)
# See the contents of "chemfp/__init__.py" for full license details.

from __future__ import absolute_import

import ctypes
from cStringIO import StringIO
import array
import itertools

from chemfp import FingerprintReader
import _chemfp
from chemfp import bitops, search

__all__ = []
    
class FingerprintArena(FingerprintReader):
    """Store fingerprints in a contiguous block of memory for fast searches

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
    """
    _search = search
    def __init__(self, metadata, alignment,
                 start_padding, end_padding, storage_size, arena,
                 popcount_indices, arena_ids, start=0, end=None,
                 id_lookup=None, num_bits=None, num_bytes=None,
                 ):
        assert isinstance(popcount_indices, bytes), type(popcount_indices) # XXX REMOVE ME
        if num_bits is None:
            num_bits = metadata.num_bits
            if num_bits is None:
                raise TypeError("Missing 'num_bits' and not available from the metadata")
        if num_bytes is None:
            num_bytes = metadata.num_bytes
            if num_bytes is None:
                raise TypeError("Missing 'num_bytes' and not available from the metadata")

        self.metadata = metadata
        self.alignment = alignment
        self.num_bits = num_bits
        self.num_bytes = num_bytes
        self.start_padding = start_padding
        self.end_padding = end_padding
        self.storage_size = storage_size
        self.arena = arena
        self.popcount_indices = popcount_indices
        self.arena_ids = arena_ids
        self.start = start   # the starting index in the arena (not byte position!)
        if end is None:      # the ending index in the arena (not byte position!)
            if num_bytes:
                end = (len(arena) - start_padding - end_padding) // self.storage_size
            else:
                end = 0
        self.end = end
        if self.start == 0 and self.end == len(arena_ids):
            self._ids = arena_ids
        else:
            self._ids = None
        self._id_lookup = id_lookup
        assert end >= start
        self._range_check = xrange(end-start)

    def __len__(self):
        """Number of fingerprint records in the FingerprintArena"""
        return self.end - self.start

    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        return  # XXX This should close the memory map
    

    @property
    def ids(self):
        """The identifiers in this arena or subarena"""
        ids = self._ids
        if ids is None:
            ids = self.arena_ids[self.start:self.end]
            self._ids = ids
        return ids

    def __getitem__(self, i):
        """Return the (id, fingerprint) pair at index i"""
        if isinstance(i, slice):
            start, end, step = i.indices(self.end - self.start)
            if step != 1:
                raise IndexError("arena slice step size must be 1")
            if start >= end:
                return FingerprintArena(self.metadata, self.alignment,
                                        0, 0, self.storage_size, b"",
                                        b"", [], 0, 0)
            return FingerprintArena(self.metadata, self.alignment,
                                    self.start_padding, self.end_padding,
                                    self.storage_size, self.arena,
                                    self.popcount_indices, self.arena_ids,
                                    self.start+start, self.start+end,
                                    self._id_lookup, self.num_bits, self.num_bytes)
        try:
            i = self._range_check[i]
        except IndexError:
            raise IndexError("arena fingerprint index out of range")
        arena_i = i + self.start
        start_offset = arena_i * self.storage_size + self.start_padding
        end_offset = start_offset + self.num_bytes
        return self.arena_ids[arena_i], self.arena[start_offset:end_offset]

    def get_fingerprint(self, i):
        """Return the fingerprint at index *i*

        Raises an IndexError if index *i* is out of range.
        """
        try:
            i = self._range_check[i]
        except IndexError:
            raise IndexError("arena fingerprint index out of range")
        arena_i = i + self.start
        start_offset = arena_i * self.storage_size + self.start_padding
        end_offset = start_offset + self.num_bytes
        return self.arena[start_offset:end_offset]

    def _make_id_lookup(self):
        d = dict((id, i) for (i, id) in enumerate(self.ids))
        self._id_lookup = d.get
        return self._id_lookup
        
    def get_by_id(self, id):
        """Given the record identifier, return the (id, fingerprint) pair,

        If the *id* is not present then return None.
        """
        id_lookup = self._id_lookup
        if id_lookup is None:
            id_lookup = self._make_id_lookup()
        i = id_lookup(id)
        if i is None:
            return None
        arena_i = i + self.start
        start_offset = arena_i * self.storage_size + self.start_padding
        end_offset = start_offset + self.num_bytes
        return self.arena_ids[arena_i], self.arena[start_offset:end_offset]

    def get_index_by_id(self, id):
        """Given the record identifier, return the record index

        If the *id* is not present then return None.
        """
        id_lookup = self._id_lookup
        if id_lookup is None:
            id_lookup = self._make_id_lookup()
        return id_lookup(id)

    def get_fingerprint_by_id(self, id):
        """Given the record identifier, return its fingerprint

        If the *id* is not present then return None
        """
        id_lookup = self._id_lookup
        if id_lookup is None:
            id_lookup = self._make_id_lookup()
        i = id_lookup(id)
        if i is None:
            return None
        arena_i = i + self.start
        start_offset = arena_i * self.storage_size + self.start_padding
        end_offset = start_offset + self.num_bytes
        return self.arena[start_offset:end_offset]

    def save(self, destination, format=None):
        """Save the arena contents to the given filename or file object"""
        from . import io
        format_name, compression = io.normalize_output_format(destination, format,
                                                              default = ("fps", ""))

        if format_name == "fps":
            output, close = io.open_binary_output(destination)
            
            try:
                io.write_fps1_magic(output)
                io.write_fps1_header(output, self.metadata)
                try:
                    for i, (id, fp) in enumerate(self):
                        io.write_fps1_fingerprint(output, fp, id)
                except ValueError as err:
                    raise ValueError("%s in record %i" % (err, i+1))
            finally:
                if close is not None:
                    close()

        elif format_name == "fpb":
            raise NotImplementedError("fpb format not implemented")
        else:
            raise ValueError("Unknown output format %r" % (format_name,))
    save.__doc__ = FingerprintReader.save.__doc__

                
    def __iter__(self):
        """Iterate over the (id, fingerprint) contents of the arena"""
        storage_size = self.storage_size
        if not storage_size:
            return
        target_fp_size = self.num_bytes
        arena = self.arena
        start_padding = self.start_padding
        for i in xrange(self.start, self.end):
            arena_start = i*storage_size+start_padding
            yield self.arena_ids[i], arena[arena_start:arena_start+target_fp_size]

    def iter_arenas(self, arena_size = 1000):
        """Iterate through *arena_size* fingerprints at a time, as subarenas"""
        if arena_size is None:
            yield self
            return
        
        storage_size = self.storage_size
        start = self.start
        for i in xrange(0, len(self), arena_size):
            end = start+arena_size
            if end > self.end:
                end = self.end
            yield FingerprintArena(self.metadata, self.alignment,
                                   self.start_padding, self.end_padding,
                                   storage_size, self.arena,
                                   self.popcount_indices, self.arena_ids, start, end)
            start = end

    iter_arenas.__doc__ = FingerprintReader.__doc__

    def count_tanimoto_hits_fp(self, query_fp, threshold=0.7):
        """Count the fingerprints which are sufficiently similar to the query fingerprint

        Return the number of fingerprints in the arena which are
        at least *threshold* similar to the query fingerprint *query_fp*.
        
        :param query_fp: query fingerprint
        :type query_fp: byte string
        :param threshold: minimum similarity threshold (default: 0.7)
        :type threshold: float between 0.0 and 1.0, inclusive
        :returns: integer count
        """
        return search.count_tanimoto_hits_fp(query_fp, self, threshold)

    def count_tanimoto_hits_arena(self, queries, threshold=0.7):
        """Count the fingerprints which are sufficiently similar to each query fingerprint

        DEPRECATED: Use `chemfp.search.count_tanimoto_hits_arena`_ or
        `chemfp.search.count_tanimoto_hits_symmetric`_ instead.
        
        Returns a list containing a count for each query fingerprint
        in the *queries* arena. The count is the number of
        fingerprints in the arena which are at least *threshold*
        similar to the query fingerprint.

        The order of results is the same as the order of the queries.
        
        :param queries: query fingerprints
        :type queries: a :class:`.FingerprintArena`
        :param threshold: minimum similarity threshold (default: 0.7)
        :type threshold: float between 0.0 and 1.0, inclusive
        :returns: list of integer counts, one for each query
        """
        return search.count_tanimoto_hits_arena(queries, self, threshold)

    def threshold_tanimoto_search_fp(self, query_fp, threshold=0.7):
        """Find the fingerprints which are sufficiently similar to the query fingerprint

        Find all of the fingerprints in this arena which are at least
        *threshold* similar to the query fingerprint *query_fp*.  The
        hits are returned as a :class:`.SearchResult`, in arbitrary
        order.
        
        :param query_fp: query fingerprint
        :type query_fp: byte string
        :param threshold: minimum similarity threshold (default: 0.7)
        :type threshold: float between 0.0 and 1.0, inclusive
        :returns: a :class:`.SearchResult`
        """
        return search.threshold_tanimoto_search_fp(query_fp, self, threshold)

    def threshold_tanimoto_search_arena(self, queries, threshold=0.7):
        """Find the fingerprints which are sufficiently similar to each of the query fingerprints

        DEPRECATED: Use `chemfp.search.threshold_tanimoto_search_arena`_
        or `chemfp.search.threshold_tanimoto_search_symmetric`_ instead.

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
        return search.threshold_tanimoto_search_arena(queries, self, threshold)

    def knearest_tanimoto_search_fp(self, query_fp, k=3, threshold=0.7):
        """Find the k-nearest fingerprints which are sufficiently similar to the query fingerprint

        Find all of the fingerprints in this arena which are at least
        *threshold* similar to the query fingerprint, and of those, select
        the top *k* hits. The hits are returned as a :class:`.SearchResult`,
        sorted from highest score to lowest.

        :param queries: query fingerprints
        :type queries: a :class:`.FingerprintArena`
        :param threshold: minimum similarity threshold (default: 0.7)
        :type threshold: float between 0.0 and 1.0, inclusive
        :returns: a :class:`.SearchResult`
        """
        return search.knearest_tanimoto_search_fp(query_fp, self, k, threshold)

    def knearest_tanimoto_search_arena(self, queries, k=3, threshold=0.7):
        """Find the k-nearest fingerprints which are sufficiently similar to each of the query fingerprints

        DEPRECATED: Use `chemfp.search.knearest_tanimoto_search_arena`_ or
        `chemfp.search.knearest_tanimoto_search_symmetric`_ instead.

        For each fingerprint in the *queries* arena, find the
        fingerprints in this arena which are at least *threshold*
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
        return search.knearest_tanimoto_search_arena(queries, self, k, threshold)
    
    def count_tversky_hits_fp(self, query_fp, threshold=0.7, alpha=1.0, beta=1.0):
        """Count the fingerprints which are sufficiently similar to the query fingerprint

        Return the number of fingerprints in the arena which are
        at least *threshold* similar to the query fingerprint *query_fp*.
        
        :param query_fp: query fingerprint
        :type query_fp: byte string
        :param threshold: minimum similarity threshold (default: 0.7)
        :type threshold: float between 0.0 and 1.0, inclusive
        :returns: integer count
        """
        return search.count_tversky_hits_fp(query_fp, self, threshold, alpha, beta)

    def threshold_tversky_search_fp(self, query_fp, threshold=0.7, alpha=1.0, beta=1.0):
        """Find the fingerprints which are sufficiently similar to the query fingerprint

        Find all of the fingerprints in this arena which are at least
        *threshold* similar to the query fingerprint *query_fp*.  The
        hits are returned as a :class:`.SearchResult`, in arbitrary
        order.
        
        :param query_fp: query fingerprint
        :type query_fp: byte string
        :param threshold: minimum similarity threshold (default: 0.7)
        :type threshold: float between 0.0 and 1.0, inclusive
        :returns: a :class:`.SearchResult`
        """
        return search.threshold_tversky_search_fp(query_fp, self, threshold, alpha, beta)

    def knearest_tversky_search_fp(self, query_fp, k=3, threshold=0.7, alpha=1.0, beta=1.0):
        """Find the k-nearest fingerprints which are sufficiently similar to the query fingerprint

        Find all of the fingerprints in this arena which are at least
        *threshold* similar to the query fingerprint, and of those, select
        the top *k* hits. The hits are returned as a :class:`.SearchResult`,
        sorted from highest score to lowest.

        :param queries: query fingerprints
        :type queries: a :class:`.FingerprintArena`
        :param threshold: minimum similarity threshold (default: 0.7)
        :type threshold: float between 0.0 and 1.0, inclusive
        :returns: a :class:`.SearchResult`
        """
        return search.knearest_tversky_search_fp(query_fp, self, k, threshold, alpha, beta)

    
    def copy(self, indices=None, reorder=None):
        """Create a new arena using either all or some of the fingerprints in this arena

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
        """
        if reorder is None:
            if indices is None:
                # This is a pure copy. Reorder only if there are popcount indices.
                reorder = (self.popcount_indices != b"")
            else:
                # The default is to go fast. If you want to preserve index order
                # then you'll need to set reorder=False
                reorder = True
            
        if indices is None:
            # Make a completely new arena
            # Handle the trivial case where I don't need to do anything.
            if (self.start == 0 and
                (self.end*self.storage_size + self.start_padding + self.end_padding == len(self.arena)) and
                (not reorder or self.popcount_indices)):
                return FingerprintArena(self.metadata, self.alignment,
                                        self.start_padding, self.end_padding, self.storage_size, self.arena,
                                        self.popcount_indices, self.arena_ids,
                                        start = 0, end = self.end,
                                        id_lookup = self._id_lookup)
            
            # Otherwise I need to do some work
            # Make a copy of the actual fingerprints. (Which could be a subarena.)
            start = self.start_padding + self.start*self.storage_size
            end = self.start_padding + self.end*self.storage_size
            arena = self.arena[start:end]

            # If we don't have popcount_indices and don't want them ordered
            # then just do the alignment and we're done.
            if not reorder and not self.popcount_indices:
                # Don't reorder the unordered fingerprints
                start_padding, end_padding, unsorted_arena = (
                    _chemfp.make_unsorted_aligned_arena(arena, self.alignment))
                return FingerprintArena(self.metadata, self.alignment, start_padding, end_padding,
                                        self.storage_size, unsorted_arena, b"", self.ids,
                                        id_lookup = self._id_lookup)

            # Either we're already sorted or we should become sorted.
            # If we're sorted then make_sorted_aligned_arena will detect
            # that and keep the old arena. Otherwise it sorts first and
            # makes a new arena block.
            current_ids = self.ids
            ordering = (ChemFPOrderedPopcount*len(current_ids))()
            popcounts = array.array("i", (0,)*(self.metadata.num_bits+2))
            start_padding, end_padding, arena = _chemfp.make_sorted_aligned_arena(
                self.metadata.num_bits, self.storage_size, arena, len(current_ids),
                ordering, popcounts, self.alignment)

            reordered_ids = [current_ids[item.index] for item in ordering]
            return FingerprintArena(self.metadata, self.alignment,
                                    start_padding, end_padding, self.storage_size,
                                    arena, popcounts.tostring(), reordered_ids)

        # On this pathway, we want to make a new arena which contains
        # selected fingerprints given indices into the old arena.
        
        arena = self.arena
        storage_size = self.storage_size
        start = self.start
        start_padding = self.start_padding
        arena_ids = self.arena_ids
        
        # First make sure that all of the indices are in range.
        # This will also convert negative indices into positive ones.
        new_indices = []
        range_check = self._range_check
        try:
            for i in indices:
                new_indices.append(range_check[i])
        except IndexError:
            raise IndexError("arena fingerprint index %d is out of range" % (i,))

        if reorder and self.popcount_indices:
            # There's a slight performance benefit because
            # make_sorted_aligned_arena will see that the fingerprints
            # are already in sorted order and not resort.
            # XXX Is that true? Why do a Python sort instead of a C sort?
            # Perhaps because then I don't need to copy fingerprints?
            new_indices.sort()

        # Copy the fingerprints over to a new arena block
        unsorted_fps = []
        new_ids = []
        for new_i in new_indices:
            start_offset = start_padding + new_i*storage_size
            end_offset = start_offset + storage_size
            unsorted_fps.append(arena[start_offset:end_offset])
            new_ids.append(arena_ids[new_i])
                
        unsorted_arena = b"".join(unsorted_fps)
        unsorted_fps = None   # regain some memory

        # If the caller doesn't want ordered data, then leave it unsorted
        if not reorder:
            start_padding, end_padding, unsorted_arena = _chemfp.make_unsorted_aligned_arena(
                unsorted_arena, self.alignment)
            return FingerprintArena(self.metadata, self.alignment, start_padding, end_padding, storage_size,
                                    unsorted_arena, b"", new_ids)

        # Otherwise, reorder and align the area, along with popcount information
        ordering = (ChemFPOrderedPopcount*len(new_ids))()
        popcounts = array.array("i", (0,)*(self.metadata.num_bits+2))

        start_padding, end_padding, sorted_arena = _chemfp.make_sorted_aligned_arena(
            self.metadata.num_bits, storage_size, unsorted_arena, len(new_ids),
            ordering, popcounts, self.alignment)

        reordered_ids = [new_ids[item.index] for item in ordering]
        return FingerprintArena(self.metadata, self.alignment,
                                start_padding, end_padding, storage_size,
                                sorted_arena, popcounts.tostring(), reordered_ids)
        

# TODO: push more of this malloc-management down into C
class ChemFPOrderedPopcount(ctypes.Structure):
    _fields_ = [("popcount", ctypes.c_int),
                ("index", ctypes.c_int)]


_methods = bitops.get_methods()
_has_popcnt = "POPCNT" in _methods
_has_ssse3 = "ssse3" in _methods

def get_optimal_alignment(num_bits):
    if num_bits <= 32:
        # Just in case!
        if num_bits <= 8:
            return 1
        return 4

    # Since the ssse3 method must examine at least 512 bits while the
    # Gillies method doesn't, this puts the time tradeoff around 210 bits.
    # I decided to save a bit of space and round that up to 224 bits.
    # (Experience will tell us if 256 is a better boundary.)
    if num_bits <= 224:
        return 8

    # If you have POPCNT (and you're using it) then there's no reason
    # to use a larger alignment
    if _has_popcnt:
        if num_bits >= 768:
            if bitops.get_alignment_method("align8-large") == "POPCNT":
                return 8
        else:
            if bitops.get_alignment_method("align8-small") == "POPCNT":
                return 8

    # If you don't have SSSE3 or you aren't using it, then use 8
    if not _has_ssse3 or bitops.get_alignment_method("align-ssse3") != "ssse3":
        return 8

    # In my timing tests:
    #    Lauradoux takes 12.6s
    #    ssse3 takes in 9.0s
    #    Gillies takes 22s


    # Otherwise, go ahead and pad up to 64 bytes
    # (Even at 768 bits/96 bytes, the SSSE3 method is faster.)
    return 64

def _get_num_bits_and_bytes(fps_reader, metadata):
    num_bits = metadata.num_bits
    num_bytes = metadata.num_bytes
    
    fps_reader_iter = iter(fps_reader)

    num_bytes_source = "the metadata"
    if num_bits is None:
        if num_bytes is None:
            # Grr. Okay, we can look-ahead by one to get the content
            try:
                id, fp = next(fps_reader_iter)
            except StopIteration:
                # No size, no fingerprints? No problem!
                num_bits = num_bytes = 0
                fps_reader_iter = iter([])
                num_bytes_source = "the lack of metadata size or fingerprints"
            else:
                # Ha! Got the number of bytes
                num_bytes = len(fp)
                num_bits = num_bytes*8
                fps_reader_iter = itertools.chain([(id, fp)], fps_reader_iter)
                num_bytes_source = "the first fingerprint"
        else:
            num_bits = num_bytes*8
    else:
        if num_bytes is None:
            num_bytes = (num_bits+7)//8
        else:
            # Check for compatibility here?
            pass
    return num_bits, num_bytes, num_bytes_source, fps_reader_iter

def fps_to_arena(fps_reader, metadata=None, reorder=True, alignment=None):
    if metadata is None:
        metadata = fps_reader.metadata
            
    num_bits, num_bytes, num_bytes_source, fps_reader_iter = _get_num_bits_and_bytes(fps_reader, metadata)

    if alignment is None:
        alignment = get_optimal_alignment(num_bits)

    storage_size = num_bytes
    if storage_size % alignment != 0:
        n = alignment - storage_size % alignment
        end_padding = "\0" * n
        storage_size += n
    else:
        end_padding = None

    ids = []
    unsorted_fps = StringIO()
    for (id, fp) in fps_reader_iter:
        if len(fp) != num_bytes:
            raise ValueError("Fingerprint for id %r has %d bytes while %s says it should have %d"
                             % (id, len(fp), num_bytes_source, num_bytes))
        unsorted_fps.write(fp)
        if end_padding:
            unsorted_fps.write(end_padding)
        ids.append(id)

    unsorted_arena = unsorted_fps.getvalue()
    unsorted_fps.close()
    unsorted_fps = None


    if not reorder or not metadata.num_bits:
        start_padding, end_padding, unsorted_arena = _chemfp.make_unsorted_aligned_arena(
            unsorted_arena, alignment)
        return FingerprintArena(metadata, alignment, start_padding, end_padding, storage_size,
                                unsorted_arena, "", ids,
                                num_bits=num_bits, num_bytes=num_bytes)

    # Reorder
        
    ordering = (ChemFPOrderedPopcount*len(ids))()
    popcounts = array.array("i", (0,)*(metadata.num_bits+2))

    start_padding, end_padding, unsorted_arena = _chemfp.make_sorted_aligned_arena(
        num_bits, storage_size, unsorted_arena, len(ids),
        ordering, popcounts, alignment)

    new_ids = [ids[item.index] for item in ordering]
    return FingerprintArena(metadata, alignment,
                            start_padding, end_padding, storage_size,
                            unsorted_arena, popcounts.tostring(), new_ids,
                            num_bits=num_bits, num_bytes=num_bytes)

from __future__ import absolute_import, print_function

import unittest2
from cStringIO import StringIO as BytesIO

import chemfp
from chemfp import bitops
from chemfp.bitops import hex_decode
import chemfp.search

from support import fullpath

queries_arena = chemfp.load_fingerprints(fullpath("queries.fps"))[2:]
targets_arena = chemfp.load_fingerprints(fullpath("targets.fps"))[3:-1]
MACCS_FPS = fullpath("chebi_rdmaccs.fps")

small = chemfp.load_fingerprints(BytesIO(b"""\
012345\tfirst
01ABCD\tsecond
672245\tthird
"""))

class ContainsFPSearch(unittest2.TestCase):
    def test_contains_fp_zero_query(self):
        hits = chemfp.search.contains_fp(hex_decode("000000"), small)
        self.assertEqual(len(hits), 3)

    def test_contains_fp_find_some(self):
        hits = chemfp.search.contains_fp(hex_decode("010300"), small)
        self.assertEqual(len(hits), 2)

    def test_contains_fp_find_none(self):
        hits = chemfp.search.contains_fp(hex_decode("67AB00"), small)
        self.assertEqual(len(hits), 0)

    def test_alignment(self):
        left_bits = hex_decode("010000000000000000000000000000")
        right_bits = hex_decode("000000000000000000000000010000")
        no_bits = hex_decode("000000000000000000000000010001")
        for alignment in (1, 4, 8, 32):
            arena = chemfp.load_fingerprints(BytesIO(b"010000000100000001000000010000\tfirst\n"),
                                             alignment=alignment)
            hits = chemfp.search.contains_fp(left_bits, arena)
            assert len(hits) == 1
            hits = chemfp.search.contains_fp(right_bits, arena)
            assert len(hits) == 1
            hits = chemfp.search.contains_fp(no_bits, arena)
            assert len(hits) == 0

    def test_single_bit(self):
        template = b"\0" * 11
        id_fp_pairs = [(None, template)]
        for i in range(len(template)*8):
            offset = i//8
            byte = b"\x01\x02\x04\x08\x10\x20\x40\x80"[i%8:i%8+1]
            fp = template[:offset] + byte + template[offset+1:]
            id_fp_pairs.append((i, fp))

        for alignment in (1, 2, 4, 8, 16):
            arena = chemfp.load_fingerprints(id_fp_pairs,
                                             metadata=chemfp.Metadata(num_bytes=len(template)),
                                             alignment=alignment)
            self.assertEqual(arena.alignment, alignment)
            first_fp = arena.get_fingerprint(0)
            self.assertNotEqual(arena.get_fingerprint(1)[0:1], b"\0")
            self.assertEqual(arena.get_fingerprint(1)[-1:], b"\0")
            self.assertNotEqual(arena.popcount_indices, "")

            for query_id, query_fp in id_fp_pairs[1:]:
                hits = chemfp.search.contains_fp(query_fp, arena)
                self.assertEqual(len(hits), 1)
                self.assertEqual(hits.get_ids(), [query_id])

            # And try it in reverse order, without the empty fingerprint
            arena = chemfp.load_fingerprints(id_fp_pairs[:0:-1],
                                             metadata=chemfp.Metadata(num_bytes=len(template)),
                                             alignment=alignment)
            self.assertEqual(arena.alignment, alignment)
            self.assertNotEqual(arena.popcount_indices, "")
            first_fp = arena.get_fingerprint(0)
            self.assertEqual(arena.get_fingerprint(0)[0:1], b"\0")
            self.assertNotEqual(arena.get_fingerprint(0)[-1:], b"\0")

            for query_id, query_fp in id_fp_pairs[1:]:
                hits = chemfp.search.contains_fp(query_fp, arena)
                self.assertEqual(len(hits), 1)
                self.assertEqual(hits.get_ids(), [query_id])

            # And try it without popcounts.
            # Use reverse ordering to ensure no popcounts are set.
            arena = chemfp.load_fingerprints(id_fp_pairs[::-1],
                                             metadata=chemfp.Metadata(num_bytes=len(template)),
                                             alignment=alignment, reorder=False)
            self.assertEqual(arena.alignment, alignment)
            self.assertEqual(arena.popcount_indices, b"")
            first_fp = arena.get_fingerprint(0)
            self.assertEqual(arena.get_fingerprint(0)[0:1], b"\0")
            self.assertNotEqual(arena.get_fingerprint(0)[-1:], b"\0")

            for query_id, query_fp in id_fp_pairs[1:]:
                hits = chemfp.search.contains_fp(query_fp, arena)
                self.assertEqual(len(hits), 1)
                self.assertEqual(hits.get_ids(), [query_id])
                 
            
class TestCrossComparison(unittest2.TestCase):
    def test_1024_bit_fingerprints(self):
        target_fingerprints = [fp for id, fp in targets_arena]

        row_hits = []
        for query_id, query_fp in queries_arena:
            hits = chemfp.search.contains_fp(query_fp, targets_arena)
            expected = sum(1 for target_fp in target_fingerprints if bitops.byte_contains(query_fp, target_fp))
            self.assertEqual(len(hits), expected)
            row_hits.append(hits)

        for hits, expected_hits in zip(chemfp.search.contains_arena(queries_arena, targets_arena), row_hits):
            self.assertEqual(len(hits), len(expected_hits))

    def test_166_bit_fingerprints(self):
        for alignment in (1, 4, 8):
            arena = chemfp.load_fingerprints(MACCS_FPS, alignment=alignment)[100:169]
            fingerprints = [fp for id, fp in arena]

            row_hits = []
            for query_id, query_fp in arena:
                hits = chemfp.search.contains_fp(query_fp, arena)
                expected = sum(1 for target_fp in fingerprints if bitops.byte_contains(query_fp, target_fp))
                self.assertEqual(len(hits), expected)
                row_hits.append(hits)

            for hits, expected_hits in zip(chemfp.search.contains_arena(arena, arena), row_hits):
                self.assertEqual(len(hits), len(expected_hits))

    def test_166_bit_fingerprints_with_no_popcount_index(self):
        # Excercise the code path which doesn't use the popcount index
        for alignment in (1, 4, 8):
            arena = chemfp.load_fingerprints(MACCS_FPS, alignment=alignment, reorder=False)[100:169]
            self.assertFalse(arena.popcount_indices)
            fingerprints = [fp for id, fp in arena]

            row_hits = []
            for query_id, query_fp in arena:
                hits = chemfp.search.contains_fp(query_fp, arena)
                expected = sum(1 for target_fp in fingerprints if bitops.byte_contains(query_fp, target_fp))
                self.assertEqual(len(hits), expected)
                row_hits.append(hits)

            for hits, expected_hits in zip(chemfp.search.contains_arena(arena, arena), row_hits):
                self.assertEqual(len(hits), len(expected_hits))

            
if __name__ == "__main__":
    unittest2.main()

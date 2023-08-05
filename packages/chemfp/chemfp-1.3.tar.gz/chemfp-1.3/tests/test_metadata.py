import unittest2

import chemfp

# Improve code coverage by testing the parts not tested elsewhere
class TestMetadata(unittest2.TestCase):
    def test_bit_byte_incompatibility(self):
        with self.assertRaisesRegexp(ValueError, "num_bits of 9 is incompatible with num_bytes of 1"):
            chemfp.Metadata(num_bits=9, num_bytes=1)

    def test_sources_as_string_is_allowed(self):
        metadata = chemfp.Metadata(sources="Spam")
        metadata.sources = ["Spam"]

    def test_basic_repr(self):
        s = repr(chemfp.Metadata())
        self.assertEqual(s, "Metadata(num_bits=None, num_bytes=None, type=None, aromaticity=None, sources=[], software=None, date=None)")
    
    def test_full_repr(self):
        s = repr(chemfp.Metadata(num_bits=14, num_bytes=2, type="1-Adam/12", aromaticity="smelly",
                                 sources=["one", "two"], software="My head", date="1970-08-22T18:12:30"))
        self.assertEqual(s,
                         "Metadata(num_bits=14, num_bytes=2, type='1-Adam/12', " +
                         "aromaticity='smelly', sources=['one', 'two'], software='My head', " +
                         "date='1970-08-22T18:12:30')")
    def test_basic_str(self):
        s = str(chemfp.Metadata())
        self.assertEqual(s, "")

    def test_full_str(self):
        s = str(chemfp.Metadata(num_bits=14, num_bytes=2, type="1-Adam/12", aromaticity="smelly",
                                sources=["one", "two"], software="My head", date="1970-08-22T18:12:30"))
        lines = s.splitlines()
        self.assertSequenceEqual(lines,
                                 ["#num_bits=14",
                                  '#type=1-Adam/12',
                                  '#software=My head',
                                  '#aromaticity=smelly',
                                  '#source=one',
                                  '#source=two',
                                  '#date=1970-08-22T18:12:30'])

    def test_copy_with_parameters(self):
        import datetime
        metadata = chemfp.Metadata(type="abc/123", num_bits=12)
        for name, value in (
                ("num_bits", 13),
                ("type", "qwe/345"),
                ("aromaticity", "lavender"),
                ("software", "MS-Dos/3.3+"),
                ("sources", []),
                ("sources", ["first"]),
                ("sources", ["first", "second"]),
                ("date", datetime.datetime.now())):
            kwargs = {name: value}
            new_metadata = metadata.copy(**kwargs)

            for verify_name in ("num_bits", "type", "aromaticity", "software", "sources", "date"):
                if verify_name == name:
                    self.assertEqual(getattr(new_metadata, verify_name), value)
                else:
                    self.assertEqual(getattr(new_metadata, verify_name), getattr(metadata, verify_name))

class TestCheckMetadataProblems(unittest2.TestCase):
    def _check(self, m1, m2, expected):
        results = chemfp.check_metadata_problems(m1, m2)
        found = [(x.severity, x.category, x.description) for x in results]
        self.assertEqual(found, expected)
        
    def test_bit_mismatch(self):
        self._check(chemfp.Metadata(num_bytes=8, num_bits=62),
                    chemfp.Metadata(num_bytes=8, num_bits=63),
                    [("error", "num_bits mismatch",
                      "query has 62 bit fingerprints but target has 63 bit fingerprints")])

    def test_byte_mismatch(self):
        # I don't think there's any way to trigger a num_bytes mismatch,
        # and I would *always* prefer a num_bits mismatch over a num_bytes mismatch
        self._check(chemfp.Metadata(num_bytes=8),
                    chemfp.Metadata(num_bytes=7),
                    [("error", "num_bits mismatch",
                      "query has 64 bit fingerprints but target has 56 bit fingerprints"),
                     #("error", "num_bytes mismatch",
                     # "query has 8 bytes fingerprints but target has 7 byte fingerprints")
                    ])


    def test_type_mismatch(self):
        metadata = chemfp.Metadata(num_bytes=8, num_bits=64)
        self._check(metadata.copy(type="RDKit-Pattern"),
                    metadata.copy(type="OpenBabel-FP2"),
                    [("warning", "type mismatch",
                      "query has fingerprints of type 'RDKit-Pattern' but target has fingerprints of type 'OpenBabel-FP2'")])

    def test_aromaticity_mismatch(self):
        metadata = chemfp.Metadata(num_bytes=8, num_bits=64)
        self._check(metadata.copy(aromaticity="daylight"),
                    metadata.copy(aromaticity="openeye"),
                    [("warning", "aromaticity mismatch",
                      "query uses aromaticity 'daylight' but target uses aromaticity 'openeye'")])

    def test_software_mismatch(self):
        metadata = chemfp.Metadata(num_bytes=8, num_bits=64)
        self._check(metadata.copy(software="OEChem/1.2.3"),
                    metadata.copy(software="OEChem/1.2.4"),
                    [("info", "software mismatch",
                      "query comes from software 'OEChem/1.2.3' but target comes from software 'OEChem/1.2.4'")])


                    
if __name__ == "__main__":
    unittest2.main()

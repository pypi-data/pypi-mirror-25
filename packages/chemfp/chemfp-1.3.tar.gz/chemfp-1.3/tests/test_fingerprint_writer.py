from __future__ import with_statement

import os
import tempfile
import shutil
from cStringIO import StringIO

import unittest2

import chemfp
from chemfp.bitops import hex_decode

import support

def _tmpdir(testcase):
    dirname = tempfile.mkdtemp()
    testcase.addCleanup(shutil.rmtree, dirname)
    return dirname

# These are the same for FPS and FPB output formats.
# (1.3 doesn't support the FPB format. These were
# backported from 3.0.)
class OutputMixin(object):
    test_filename = None
    def _get_writer(self, **kwargs):
        d = self.test_kwargs.copy()
        d.update(kwargs)
        self.dirname = dirname = _tmpdir(self)
        #self.dirname = dirname = "."
        self.filename = filename = os.path.join(dirname, self.test_filename)
        return chemfp.open_fingerprint_writer(filename, **d)

    def test_save_empty_file(self):
        writer = self._get_writer()
        self.assertFalse(writer.closed)
        writer.close()
        self.assertTrue(writer.closed)

        for id, fp in chemfp.open(self.filename):
            raise AssertionError("Should be empty")
        
    
    def test_save_basic(self):
        writer = self._get_writer()
        writer.write_fingerprint("ABC", b"\r\t\n\0")
        writer.close()

        reader = iter(chemfp.open(self.filename))
        id, fp = next(reader)
        self.assertEqual(id, "ABC")
        self.assertEqual(fp, b"\r\t\n\0")
        with self.assertRaisesRegexp(StopIteration, ""):
            next(reader)

    def test_write_iterator_without_metadata(self):
        fps = [("AB", b"1234")]
        
        x = self._get_writer()
        with x as writer:
            writer.write_fingerprints(fps)

        reader = chemfp.open(self.filename)
        self.assertEqual(reader.metadata.type, None)
        self.assertEqual(reader.metadata.num_bits, 32)
        self.assertEqual(reader.metadata.num_bytes, 4)
        data = list(reader)
        self.assertEqual(data, [("AB", b"1234")])
        
    def test_write_iterator_with_metadata(self):
        fps = chemfp.FingerprintIterator(chemfp.Metadata(type="Spam/1", num_bytes=4), [("AB", b"1234")])
        
        x = self._get_writer(metadata=fps.metadata)
        with x as writer:
            self.assertFalse(x.closed)
            writer.write_fingerprints(fps)
        self.assertTrue(x.closed)

        reader = chemfp.open(self.filename)
        self.assertEqual(reader.metadata.type, "Spam/1")
        self.assertEqual(reader.metadata.num_bits, 32)
        self.assertEqual(reader.metadata.num_bytes, 4)
        data = list(reader)
        self.assertEqual(data, [("AB", b"1234")])

    def test_write_with_unusual_bits(self):
        with self._get_writer(metadata=chemfp.Metadata(num_bits=63)) as writer:
            writer.write_fingerprint("first", b"        ")
            writer.write_fingerprint("second", b"ZXCVBNM<")

        reader = chemfp.open(self.filename)
        self.assertEqual(reader.metadata.num_bytes, 8)
        self.assertEqual(reader.metadata.num_bits, 63)
        values = list(reader)
        self.assertEqual(values, [("first", b"        "),
                                  ("second", b"ZXCVBNM<")])

    def test_force_format_fps(self):
        with self._get_writer(format="fps") as writer:
            writer.write_fingerprint("first", hex_decode("deadbeef"))
        text = open(self.filename).read()
        self.assertEqual(text, "#FPS1\ndeadbeef\tfirst\n")  # though capitalization shouldn't matter

    def test_force_format_fps_gz(self):
        with self._get_writer(format="fps.gz") as writer:
            writer.write_fingerprint("first", hex_decode("deadbeef"))
        import gzip
        text = gzip.open(self.filename).read()
        self.assertEqual(text, b"#FPS1\ndeadbeef\tfirst\n")  # though capitalization shouldn't matter


class TestFPSOutput(unittest2.TestCase, OutputMixin):
    test_filename = "scratch.fps"
    test_kwargs = {}

    def test_save_id_with_tab(self):
        # The binary writer doesn't worry about special characters
        fps = [("Hello!", b"FFFF"), ("A\tB", b"1234")]
        with self._get_writer() as writer:
            with self.assertRaisesRegexp(
                    ValueError,
                    r"Unable to write an identifier containing a tab: 'A\\tB'.*scratch.fps', line 2, record #2"):
                writer.write_fingerprints(fps)

    def test_save_id_with_newline(self):
        # The binary writer doesn't worry about special characters
        fps = [("Hello!", b"FFFF"), ("AB", b"1234"),  ("A\nB", b"1234")]
        with self._get_writer() as writer:
            with self.assertRaisesRegexp(
                    ValueError,
                    r"Unable to write an identifier containing a newline: 'A\\nB'.*scratch.fps', line 3, record #3"):
                writer.write_fingerprints(fps)

    def test_save_id_with_empty_id(self):
        # The binary writer doesn't worry about empty ids
        fps = [("Hello!", b"FFFF"), ("", b"1234")]
        with self._get_writer() as writer:
            with self.assertRaisesRegexp(
                    ValueError,
                    r"Unable to write a fingerprint with an empty identifier.*scratch.fps', line 2, record #2"):
                writer.write_fingerprints(fps)


class UserWriter(object):
    def __init__(self):
        self.value = b""
    def write(self, text):
        self.value += text
    
class TestUserDefinedWriter(unittest2.TestCase):
    def test_user_writer(self):
        f = UserWriter()
        writer = chemfp.open_fingerprint_writer(f)
        writer.write_fingerprint("first", b"AA")
        writer.close()
        self.assertEqual(f.value, b"#FPS1\n4141\tfirst\n")
        
    def test_user_writer_must_implement_write(self):
        class NotAWriter(object):
            pass
        f = NotAWriter()
        with self.assertRaisesRegexp(ValueError, "Unknown destination type.*NotAWriter"):
            chemfp.open_fingerprint_writer(f)


class TestWriterLocation(unittest2.TestCase):
    def test_write_empty(self):
        f = StringIO()
        with chemfp.open_fingerprint_writer(f) as writer:
            self.assertEqual(writer.location.lineno, 1)
        self.assertEqual(f.getvalue(), b"#FPS1\n")
            
    def test_write_metadata_bytes(self):
        f = StringIO()
        with chemfp.open_fingerprint_writer(f, metadata=chemfp.Metadata(num_bytes=8)) as writer:
            self.assertEqual(writer.location.lineno, 2)
        self.assertEqual(f.getvalue(), b"#FPS1\n#num_bits=64\n")
            
    def test_write_metadata_bits(self):
        f = StringIO()
        with chemfp.open_fingerprint_writer(f, metadata=chemfp.Metadata(num_bits=60)) as writer:
            self.assertEqual(writer.location.lineno, 2)
        self.assertEqual(f.getvalue(), b"#FPS1\n#num_bits=60\n")
            
    def test_write_complex_metadata(self):
        f = StringIO()
        metadata = chemfp.Metadata(
            type = "blah/1",
            num_bytes = 16,
            sources = [u"G\x00F6teborg", u"Trollh\00E4ttan", "Miami"],
            )
            
        with chemfp.open_fingerprint_writer(f, metadata=metadata) as writer:
            self.assertEqual(writer.location.lineno, 6)
        self.assertEqual(
            f.getvalue(),
            b"#FPS1\n"
            b"#num_bits=128\n"
            b"#type=blah/1\n"
            b"#source=G\x00F6teborg\n"
            b"#source=Trollh\x00E4ttan\n"
            b"#source=Miami\n"
            )

    def test_write_fingerprint(self):
        f = StringIO()
        with chemfp.open_fingerprint_writer(f, chemfp.Metadata(num_bytes=2)) as writer:
            self.assertEqual(writer.location.lineno, 2)
            self.assertEqual(writer.location.recno, 0)
            self.assertEqual(writer.location.output_recno, 0)

            writer.write_fingerprint("first", b"AB")
            self.assertEqual(writer.location.recno, 1)
            self.assertEqual(writer.location.output_recno, 1)

            try:
                writer.write_fingerprint("", b"AB")
            except chemfp.ParseError as err:
                self.assertEqual("Unable to write a fingerprint with an empty identifier", err.msg)
                self.assertIs(err.location, writer.location)
                self.assertEqual(writer.location.recno, 2)
                self.assertEqual(writer.location.output_recno, 1)
            else:
                raise AssertionError
            
            writer.write_fingerprint("second", b"BC")
            self.assertEqual(writer.location.recno, 3)
            self.assertEqual(writer.location.output_recno, 2)
            
            try:
                writer.write_fingerprint("q\tw", b"CD")
            except chemfp.ParseError as err:
                self.assertIn("Unable to write an identifier containing a tab", err.msg)
            else:
                raise AssertionError
                
            try:
                writer.write_fingerprint("q\nw", b"EF")
            except chemfp.ParseError as err:
                self.assertIn("Unable to write an identifier containing a newline", err.msg)
            else:
                raise AssertionError
            
            writer.write_fingerprint("third", b"GH")

            self.assertEqual(writer.location.recno, 6)
            self.assertEqual(writer.location.output_recno, 3)
            self.assertEqual(writer.location.lineno, 5)
        
        self.assertEqual(f.getvalue(),
                b"#FPS1\n"
                b"#num_bits=16\n"
                b"4142\tfirst\n"
                b"4243\tsecond\n"
                b"4748\tthird\n"
                )
        
    def test_write_fingerprint_ignore_errors(self):
        f = StringIO()
        with chemfp.open_fingerprint_writer(f, chemfp.Metadata(num_bytes=2), errors="ignore") as writer:
            self.assertEqual(writer.location.lineno, 2)
            self.assertEqual(writer.location.recno, 0)
            self.assertEqual(writer.location.output_recno, 0)

            writer.write_fingerprint("first", b"AB")
            self.assertEqual(writer.location.recno, 1)
            self.assertEqual(writer.location.output_recno, 1)

            writer.write_fingerprint("", b"AB")
            self.assertEqual(writer.location.recno, 2)
            self.assertEqual(writer.location.output_recno, 1)
            
            writer.write_fingerprint("second", b"BC")
            self.assertEqual(writer.location.recno, 3)
            self.assertEqual(writer.location.output_recno, 2)
            
            writer.write_fingerprint("q\tw", b"CD")
                
            writer.write_fingerprint("q\nw", b"EF")
            
            writer.write_fingerprint("third", b"GH")

            self.assertEqual(writer.location.recno, 6)
            self.assertEqual(writer.location.output_recno, 3)
            self.assertEqual(writer.location.lineno, 5)

        self.assertEqual(f.getvalue(),
                b"#FPS1\n"
                b"#num_bits=16\n"
                b"4142\tfirst\n"
                b"4243\tsecond\n"
                b"4748\tthird\n"
                )
        
    def test_write_many_fingerprints(self):
        f = StringIO()
        with chemfp.open_fingerprint_writer(f, chemfp.Metadata(num_bytes=2)) as writer:
            writer.write_fingerprints( [("first", b"AB"),
                                        ("second", b"BC")] )
            self.assertEqual(writer.location.lineno, 4)
            self.assertEqual(writer.location.recno, 2)
            self.assertEqual(writer.location.output_recno, 2)

            writer.write_fingerprints( [] )
            
            try:
                writer.write_fingerprints( [("third", b"CD"),
                                            ("q\tw", b"DE"),
                                            ("fourth", b"EF")] )
            except chemfp.ParseError as err:
                self.assertIn("Unable to write an identifier containing a tab", err.msg)
                self.assertIs(writer.location, err.location)
                self.assertEqual(err.location.lineno, 5)
                self.assertEqual(err.location.recno, 4)
                self.assertEqual(err.location.output_recno, 3)
            else:
                raise AssertionError(f.getvalue())

            try:
                writer.write_fingerprints( [("fifth", b"FG"),
                                            ("q\ne", b"GH"),
                                            ("sixth", b"HI")] )
            except chemfp.ParseError as err:
                self.assertIn("Unable to write an identifier containing a newline", err.msg)
                self.assertIs(writer.location, err.location)
                self.assertEqual(err.location.lineno, 6)
                self.assertEqual(err.location.recno, 6)
                self.assertEqual(err.location.output_recno, 4)
            else:
                raise AssertionError(f.getvalue())

            try:
                writer.write_fingerprints( [("seventh", b"IJ"),
                                            ("", b"GH"),
                                            ("eighth", b"JK")] )
            except chemfp.ParseError as err:
                self.assertIn("Unable to write a fingerprint with an empty identifier", err.msg)
                self.assertIs(writer.location, err.location)
                self.assertEqual(err.location.lineno, 7)
                self.assertEqual(err.location.recno, 8)
                self.assertEqual(err.location.output_recno, 5)
            else:
                raise AssertionError(f.getvalue())

        self.assertEqual(
            f.getvalue(),
            b"#FPS1\n"
            b"#num_bits=16\n"
            b"4142\tfirst\n"
            b"4243\tsecond\n"
            b"4344\tthird\n"
            b"4647\tfifth\n"
            b"494a\tseventh\n")

    def test_write_many_fingerprints_ignore(self):
        f = StringIO()
        with chemfp.open_fingerprint_writer(f, chemfp.Metadata(num_bytes=2), errors="ignore") as writer:
            writer.write_fingerprints( [("first", b"AB"),
                                        ("second", b"BC")] )
            self.assertEqual(writer.location.lineno, 4)
            self.assertEqual(writer.location.recno, 2)
            self.assertEqual(writer.location.output_recno, 2)

            writer.write_fingerprints( [] )
            
            writer.write_fingerprints( [("third", b"CD"),
                                        ("q\tw", b"DE"),
                                        ("fourth", b"EF")] )
            self.assertEqual(writer.location.lineno, 6)
            self.assertEqual(writer.location.recno, 5)
            self.assertEqual(writer.location.output_recno, 4)

            writer.write_fingerprints( [("fifth", b"FG"),
                                        ("q\ne", b"GH"),
                                        ("sixth", b"HI")] )
            self.assertEqual(writer.location.lineno, 8)
            self.assertEqual(writer.location.recno, 8)
            self.assertEqual(writer.location.output_recno, 6)

            writer.write_fingerprints( [("seventh", b"IJ"),
                                        ("", b"GH"),
                                        ("eighth", b"JK")] )
            self.assertEqual(writer.location.lineno, 10)
            self.assertEqual(writer.location.recno, 11)
            self.assertEqual(writer.location.output_recno, 8)

        self.assertEqual(
            f.getvalue(),
            b"#FPS1\n"
            b"#num_bits=16\n"
            b"4142\tfirst\n"
            b"4243\tsecond\n"
            b"4344\tthird\n"
            b"4546\tfourth\n"
            b"4647\tfifth\n"
            b"4849\tsixth\n"
            b"494a\tseventh\n"
            b"4a4b\teighth\n")

class TestErrorHandling(unittest2.TestCase):
    def test_unknown_format_name(self):
        with self.assertRaisesRegexp(ValueError, "Unable to determine fingerprint format type from 'blah.zztop"):
            chemfp.open_fingerprint_writer(support.get_tmpfile(self, "blah.zztop"))
            
    def test_unknown_format_name(self):
        with self.assertRaisesRegexp(ValueError, "Unsupported output fingerprint format 'zztop'"):
            chemfp.open_fingerprint_writer(support.get_tmpfile(self, "blah.fps"), format="zztop")
        
if __name__ == "__main__":
    unittest2.main()

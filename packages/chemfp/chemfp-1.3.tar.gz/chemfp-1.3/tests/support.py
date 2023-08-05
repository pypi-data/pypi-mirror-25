import sys
import os
from cStringIO import StringIO
import tempfile
import shutil

# Ignore the close. io.write_fps1_output() auto-closes its output.
class SIO(object):
    def __init__(self):
        self.sio = StringIO()
    def write(self, s):
        return self.sio.write(s)
    def writelines(self, lines):
        return self.sio.writelines(lines)
    def close(self):
        # Ignore this
        pass
    def getvalue(self):
        return self.sio.getvalue()

class wrap_stdin(object):
    def __init__(self, content):
        self.content = content
    def __enter__(self):
        self._old_stdin = sys.stdin
        sys.stdin = StringIO(self.content)
        return self
    def __exit__(self, *args):
        sys.stdin = self._old_stdin
    
# Given a filename in the "tests/" directory, return its full path

_dirname = os.path.dirname(__file__)
def fullpath(name):
    path = os.path.join(_dirname, name)
    assert os.path.exists(path), path
    return path

PUBCHEM_SDF = fullpath("pubchem.sdf")
PUBCHEM_SDF_GZ = fullpath("pubchem.sdf.gz")
PUBCHEM_ANOTHER_EXT = fullpath("pubchem.should_be_sdf_but_is_not")

MISSING_TITLE = fullpath("missing_title.sdf")

real_stdin = sys.stdin
real_stdout = sys.stdout
real_stderr = sys.stderr

class Runner(object):
    def __init__(self, main):
        self.main = main

    def pre_run(self):
        pass
    def post_run(self):
        pass

    def run(self, cmdline, source=PUBCHEM_SDF):
        if isinstance(cmdline, basestring):
            args = cmdline.split()
        else:
            args = cmdline
            assert isinstance(args, list) or isinstance(args, tuple)
        if source is not None:
            args = args + [source]
        self.pre_run()

        try:
            sys.stdout = stdout = SIO()
            self.main(args)
        finally:
            sys.stdout = real_stdout

        self.post_run()

        result = stdout.getvalue().splitlines()
        if result:
            self.verify_result(result)
        return result

    def verify_result(self, result):
        assert result[0] == "#FPS1", result[0]
        # TODO: .. verify more more line format ...

    def run_stdin(self, cmdline):
        raise NotImplementedError("Implement in the derived class")

    def run_fps(self, cmdline, expect_length=None, source=PUBCHEM_SDF):
        result = self.run(cmdline, source)
        while result[0].startswith("#"):
            del result[0]
        if expect_length is not None:
            assert len(result) == expect_length, (len(result), expect_length)
        return result

    def run_split(self, cmdline, expect_length=None, source=PUBCHEM_SDF):
        "split into dict of headers and list of values"
        result = self.run(cmdline, source)
        headers = {}
        fps = []
        result_iter = iter(result)
        # I know the first line is correct (it was tested in verify_result)
        # Plus, this lets the SimsearchRunner use run_split
        result_iter.next()
        for line in result_iter:
            if line.startswith("#"):
                k, v = line.split("=", 1)
                assert k not in headers, k
                headers[k] = v
                continue
            fps.append(line)
            break
        fps.extend(result_iter)
        if expect_length is not None:
            assert len(fps) == expect_length, (len(fps), expect_length)
        return headers, fps
            

    def run_exit(self, cmdline, source=PUBCHEM_SDF):
        sys.stderr = stderr = SIO()
        try:
            try:
                result = self.run(cmdline, source)
            except SystemExit:
                pass
            else:
                raise AssertionError("should have exited: %r gave: %r" % (cmdline, result))
        finally:
            sys.stderr = real_stderr
        return stderr.getvalue()

    def run_split_capture(self, cmdline, expect_length=None, source=PUBCHEM_SDF):
        sys.stderr = stderr = SIO()
        try:
            try:
                headers, fps = self.run_split(cmdline, expect_length, source)
            except SystemExit:
                raise AssertionError("unexpected SystemExit")
        finally:
            sys.stderr = real_stderr
        return headers, fps, stderr.getvalue()
        

####

def can_skip(name):
    s = os.environ.get("TOX_CHEMFP_TEST", "")
    return not (s.startswith(name) or (","+name) in s)

#### fingerprint encoding

def set_bit(n):
    assert n <= 16
    bytes = [0, 0, 0]
    bytes[n//8] = 1<<(n%8)
    return "%02x%02x%02x" % tuple(bytes)

class TestIdAndErrors(object):
    #
    # One of the records doesn't have an XLOGP field
    #
    def test_missing_id_tag(self):
        headers, fps, errmsg = self._runner.run_split_capture("--id-tag PUBCHEM_CACTVS_XLOGP", 18)
        self.assertNotIn("ERROR:", errmsg)
        self.assertNotIn("record #1", errmsg)
        self.assertNotIn("missing_title.sdf", errmsg)
        ids = [fp.split("\t")[1] for fp in fps]
        self.assertEquals(ids, ['2.8', '1.9', '1', '3.3', '1.5', '2.6', '-0.9', '2', '2.1', 
                                '2.9', '1.7', '-1.5', '0.4', '0.6', '0.4', '0.4', '2', '2.5'])

        
    def test_missing_id_strict(self):
        errmsg = self._runner.run_exit("--id-tag PUBCHEM_CACTVS_XLOGP --errors strict")
        self.assertIn("ERROR: Missing id tag 'PUBCHEM_CACTVS_XLOGP' in SD record", errmsg)
        self.assertIn("record #7", errmsg)
        self.assertIn("pubchem.sdf", errmsg)
    

    def test_missing_id_tag_report(self):
        headers, fps, errmsg = self._runner.run_split_capture("--id-tag PUBCHEM_CACTVS_XLOGP --errors report", 18)
        self.assertIn("ERROR: Missing title in SD record", errmsg)
        self.assertIn("record #1", errmsg)
        self.assertIn("missing_title.sdf'", errmsg)
        self.assertEquals(fps[-1], "")

    # Should be the same as the default case.
    def test_missing_id_tag_ignore(self):
        headers, fps, errmsg = self._runner.run_split_capture("--id-tag PUBCHEM_CACTVS_XLOGP --errors ignore", 18)
        self.assertNotIn("ERROR:", errmsg)
        self.assertNotIn("record #1", errmsg)
        self.assertNotIn("missing_title.sdf", errmsg)
        ids = [fp.split("\t")[1] for fp in fps]
        self.assertEquals(ids, ['2.8', '1.9', '1', '3.3', '1.5', '2.6', '-0.9', '2', '2.1', 
                                '2.9', '1.7', '-1.5', '0.4', '0.6', '0.4', '0.4', '2', '2.5'])


    def test_missing_a_lot_of_ids_bypasses_ignore_errors(self):
        filename = get_tmpfile(self, "empty.smi")
        outfile = open(filename, "w")
        outfile.write("C\n" * 100)
        outfile.close()
        errmsg = self._runner.run_exit("--errors ignore", filename)
        self.assertIn(
            "Each of the first 100 records contained errors. Final error: Missing SMILES identifier (second column)",
            errmsg)
        self.assertIn("empty.smi'", errmsg)
        self.assertIn(", record #100", errmsg)
        self.assertIn("Exiting.", errmsg)
        
    #
    # Various ways of having a strange title
    #

    def test_missing_title(self):
        headers, fps, errmsg = self._runner.run_split_capture("", 1, MISSING_TITLE)
        self.assertIn("record #1", errmsg)
        self.assertIn("record #3", errmsg)
        self.assertEquals(len(fps), 1)
        self.assertEquals(fps[0].split(b"\t")[1], b"Good")

    def test_missing_title_strict(self):
        errmsg = self._runner.run_exit("--errors strict", MISSING_TITLE)
        self.assertIn("ERROR: Missing title in SD record", errmsg)
        self.assertIn("record #1", errmsg)

    def test_missing_title_report(self):
        headers, fps, errmsg = self._runner.run_split_capture("--errors report", 1, MISSING_TITLE)
        self.assertIn("ERROR: Missing title", errmsg)
        self.assertIn("record #1", errmsg)
        self.assertNotIn("record #2", errmsg)
        self.assertIn("record #3", errmsg)
        self.assertEquals(len(fps), 1)
        self.assertEquals(fps[0].split(b"\t")[1], b"Good")

    def test_missing_title_ignore(self):
        headers, fps, errmsg = self._runner.run_split_capture("--errors ignore", 1, MISSING_TITLE)
        self.assertEqual(errmsg.count("record #1"), 1, errmsg)
        self.assertNotIn("record #2", errmsg)
        self.assertEqual(errmsg.count("record #3"), 1, errmsg)
        self.assertEquals(len(fps), 1)
        self.assertEquals(fps[0].split(b"\t")[1], b"Good")

    #
    # Various ways of handling a missing id in a tag
    #

    # Open Babel doesn't preserve the "    " so executes a different path
        
    def test_missing_id_tag(self):
        headers, fps, errmsg = self._runner.run_split_capture(
            "--id-tag Blank", 1, MISSING_TITLE)
        self.assertEqual(errmsg.count("ERROR"), 2, errmsg)
        self.assertEqual(errmsg.count("Empty id tag 'Blank' in SD record") +
                         errmsg.count("Missing id tag 'Blank' in SD record"), 2, errmsg)
        self.assertEqual(errmsg.count("record #"), 2, errmsg)
        self.assertEquals(fps[0].split(b"\t")[1], b"This is not Blank")

    def test_missing_id_tag_strict(self):
        errmsg = self._runner.run_exit(
            "--id-tag Blank --errors strict", MISSING_TITLE)
        if self.toolkit == "openbabel":
            self.assertIn("ERROR: Missing id tag 'Blank' in SD record", errmsg)
        else:
            self.assertIn("ERROR: Empty id tag 'Blank' in SD record after cleanup", errmsg)
        self.assertIn("record #1", errmsg)
        self.assertIn("missing_title.sdf'", errmsg)

    def test_missing_id_tag_report(self):
        headers, fps, errmsg = self._runner.run_split_capture(
            "--id-tag Blank --errors report", 1, MISSING_TITLE)
        if self.toolkit == "openbabel":
            self.assertIn("ERROR: Missing id tag 'Blank' in SD record", errmsg)
        else:
            self.assertIn("ERROR: Empty id tag 'Blank'", errmsg)
        self.assertIn("record #1", errmsg)
        self.assertIn("record #2", errmsg)
        self.assertNotIn("record #3", errmsg)
        self.assertEquals(fps[0].split(b"\t")[1], b"This is not Blank")

    def test_missing_id_tag_ignore(self):
        headers, fps, errmsg = self._runner.run_split_capture(
            "--id-tag Blank --errors ignore", 1, MISSING_TITLE)
        self.assertEqual(errmsg.count("ERROR"), 2, errmsg)
        self.assertEqual(errmsg.count("Missing id tag 'Blank'") +
                         errmsg.count("Empty id tag 'Blank'"), 2, errmsg)
        self.assertEqual(errmsg.count("record #"), 2, errmsg)
        self.assertEquals(fps[0].split(b"\t")[1], b"This is not Blank")

    #
    # Various ways of handling a tab characters in an id tag
    #

    def test_tab_id_tag(self):
        headers, fps, errmsg = self._runner.run_split_capture(
            "--id-tag Tab", 2, MISSING_TITLE)
        ##  self.assertNotIn("ERROR: Empty id tag 'Tab'", errmsg)
        self.assertEquals(fps[0].split(b"\t")[1], b"Leading tab")
        self.assertEquals(fps[1].split(b"\t")[1], b"This does not")

    def test_tab_id_tag_strict(self):
        errmsg = self._runner.run_exit(
            "--id-tag Tab --errors strict", MISSING_TITLE)
        if self.toolkit == "openbabel":
            self.assertIn("ERROR: Missing id tag 'Tab' in SD record", errmsg)
        else:
            self.assertIn("ERROR: Empty id tag 'Tab' in SD record after cleanup", errmsg)
        self.assertIn("record #2", errmsg)
        self.assertIn("missing_title.sdf'", errmsg)

    def test_tab_id_tag_report(self):
        headers, fps, errmsg = self._runner.run_split_capture(
            "--id-tag Tab --errors report", 2, MISSING_TITLE)
        if self.toolkit == "openbabel":
            self.assertIn("ERROR: Missing id tag 'Tab' in SD record", errmsg)
        else:
            self.assertIn("ERROR: Empty id tag 'Tab' in SD record after cleanup", errmsg)
        self.assertIn("record #2", errmsg)
        self.assertEquals(fps[0].split(b"\t")[1], b"Leading tab")
        self.assertEquals(fps[1].split(b"\t")[1], b"This does not")

    def test_tab_id_tag_ignore(self):
        headers, fps, errmsg = self._runner.run_split_capture(
            "--id-tag Tab --errors ignore", 2, MISSING_TITLE)
        ##  self.assertNotIn("ERROR: Empty id tag 'Tab'", errmsg)
        self.assertEquals(fps[0].split(b"\t")[1], b"Leading tab")
        self.assertEquals(fps[1].split(b"\t")[1], b"This does not")


    def test_contains_tab_id_tag(self):
        headers, fps, errmsg = self._runner.run_split_capture("--id-tag ContainsTab", 3, MISSING_TITLE)
        self.assertNotIn("ERROR: Empty id tag 'ContainsTab'", errmsg)
        ids = [fp.split(b"\t")[1] for fp in fps]
        self.assertEquals(ids, [b"ThreeTabs", b"tabseparated", b"twotabs"])

    def test_contains_tab_id_tag_strict(self):
        headers, fps = self._runner.run_split("--id-tag ContainsTab --errors strict", 3, MISSING_TITLE)
        ids = [fp.split(b"\t")[1] for fp in fps]
        self.assertEquals(ids, [b"ThreeTabs", b"tabseparated", b"twotabs"])

    def test_contains_tab_id_tag_report(self):
        headers, fps, errmsg = self._runner.run_split_capture("--id-tag ContainsTab --errors report", 3, MISSING_TITLE)
        self.assertNotIn("ContainsTab", errmsg)
        self.assertNotIn("ERROR", errmsg)
        ids = [fp.split(b"\t")[1] for fp in fps]
        self.assertEquals(ids, [b"ThreeTabs", b"tabseparated", b"twotabs"])

    def test_contains_tab_id_tag_ignore(self):
        headers, fps, errmsg = self._runner.run_split_capture("--id-tag ContainsTab --errors ignore", 3, MISSING_TITLE)
        self.assertNotIn("ERROR: Empty id tag 'ContainsTab'", errmsg)
        ids = [fp.split(b"\t")[1] for fp in fps]
        self.assertEquals(ids, [b"ThreeTabs", b"tabseparated", b"twotabs"])

    #
    # Handling bad files
    #

    def test_handles_missing_filename(self):
        errmsg = self._runner.run_exit("this_file_does_not_exist.sdf", PUBCHEM_SDF)
        self.assertIn("Structure file '", errmsg)
        self.assertIn("this_file_does_not_exist.sdf", errmsg)
        self.assertIn("' does not exist", errmsg)
        self.assertNotIn("pubchem", errmsg)

    def test_handles_missing_filename_at_end(self):
        errmsg = self._runner.run_exit([PUBCHEM_SDF, "this_file_does_not_exist.sdf"])
        self.assertIn("Structure file '", errmsg)
        self.assertIn("this_file_does_not_exist.sdf", errmsg)
        self.assertIn("' does not exist", errmsg)
        self.assertNotIn("pubchem", errmsg)

    def test_unreadable_file(self):
        # Read three files. The second file is not readable.
        tf = tempfile.NamedTemporaryFile(suffix="unreadable.sdf")
        try:
            os.chmod(tf.name, 0o222)
            errmsg = self._runner.run_exit([PUBCHEM_SDF, tf.name])
            self.assertIn("Problem reading structure fingerprints", errmsg)
            self.assertIn("unreadable.sdf", errmsg)
            self.assertNotIn("pubchem", errmsg)
        finally:
            tf.close()

    def test_output_directory_does_not_exist(self):
        errmsg = self._runner.run_exit(["-o", "/never/never/land/exists/forever/xyzzy.fps", PUBCHEM_SDF])
        self.assertIn("Cannot open output fingerprint file:", errmsg)
        self.assertIn("/never/never/land/exists", errmsg)

    def test_bad_tag(self):
        result = self._runner.run_exit("--id-tag >nogood")
        self.assertIn("Invalid id tag: '>nogood'", result)

    def test_unknown_output_format(self):
        errmsg = self._runner.run_exit(["-o", "/another/path/that/does/not/exist.sdf.gz", PUBCHEM_SDF])
        self.assertIn("Cannot open output fingerprint file: Unable to determine fingerprint format type from",
                      errmsg)
        self.assertIn("does/not/exist", errmsg)
        self.assertIn("usage:", errmsg)
        
class TestIO(object):
    # '_runner' must be defined in the subclass
    def test_can_specify_input_format_matching_file(self):
        def without_source_header(cmdline, source):
            return [line for line in self._runner.run(cmdline, source)
                        if not line.startswith(b"#source=") and
                           not line.startswith(b"#date=")]
        result1 = without_source_header("", PUBCHEM_SDF)
        result2 = without_source_header("", PUBCHEM_SDF_GZ)
        self.assertEquals(result1, result2)

        result3 = without_source_header("--in sdf.gz", PUBCHEM_SDF_GZ)
        self.assertEquals(result1, result3)
        
        result4 = without_source_header("--in sdf", PUBCHEM_ANOTHER_EXT)
        self.assertEquals(result1, result4)
    
    
    def test_missing_filename(self):
        errmsg = self._runner.run_exit([], "does_not_exist.smi")
        self.assertIn("Structure file", errmsg)
        self.assertIn("does not exist", errmsg)
        self.assertIn("does_not_exist.smi", errmsg)

    def test_file_does_not_exist(self):
        msg = self._runner.run_exit([], source="/asdfaserwe.does.not.exist")
        self.assertIn("Structure file '/asdfaserwe.does.not.exist' does not exist", msg)

        
    def test_bad_input_extension(self):
        filename = get_tmpfile(self, "qwerty.xyzzy")
        open(filename, "wb").close()
        errmsg = self._runner.run_exit([], source=filename)
        self.assertIn("does not support the 'xyzzy' format", errmsg)
        
    def test_bad_input_flag(self):
        errmsg = self._runner.run_exit(" --in xyzzy")
        self.assertIn("Unsupported format specifier", errmsg)
        self.assertIn("xyzzy", errmsg)

    def test_unreadable_input(self):
        filename = get_tmpfile(self, "unreadable.smi")
        open(filename, "wb").close()
        os.chmod(filename, 0)
        try:
            open(filename)
        except IOError as err:
            expected_msg = str(err)
            
        errmsg = self._runner.run_exit([], source=filename)
        self.assertIn("Problem reading structure fingerprints", errmsg)
        self.assertIn(expected_msg, errmsg)

    def test_bad_output_extension(self):
        filename = get_tmpfile(self, "bad_extension.fpq")
        errmsg = self._runner.run_exit(["--output", filename])
        self.assertIn("Cannot open output fingerprint file: Unable to determine fingerprint format type from", errmsg)
        self.assertIn("bad_extension.fpq", errmsg)
        self.assertIn("\nUse --out to specify 'fps' or 'fps.gz'.", errmsg)
        
    def test_bad_output_flag(self):
        errmsg = self._runner.run_exit(["--out", "fpq"])
        self.assertIn("invalid choice: 'fpq' (choose from 'fps', 'fps.gz')", errmsg)
        
def get_tmpdir(test_case):
    dirname = tempfile.mkdtemp()
    test_case.addCleanup(shutil.rmtree, dirname)
    return dirname

def get_tmpfile(testcase, filename):
    dirname = tempfile.mkdtemp(prefix="chemfp_test")
    testcase.addCleanup(shutil.rmtree, dirname)
    filename = os.path.join(dirname, filename)
    return filename

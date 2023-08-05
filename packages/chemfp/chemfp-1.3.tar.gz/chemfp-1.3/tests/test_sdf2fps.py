import sys
import unittest2

from chemfp.commandline import sdf2fps
from chemfp.bitops import hex_encode_as_bytes

import support

real_stdin = sys.stdin
real_stdout = sys.stdout
real_stderr = sys.stderr

DECODER_SDF = support.fullpath("decoder.sdf")
DECODER_SDF_BYTES = open(DECODER_SDF, "rb").read()

PUBCHEM_SDF = support.fullpath("pubchem.sdf")
PUBCHEM_SDF_BYTES = open(PUBCHEM_SDF, "rb").read()
PUBCHEM_SDF_GZ = support.fullpath("pubchem.sdf.gz")

_runner = support.Runner(sdf2fps.main)
run_exit = _runner.run_exit

run = _runner.run
run_split_capture = _runner.run_split_capture


def run_fps(s, expect_length=None):
    result = run(s, DECODER_SDF)
    while result[0].startswith(b"#"):
        del result[0]
    if expect_length is not None:
        assert len(result) == expect_length
    return result


class TestDecoderFlags(unittest2.TestCase):
    def test_cactvs(self):
        result = run_fps("--cactvs --fp-tag PUBCHEM_CACTVS_SUBSKEYS")
        self.assertEquals(result, [b"07de8d002000000000000000000000000080060000000c000000000000000080030000f8401800000030508379344c014956000055c0a44e2a0049200084e140581f041d661b10064483cb0f2925100619001393e10001007000000000008000000000000000400000000000000000\t9425004",
                                   b"07de0d000000000000000000000000000080460300000c0000000000000000800f0000780038000000301083f920cc09695e0800d5c0e44e6e00492190844145dc1f841d261911164d039b8f29251026b9401313e0ec01007000000000000000000000000000000000000000000000\t9425009"])

    def test_binary40(self):
        result = run_fps("--binary --fp-tag binary40", 2)
        self.assertEquals(result[0], b"000500c000\t9425004")
        self.assertEquals(result[1], b"00fab75300\t9425009")

    def test_binary_msb40(self):
        result = run_fps("--binary-msb --fp-tag binary40", 2)
        self.assertEquals(result[0], b"000300a000\t9425004")
        self.assertEquals(result[1], b"00caed5f00\t9425009")

    def test_binary3(self):
        result = run_fps("--binary --fp-tag binary3", 2)
        self.assertEquals(result[0], b"04\t9425004")
        self.assertEquals(result[1], b"03\t9425009")

    def test_binary_msb3(self):
        result = run_fps("--binary-msb --fp-tag binary3", 2)
        self.assertEquals(result[0], b"01\t9425004")
        self.assertEquals(result[1], b"06\t9425009")

    def test_binary8(self):
        result = run_fps("--binary --fp-tag binary8", 2)
        self.assertEquals(result[0], b"76\t9425004")
        self.assertEquals(result[1], b"bc\t9425009")

    def test_binary_msb8(self):
        result = run_fps("--binary-msb --fp-tag binary8", 2)
        self.assertEquals(result[0], b"6e\t9425004")
        self.assertEquals(result[1], b"3d\t9425009")


    def test_binary17(self):
        result = run_fps("--binary --fp-tag binary17", 2)
        self.assertEquals(result[0], b"38b701\t9425004")
        self.assertEquals(result[1], b"489d01\t9425009")

    def test_binary_msb17(self):
        result = run_fps("--binary-msb --fp-tag binary17", 2)
        self.assertEquals(result[0], b"db3900\t9425004")
        self.assertEquals(result[1], b"732500\t9425009")


    def test_binary_failure(self):
        errmsg = run_exit("--binary --fp-tag PUBCHEM_CACTVS_SUBSKEYS", DECODER_SDF)
        self.assertIn("Could not binary decode tag 'PUBCHEM_CACTVS_SUBSKEYS' value 'AAADceB7sQ", errmsg)
        self.assertIn("Must pass in a string containing only 0s and 1s", errmsg)
        self.assertIn("line 1", errmsg)
        self.assertIn("record #1", errmsg)
        self.assertIn("decoder.sdf", errmsg)

    def test_binary_msb_failure(self):
        errmsg = run_exit("--binary-msb --fp-tag PUBCHEM_CACTVS_SUBSKEYS", DECODER_SDF)
        self.assertIn("Could not binary_msb decode tag 'PUBCHEM_CACTVS_SUBSKEYS' value 'AAADceB7sQ", errmsg)
        self.assertIn("Must pass in a string containing only 0s and 1s", errmsg)
        self.assertIn("line 1", errmsg)
        self.assertIn("record #1", errmsg)
        self.assertIn("decoder.sdf", errmsg)


    def test_hex2(self):
        result = run_fps("--hex --fp-tag hex2", 2)
        self.assertEquals(result[0], b"ab\t9425004")
        self.assertEquals(result[1], b"01\t9425009")
        
    def test_hex_lsb2(self):
        # 0xab == 0b10101011
        # 10101011 with LSB first is 5 d => "d5"
        # 0x01 == 0b00000001 => 80 when in LSB first
        result = run_fps("--hex-lsb --fp-tag hex2", 2)
        self.assertEquals(result[0], b"d5\t9425004")
        self.assertEquals(result[1], b"80\t9425009")

    def test_hex_msb2(self):
        # With 2 nibbles the result is the same as hex
        result = run_fps("--hex-msb --fp-tag hex2", 2)
        self.assertEquals(result[0], b"ab\t9425004")
        self.assertEquals(result[1], b"01\t9425009")

    def test_hex16(self):
        result = run_fps("--hex --fp-tag hex16", 2)
        self.assertEquals(result[0], b"0123456789abcdef\t9425004")
        self.assertEquals(result[1], b"abcdef0123456789\t9425009")
        
    def test_hex_lsb16(self):
        result = run_fps("--hex-lsb --fp-tag hex16", 2)
        # 0123456789abcdef in LSB form => 
        # 084c2a6e195d3b7f when nibbles bits are in MSB form but nibbles are LSB
        # 80 c4 a2 e6 91 d5 b3 f7 when byte bits are in MSB and bytes are LSB
        self.assertEquals(result[0], b"80c4a2e691d5b3f7\t9425004")
        # abcdef0123456789 in LSB form =>
        # 5d3b7f084c2a6e19 =>
        # d5 b3 f7 80 c4 a2 e6 91
        self.assertEquals(result[1], b"d5b3f780c4a2e691\t9425009")

    def test_hex_msb16(self):
        # Just a bit of reordering
        result = run_fps("--hex-msb --fp-tag hex16", 2)
        self.assertEquals(result[0], b"efcdab8967452301\t9425004")
        self.assertEquals(result[1], b"8967452301efcdab\t9425009")
        
    def test_base64_16(self):
        result = run_fps("--base64 --fp-tag base64_16", 2)
        self.assertEquals(result[0], hex_encode_as_bytes("Greetings, human") + b"\t9425004")
        self.assertEquals(result[1], hex_encode_as_bytes("blahblahspamblah") + b"\t9425009")

    def test_daylight1(self):
        result = run_fps("--daylight --fp-tag daylight1", 2)
        self.assertEquals(result[0], hex_encode_as_bytes("PyDaylight") + b"\t9425004")
        self.assertEquals(result[1], hex_encode_as_bytes("chemfptest") + b"\t9425009")

    def test_daylight2(self):
        result = run_fps("--daylight --fp-tag daylight2", 2)
        self.assertEquals(result[0], hex_encode_as_bytes("Okie dokie pokie!") + b"\t9425004")
        self.assertEquals(result[1], hex_encode_as_bytes("Testing   1, 2, 3") + b"\t9425009")

    def test_daylight3(self):
        result = run_fps("--daylight --fp-tag daylight3", 2)
        self.assertEquals(result[0], b"\t9425004")
        self.assertEquals(result[1], b"\t9425009")

    def test_daylight_end_error(self):
        errmsg = run_exit("--daylight --fp-tag daylight-end-illegal", DECODER_SDF)
        self.assertIn("Could not daylight decode tag 'daylight-end-illegal' value '1P!_P'", errmsg)
        self.assertIn("Last character of encoding must be 1, 2, or 3, not 'P'", errmsg)
        self.assertIn("line 1", errmsg)
        self.assertIn("decoder.sdf", errmsg)

    def test_daylight_symbol_error(self):
        errmsg = run_exit("--daylight --fp-tag daylight-illegal", DECODER_SDF)
        self.assertIn("Could not daylight decode tag 'daylight-illegal' value '1P!_3'", errmsg)
        self.assertIn("Unknown encoding symbol", errmsg)
        self.assertIn("line 1", errmsg)
        self.assertIn("decoder.sdf", errmsg)

    def test_daylight_length_error(self):
        errmsg = run_exit("--daylight --fp-tag PUBCHEM_CACTVS_SUBSKEYS", DECODER_SDF)
        self.assertIn("Could not daylight decode tag 'PUBCHEM_CACTVS_SUBSKEYS' value 'AAADceB7sQ", errmsg)
        self.assertIn("Daylight binary encoding is of the wrong length", errmsg)
        self.assertIn("line 1", errmsg)
        self.assertIn("decoder.sdf", errmsg)


    def test_bad_decoding(self):
        _, _, msg = run_split_capture("--base64 --fp-tag binary17 --errors report")
        self.assertIn("Missing fingerprint tag 'binary17'", msg)
        self.assertIn("Skipping.", msg)

class TestBitSizes(unittest2.TestCase):
    def test_exact_fingerprint_bits(self):
        result = run("--binary --fp-tag binary3", DECODER_SDF)
        self.assertIn(b"#num_bits=3", result)
        
    def test_user_bits_match_fingerprint_bits(self):
        result = run("--binary --fp-tag binary3 --num-bits 3", DECODER_SDF)
        self.assertIn(b"#num_bits=3", result)
        self.assertIn(b"04\t9425004", result)
        self.assertIn(b"03\t9425009", result)

    def test_user_bits_disagree_with_fingerprint_bits(self):
        errmsg = run_exit("--binary --fp-tag binary3 --num-bits 2", DECODER_SDF)
        self.assertIn("has 3 bits", errmsg)
        self.assertIn(" 2", errmsg)

    def test_implied_from_fingerprint_bytes(self):
        result = run("--hex --fp-tag hex2", DECODER_SDF)
        self.assertIn(b"#num_bits=8", result)

    def test_user_bits_matches_fingerprint_bytes(self):
        result = run("--hex --fp-tag hex2 --num-bits 8", DECODER_SDF)
        self.assertIn(b"#num_bits=8", result)

    def test_user_bits_too_large_for_bytes(self):
        result = run_exit("--hex --fp-tag hex2 --num-bits 9", DECODER_SDF)
        self.assertIn("1 <= num-bits <= 8, not 9", result)

    def test_user_bits_acceptably_smaller_than_bytes(self):
        result = run("--hex --fp-tag hex2 --num-bits 6", DECODER_SDF)
        self.assertIn(b"#num_bits=6", result)

    def test_user_bits_too_much_smaller_than_bytes(self):
        result = run_exit("--hex --fp-tag hex16 --num-bits 56", DECODER_SDF)
        self.assertIn("57 <= num-bits <= 64, not 56", result)

class TestTitleProcessing(unittest2.TestCase):
    def test_title_from_title_tag(self):
        result = run("--hex --fp-tag hex2 --id-tag binary3", DECODER_SDF)
        self.assertIn(b"ab\t001", result)

    def test_missing_title_from_title_line(self):
        _, _, warning = run_split_capture("--hex --fp-tag hex2 --id-tag FAKE_TITLE --errors report")
        self.assertIn("Missing id tag 'FAKE_TITLE'", warning)
        self.assertIn("line 191", warning)
        self.assertIn("record #2", warning)
        self.assertIn("first line is '9425009'", warning)
        self.assertIn("Skipping.", warning)

    def test_missing_all_titles(self):
        _, _, warning = run_split_capture("--hex --fp-tag hex2 --id-tag DOES_NOT_EXIST --errors report")
        self.assertIn("Missing id tag 'DOES_NOT_EXIST'", warning)
        self.assertIn("line 1", warning)
        self.assertIn("record #1", warning)
        self.assertIn("line 191", warning)
        self.assertIn("record #2", warning)

    def test_control_return_in_title(self):
        filename = support.get_tmpfile(self, "control_return.sdf")
        with open(filename, "wb") as f:
            f.write(PUBCHEM_SDF_BYTES.replace(b"94250", b"QZ\r350"))
        header, output, warning = run_split_capture("--pubchem", source=filename)
        self.assertEqual(len(output), 19)
        for line in output:
            self.assertIn(b"QZ350", line)

    def test_nul_in_title(self):
        filename = support.get_tmpfile(self, "nul.sdf")
        with open(filename, "wb") as f:
            f.write(PUBCHEM_SDF_BYTES.replace(b"94250", b"QZ\x00350"))
        header, output, warning = run_split_capture("--pubchem", source=filename)
        self.assertEqual(len(output), 19)
        for line in output:
            self.assertIn(b"QZ350", line)
            
    def test_tab_in_title(self):
        filename = support.get_tmpfile(self, "tab.sdf")
        with open(filename, "wb") as f:
            f.write(PUBCHEM_SDF_BYTES.replace(b"94250", b"QZ\t350"))
        header, output, warning = run_split_capture("--pubchem", source=filename)
        self.assertEqual(len(output), 19)
        for line in output:
            self.assertIn(b"QZ350", line)

    def test_strip_title(self):
        filename = support.get_tmpfile(self, "strip_title.sdf")
        with open(filename, "wb") as f:
            f.write(PUBCHEM_SDF_BYTES.replace(b"9425009", b"\r\t\0"))
        header, output, warning = run_split_capture("--pubchem --errors report", source=filename)
        self.assertEqual(len(output), 18)
        for line in output:
            self.assertIn(b"9425", line)
        self.assertIn("Empty title in SD record after cleanup", warning)
        self.assertIn("record #2", warning)
        self.assertIn(r"'\r\t\x00'", warning)

class TestFingerprintProcessing(unittest2.TestCase):
    def test_fingerprint_length_changes(self):
        content = DECODER_SDF_BYTES.replace(b"0000000001011111111011011100101000000000", b"000000000101111111101101")
        with support.wrap_stdin(content):
            errmsg = run_exit("--binary --fp-tag binary40", source=None)
        self.assertIn("ERROR: Tag 'binary40' value '000000000101111111101101' has 24 bits but expected 40, "
                      "file '<stdin>', line 160, record #2: first line is '9425009'",
                      errmsg)

    def test_fingerprint_length_changes_ignore(self):
        content = DECODER_SDF_BYTES.replace(b"0000000001011111111011011100101000000000", b"000000000101111111101101")
        with support.wrap_stdin(content):
             header, lines, errmsg = run_split_capture("--binary --fp-tag binary40 --errors ignore", source=None)
        self.assertEqual(len(lines), 1)
        self.assertFalse(errmsg)

    def test_fingerprint_length_changes_report(self):
        content = DECODER_SDF_BYTES.replace(b"0000000001011111111011011100101000000000", b"000000000101111111101101")
        with support.wrap_stdin(content + DECODER_SDF_BYTES):
             header, lines, errmsg = run_split_capture("--binary --fp-tag binary40 --errors report", source=None)
        self.assertEqual(len(lines), 3)
        self.assertIn("ERROR: Tag 'binary40' value '000000000101111111101101' has 24 bits but expected 40, "
                      "file '<stdin>', line 160, record #2: first line is '9425009'",
                      errmsg)
    

        
FPS_9425004 = b"07de8d002000000000000000000000000080060000000c000000000000000080030000f8401800000030508379344c014956000055c0a44e2a0049200084e140581f041d661b10064483cb0f2925100619001393e10001007000000000008000000000000000400000000000000000\t9425004"

class TestParameters(unittest2.TestCase):
    def _check_valid(self, result, count=1):
        self.assertIn(b"#num_bits=881", result)
        self.assertIn(b"#software=CACTVS/unknown", result)
        self.assertIn(b"#type=CACTVS-E_SCREEN/1.0 extended=2", result)
        self.assertIn(FPS_9425004, result)
        self.assertIn(b"07de0d000000000000000000000000000080460300000c0000000000000000800f0000780038000000301083f920cc09695e0800d5c0e44e6e00492190844145dc1f841d261911164d039b8f29251026b9401313e0ec01007000000000000000000000000000000000000000000000\t9425009", result)
        if count != 1:
            self.assertEqual(result.count(FPS_9425004), count, result)

    def test_pubchem(self):
        result = run("--pubchem")
        self._check_valid(result)
        
    def test_in_sdf(self):
        result = run("--pubchem --in sdf", source=PUBCHEM_SDF)
        self._check_valid(result)
        
    def test_in_sdf_but_not_sdf(self):
        result = run_exit("--pubchem --in sdf", source=PUBCHEM_SDF_GZ)
        self.assertIn("Could not find a valid SD record", result)
        
    def test_in_sdf_gz(self):
        result = run("--pubchem --in sdf.gz", source=PUBCHEM_SDF_GZ)
        self._check_valid(result)

    def test_in_sdf_gz_but_not_sdf_gz(self):
        result = run_exit("--pubchem --in sdf.gz", source=PUBCHEM_SDF)
        self.assertIn("ERROR: Not a gzipped file", result)
        
    def test_multiple_input_files_with_mixed_compression(self):
        result = run(["--pubchem", PUBCHEM_SDF], source=PUBCHEM_SDF_GZ)
        self._check_valid(result, 2)

    def test_filename_does_not_exist(self):
        result = run_exit(["--pubchem"], source="/this/file/does/not/exist.sdf")
        self.assertIn("Structure file '/this/file/does/not/exist.sdf' does not exist", result)

    def test_filename_does_not_exist_with_multiple_files(self):
        result = run_exit(["--pubchem", PUBCHEM_SDF], source="/this/file/does/not/exist.sdf")
        self.assertIn("Structure file '/this/file/does/not/exist.sdf' does not exist", result)

    def test_from_stdin(self):
        with support.wrap_stdin(PUBCHEM_SDF_BYTES):
            result = run("--pubchem", source=None)
            self._check_valid(result)

    def test_wrong_encoding(self):
        result = run_exit("--fp-tag=PUBCHEM_CACTVS_SUBSKEYS --hex")
        self.assertIn("Could not hex decode tag 'PUBCHEM_CACTVS_SUBSKEYS' value", result)
        self.assertIn("Non-hexadecimal digit found", result)
        
    def test_wrong_encoding_ignore_errors(self):
        header, output, warning = run_split_capture("--fp-tag=PUBCHEM_CACTVS_SUBSKEYS --hex --errors ignore")
        self.assertEqual(len(output), 0)
        self.assertFalse(warning)
        
    def test_wrong_encoding_report_errors(self):
        header, output, warning = run_split_capture("--fp-tag=PUBCHEM_CACTVS_SUBSKEYS --hex --errors report")
        self.assertEqual(len(output), 0)
        self.assertEqual(warning.count("Could not hex decode tag"), 19)
        self.assertIn("'9425004'", warning)
        self.assertIn("'9425009'", warning)
        self.assertIn("'9425046'", warning)

    def test_bitlength_changes(self):
        content = PUBCHEM_SDF_BYTES.replace(
            b"AAADceB7sABAAAAAAAAAAAAAAAAAAWLAAAAwAAAAAAAAAFgB/AAAHgQYAAAACAjB1gQywbJqEAiuASVyVACT9KBhij"
            b"pa+D24ZJgIYLLg0fGUpAhgmADoyAcYCAAAAAAAAAAAAQAAAAAAAAACAAAAAAAAAA==", b"QW5kcmV3IERhbGtl")
        with support.wrap_stdin(content):
            result = run_exit("--fp-tag=PUBCHEM_CACTVS_SUBSKEYS --base64", source=None)
        self.assertIn("ERROR: Tag 'PUBCHEM_CACTVS_SUBSKEYS' value", result)
        self.assertIn("'QW5kcmV3IERhbGtl'", result)
        self.assertIn("has 12 bytes but expected 115", result)
        self.assertIn("record #18", result)
        
    def test_bitlength_changes_ignore_errors(self):
        content = PUBCHEM_SDF_BYTES.replace(
            b"AAADceB7sABAAAAAAAAAAAAAAAAAAWLAAAAwAAAAAAAAAFgB/AAAHgQYAAAACAjB1gQywbJqEAiuASVyVACT9KBhij"
            b"pa+D24ZJgIYLLg0fGUpAhgmADoyAcYCAAAAAAAAAAAAQAAAAAAAAACAAAAAAAAAA==", b"QW5kcmV3IERhbGtl")
        with support.wrap_stdin(content):
            header, output, warning = run_split_capture("--fp-tag=PUBCHEM_CACTVS_SUBSKEYS --base64 --errors ignore", source=None)
        self.assertEqual(len(output), 18)
        self.assertFalse(warning)
        
    def test_bitlength_changes_report_errors(self):
        content = PUBCHEM_SDF_BYTES.replace(
            b"AAADceB7sABAAAAAAAAAAAAAAAAAAWLAAAAwAAAAAAAAAFgB/AAAHgQYAAAACAjB1gQywbJqEAiuASVyVACT9KBhij"
            b"pa+D24ZJgIYLLg0fGUpAhgmADoyAcYCAAAAAAAAAAAAQAAAAAAAAACAAAAAAAAAA==", b"QW5kcmV3IERhbGtl")
        with support.wrap_stdin(content):
            header, output, warning = run_split_capture("--fp-tag=PUBCHEM_CACTVS_SUBSKEYS --base64 --errors report", source=None)
        self.assertEqual(len(output), 18)
        self.assertIn("ERROR: Tag 'PUBCHEM_CACTVS_SUBSKEYS' value", warning)
        self.assertIn("'QW5kcmV3IERhbGtl'", warning)
        self.assertIn("has 12 bytes but expected 115", warning)
        self.assertIn("record #18", warning)
        
    def test_output_file_does_not_exist(self):
        result = run_exit("--pubchem -o /this/also/does/not/exist/at/all.fps")
        self.assertIn("Cannot open output file", result)
        self.assertIn("'/this/also/does/not/exist/at/all.fps'", result)
        
    def test_output_file_uses_unsupported_format(self):
        result = run_exit("--pubchem -o /this/also/does/not/exist/at/all.fps.xz")
        self.assertIn("Cannot open output fingerprint file", result)
        self.assertIn("chemfp does not yet support xz compression", result)

        
class TestBadArgs(unittest2.TestCase):
    def test_missing_fp_tag(self):
        msg = run_exit("")
        self.assertIn("argument --fp-tag is required", msg)

    def test_num_bits_positive(self):
        msg = run_exit("--fp-tag SPAM --num-bits 0")
        self.assertIn("--num-bits must be a positive integer", msg)
        msg = run_exit("--fp-tag SPAM --num-bits -1")
        self.assertIn("--num-bits must be a positive integer", msg)

    def test_bad_char(self):
        msg = run_exit("--fp-tag SPAM --software this\bthat")
        self.assertIn("--software", msg)
        self.assertIn("'\\x08'", msg)
        
        
if __name__ == "__main__":
    unittest2.main()

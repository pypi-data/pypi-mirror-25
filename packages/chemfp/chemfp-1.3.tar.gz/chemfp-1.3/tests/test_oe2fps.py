import unittest2
import sys
import os
from cStringIO import StringIO as SIO

from chemfp.bitops import hex_contains_bit
import support

try:
    from openeye import oechem  # These tests require OEChem
    if not oechem.OEChemIsLicensed():
        print >>sys.stderr, "oechem library available but not license found. Skipping its tests."
        raise ImportError
    has_oechem = True
    skip_oechem = False
except ImportError:
    has_oechem = False
    skip_oechem = True
    if not support.can_skip("oe"):
        skip_oechem = False
        from openeye import oechem

if has_oechem:
    from chemfp.commandline import oe2fps
    import chemfp.openeye
    chemfp.openeye._USE_SELECT = False # Grrr. Needed to automate testing.

    real_stdout = sys.stdout
    real_stderr = sys.stderr

    PUBCHEM_SDF = support.fullpath("pubchem.sdf")
    PUBCHEM_SDF_GZ = support.fullpath("pubchem.sdf.gz")
    PUBCHEM_ANOTHER_EXT = support.fullpath("pubchem.should_be_sdf_but_is_not")

    MACCS_SMI = support.fullpath("maccs.smi")

    oeerrs = oechem.oeosstream()
    oechem.OEThrow.SetOutputStream(oeerrs)

def _check_for_oe_errors():
    lines = oeerrs.str().splitlines()
    for line in lines:
        if line.startswith("Warning: Stereochemistry corrected on atom number"):
            continue
        if line.startswith("Warning: Unknown file format set in input stream"):
            # There's a bug in OEChem where it generates this warning on unknown
            # file extensions even after SetFormat has been called
            continue
        raise AssertionError("Unexpected message from OEChem: %r" % (line,))


# I build the fingerprints using bit offsets to ensure that the test
# data matches the actual bit results from OEChem. While I could
# reproduce the method in chemfp.openeye.get_maccs_fingerprinter, that
# would be cheating. I could test against ToHexString() but then I
# would have the nagging feeling that I got the ordering
# backwards. Instead, I do it from scratch using the bit offset.

def _construct_test_values(fp_func = None, num_bits=4096):
    from openeye.oechem import oemolistream
    from openeye.oegraphsim import OEFingerPrint, OEMakePathFP
    fp = OEFingerPrint()
    ifs = oemolistream()
    assert ifs.open(PUBCHEM_SDF)
    hex_data = []
    if fp_func is None:
        fp_func = OEMakePathFP

    def _convert_to_chemfp_order(s):
        # The FPS format allows either case but I prefer lowercase
        s = s.lower()
        # OpenEye orders hex values on nibbles. Chemfp orders on bytes.
        return "".join( (s[i+1]+s[i]) for i in range(0, len(s), 2))

    for mol in ifs.GetOEGraphMols():
        fp_func(fp, mol)
        # Set the byte values given the bit offsets
        bytes = [0] * (num_bits//8)
        i = fp.FirstBit()
        while i >= 0:
            bytes[i//8] |= 1<<(i%8)
            i = fp.NextBit(i)
        as_hex = "".join("%02x" % i for i in bytes)
        assert len(as_hex) == 2*(num_bits//8), len(as_hex)
        # Double-check that it matches the (reordered) ToHexString()
        oe_hex = fp.ToHexString()[:-1]
        assert as_hex == _convert_to_chemfp_order(oe_hex), (
            as_hex, _convert_to_chemfp_order(oe_hex))
        
        hex_data.append("%s\t%s" % (as_hex, mol.GetTitle()))
    return hex_data

# I have this to flag any obvious changes in the OEChem algorithm and
# to help with figuring out how to build a test case.

_fp1 = "00001002200200000000000000000000000008400020000300801002300000000200000840000000000080000000000000204008000000000010000c10000000400000010100000210800002000000009400000000020020088000000000010000918000200000580400002000010020002440000008001001404000000200010000a8c00020400200002000004084000000030100820000000000000002000000510001800000010001000081100110000800480000100400000c00004c000800000808000100000022000228800020004000000200182100000100000000101000010004004808000000800000000001010010201000000090400000100000020010000010201000000040300100000000580000000000000200000000401000000000000008040004000000008002080820000310280200004040a000000010000080005000004010010018000000800000020008208040000400000200000000000000000800080050000008400100004000000200ac001000000000800100200060900010002000000040200000000000040808000048400040000000020000001001000000000302002008200000a044000180800000100000000200000049004080080000100022a00084000400280480000000402400080400404100000000040000020c10000000000c000100002000080010002080100002000600"

if has_oechem:
    hex_test_values = _construct_test_values()
    assert hex_test_values[0].startswith(_fp1)

class OERunner(support.Runner):
    def pre_run(self):
        oeerrs.clear()
    def post_run(self):
        _check_for_oe_errors()

    def run_stdin(self, cmdline, source):
        fd = os.open(source, os.O_RDONLY)
        oechem.oein.openfd(fd, False)
        try:
            return self.run(cmdline, None)
        finally:
            oechem.oein.openfd(0, False)
            os.close(fd)

if has_oechem:
    runner = OERunner(oe2fps.main)
    run = runner.run
    run_stdin = runner.run_stdin
    run_fps = runner.run_fps
    run_exit = runner.run_exit
else:
    runner = None

def headers(lines):
    assert lines[0] == "FPS1"
    del lines[0]
    return [line for line in lines if line.startswith("#")]


class TestMACCS(unittest2.TestCase):
    def test_bitorder(self):
        result = run_fps("--maccs166", 7, support.fullpath("maccs.smi"))
        # The fingerprints are constructed to test the first few bytes.
        self.assertEquals(result[0][:6], support.set_bit(2))
        self.assertEquals(result[1][:6], support.set_bit(3))
        self.assertEquals(result[2][:6], support.set_bit(4))
        self.assertEquals(result[3][:6], support.set_bit(5))
        self.assertEquals(result[4][:6], support.set_bit(9))
        self.assertEquals(result[5][:6], support.set_bit(10))
        self.assertEquals(result[6][:6], support.set_bit(16))

TestMACCS = unittest2.skipIf(skip_oechem, "OEChem not installed")(TestMACCS)

class TestPath(unittest2.TestCase):
    def test_default(self):
        result = run_fps("", 19)
        hexfp, id = result[0].split()
        self.assertEquals(len(hexfp), 4096//4)
        self.assertEquals(result[0], hex_test_values[0])
        self.assertEquals(result, hex_test_values)

    def test_path_option(self):
        result = run_fps("--path", 19)
        self.assertEquals(result, hex_test_values)

    @unittest2.skipIf(has_oechem and oechem.OEChemGetRelease() == "2.1.3.b.1 debug",
                      "skip an assertion failure in this debug version")
    def test_num_bits(self):
        result = run_fps("--numbits 16", 19)
        self.assertEquals(result[0][:5], "ff1f\t")

    def test_min_bonds_default(self):
        result = run_fps("--minbonds 0", 19)
        self.assertEquals(result, hex_test_values)

    def test_min_bonds_changed(self):
        result = run_fps("--minbonds 1", 19)
        self.assertNotEquals(result, hex_test_values)

    def test_max_bonds_default(self):
        result = run_fps("--maxbonds 5", 19)
        self.assertEquals(result, hex_test_values)
        
    def test_max_bonds_changed(self):
        result = run_fps("--minbonds 4", 19)
        self.assertNotEquals(result, hex_test_values)

    def test_atype_default_named(self):
        result = run_fps("--atype DefaultAtom", 19)
        self.assertEquals(result, hex_test_values)

    def test_atype_default_flags(self):
        result = run_fps(
            "--atype Arom|AtmNum|Chiral|EqHalo|FCharge|HvyDeg|Hyb", 19)
        self.assertEquals(result, hex_test_values)


    def test_atype_default_flags_with_duplicates(self):
        result = run_fps(
            "--atype Arom|Chiral|AtmNum|EqHalo|HvyDeg|FCharge|Hyb", 19)
        self.assertEquals(result, hex_test_values)

    # Make sure that each of the flags returns some other answer
    def test_atype_different_1(self):
        result = run_fps(
            "--atype AtmNum|Chiral|EqHalo|FCharge|HvyDeg|Hyb", 19)
        self.assertNotEquals(result, hex_test_values)

    def test_atype_different_2(self):
        result = run_fps(
            "--atype Arom|Chiral|EqHalo|FCharge|HvyDeg|Hyb", 19)
        self.assertNotEquals(result, hex_test_values)

    def test_atype_different_3(self):
        result = run_fps(
            "--atype Arom|AtmNum|EqHalo|FCharge|HvyDeg|Hyb", 19)
        self.assertNotEquals(result, hex_test_values)

    def test_atype_different_4(self):
        result = run_fps(
            "--atype Arom|AtmNum|Chiral|FCharge|HvyDeg|Hyb", 19)
        self.assertNotEquals(result, hex_test_values)

    def test_atype_different_5(self):
        result = run_fps(
            "--atype Arom|AtmNum|Chiral|EqHalo|HvyDeg|Hyb", 19)
        self.assertNotEquals(result, hex_test_values)

    def test_atype_different_6(self):
        result = run_fps(
            "--atype Arom|AtmNum|Chiral|EqHalo|FCharge|Hyb", 19)
        self.assertNotEquals(result, hex_test_values)

    def test_atype_different_7(self):
        result = run_fps(
            "--atype Arom|AtmNum|Chiral|EqHalo|FCharge|HvyDeg", 19)
        self.assertNotEquals(result, hex_test_values)


    def test_btype_default_named(self):
        result = run_fps("--btype DefaultBond", 19)
        self.assertEquals(result, hex_test_values)

    def test_btype_default_flags(self):
        result = run_fps("--btype Order|Chiral", 19)
        self.assertEqual(result, hex_test_values)

    def test_btype_different_1(self):
        result = run_fps("--btype Order", 19)
        self.assertNotEquals(result, hex_test_values)

    def test_btype_different_2(self):
        result = run_fps("--btype Chiral", 19)
        self.assertNotEquals(result, hex_test_values)

TestPath = unittest2.skipIf(skip_oechem, "OEChem not installed")(TestPath)

class TestPatterns(unittest2.TestCase):
    def test_rdmaccs(self):
        headers, fps = runner.run_split("--rdmaccs", 19)
        self.assertEqual(headers[b"#type"], b"RDMACCS-OpenEye/2")
        self.assertEqual(fps[0], b"000000000002080019c444eacd6c981baea178ef1f\t9425004")
        self.assertEqual(fps[1], b"000000002000082159d404eea968b81b8ea17eef1f\t9425009")
        self.assertEqual(fps[2], b"000000000000080159c404efa9689a1b8eb1faef1b\t9425012")
        self.assertEqual(fps[3], b"000000000000082019c404ee8968b81b8ea1ffef1f\t9425015")
        self.assertEqual(fps[4], b"000000000000088419c6b5fa8968981b8eb37aef1f\t9425018")

    def test_rdmaccs1_key44(self):
        header, output = runner.run_split("--rdmaccs/1", 7, source=MACCS_SMI)
        self.assertEqual(header[b"#type"], b"RDMACCS-OpenEye/1")
        hex_fp, id = output[0].split(b"\t")
        self.assertFalse(hex_contains_bit(hex_fp, 43))
        self.assertEqual(output[0], b"040000000000000000000000000000000000000000\t3->bit_2")
        
    def test_rdmaccs2_key44(self):
        header, output = runner.run_split("--rdmaccs/2", 7, source=MACCS_SMI)
        self.assertEqual(header[b"#type"], b"RDMACCS-OpenEye/2")
        hex_fp, id = output[0].split(b"\t")
        self.assertTrue(hex_contains_bit(hex_fp, 43))
        self.assertEqual(output[0], b"040000000008000000000000000000000000000000\t3->bit_2")
        #                   There's an 8 here ---^
    
    def test_both_rdmaccs_flags_gives_error(self):
        result = runner.run_exit("--rdmaccs/1 --rdmaccs/2")
        self.assertIn("Cannot specify both --rdmaccs and --rdmaccs/1", result)
        result = runner.run_exit("--rdmaccs --rdmaccs/1")
        self.assertIn("Cannot specify both --rdmaccs and --rdmaccs/1", result)
        runner.run_split("--rdmaccs --rdmaccs/2", 7, source=MACCS_SMI)
        
    def test_substruct(self):
        headers, fps = runner.run_split("--substruct", 19)
        self.assertEquals(headers["#type"], "ChemFP-Substruct-OpenEye/1")
        self.assertEquals(fps[0], "07de8d002000000000000000000000000080060000000c000000000000000080030000f8401800000030508379344c014956000055c0a44e2a0049200084e140581f041d661b10064483cb0f2925100619001393e10001007000000000008000000000000000400000000000000000\t9425004")
        # Note: not the same as OpenBabel's answer; bit 260 (>= 3 hetero-aromatic rings) is different.
        # openeye_patterns doesn't handle this.
        self.assertEquals(fps[1], "07de0d000000000000000000000000000080460300000c000000000000000080070000780038000000301083f920cc09695e0800d5c0e44e6e00492190844145dc1f841d261911164d039b8f29251026b9401313e0ec01007000000000000000000000000000000000000000000000\t9425009")

TestPatterns = unittest2.skipIf(skip_oechem, "OEChem not installed")(TestPatterns)

@unittest2.skipIf(skip_oechem, "OEChem not installed")
class TestIdAndErrors(unittest2.TestCase, support.TestIdAndErrors):
    _runner = runner
    toolkit = "openeye"

@unittest2.skipIf(skip_oechem, "OEChem not installed")
class TestIO(unittest2.TestCase, support.TestIO):
    _runner = runner
    def test_compressed_input(self):
        result = run_fps("", source=PUBCHEM_SDF_GZ)
### XXX Fix how I handle unknown extensions. 
#    def test_unknown_extension(self):
#        # OEChem's default assumes SMILES. This will parse some of the
#        # SD file lines as SMILES and skip the ones it doesn't know.
#        # The error output will have a bunch of warnings, starting
#        # with the "Unknown file format ... " warning, and then this
#        # string about a SMILES parse error.
#        try:
#            run("--errors ignore", source=PUBCHEM_ANOTHER_EXT)
#        except AssertionError, x:
#            self.assertEquals("Problem parsing SMILES" in str(x), True, str(x))
            
    def test_specify_input_format(self):
        result = run_fps("--in sdf", source=PUBCHEM_ANOTHER_EXT)


    def test_from_stdin(self):
        run_stdin("--in sdf", source=PUBCHEM_SDF)

    def test_from_gziped_stdin(self):
        run_stdin("--in sdf.gz", source=PUBCHEM_SDF_GZ)


# XXX how to test that this generates a warning?
#    def test_specify_input_format_with_dot(self):
#        result = run_fps("--in .sdf", source=PUBCHEM_ANOTHER_EXT)

class TestArgErrors(unittest2.TestCase):
    def _run(self, cmd, expect):
        msg = run_exit(cmd)
        self.assertIn(expect, msg)

    def test_two_fp_types(self):
        self._run("--maccs166 --path", "Cannot specify both --maccs166 and --path")

    def test_num_bits_too_small(self):
        self._run("--numbits 0", "between 16 and 65536 bits")
        self._run("--numbits 1", "between 16 and 65536 bits")
        self._run("--numbits 15", "between 16 and 65536 bits")

    def test_num_bits_too_large(self):
        self._run("--numbits 65537", "between 16 and 65536 bits")
        # Check for overflow, even though I know it won't happen in Python
        self._run("--numbits %(big)s"%dict(big=2**32+32), "between 16 and 65536 bits")

    def test_min_bonds_too_small(self):
        self._run("--minbonds=-1", "0 or greater")

    def test_min_bonds_larger_than_default_max_bonds(self):
        self._run("--minbonds=6", "--maxbonds must not be smaller than --minbonds")

    def test_min_bonds_too_large(self):
        self._run("--minbonds=4 --maxbonds=3",
                  "--maxbonds must not be smaller than --minbonds")

    def test_bad_atype(self):
        self._run("--atype spam", "Unknown path atom type 'spam'")

    def test_bad_atype2(self):
        self._run("--atype DefaultAtom|spam", "Unknown path atom type 'spam'")

    def test_bad_atype3(self):
        self._run("--atype DefaultAtom|", "Missing path atom flag")

    def test_bad_btype(self):
        self._run("--btype eggs", "Unknown path bond type 'eggs'")

    def test_bad_btype2(self):
        self._run("--btype DefaultBond|eggs", "Unknown path bond type 'eggs'")

    def test_bad_btype3(self):
        self._run("--btype DefaultBond|", "Missing path bond flag")

TestArgErrors = unittest2.skipIf(skip_oechem, "OEChem not installed")(TestArgErrors)

class TestHeaderOutput(unittest2.TestCase):
    def _field(self, s, field):
        try:
            result = run(s)
        except SystemExit, err:
            raise
            raise AssertionError("Should not die: %r" % (err,))
        filtered = [line for line in result if line.startswith(field)]
        self.assertEquals(len(filtered), 1, result)
        return filtered[0]

    def test_software(self):
        result = self._field("", "#software")
        self.assertEquals("#software=OEGraphSim/" in result, True, result)
        self.assertIn("(", result)
        self.assertIn(")", result)
        result = self._field("--maccs166", "#software")
        self.assertIn("#software=OEGraphSim/", result)

    def test_type(self):
        result = self._field("", "#type")
        self.assertEqual(result, 
                b"#type=OpenEye-Path/2 numbits=4096 minbonds=0 maxbonds=5 "
                b"atype=Arom|AtmNum|Chiral|EqHalo|FCharge|HvyDeg|Hyb btype=Order|Chiral")

    def test_default_atom_and_bond(self):
        result = self._field(
            "--atype=Arom|AtmNum|Chiral|EqHalo|FCharge|HvyDeg|Hyb "
            "--btype=Order|Chiral", b"#type")
        self.assertEqual(result,
            b"#type=OpenEye-Path/2 numbits=4096 minbonds=0 maxbonds=5 "
            b"atype=Arom|AtmNum|Chiral|EqHalo|FCharge|HvyDeg|Hyb btype=Order|Chiral")

        
    # different flags. All flags? and order
    def test_num_bits(self):
        result = self._field("--numbits 38", b"#num_bits")
        self.assertEqual(result, b"#num_bits=38")
        
    def test_atype_flags(self):
        result = self._field("--atype FCharge|FCharge", b"#type") + b" "
        self.assertIn(b" atype=FCharge ", result)
    
    def test_btype_flags(self):
        result = self._field("--btype Chiral|Order", b"#type") + b" "
        self.assertIn(b" btype=Order|Chiral ", result)
        result = self._field("--btype Order|Chiral", b"#type") + b" "
        self.assertIn(b" btype=Order|Chiral ", result)
    
    def test_pipe_or_comma(self):
        result = self._field("--atype HvyDeg,FCharge --btype Chiral,Order",
                             b"#type") + b" "
        self.assertIn(b" atype=FCharge|HvyDeg ", result)
        self.assertIn(b" btype=Order|Chiral ", result)
        
    def test_maccs_header(self):
        name = "OpenEye-MACCS166/" + chemfp.openeye._maccs_version
        result = self._field("--maccs166", b"#type")
        self.assertEqual(result, b"#type=" + name.encode("ascii"))
        
TestHeaderOutput = unittest2.skipIf(skip_oechem, "OEChem not installed")(TestHeaderOutput)


if has_oechem:
    from openeye.oegraphsim import (
        OEMakePathFP, OEFPAtomType_DefaultPathAtom, OEFPBondType_DefaultPathBond,
        OEMakeCircularFP, OEFPAtomType_DefaultCircularAtom, OEFPBondType_DefaultCircularBond,
        OEMakeTreeFP, OEFPAtomType_DefaultTreeAtom, OEFPBondType_DefaultTreeBond,
        OEFPAtomType_Aromaticity, OEFPAtomType_AtomicNumber, OEFPAtomType_EqHalogen,
        OEFPAtomType_HvyDegree, OEFPAtomType_FormalCharge,
        OEFPBondType_Chiral, OEFPBondType_InRing, OEFPBondType_BondOrder,
        )


class TestOEGraphSimVersion2(unittest2.TestCase):
    def test_hash(self):
        header, result = runner.run_split("--path", 19)
        self.assertEquals(header["#type"], "OpenEye-Path/2 numbits=4096 minbonds=0 maxbonds=5 atype=Arom|AtmNum|Chiral|EqHalo|FCharge|HvyDeg|Hyb btype=Order|Chiral")
        self.assertEquals(result, _construct_test_values())
        
    def test_path_defaults(self):
        header, result = runner.run_split("--path --numbits 4096 --minbonds 0 --maxbonds 5 "
                                          "--atype AtmNum|Arom|Chiral|FCharge|HvyDeg|Hyb|EqHalo --btype Order|Chiral", 19)
        self.assertEquals(header["#type"], "OpenEye-Path/2 numbits=4096 minbonds=0 maxbonds=5 atype=Arom|AtmNum|Chiral|EqHalo|FCharge|HvyDeg|Hyb btype=Order|Chiral")
        self.assertEquals(result, _construct_test_values())

    def test_change_all_path_fields(self):
        header, result = runner.run_split("--path --numbits 1024 --minbonds 2 --maxbonds 4 "
                                          "--atype AtmNum|EqHalo --btype InRing|Order", 19)
        self.assertEquals(header["#type"], "OpenEye-Path/2 numbits=1024 minbonds=2 maxbonds=4 atype=AtmNum|EqHalo btype=Order|InRing")
        def compute_path_fingerprints(fp, mol):
            OEMakePathFP(fp, mol, 1024, 2, 4,
                         OEFPAtomType_AtomicNumber|OEFPAtomType_EqHalogen,
                         OEFPBondType_InRing|OEFPBondType_BondOrder)
        self.assertEquals(result, _construct_test_values(compute_path_fingerprints, 1024))
        
    def test_path_default_type(self):
        result = run("--atype DefaultPathAtom") # (DefaultPathAtom is the same as DefaultAtom)
        typename = [line for line in result if line.startswith("#type=")][0]
        self.assertEquals(typename, "#type=OpenEye-Path/2 numbits=4096 minbonds=0 maxbonds=5 atype=Arom|AtmNum|Chiral|EqHalo|FCharge|HvyDeg|Hyb btype=Order|Chiral")

    def test_check_path_default_types(self):
        header, result = runner.run_split("--path --atype Default --btype Default")
        self.assertEquals(header["#type"],
              "OpenEye-Path/2 numbits=4096 minbonds=0 maxbonds=5 atype=Arom|AtmNum|Chiral|EqHalo|FCharge|HvyDeg|Hyb btype=Order|Chiral")
        header, result = runner.run_split("--path --atype DefaultCircularAtom --btype DefaultCircularBond")
        self.assertEquals(header["#type"],
              "OpenEye-Path/2 numbits=4096 minbonds=0 maxbonds=5 atype=Arom|AtmNum|Chiral|EqHalo|FCharge|HCount btype=Order")
        header, result = runner.run_split("--path --atype DefaultPathAtom --btype DefaultPathBond")
        self.assertEquals(header["#type"],
              "OpenEye-Path/2 numbits=4096 minbonds=0 maxbonds=5 atype=Arom|AtmNum|Chiral|EqHalo|FCharge|HvyDeg|Hyb btype=Order|Chiral")


    ########################
    # Note: The documentation says that OEFPBondType_DefaultCircularBond is Order|Chiral
    # but the code says it's only Order.
        
    def test_circular(self):
        header, result = runner.run_split("--circular", 19)
        def compute_circular_fingerprints(fp, mol):
            OEMakeCircularFP(fp, mol, 4096, 0, 5,
                             OEFPAtomType_DefaultCircularAtom, OEFPBondType_DefaultCircularBond)
        self.assertEquals(header["#type"], "OpenEye-Circular/2 numbits=4096 minradius=0 maxradius=5 atype=Arom|AtmNum|Chiral|EqHalo|FCharge|HCount btype=Order")
        self.assertEquals(result, _construct_test_values(compute_circular_fingerprints))

    def test_circular_defaults(self):
        # Make sure that when I specify the defaults then I get the same results
        header, result = runner.run_split("--circular --numbits 4096 --minradius 0 --maxradius 5 "
                                          "--atype AtmNum|Arom|Chiral|FCharge|HCount|EqHalo --btype Order")
        self.assertEquals(header["#type"], "OpenEye-Circular/2 numbits=4096 minradius=0 maxradius=5 atype=Arom|AtmNum|Chiral|EqHalo|FCharge|HCount btype=Order")
                
        def compute_circular_fingerprints(fp, mol):
            OEMakeCircularFP(fp, mol, 4096, 0, 5,
                             OEFPAtomType_DefaultCircularAtom, OEFPBondType_DefaultCircularBond)
        self.assertEquals(result, _construct_test_values(compute_circular_fingerprints))

    def test_change_all_circular_fields(self):
        header, result = runner.run_split("--circular --numbits 1024 --minradius 2 --maxradius 4 --atype Arom --btype Chiral", 19)
        def compute_circular_fingerprints(fp, mol):
            OEMakeCircularFP(fp, mol, 1024, 2, 4,
                             OEFPAtomType_Aromaticity, OEFPBondType_Chiral)
        self.assertEquals(header["#type"],
              "OpenEye-Circular/2 numbits=1024 minradius=2 maxradius=4 atype=Arom btype=Chiral")
        self.assertEquals(result, _construct_test_values(compute_circular_fingerprints, 1024))

    def test_check_circular_default_types(self):
        header, result = runner.run_split("--circular --atype Default --btype Default")
        self.assertEquals(header["#type"],
              "OpenEye-Circular/2 numbits=4096 minradius=0 maxradius=5 atype=Arom|AtmNum|Chiral|EqHalo|FCharge|HCount btype=Order")
        header, result = runner.run_split("--circular --atype DefaultCircularAtom --btype DefaultCircularBond")
        self.assertEquals(header["#type"],
              "OpenEye-Circular/2 numbits=4096 minradius=0 maxradius=5 atype=Arom|AtmNum|Chiral|EqHalo|FCharge|HCount btype=Order")
        header, result = runner.run_split("--circular --atype DefaultPathAtom --btype DefaultPathBond")
        self.assertEquals(header["#type"],
              "OpenEye-Circular/2 numbits=4096 minradius=0 maxradius=5 atype=Arom|AtmNum|Chiral|EqHalo|FCharge|HvyDeg|Hyb btype=Order|Chiral")


    ########################

    def test_tree(self):
        header, result = runner.run_split("--tree", 19)
        self.assertEquals(header["#type"], "OpenEye-Tree/2 numbits=4096 minbonds=0 maxbonds=4 atype=Arom|AtmNum|Chiral|FCharge|HvyDeg|Hyb btype=Order")
        def compute_tree_fingerprints(fp, mol):
            OEMakeTreeFP(fp, mol, 4096, 0, 4,
                         OEFPAtomType_DefaultTreeAtom, OEFPBondType_DefaultTreeBond)
        self.assertEquals(result, _construct_test_values(compute_tree_fingerprints))
    
    def test_tree_defaults(self):
        # Make sure that when I specify the defaults then I get the same results
        header, result = runner.run_split("--tree --numbits 4096 --minradius 0 --maxradius 5 "
                                          "--atype FCharge|HvyDeg|AtmNum|Arom|Chiral|Hyb --btype Order")
        self.assertEquals(header["#type"], "OpenEye-Tree/2 numbits=4096 minbonds=0 maxbonds=4 atype=Arom|AtmNum|Chiral|FCharge|HvyDeg|Hyb btype=Order")
        def compute_tree_fingerprints(fp, mol):
            OEMakeTreeFP(fp, mol, 4096, 0, 4,
                         OEFPAtomType_DefaultTreeAtom, OEFPBondType_DefaultTreeBond)
        self.assertEquals(result, _construct_test_values(compute_tree_fingerprints))

    
    def test_change_all_tree_fields(self):
        header, result = runner.run_split("--tree --numbits 1024 --minbonds 1 --maxbonds 2 --atype HvyDeg|FCharge --btype InRing", 19)
        def compute_circular_fingerprints(fp, mol):
            OEMakeTreeFP(fp, mol, 1024, 1, 2,
                         OEFPAtomType_HvyDegree | OEFPAtomType_FormalCharge, OEFPBondType_InRing)
        self.assertEquals(header["#type"],
              "OpenEye-Tree/2 numbits=1024 minbonds=1 maxbonds=2 atype=FCharge|HvyDeg btype=InRing")
        self.assertEquals(result, _construct_test_values(compute_circular_fingerprints, 1024))
    
if skip_oechem:
    TestOEGraphSimVersion2 = unittest2.skipIf(skip_oechem, "OEChem not installed")(TestOEGraphSimVersion2)
        
if __name__ == "__main__":
    unittest2.main()

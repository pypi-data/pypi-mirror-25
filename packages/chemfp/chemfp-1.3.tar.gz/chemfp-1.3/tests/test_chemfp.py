import unittest2
import re
import os
import sys
from cStringIO import StringIO

import chemfp
import _chemfp
from chemfp import __version__ as chemfp_version

version_pattern = re.compile(r"\d+\.\d+(\.\d)?((a|b|p)\d+)?$")

class SystemTests(unittest2.TestCase):
    def test_version(self):
        m = version_pattern.match(_chemfp.version())
        self.assertNotEqual(m, None, "bad version: %s" % (_chemfp.version(),))


skip_omp = (chemfp.get_max_threads() == 1)

class OpenMPTests(unittest2.TestCase):
    def setUp(self):
        self._num_threads = chemfp.get_num_threads()
    def tearDown(self):
        chemfp.set_num_threads(self._num_threads)

    def test_num_threads_is_max_threads(self):
        self.assertEquals(chemfp.get_num_threads(), chemfp.get_max_threads())

    def test_set_to_zero(self):
        chemfp.set_num_threads(0)
        self.assertEquals(chemfp.get_num_threads(), 1)

    def test_set_to_one(self):
        chemfp.set_num_threads(1)
        self.assertEquals(chemfp.get_num_threads(), 1)

    def test_set_to_two(self):
        chemfp.set_num_threads(2)
        self.assertEquals(chemfp.get_num_threads(), 2)
    test_set_to_two = unittest2.skipIf(skip_omp, "Multiple OMP threads not available")(
        test_set_to_two)

    def test_set_to_max(self):
        chemfp.set_num_threads(chemfp.get_max_threads())
        self.assertEquals(chemfp.get_num_threads(), chemfp.get_max_threads())

    def test_set_beyond_max(self):
        chemfp.set_num_threads(chemfp.get_max_threads()+1)
        self.assertEquals(chemfp.get_num_threads(), chemfp.get_max_threads())

class SaveVersionStdout(object):
    def __init__(self, module, file):
        self.module = module
        self.prog = module.__name__
        self.file = file
        
    def __enter__(self):
        self.real_stdout = sys.stdout
        self.real_prog = self.module.parser.prog
        self.module.parser.prog = self.prog
        sys.stdout = self.file
    
    def __exit__(self, type, value, traceback):
        sys.stdout = self.real_stdout
        self.module.parser.prog = self.prog
        if issubclass(type, SystemExit):
            if value.code:
                self.file.write("I don't think you expected a %r" % (value,))
            return True
        
# Check that all of the command-line tools save a version to stdout
class CommandlineVersionTest(unittest2.TestCase):
    def check_version(self, module):
        f = StringIO()
        with SaveVersionStdout(module, f):
            module.main(args=["--version"])
        output = f.getvalue()
        expected_output = module.__name__ + " " + chemfp_version + "\n"
        self.assertEqual(output, expected_output)

    def test_simsearch(self):
        from chemfp.commandline import simsearch
        self.check_version(simsearch)
        
    def test_oe2fps(self):
        try:
            import openeye.oechem
        except ImportError:
            return
        
        from chemfp.commandline import oe2fps
        self.check_version(oe2fps)
        
    def test_rdkit2fps(self):
        try:
            import rdkit
        except ImportError:
            return
        from chemfp.commandline import rdkit2fps
        self.check_version(rdkit2fps)
        
    def test_ob2fps(self):
        try:
            import openbabel
        except ImportError:
            return
        from chemfp.commandline import ob2fps
        self.check_version(ob2fps)
        
    def test_sdf2fps(self):
        from chemfp.commandline import sdf2fps
        self.check_version(sdf2fps)
        
if __name__ == "__main__":
    unittest2.main()

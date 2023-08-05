# This tests that the tox environment is set up the way it should be
# set up, and that the available toolkits matches the environment.

import sys
import os
import unittest2

import support
import chemfp

envstr = os.environ.get("TOX_CHEMFP_TEST", None)
if not envstr:
    versions = []
else:
    versions = envstr.split(",")

def check_py27():
    version = sys.version_info[:2]
    assert version == (2,7), version
    assert not support.can_skip("py27")
    
def check_py35():
    version = sys.version_info[:2]
    assert version == (3,5), version
    assert not support.can_skip("py35")

### I no longer have a 32-bit test environment.
## def check_x32():
##     assert sys.maxint == 2147483647
##     assert not support.can_skip("x32")

def check_x64():
    # sys.maxint doesn't exist under Python 3.
    if sys.version_info[0] == 2:
        assert sys.maxint == 9223372036854775807
    assert not support.can_skip("x64")

## def check_oe174():
##     from openeye.oechem import OEChemGetRelease
##     version = OEChemGetRelease()
##     assert version == "1.7.4", version
##     assert not support.can_skip("oe")
##     assert not support.can_skip("oe174")
    

## def check_oe2011Oct():
##     from openeye.oechem import OEChemGetRelease
##     version = OEChemGetRelease()
##     assert version == "1.7.6", version
##     assert not support.can_skip("oe")
##     assert not support.can_skip("oe2011Oct")

## def check_oe2013Jun4():
##     from openeye.oechem import OEChemGetRelease
##     version = OEChemGetRelease()
##     assert version == "1.9.2", version
##     assert not support.can_skip("oe")
##     assert not support.can_skip("oe2013Jun4")

def check_oe20140707():
    from openeye.oechem import OEChemGetRelease
    version = OEChemGetRelease()
    assert version == "2.0.1", version
    assert not support.can_skip("oe")
    assert not support.can_skip("oe20140707")

def check_oe20161001():
    from openeye.oechem import OEChemGetRelease
    version = OEChemGetRelease()
    assert version == "2.1.0", version
    assert not support.can_skip("oe")
    assert not support.can_skip("oe20161001")

def check_oe201710b2():
    from openeye.oechem import OEChemGetRelease
    version = OEChemGetRelease()
    assert version == "2.1.3.b.2 debug", version
    assert not support.can_skip("oe")
    assert not support.can_skip("oe201710b2")


def check_ob230():
    import openbabel
    from chemfp import openbabel as _openbabel_toolkit
    assert _openbabel_toolkit._ob_version == "2.3.0", openbabel._ob_version
    assert not support.can_skip("ob")
    assert not support.can_skip("ob230")

## def check_ob23svn1():
##     import openbabel
##     from chemfp import _openbabel_toolkit
##     assert _openbabel_toolkit._ob_version == "2.3.90", openbabel._ob_version
##     assert not support.can_skip("ob")
##     assert not support.can_skip("ob23svn1")

def check_ob241():
    import openbabel
    from chemfp import openbabel as _openbabel_toolkit
    assert _openbabel_toolkit._ob_version == "2.4.1", openbabel._ob_version
    assert not support.can_skip("ob")
    assert not support.can_skip("ob241")

# It was hard ensure the pattern version were correct.
def check_rd201303():
    import rdkit.rdBase
    from rdkit.rdBase import rdkitVersion
    assert rdkitVersion[:7] == "2013.03", rdkitVersion

    from chemfp.rdkit import PATTERN_VERSION
    assert PATTERN_VERSION == "1", PATTERN_VERSION
    
def check_rd201609():
    import rdkit.rdBase
    from rdkit.rdBase import rdkitVersion
    assert rdkitVersion[:7] == "2016.09", rdkitVersion

    from chemfp.rdkit import PATTERN_VERSION
    assert PATTERN_VERSION == "2", PATTERN_VERSION
    
def check_rd201703():
    import rdkit.rdBase
    from rdkit.rdBase import rdkitVersion
    assert rdkitVersion == "2017.03.3", rdkitVersion

    from chemfp.rdkit import PATTERN_VERSION
    assert PATTERN_VERSION == "3", PATTERN_VERSION
    
def check_rd201709_dev():
    import rdkit.rdBase
    from rdkit.rdBase import rdkitVersion
    assert rdkitVersion == "2017.09.1.dev1", rdkitVersion

    from chemfp.rdkit import PATTERN_VERSION
    assert PATTERN_VERSION == "4", PATTERN_VERSION
    

def _check(required):
    req = required.split()
    for name in versions:
        if name in req:
            return
    raise AssertionError("Missing one of %r: %r" % (required, versions))

class TestToxVersion(unittest2.TestCase):
    def test_enough_specifications(self):
        _check("x64")
        _check("py27 py35")
        _check("ob241 rd201303 rd201609 oe20140707 oe20161001 oe201710b2 rd201703 rd201709_dev")
        
    def test_version(self):
        for name in versions:
            func = globals()["check_" + name]
            func()

TestToxVersion = unittest2.skipUnless(envstr, "Not building under the tox environment")(
    TestToxVersion)

if __name__ == "__main__":
    unittest2.main()

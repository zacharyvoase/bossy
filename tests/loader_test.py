import os
import shutil
import tempfile

from bossy import loader


## Fixture
# Creates a temporary directory to hold bossfiles.

oldcwd = os.getcwd()
tempdir = None


def setup():
    global tempdir
    tempdir = tempfile.mkdtemp()
    os.chdir(tempdir)

def teardown():
    os.chdir(oldcwd)
    shutil.rmtree(tempdir)


## Tests

def test_modules_have_a_scope():
    with open(os.path.join(tempdir, 'Bossfile'), 'w') as fp:
        fp.write('\n'.join((
            "x = 5",
            "def func():",
            "    return x",
            "")))
    mod = loader.load_module('bossfile', os.path.join(tempdir, 'Bossfile'))
    assert mod.func() == 5

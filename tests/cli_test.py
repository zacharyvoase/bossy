import os
import shutil
import subprocess
import sys
import tempfile


## Fixture
# Creates a temporary directory to hold bossfiles.

oldcwd = os.getcwd()
tempdir = None


def run_boss(*args):
    p = subprocess.Popen(
        ['python', '-m', 'boss.main'] + list(args),
        executable=sys.executable, cwd=tempdir,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = p.communicate()
    return (p.returncode, stdout)


def setup():
    global tempdir
    tempdir = tempfile.mkdtemp()
    os.chdir(tempdir)

def teardown():
    os.chdir(oldcwd)
    shutil.rmtree(tempdir)


## Tests

def test_bad_bossfile_causes_error():
    with open('Bossfile.error', 'w') as bf:
        bf.write("""raise Exception\n""")

    rc, output = run_boss('-f', 'Bossfile.error', 'command')
    assert rc != 0
    assert 'Traceback' in output


def test_can_get_help_with_bad_bossfile():
    with open('Bossfile.error', 'w') as bf:
        bf.write("""raise Exception\n""")

    rc, output = run_boss('-f', 'Bossfile.error', '-h')
    assert rc == 0


def test_non_existent_bossfile_causes_error():
    rc, output = run_boss('command', 'arg1')
    assert rc != 0
    assert 'locate the Bossfile' in output


def test_can_get_help_with_non_existent_bossfile():
    rc, output = run_boss('--help')
    assert rc == 0


def test_can_run_commands_with_valid_bossfile():
    with open('Bossfile', 'w') as bf:
        bf.write('\n'.join((
            "from boss import *",
            "@command",
            "def hello():",
            "    print 123456",
            "")))

    rc, output = run_boss('hello')
    assert rc == 0
    assert '123456' in output


def test_can_run_commands_with_arguments():
    with open('Bossfile', 'w') as bf:
        bf.write('\n'.join((
            "from boss import *",
            "@command",
            "@argument('-r', '--repetitions', type=int)",
            "def hello_n(repetitions):",
            "    for i in xrange(repetitions):",
            "        print 123456",
            "")))

    rc, output = run_boss('hello_n', '-r', '3')
    assert rc == 0
    assert output.split() == ['123456'] * 3

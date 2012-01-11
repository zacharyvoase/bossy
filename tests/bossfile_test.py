from boss.bossfile import Bossfile
from boss.commands import Command


def make_bossfile_mod():
    class TestMod(object):
        pass
    mod = TestMod()
    mod.__file__ = '/tmp/Bossfile'
    return mod


def test_bossfile_can_filter_out_defined_commands():
    bossfile_mod = make_bossfile_mod()
    # Commands
    bossfile_mod.foo = Command(lambda: 123, name='foo')
    bossfile_mod.bar = Command(lambda: 456, name='bar')
    bossfile_mod.baz = Command(lambda: 789, name='baz')
    # Scalar values
    bossfile_mod.spam = object()
    bossfile_mod.ham = 123
    bossfile_mod.eggs = 'abc'

    bossfile = Bossfile(bossfile_mod)

    assert bossfile.commands() == {'foo': bossfile_mod.foo,
                                   'bar': bossfile_mod.bar,
                                   'baz': bossfile_mod.baz}

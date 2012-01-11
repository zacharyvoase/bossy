import errno
import os
import sys
import types


class BossfileLoadingError(Exception):
    """An exception occurred when loading the Bossfile."""

    exc_type = property(lambda self: self.args[0])
    exc_value = property(lambda self: self.args[1])
    exc_traceback = property(lambda self: self.args[2])


class BossfileNotFound(BossfileLoadingError):
    """Couldn't find the Bossfile at the specified location."""
    pass


def load_module(name, filename, install=True):
    """Load a Python module from a filename."""

    mod = types.ModuleType(name)
    mod.__file__ = filename
    execfile(filename, globals(), mod.__dict__)
    if install:
        sys.modules[name] = mod
    return mod


def load_bossfile_module(location=None):

    """
    Load a Bossfile module, with an optional explicit location.

    If no location is provided, a file called ``Bossfile`` in the current
    directory will be used. If the name of a directory is provided, a file
    called ``Bossfile`` in that directory will be used. Otherwise the location
    is treated as the path to the file itself.
    """

    if location is None:
        location = os.path.join(os.getcwdu(), 'Bossfile')
    elif os.path.isdir(location):
        location = os.path.join(location, 'Bossfile')

    try:
        bossfile_mod = load_module('bossfile', location)
    except IOError, exc:
        if exc.errno == errno.ENOENT:
            raise BossfileNotFound(*sys.exc_info())
        raise BossfileLoadingError(*sys.exc_info())
    except Exception, exc:
        raise BossfileLoadingError(*sys.exc_info())

    return bossfile_mod

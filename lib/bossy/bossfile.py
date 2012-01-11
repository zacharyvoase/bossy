from bossy import loader
from bossy.commands import Command


class Bossfile(object):

    """A Bossfile."""

    NotFound = loader.BossfileNotFound
    LoadingError = loader.BossfileLoadingError

    def __init__(self, bossfile_mod):
        self.mod = bossfile_mod
        self.filename = self.mod.__file__

    def command(self, command_name):
        """Retrieve a :class:`Command` instance, given its name."""

        return self.commands()[command_name]

    def commands(self):
        """Get a dictionary of command names -> :class:`Command` instances."""

        commands = {}
        for name, value in vars(self.mod).iteritems():
            if isinstance(value, Command):
                commands[value.name] = value
        return commands

    def install(self, sub_parsers):

        """
        Install the commands from this Bossfile on a subparser group.

        Returns a dictionary of command names -> command subparsers.
        """

        sub_parser_names = {}
        for name, command in self.commands().iteritems():
            sub_parser_names[name] = command.install(sub_parsers)
        return sub_parser_names

    @classmethod
    def load(cls, location=None):
        """Load a :class:`Bossfile`, optionally with an explicit location."""

        return cls(loader.load_bossfile_module(location=location))

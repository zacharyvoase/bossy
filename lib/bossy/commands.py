class Command(object):

    """Wraps a Python function and exposes it as a Bossy command."""

    def __init__(self, function, **opts):
        self.function = function
        self.name = opts.pop('name', function.__name__)
        self.opts = opts

        doc = getattr(function, '__doc__', '') or ''
        self.opts.setdefault('description', doc)
        self.opts.setdefault('help', (doc.lstrip('\r\n') or '\n').splitlines()[0])

        self.opts.setdefault('prog', 'bossy %s' % (self.name,))

        self.arguments = getattr(function, 'arguments', [])

    def __call__(self, *args, **kwargs):
        kwargs.pop('__func', None)
        return self.function(*args, **kwargs)

    def add_argument(self, *args, **kwargs):
        self.arguments.append((args, kwargs))

    def install(self, sub_parsers):

        """
        Install this command on an ``argparse`` subparser group.

        Returns the command's subparser.
        """

        sub_parser = sub_parsers.add_parser(self.name,
                                            **self.opts)
        for args, kwargs in self.arguments:
            sub_parser.add_argument(*args, **kwargs)
        sub_parser.set_defaults(__func=self)
        return sub_parser


def command(*args, **kwargs):

    """
    Decorate a function as a command.

    Allows both optionless declaration:

        @command
        def implicit_name():
            pass
        assert isinstance(implicit_name, Command)

    And declaration with options:

        @command(name='explicit_name')
        def function():
            pass
        assert isinstance(function, Command)
        assert function.name == 'explicit_name'
    """

    def make_command_instance(*args):
        return Command(*args, **kwargs)
    if args:
        return make_command_instance(*args)
    return make_command_instance


def argument(*args, **kwargs):
    def decorator(func):
        if not hasattr(func, 'arguments'):
            func.arguments = []
        func.arguments.insert(0, (args, kwargs))
        return func
    return decorator

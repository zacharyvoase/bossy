import argparse
import pdb
import sys
import traceback

import pkg_resources

from bossy.bossfile import Bossfile


def get_version(pkg_name):
    req = pkg_resources.Requirement.parse(pkg_name)
    return pkg_resources.working_set.find(req).version


parser = argparse.ArgumentParser(
    prog='bossy',
    description="Run commands from a Bossfile.",
    usage='bossy [-h|-v|-f BOSSFILE] <command> ...',
    add_help=False)
global_opts = parser.add_argument_group('global options')
global_opts.add_argument('-f', '--file', metavar='BOSSFILE',
                         default='Bossfile',
                         help="Location of an alternative Bossfile to use. "
                         "By default, bossy will look for a file called "
                         "'Bossfile' in the current directory.")
global_opts.add_argument('--pdb', action='store_true', default=False,
                         help="Launch the Python Debugger on uncaught "
                         "exceptions.")
global_opts.add_argument('-v', '--version', action='version',
                         version='bossy ' + get_version('bossy'))


def add_help(parser):
    """Add a help option to a parser afterwards."""

    parser.add_argument('-h', '--help', action='help',
                        default=argparse.SUPPRESS,
                        help='show this help message and exit')


def select_args(parsed_args, subparser):
    selected_args = {}
    for action in subparser._actions:
        if getattr(action, 'dest', None) in parsed_args:
            selected_args[action.dest] = getattr(parsed_args, action.dest)
    return selected_args


def main(args=None):
    pre_args, remaining_args = parser.parse_known_args()
    if pre_args.pdb:
        sys.excepthook = lambda *exc_info: pdb.pm()

    try:
        bossfile = Bossfile.load(pre_args.file)
    except Bossfile.LoadingError, exc:
        add_help(global_opts)
        # This will catch any -h/--help options.
        parser.parse_known_args(remaining_args)

        if isinstance(exc, Bossfile.NotFound):
            parser.error("Couldn't locate the Bossfile in the current directory.")

        error = "Error occurred loading the Bossfile:\n"
        for line in traceback.format_exception(*exc.args):
            error += "  " + line
        parser.error(error)

    subparsers = parser.add_subparsers(title='sub-commands',
                                       metavar='<command>')
    subparser_names = bossfile.install(subparsers)
    add_help(global_opts)
    args = parser.parse_args(remaining_args)
    selected_args = select_args(args, subparser_names[args.__func.name])
    args.__func(**selected_args)


if __name__ == '__main__':
    main()

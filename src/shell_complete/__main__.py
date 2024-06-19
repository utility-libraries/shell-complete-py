#!/usr/bin/env python3
# -*- coding=utf-8 -*-
r"""

"""
import sys
import importlib
import argparse as ap
from . import __description__, __version__, ShellCompleteAction, generate, types


parser = ap.ArgumentParser(prog='shell-complete', description=__description__)
parser.epilog = ("Note: to specify the parser for an executable module use the format"
                 " 'module[.submodule].__main__[:variable]'.\n"
                 "Try it for shell-complete with 'python3 -m shell-complete shell_complete.__main__:parser'")
parser.add_argument('-v', '--version', action='version', version=__version__)
parser.add_argument('--completion', action=ShellCompleteAction,
                    help="generate a shell-completion for this CLI")
parser.add_argument('--root', default=".", type=types.directory,
                    help="Root directory to search the module in")
parser.add_argument('parser', type=types.file,
                    help="Entrypoint-Specification to the parser."
                         "(Format: 'module[.submodule][:variable]')")


def main():
    args = vars(parser.parse_args())
    modname, qualname_seperator, qualname = args['parser'].partition(':')
    sys.path.insert(0, args['root'])
    try:
        module = importlib.import_module(modname)
    except ModuleNotFoundError as error:
        print(f"Could not import {modname!r} ({error!s})", file=sys.stderr)
        return 1
    finally:
        sys.path.pop(0)
    if qualname_seperator:
        try:
            module_parser = getattr(module, qualname)
        except KeyError as error:
            print(f"Failed to get parser {qualname!r} ({error!s})", file=sys.stderr)
            return 1
    else:
        module_parser = next((v for v in vars(module).values() if isinstance(v, ap.ArgumentParser)), None)
        if module_parser is None:
            print(f"Failed to auto-detect parser for {modname!r}", file=sys.stderr)
            return 1
    print(generate(module_parser))
    return 0


if __name__ == '__main__':
    sys.exit(main())

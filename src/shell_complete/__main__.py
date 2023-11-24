#!/usr/bin/env python3
# -*- coding=utf-8 -*-
r"""

"""
import argparse as ap
import sys
from . import __description__, __version__, ActionShellComplete


parser = ap.ArgumentParser(prog='shell-complete', description=__description__)
parser.add_argument('-v', '--version', action='version', version=__version__)
parser.add_argument('--completion', action=ActionShellComplete,
                    help="generate a shell-completion for this CLI")

arguments = parser.parse_args()


def main():
    print("Currently under development")
    return 0


if __name__ == '__main__':
    sys.exit(main())

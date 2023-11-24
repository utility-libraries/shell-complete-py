# -*- coding=utf-8 -*-
r"""

"""
import argparse as ap
from ..core import generate


class ActionShellComplete(ap.Action):
    def __init__(self, option_strings, dest, help=None):
        super().__init__(option_strings, dest=ap.SUPPRESS, nargs=0, help=help)

    def __call__(self, parser: ap.ArgumentParser, namespace: ap.Namespace, values, option_string=None):
        print([namespace, values, option_string])
        print(generate(parser))
        parser.exit()

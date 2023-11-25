# -*- coding=utf-8 -*-
r"""

"""
import argparse as ap
from ..core import generate


class ActionShellComplete(ap.Action):
    # noinspection PyShadowingBuiltins
    def __init__(self, option_strings, dest, help=None):
        super().__init__(option_strings, dest=ap.SUPPRESS, nargs=0, help=help)

    # (parser, namespace, values, option_string)
    # but we only need `parser`
    def __call__(self, parser: ap.ArgumentParser, *_, **__):
        print(generate(parser))
        parser.exit()

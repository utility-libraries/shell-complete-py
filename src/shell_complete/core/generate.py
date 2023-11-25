# -*- coding=utf-8 -*-
r"""

"""
import argparse as ap
from ._writer import BashWriter


def generate(parser: ap.ArgumentParser) -> str:
    writer = BashWriter()

    return str(writer)

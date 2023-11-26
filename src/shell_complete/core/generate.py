# -*- coding=utf-8 -*-
r"""

"""
import argparse as ap
from ._writer import BashWriter


__all__ = ['generate']


def generate(parser: ap.ArgumentParser, program: str) -> str:
    writer = BashWriter(program)

    return str(writer)

# -*- coding=utf-8 -*-
r"""

"""
import io
import argparse as ap


def generate(parser: ap.ArgumentParser) -> str:
    stream = io.StringIO()
    write = stream.write
    write("#!/usr/bin/env bash")

    return stream.getvalue()

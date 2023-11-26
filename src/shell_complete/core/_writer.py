# -*- coding=utf-8 -*-
r"""

"""
import io


class BashWriter:
    def __init__(self, program: str):
        self._program = program
        self.stream = io.StringIO()
        self.indentation = 0
        self("#!/usr/bin/env bash")
        self()

    def __str__(self):
        return self.stream.getvalue()

    def __call__(self, line: str = "\n", *args, **kwargs):
        self.stream.write(('  ' * self.indentation) + line.format(*args, **kwargs))

    def __enter__(self):
        self.indentation += 1

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.indentation -= 1

# -*- coding=utf-8 -*-
r"""

"""
import io
import typing as t
import contextlib
from shlex import quote
from functools import cached_property


__all__ = ['BashWriter', 'quote']


class BashWriter:
    def __init__(self, program: str):
        self._program = program
        self._indentation = 0
        self.stream = io.StringIO()

    @cached_property
    def safe_program(self):
        import re
        return re.sub(r'\W', '_', self._program)

    def __str__(self):
        return self.stream.getvalue()

    def __call__(self, line: str = "", *, xend="\n"):
        self.stream.write(('  ' * self._indentation) + line + xend)

    @contextlib.contextmanager
    def indent(self) -> t.ContextManager:
        self._indentation += 1
        try:
            yield
        finally:
            self._indentation -= 1

    def __enter__(self):
        # adds the head
        self(fr'#!/usr/bin/env bash')
        self()
        self(fr'__{self.safe_program} () {{')
        self._indentation += 1

    def __exit__(self, exc_type, exc_val, exc_tb):
        # adds the tail
        self._indentation -= 1
        self(fr'}}')
        self()
        self(fr'# complete is a bash builtin, but recent versions of ZSH come with a function')
        self(fr'# called bashcompinit that will create a complete in ZSH. If the user is in')
        self(fr'# ZSH, load and run bashcompinit before calling the complete function.')
        self(fr'if [[ -n ${{ZSH_VERSION-}} ]]; then')
        with self.indent():
            self(r'autoload -U +X bashcompinit && bashcompinit')
            self(r'autoload -U +X compinit && compinit')
        self(fr'fi')
        self(fr'')
        self(fr'complete -o default -F __{self.safe_program} {quote(self._program)}')

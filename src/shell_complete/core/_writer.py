# -*- coding=utf-8 -*-
r"""

"""
import io
import textwrap
import typing as t
import contextlib
from shlex import quote
from functools import cached_property


__all__ = ['BashWriter', 'quote']


class BashWriter:
    def __init__(self, program: str):
        self._program = program
        self._indentation = 0
        self._stream = io.StringIO()

    @cached_property
    def _safe_program(self) -> str:
        import re
        return re.sub(r'\W', '_', self._program)

    @cached_property
    def _complete_function(self) -> str:
        return f"__{self._safe_program}_completions"

    def __str__(self):
        return self._stream.getvalue()

    def __call__(self, *parts, sep=" ", end="\n"):
        self._stream.write(('  ' * self._indentation) + sep.join(parts) + end)

    @contextlib.contextmanager
    def indent(self) -> t.ContextManager:
        self._indentation += 1
        try:
            yield
        finally:
            self._indentation -= 1

    def __enter__(self):
        # adds the head
        self('#!/usr/bin/env bash')
        self.comment_block(
            "=Generated with shell-complete",
            "-----",
            "https://pypi.org/project/shell-complete/",
            "https://github.com/utility-libraries/shell-complete-py",
        )
        self()
        self('if ! command -v', self._program, '&> /dev/null; then')
        with self.indent():
            self('return')
        self('fi')
        self()
        self(self._complete_function, '() {')
        self._indentation += 1
        self('local CURRENT=${COMP_WORDS[$COMP_CWORD]}')
        self('local LAST=${COMP_WORDS[$((COMP_CWORD - 1))]}')
        self('local LINE=${COMP_LINE}')
        self()

    def __exit__(self, exc_type, exc_val, exc_tb):
        # adds the tail
        self._indentation -= 1
        self('}')
        self()
        self.comment("complete is a bash builtin, but recent versions of ZSH come with a function called bashcompinit "
                     "that will create a complete in ZSH. If the user is in ZSH, load and run bashcompinit before "
                     "calling the complete function.")
        self('if [[ -n ${ZSH_VERSION-} ]]; then')
        with self.indent():
            self('autoload -U +X bashcompinit && bashcompinit')
            self('autoload -U +X compinit && compinit')
        self('fi')
        self()
        self('complete -F', self._complete_function, self._program)

    def comment(self, *lines):
        width = 80 - self._indentation*2 - 2
        for line in lines:
            for wrapped in textwrap.wrap(line, width):
                self('# ' + wrapped)

    def comment_block(self, *lines):
        width = 80 - (self._indentation * 2) - 2 - 2
        self('#' * (width + 4))
        for line in lines:
            if line.startswith(3*'='):
                self('# ' + '=' * width + ' #')
            elif line.startswith(3*'-'):
                self('# ' + '-' * width + ' #')
            elif line.startswith("="):
                self('# ' + line[1:].center(width) + ' #')
            else:
                for wrapped in textwrap.wrap(line, width):
                    self('# ' + wrapped.ljust(width) + ' #')
        self('#' * (width + 4))

    @contextlib.contextmanager
    def switch(self, variable: str):
        self('case', variable, 'in')
        try:
            yield
        finally:
            self('esac')

    @contextlib.contextmanager
    def case(self, *patterns: str):
        self('|'.join(patterns) + ')')
        self._indentation += 1
        try:
            yield
        finally:
            self._indentation -= 1
            self(';;')

    def complete(self, *options: str, word: str):
        self('mapfile -t COMPREPLY < <(compgen -W', quote(' '.join(map(quote, options))), '--', word, ')')

# -*- coding=utf-8 -*-
r"""

"""
import io
import textwrap
import typing as t
from contextlib import contextmanager


__all__ = ['ShellWriter']


class ShellWriter:
    def __init__(self):
        self._stream = io.StringIO()
        self._indentation = 0

    def __str__(self):
        return self._stream.getvalue()

    def __repr__(self):
        return super().__repr__()

    def write(self, *parts, sep=" ", end="\n") -> None:
        head = '  ' * self._indentation
        body = textwrap.dedent(sep.join(parts))
        tail = end
        self._stream.write(head + body + tail)

    def write_block(self, block: str, indent: bool = True) -> None:
        body = textwrap.dedent(block).strip()
        if indent:
            body = textwrap.indent(body, '  ' * self._indentation)
        self._stream.write(body + '\n')

    @contextmanager
    def indent(self) -> t.ContextManager:
        self._indentation += 1
        try:
            yield
        finally:
            self._indentation -= 1

    def comment(self, *lines):
        width = 80 - self._indentation*2 - 2
        for line in lines:
            for wrapped in textwrap.wrap(line, width):
                self.write('# ' + wrapped)

    def comment_block(self, *lines):
        width = 80 - (self._indentation * 2) - 2 - 2
        self.write('#' * (width + 4))
        for line in lines:
            if not line:
                continue
            if line.startswith(3*'='):
                self.write('# ' + ('=' * width) + ' #')
            elif line.startswith(3*'-'):
                self.write('# ' + ('-' * width) + ' #')
            elif line.startswith("="):
                self.write('# ' + line[1:].strip().center(width) + ' #')
            else:
                for wrapped in textwrap.wrap(line, width):
                    self.write('# ' + wrapped.ljust(width) + ' #')
        self.write('#' * (width + 4))

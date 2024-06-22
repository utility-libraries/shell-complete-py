# -*- coding=utf-8 -*-
r"""

"""
import sys
import shlex
from ..core.imbued import ImbuedCode


__all__ = ['ShellCode', 'Recommended', 'PythonCode']


class Recommended(ImbuedCode):
    r"""
    recommends some options.
    similar to settings choices (argparse.ArgumentParser.add_argument(choices=)) but does not change your parser
    """

    def __init__(self, *options):
        self.options = options

    def __str__(self) -> str:
        return fr"""
        OPTIONS=({shlex.join(self.options)})
        mapfile -t COMPREPLY < <(compgen -W "${{OPTIONS[*]}}" -- "$cur")
        """


class ShellCode(ImbuedCode):
    r"""
    marks a piece of shell code that gets directly imbued into the completion-file.
    """

    def __init__(self, code: str):
        self.code = code

    def __str__(self) -> str:
        return self.code


class PythonCode(ImbuedCode):
    r"""
    wrapper for python code that should be imbued into the completion-file.
    """

    BEAUTIFY = False

    SHELL_CODE_TEMPLATE = r"""
    STROPTIONS="$({command})"
    mapfile -t COMPREPLY < <(compgen -W "$STROPTIONS" -- "$cur")
    """

    PYTHON_CODE_HEAD = r"""
    def compreply(options):
        import shlex
        print(shlex.join(map(str, options)))

    """

    def __init__(self, code: str, *, python: str = None):
        self.code = code
        self.python = python

    def __str__(self) -> str:
        python = self.python or sys.executable
        code = self.PYTHON_CODE_HEAD + self.code

        pycommand = shlex.join([python, '-B', '-O', '-X', 'utf8', '-c', code])

        return self.SHELL_CODE_TEMPLATE.format(command=pycommand)

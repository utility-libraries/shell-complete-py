# -*- coding=utf-8 -*-
r"""

"""
import sys
import shlex
import typing as t
from ..core.imbued import ImbuedCode


__all__ = ['Recommended', 'ShellCode', 'ShellCommand', 'PythonCode']


class Recommended(ImbuedCode):
    r"""
    recommends some options.
    similar to settings choices (argparse.ArgumentParser.add_argument(choices=)) but does not change your parser

    >>> parser.add_argument(...).completer = Recommended(1, 2, 3)
    """

    def __init__(self, *options):
        self.options = options

    def __str__(self) -> str:
        return fr"""
        OPTIONS=({shlex.join(map(str, self.options))})
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


class ShellCommand(ImbuedCode):
    r"""
    code for a shell-command that generates the completion which gets imbued into the completion-file.

    >>> parser.add_argument(...).completer = ShellCommand(..., "command | formatter")
    >>> parser.add_argument(...).completer = ShellCommand("command", "--option")
    >>> parser.add_argument(...).completer = ShellCommand(["command", "--option"])
    """

    BEAUTIFY = False

    SHELL_CODE_TEMPLATE = r"""
    STROPTIONS="$({command})"
    mapfile -t COMPREPLY < <(compgen -W "$STROPTIONS" -- "$cur")
    """

    @t.overload
    def __init__(self, marker: Ellipsis, command: str): ...
    @t.overload
    def __init__(self, command: t.List[str]): ...
    @t.overload
    def __init__(self, *command: str): ...

    def __init__(self, *args):
        if len(args) == 2 and args[0] is ... and isinstance(args[1], str):
            self.command = shlex.split(args[0])
        elif len(args) == 1 and isinstance(args[0], (tuple, list)):
            self.command = args[0]
        else:
            self.command = args

    def __str__(self) -> str:
        command = shlex.join(self.command)
        return self.SHELL_CODE_TEMPLATE.format(command=command)


class PythonCode(ImbuedCode):
    r"""
    wrapper for python code that generates the completion which gets imbued into the completion-file.

    >>> parser.add_argument(...).completer = PythonCode(r'''
    >>> compreply([1, 2, 3])
    >>> ''')
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

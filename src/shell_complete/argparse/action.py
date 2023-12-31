# -*- coding=utf-8 -*-
r"""

"""
import os
import shlex
import fileinput
import typing as t
import os.path as p
import argparse as ap
from functools import cached_property
from ..core import generate


__all__ = ['ActionShellComplete']


class ActionShellComplete(ap.Action):
    r"""
    $ myprog --completion [{print,install,uninstall}]
    """
    __parser: ap.ArgumentParser

    # noinspection PyShadowingBuiltins
    def __init__(self, option_strings, dest, help=None, required: bool = False):
        super().__init__(
            option_strings,
            dest=ap.SUPPRESS,
            nargs=ap.OPTIONAL,
            choices=["print", "install", "uninstall"],
            help=help,
            required=required,
        )

    # ---------------------------------------------------------------------------------------------------------------- #

    @cached_property
    def bash_completion_dir(self) -> str:
        return p.abspath(
            p.expanduser(
                p.join("~", ".bash_completion.d")
            )
        )

    @cached_property
    def bash_complete_file(self) -> str:
        return p.abspath(
            p.expanduser(
                p.join(self.bash_completion_dir, f"{self.__parser.prog}.completion.bash")
            )
        )

    @cached_property
    def bashrc_file(self):
        return p.abspath(
            p.expanduser(
                p.join("~", ".bashrc")
            )
        )

    @cached_property
    def load_line(self) -> str:
        return f"source {shlex.quote(self.bash_complete_file)}\n"

    # ---------------------------------------------------------------------------------------------------------------- #

    def ensure_completion_root(self):
        os.makedirs(self.bash_completion_dir, exist_ok=True)

    def generate_completion_file(self, parser: ap.ArgumentParser):
        content = generate(parser)
        with open(self.bash_complete_file, 'w') as file:
            file.write(content)

    def install_loading(self):
        last_line_is_empty = False
        with open(self.bashrc_file, 'r+') as file:
            for line in file:
                if line == self.load_line:
                    break
                last_line_is_empty = line == "\n"
            else:
                if not last_line_is_empty:
                    file.write('\n')  # separation-line
                file.write(self.load_line)

    def remove_completion_file(self):
        if p.isfile(self.bash_complete_file):
            os.remove(self.bash_complete_file)

    def remove_loading(self):
        with fileinput.FileInput(self.bashrc_file, inplace=True) as file:
            for line in file:
                if line != self.load_line:
                    print(line, end='')

    def __call__(self, parser: ap.ArgumentParser, ns: ap.Namespace, value: t.Optional[str], opt: str = None):
        self.__parser = parser
        if value in {None, "print"}:
            print(generate(parser=parser))
        elif value == "install":
            self.ensure_completion_root()
            self.generate_completion_file(parser=parser)
            self.install_loading()
        elif value == "uninstall":
            self.remove_completion_file()
            self.remove_loading()
        else:
            raise ValueError(f"unknown option {value!r} ({'|'.join(self.choices)})")
        parser.exit()

# -*- coding=utf-8 -*-
r"""

"""
import argparse as ap
from ._writer import BashWriter, quote


__all__ = ['generate']


def generate(parser: ap.ArgumentParser) -> str:
    r"""
    :param parser: the parser to convert to a .completion.bash script
    :return: .completion.bash script
    """
    writer = BashWriter(program=parser.prog, smart=True)
    with writer:
        # noinspection PyProtectedMember
        actions = parser._actions

        with writer.switch('"$LAST"'):
            for action in actions:
                if not action.option_strings:
                    continue
                if action.choices:
                    with writer.case(*map(quote, action.option_strings)):
                        writer.complete(*action.choices, word='"$CURRENT"')
                elif hasattr(action.type, '__completion__'):
                    with writer.case(*map(quote, action.option_strings)):
                        writer(action.type.__completion__)
            with writer.case("*"):
                writer.complete(
                    *(
                        option
                        for action in actions
                        for option in action.option_strings
                        if option[0] not in parser.prefix_chars  # sub-command (prog option)
                        or option[1] in parser.prefix_chars  # long-option (prog --option)
                    ),
                    word='"$CURRENT"',
                )

    return str(writer)

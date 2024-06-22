# -*- coding=utf-8 -*-
r"""

"""
import re
import typing as t
import argparse as ap
from shlex import quote, join
from .writing import ShellWriter
from .. import __version__
from . import _argparse_actions as ap_actions
from .imbued import ImbuedCode


__all__ = ['generate']


HAVE_VALUE_ACTIONS = (ap_actions.StoreAction, ap_actions.AppendAction, ap_actions.ExtendAction)
HAVE_NO_VALUE_ACTIONS = (ap_actions.StoreConstAction, ap_actions.StoreTrueAction, ap_actions.StoreFalseAction,
                         ap_actions.AppendConstAction, ap_actions.CountAction, ap_actions.HelpAction,
                         ap_actions.VersionAction, ap_actions.BooleanOptionalAction)


def generate(parser: ap.ArgumentParser) -> str:
    r"""
    :param parser: the parser to convert to a .completion.bash script
    :return: .completion.bash script
    """
    root_parser = parser
    writer = ShellWriter()

    # head ---------------------------------------------------------------------
    writer.comment_block(
        f"= Generated with shell-complete {__version__}",
        "-----",
        f"https://pypi.org/project/shell-complete/{__version__}",
        "https://github.com/utility-libraries/shell-complete-py",
        "=====",
        f"= {parser.prog}",
        parser.description.strip(),
    )
    writer.write()
    # this prevents 'eval "$(foo --completion)"' execution
    # # prevent idiot execution --------------------------------------------------
    # writer.comment("prevent execution of this script as it has to be sourced")
    # writer.write('if ! [[ -n $ZSH_VERSION && $ZSH_EVAL_CONTEXT =~ :file$ ]] \\\n'
    #              '   || [[ -n $BASH_VERSION ]] && ! (return 0 2>/dev/null); then')
    # with writer.indent():
    #     writer.write('echo "\'source ${BASH_SOURCE[0]}\' is the correct usage"')
    #     writer.write('exit 1')
    # writer.write('fi')
    # writer.write()
    # only completion if command exist -----------------------------------------
    writer.comment("only register autocompletion if the command actually exists")
    writer.comment("or source with 'FORCE_COMPLETION= source ${BASH_SOURCE[0]}'")
    writer.write('if [[ -z ${FORCE_COMPLETION+x} ]] && ! command -v', quote(root_parser.prog), '&> /dev/null; then')
    with writer.indent():
        writer.write('return')
    writer.write('fi')
    writer.write()

    parser_queue = [root_parser]

    while parser_queue:
        parser = parser_queue.pop(0)
        # noinspection PyProtectedMember
        actions = parser._actions

        long_options: t.Set[str] = set(
            option
            for action in actions
            for option in action.option_strings
            if option.startswith(parser.prefix_chars * 2)  # only long ones
        )
        short_options: t.Set[str] = set(
            option
            for action in actions
            for option in action.option_strings
            if option.startswith(parser.prefix_chars) and option not in long_options
        )
        subcommands: t.Set[str] = set()

        writer.comment(f"auto-completion function for '{parser.prog}'")
        writer.write('function _shell_complete_', get_prog(parser), '() {', sep="")
        with writer.indent():
            writer.write('local depth=$1')
            writer.write('shift')
            writer.write('local loop_count=0')
            writer.write('local cur=${COMP_WORDS[$COMP_CWORD]}')
            writer.write('')
            writer.write('while [[ $# -gt 0 ]]; do')
            with writer.indent():
                writer.comment("security protocol to prevent an infinite loop")
                writer.write('(( loop_count += 1 ))')
                writer.write('if [ "$loop_count" -gt 10000 ]; then')
                with writer.indent():
                    writer.write(f'>&2 echo "Loop overflow for \'{parser.prog}\'"')
                    writer.write(f'>&2 echo "depth=$depth with \'$*\'"')
                    writer.write('break')
                writer.write('fi')
                writer.write()
                writer.write('case $1 in')
                with writer.indent():
                    for action in actions:
                        # noinspection PyProtectedMember,PyUnresolvedReferences
                        if isinstance(action, ap_actions.SubParsersAction):
                            # noinspection PyUnresolvedReferences
                            for choice, subparser in action.choices.items():
                                subparser: ap.ArgumentParser
                                subcommands.add(choice)
                                parser_queue.append(subparser)

                                writer.write(choice, ')', sep="")
                                with writer.indent():
                                    writer.write('(( depth += 1 )); shift')
                                    writer.write('_shell_complete_', get_prog(subparser), ' "$depth" "$@"', sep="")
                                    writer.write('break  # we should have our completion')
                                writer.write(';;')
                            continue

                        if not action.option_strings:
                            continue

                        writer.write('|'.join(map(quote, action.option_strings)), ')', sep="")
                        with writer.indent():
                            writer.write('(( depth += 1 )); shift')
                            if has_completer(action):
                                completer = get_completer(action)
                                writer.write_block(str(completer), indent=completer.BEAUTIFY)
                            elif action.choices:
                                writer.write('if [ "$depth" -eq "$COMP_CWORD" ]; then')
                                with writer.indent():
                                    writer.write(f'OPTIONS=({join(map(str, action.choices))})')
                                    writer.write('mapfile -t COMPREPLY < <(compgen -W "${OPTIONS[*]}" -- "$cur")')
                                    writer.write('break  # we should have our completion')
                                writer.write('fi')
                                writer.write('(( depth += 1 )); shift')
                            elif isinstance(action, HAVE_VALUE_ACTIONS):
                                if isinstance(action.nargs, int) and action.nargs > 0:
                                    writer.write(f'(( depth += {action.nargs} ))')
                                    writer.write(f'shift {action.nargs}')
                                else:
                                    writer.write('(( depth += 1 )); shift')
                            else:
                                if isinstance(action.nargs, int) and action.nargs > 0:
                                    writer.write(f'(( depth += {action.nargs} ))')
                                    writer.write(f'shift {action.nargs}')
                                elif isinstance(action, HAVE_VALUE_ACTIONS):
                                    writer.write('(( depth += 1 )); shift')
                                elif isinstance(action, HAVE_NO_VALUE_ACTIONS):
                                    pass
                                else:
                                    writer.comment(f'Dunno how to complete: {action}')
                        writer.write(';;')
                    writer.write('*)')
                    with writer.indent():
                        writer.write('(( depth += 1 )); shift')
                    writer.write(';;')
                writer.write('esac')
            writer.write('done')
            writer.write()
            writer.comment('if no completion is set yet')
            writer.write('if [ ${#COMPREPLY} -eq 0 ]; then')
            with writer.indent():
                pfx = quote(parser.prefix_chars)
                writer.write(f'if [[ "$cur" == "{pfx}" ]]; then')
                with writer.indent():
                    writer.write(f'OPTIONS=({join(sorted(short_options))})')
                writer.write('else')
                with writer.indent():
                    writer.write(f'OPTIONS=({join(sorted(long_options | subcommands))})')
                writer.write('fi')
                writer.write('mapfile -t COMPREPLY < <(compgen -W "${OPTIONS[*]}" -- "$cur")')
            writer.write('fi')
        writer.write('}')
        writer.write()

    # entry function -----------------------------------------------------------
    writer.comment("entry point for bash-complete function")
    writer.write('function _shell_complete_entry_', get_prog(root_parser), '() {', sep="")
    with writer.indent():
        writer.write('_shell_complete_', get_prog(root_parser), ' 0 "${COMP_WORDS[@]}"', sep="")
    writer.write('}')
    writer.write()

    # zsh compatibility --------------------------------------------------------
    writer.comment("complete is a bash builtin, but recent versions of ZSH come with a function called bashcompinit"
                   " that will create a complete in ZSH. If the user is in ZSH, load and run bashcompinit before"
                   " calling the complete function.")
    writer.write('if [[ -n ${ZSH_VERSION-} ]]; then')
    with writer.indent():
        writer.write('autoload -U +X bashcompinit && bashcompinit')
        writer.write('autoload -U +X compinit && compinit')
    writer.write('fi')
    writer.write()

    # registering the completion -----------------------------------------------
    writer.comment("registering the entry point")
    writer.write('complete -F _shell_complete_entry_', get_prog(root_parser), ' ', quote(root_parser.prog), sep="")

    return str(writer)


def has_completer(action: ap.Action) -> bool:
    return hasattr(action, 'completer') or hasattr(action.type, '__completer__')


def get_completer(action: ap.Action) -> ImbuedCode:
    completer = getattr(action, 'completer')
    if completer is None:
        completer = getattr(action.type, '__completer__')
    if not isinstance(completer, ImbuedCode):
        if not isinstance(completer, ImbuedCode):
            raise TypeError(f'completer type must be a subclass of ImbuedCode ({action})')
    return completer


def get_prog(parser: ap.ArgumentParser) -> str:
    return re.sub(r'\W', '_', parser.prog)

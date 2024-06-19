# -*- coding=utf-8 -*-
r"""

"""
import typing as t
from argparse import Action
# noinspection PyUnresolvedReferences,PyProtectedMember
from argparse import (
    _StoreAction as StoreAction,
    _StoreConstAction as StoreConstAction,
    _StoreTrueAction as StoreTrueAction,
    _StoreFalseAction as StoreFalseAction,
    _AppendAction as AppendAction,
    _AppendConstAction as AppendConstAction,
    _CountAction as CountAction,
    _HelpAction as HelpAction,
    _VersionAction as VersionAction,
    _SubParsersAction as SubParsersAction,
)
try:  # added in 3.9
    # noinspection PyUnresolvedReferences,PyProtectedMember
    from argparse import _ExtendAction as ExtendAction
except ImportError:
    class ExtendAction:  # pseudo-class
        pass
try:  # added in 3.9
    from argparse import BooleanOptionalAction
except ImportError:
    class BooleanOptionalAction:  # pseudo-class
        pass

# noinspection PyProtectedMember
ChoicesPseudoAction = SubParsersAction._ChoicesPseudoAction

StoreAction: t.Type[Action]
StoreConstAction: t.Type[Action]
StoreTrueAction: t.Type[Action]
StoreFalseAction: t.Type[Action]
AppendAction: t.Type[Action]
AppendConstAction: t.Type[Action]
CountAction: t.Type[Action]
HelpAction: t.Type[Action]
VersionAction: t.Type[Action]
SubParsersAction: t.Type[Action]
ChoicesPseudoAction: t.Type[Action]
ExtendAction: t.Type[Action]

__all__ = [
    'StoreAction',
    'StoreConstAction',
    'StoreTrueAction',
    'StoreFalseAction',
    'AppendAction',
    'AppendConstAction',
    'CountAction',
    'HelpAction',
    'VersionAction',
    'SubParsersAction',
    'ChoicesPseudoAction',
    'ExtendAction',
    'BooleanOptionalAction',
]

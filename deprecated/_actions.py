# -*- coding=utf-8 -*-
r"""

"""
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
try:
    # noinspection PyUnresolvedReferences,PyProtectedMember
    from argparse import _ExtendAction as ExtendAction
except ImportError:
    ExtendAction = object()
try:
    from argparse import BooleanOptionalAction as BooleanOptionalAction
except ImportError:
    BooleanOptionalAction = object()

# noinspection PyProtectedMember
ChoicesPseudoAction = SubParsersAction._ChoicesPseudoAction

# noinspection PyUnresolvedReferences
__all__ = [
    'BooleanOptionalAction',
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
]

# -*- coding=utf-8 -*-
r"""

"""

__all__ = ['ImbuedCode']


class ImbuedCode:
    r"""
    marks a piece of shell code that gets directly imbued into the completion-file.
    """

    BEAUTIFY: bool = True

    def __str__(self) -> str:
        raise NotImplementedError()

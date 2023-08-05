# main.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2011 Róbert Čerňanský



""":func:`createMainfEngine` function."""



__all__ = ["createMainfEngine"]



# {{{ FUNCTIONS

def createMainfEngine():
    """Creates an instance of :class:`.MainfEngine`.

    :return: A :class:`.MainfEngine` instance.
    :rtype: :class:`.MainfEngine`"""
    
    # Do not import ._core globally because of recursive import.  If the import from ._core would be global then
    # importing this module (as a start script that creates and initializes Mainf framework should do) would result to
    # a recursive import (by modules in ._core) of the mainf package _during_ the ._core import.  Modules in ._core
    # typically imports their public symbols so as, in this case, the ._core.mainf_core module.
    from ._core.mainf_engine import MainfEngine

    return MainfEngine()

# }}} FUNCTIONS

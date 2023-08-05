# __init__.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2011 Róbert Čerňanský



""":term:`Cmdline UI` :term:`component`.

Package defines a :term:`Mainf` :term:`component` for a command-line user interface."""



from .cmdline_commands import *



__all__ = cmdline_commands.__all__[:]

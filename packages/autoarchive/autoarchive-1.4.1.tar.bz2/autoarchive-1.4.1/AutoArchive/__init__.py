# __init__.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2011 Róbert Čerňanský



"""**A simple backup utility.**

This package does not provide any public library (API) intended to be imported by 3rd-party programs.  All its content
and content of its subpackages is the implementation of :term:`AutoArchive` utility."""



from .starter import Starter



__all__ = ["Starter"]

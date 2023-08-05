# __init__.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2012 Róbert Čerňanský



""":term:`Archiver Service Component`.

Provides services for creating the backup."""



from .archiver_service_creator import *



__all__ = archiver_service_creator.__all__[:]

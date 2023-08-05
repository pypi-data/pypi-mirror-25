# _meta.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2017 Róbert Čerňanský



""":class:`_Meta` class."""



__all__ = ["_Meta"]



# {{{ INCLUDES

from abc import *

# }}} INCLUDES



# {{{ CLASSES

class _Meta(metaclass = ABCMeta):
    "Defines various project metadata like version, license etc."

    PACKAGE_NAME = "autoarchive"
    VERSION = "1.4.1"

    DESCRIPTION = "A simple backup utility."

    COPYRIGHT = "Copyright (C) 2003 - 2017 Robert Cernansky"

    LICENSE = """\
This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License version 3 as published by the Free
Software Foundation.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <http://www.gnu.org/licenses/>."""



    @abstractmethod
    def __init__(self):
        pass

# }}} CLASSES

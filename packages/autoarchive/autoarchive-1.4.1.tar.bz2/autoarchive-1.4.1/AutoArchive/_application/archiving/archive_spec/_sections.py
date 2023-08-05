# _sections.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2017 Róbert Čerňanský



""":class:`_Sections`."""



__all__ = ["_Sections"]



# {{{ INCLUDES

from abc import *

# }}} INCLUDES



# {{{ CLASSES

class _Sections(metaclass = ABCMeta):
    ":term:`archive specification file` section names."

    #: Contains referenced :term:`archive specification files<archive specification file>`.
    EXTERNAL = "External"

    #: Contains options that modifies aspects of the backup creation.
    ARCHIVE = "Archive"

    #: Parameters of the archive.
    CONTENT = "Content"



    @abstractmethod
    def __init__(self):
        pass

# }}} CLASSES

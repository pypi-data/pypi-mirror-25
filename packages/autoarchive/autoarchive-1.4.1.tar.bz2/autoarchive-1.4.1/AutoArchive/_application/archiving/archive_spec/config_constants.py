# config_constants.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2014 Róbert Čerňanský



""":class:`ArchiveSpecInfo` and :class:`ConfigConstants`."""



__all__ = ["ArchiveSpecInfo", "ConfigConstants"]



# {{{ INCLUDES

from abc import *
from collections import namedtuple

# }}} INCLUDES



# {{{ CLASSES

class ConfigConstants(metaclass = ABCMeta):
    "Configuration related constants."

    #: Extension of :term:`archive specification files <archive specification file>`.
    ARCHIVE_SPEC_EXT = ".aa"



    @abstractmethod
    def __init__(self):
        pass



#: Holds information about an archive specification file; its name and full path.
ArchiveSpecInfo = namedtuple("ArchiveSpecInfo", "name path")

# }}} CLASSES

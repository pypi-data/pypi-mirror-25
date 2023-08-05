# iapp_config.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2011 Róbert Čerňanský



""":class:`IAppConfig` interface, :class:`ConfigConstants` static class and :class:`ArchiveSpecInfo` namedtuple."""



__all__ = ["ArchiveSpecInfo", "IAppConfig", "ConfigConstants"]



# {{{ INCLUDES

from abc import *
from collections import namedtuple

from .._mainf import *
from . import *

# }}} INCLUDES



# {{{ CLASSES

#: Holds information about an archive specification file; its name and full path.
ArchiveSpecInfo = namedtuple("ArchiveSpecInfo", "name path")



class IAppConfig(IConfiguration, IComponentInterface):
    "Provides access to application configuration."

    @abstractmethod
    def getArchiveSpecs(self):
        """Iterable of all known archive specification files.

        :return: Iterable of archive specification files information.
        :rtype: ``Iterable<ArchiveSpecInfo>``

        :raise RuntimeError: If list of archive specification can not be obtained."""



class ConfigConstants(metaclass = ABCMeta):
    "Configuration related constants."

    #: Extension of :term:`archive specification files <archive specification file>`.
    ARCHIVE_SPEC_EXT = ".aa"



    @abstractmethod
    def __init__(self):
        pass

# }}} CLASSES

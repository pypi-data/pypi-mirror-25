# _archiving_constants.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2012 Róbert Čerňanský



""":class:`_ArchiverMaps` and :class:`_RestartStorageVariables` classes."""



__all__ = ["_ArchiverMaps", "_RestartStorageVariables"]



# {{{ INCLUDES

from abc import *

from ..._services.archiver import *
from .. import *

# }}} INCLUDES



# {{{ CLASSES

class _ArchiverMaps(metaclass = ABCMeta):
    """Mappings which involves archiver types."""

    ARCHIVER_TYPE_TO_SERVICE_MAP = {ArchiverTypes.Tar: ArchiverServiceProviders.TarExternal,
                                    ArchiverTypes.TarGz: ArchiverServiceProviders.TarExternal,
                                    ArchiverTypes.TarBz2: ArchiverServiceProviders.TarExternal,
                                    ArchiverTypes.TarXz: ArchiverServiceProviders.TarExternal,
                                    ArchiverTypes.TarInternal: ArchiverServiceProviders.TarInternal,
                                    ArchiverTypes.TarGzInternal: ArchiverServiceProviders.TarInternal,
                                    ArchiverTypes.TarBz2Internal: ArchiverServiceProviders.TarInternal}



    @abstractmethod
    def __init__(self):
        pass



class _RestartStorageVariables(metaclass = ABCMeta):
    """Names of storage variables for backup level restarting."""

    LAST_RESTART = "archiving-last-restart"
    LAST_FULL_RESTART = "archiving-last-full-restart"
    BACKUP_SIZE = "archiving-size-level"
    RESTART_COUNT = "archiving-restart-count"



    @abstractmethod
    def __init__(self):
        pass

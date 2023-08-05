# _archiving_constants.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2014 Róbert Čerňanský



""":class:`_ArchiverMaps` and :class:`_RestartStorageVariables` classes."""



__all__ = ["_ArchiverMaps", "_RestartStorageVariables"]



# {{{ INCLUDES

from abc import ABCMeta, abstractmethod
from AutoArchive._services.archiver import ArchiverServiceProviderIDs
from AutoArchive._infrastructure.configuration import ArchiverTypes

# }}} INCLUDES



# {{{ CLASSES

class _ArchiverMaps(metaclass = ABCMeta):
    """Mappings which involves archiver types."""

    ARCHIVER_TYPE_TO_SERVICE_MAP = {ArchiverTypes.Tar: ArchiverServiceProviderIDs.TarExternal,
                                    ArchiverTypes.TarGz: ArchiverServiceProviderIDs.TarExternal,
                                    ArchiverTypes.TarBz2: ArchiverServiceProviderIDs.TarExternal,
                                    ArchiverTypes.TarXz: ArchiverServiceProviderIDs.TarExternal,
                                    ArchiverTypes.TarInternal: ArchiverServiceProviderIDs.TarInternal,
                                    ArchiverTypes.TarGzInternal: ArchiverServiceProviderIDs.TarInternal,
                                    ArchiverTypes.TarBz2Internal: ArchiverServiceProviderIDs.TarInternal}



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

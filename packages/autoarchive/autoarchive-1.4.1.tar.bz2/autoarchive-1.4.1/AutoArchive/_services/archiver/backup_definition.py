# backup_definition.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2014 Róbert Čerňanský



""":const:`MIN_COMPRESSION_STRENGTH` and :const:`MAX_COMPRESSION_STRENGTH` constants, :data:`BackupTypes`,
:data:`ArchiverFeatures`, :data:`BackupSubOperations`, :data:`BackupOperationErrors` enums
and :class:`BackupDefinition` class."""



__all__ = ["MIN_COMPRESSION_STRENGTH", "MAX_COMPRESSION_STRENGTH", "BackupTypes", "ArchiverFeatures",
           "BackupSubOperations", "BackupOperationErrors", "BackupDefinition"]



# {{{ INCLUDES

from AutoArchive._infrastructure.py_additions import Enum

# }}} INCLUDES



# {{{ CONSTANTS

#: Minimal compression strength value.
MIN_COMPRESSION_STRENGTH = 0

#: Maximal compression strength value.
MAX_COMPRESSION_STRENGTH = 9

# }}} CONSTANTS



# {{{ CLASSES

#: Backup types.
BackupTypes = Enum(
    "Tar",
    "TarGz",
    "TarBz2",
    "TarXz")



#: Features that archiver service may support.
ArchiverFeatures = Enum(
    "CompressionStrength",
    "Incremental")



#: Operations executed during backup creation.
BackupSubOperations = Enum(

    #: Unknown operation
    "Unknown",

    #: Unknown operation on a filesystem object.
    "UnknownFileOperation",

    #: :meth:`os.stat()` (or access) operation on a filesystem object.
    "Stat",

    #: Filesystem object open operation.
    "Open",

    #: File read operation.
    "Read",

    #: Finishing the backup creation.
    "Finish")



#: Errors that may occur during backup operation.
BackupOperationErrors = Enum(

    #: Unknown error.
    "UnknownError",

    #: An operation on a filesystem object was not successful due to other/unknown system error.
    "UnknownOsError",

    #: An operation on a filesystem object was not successful due to permission denied system error.
    "PermissionDenied",

    #: A socket was ignored.
    "SocketIgnored",

    #: An unknown filesystem object typ was ignored.
    "UnknownTypeIgnored",

    #: The file was changed while it has been adding to the backup.
    "FileChanged",

    #: Some files were changed during backup creation.
    "SomeFilesChanged",

    #: A directory has been renamed since last backup level.
    "DirectoryRenamed")



class BackupDefinition:
    """Container class for information needed to create a backup."""

    def __init__(self):
        self.__backupId = None
        self.__backupType = None
        self.__destination = None
        self.__root = None
        self.__includeFiles = None
        self.__excludeFiles = frozenset()



    @property
    def backupId(self):
        """The backup identifier, typically the name is used.

        :rtype: ``str``"""

        return self.__backupId

    @backupId.setter
    def backupId(self, value):
        self.__backupId = value



    @property
    def backupType(self):
        """Type of the backup.

        :rtype: :data:`BackupTypes`"""

        return self.__backupType

    @backupType.setter
    def backupType(self, value):
        self.__backupType = value



    @property
    def destination(self):
        """Path to the directory which contains the backup.

        :rtype: ``str``"""

        return self.__destination

    @destination.setter
    def destination(self, value):
        self.__destination = value



    @property
    def root(self):
        """Path to the root directory of the source content.

        :rtype: ``str``"""

        return self.__root

    @root.setter
    def root(self, value):
        self.__root = value



    @property
    def includeFiles(self):
        """Set of source filesystem objects paths relative to :attr:`root`.

        :rtype: ``Set<str>``"""

        return self.__includeFiles

    @includeFiles.setter
    def includeFiles(self, value):
        self.__includeFiles = value



    @property
    def excludeFiles(self):
        """Set of excluded filesystem objects paths relative to :attr:`root`.

        :rtype: ``Set<str>``"""

        return self.__excludeFiles

    @excludeFiles.setter
    def excludeFiles(self, value):
        self.__excludeFiles = value

# }}} CLASSES

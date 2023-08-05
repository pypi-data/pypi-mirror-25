# iarchiver.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2012 Róbert Čerňanský



""":const:`MIN_COMPRESSION_STRENGTH` and :const:`MAX_COMPRESSION_STRENGTH` constants, :data:`BackupTypes`,
:data:`ArchiverFeatures`, :data:`BackupSubOperations`, :data:`BackupOperationErrors` enums and :class:`IArchiver`
interface and :class:`BackupDefinition` class."""



__all__ = ["MIN_COMPRESSION_STRENGTH", "MAX_COMPRESSION_STRENGTH", "BackupTypes", "ArchiverFeatures",
           "BackupSubOperations", "BackupOperationErrors", "IArchiver", "BackupDefinition"]



# {{{ INCLUDES

from abc import *
from .._py_additions import *

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



class IArchiver(metaclass = ABCMeta):
    """SPI for backup creation and management."""

    @abstractproperty
    def supportedBackupTypes(self):
        """Gets a set of backup types supported by this archiver service.

        :rtype: ``set<BackupTypes>``"""



    @abstractmethod
    @event
    def fileAdd(filesystemObjectName):
        """Raised when an filesystem object is added to the backup.

        :param filesystemObjectName: Name of the filesystem object.
        :type filesystemObjectName: ``str``"""



    @abstractmethod
    @event
    def backupOperationError(operation, error, filesystemObjectName = None, unknownErrorString = None):
        """Raised when an non-fatal error occur during the backup operation.

        :param operation: The operation which was running when the error occurred.
        :type operation: :data:`BackupSubOperations`
        :param error: The error that occurred.
        :type error: :data:`BackupOperationErrors`
        :param filesystemObjectName: Name of the filesystem object that was processed when the error occurred.  It is
           non-None only if ``operation`` is one of ``UnknownFileOperation``, ``Stat``, ``Open`` or ``Read``.
        :type filesystemObjectName: ``str``
        :param unknownErrorString: Error string.  It is non-None only if the ``error`` is either ``UnknownError`` or,
           ``UnknownOsError``.
        :type unknownErrorString: ``str``"""



    @abstractmethod
    def backupFiles(self, backupDefinition, compressionStrength = None):
        """Creates a backup.

        :param backupDefinition: Defines the backup that shall be created.  All attributes of the passed instance has
           to be initialized.
        :type backupDefinition: :class:`BackupDefinition`
        :param compressionStrength: Value from interval <MIN_COMPRESSION_STRENGTH, MAX_COMPRESSION_STRENGTH>
           representing the strength of compression.  It has to be non-None only for backup types that supports
           compression and compression strength setting.
        :type compressionStrength: ``int``

        :return: Path to the created backup.
        :rtype: ``str``

        :raise RuntimeError: If ``compressionStrength`` is non-``None`` and ``backupDefinition.backupType`` does not
           supports compression or compression strength setting.  If an unknown error occurred during backup creation.
        :raise ValueError: If ``compressionStrength`` is outside of required interval or if
           ``backupDefinition.backupType`` is not supported by the implementation.
        :raise OSError: If a system error occurred while making the backup."""



    @abstractmethod
    def backupFilesIncrementally(self, backupDefinition, compressionStrength = None, level = None):
        """Creates an incremental backup.

        A backup of specified level or the next level in a row will be created.  The maximal backup level will be
        increased (see :meth:`getMaxBackupLevel()`).

        :param backupDefinition: Defines the backup that shall be created.  All attributes of the passed instance has
           to be initialized.
        :type backupDefinition: :class:`BackupDefinition`
        :param compressionStrength: Value from interval <MIN_COMPRESSION_STRENGTH, MAX_COMPRESSION_STRENGTH>
           representing the strength of compression.  It has to be non-None only for backup types that supports
           compression and compression strength setting.
        :type compressionStrength: ``int``
        :param level: Backup level that shall be created.  If ``None``, the next level in a row will be created, which
           is the the one returned by :meth:`getMaxBackupLevel()`.  The value has to be from interval
           <0, :meth:`getMaxBackupLevel()`>.
        :type level: ``int``

        :return: Path to the created backup.
        :rtype: ``str``

        :raise RuntimeError: If ``compressionStrength`` is non-``None`` and ``backupDefinition.backupType`` does not
           supports compression or compression strength setting.  If an unknown error occurred during backup creation.
        :raise ValueError: If ``compressionStrength`` or ``level`` is outside of required interval or if
           ``backupDefinition.backupType`` is not supported by the implementation.
        :raise NotImplementedError: If incremental backup is not supported.
        :raise OSError: If a system error occurred while making the backup."""



    @abstractmethod
    def removeBackup(self, backupDefinition):
        """Remove a backup.

        Backup defined by ``backupDefinition`` will be removed.

        :param backupDefinition: Defines backup that shall be removed.  :attr:`BackupDefinition.backupId`,
           :attr:`BackupDefinition.backupType` and :attr:`BackupDefinition.destination` attributes of the passed
           instance has to be initialized.
        :type backupDefinition: :class:`BackupDefinition`

        :raise ValueError: If ``backupDefinition.backupType`` is not supported by the implementation.
        :raise OSError: If a system error occurred during removing operation."""



    @abstractmethod
    def removeBackupIncrements(self, backupDefinition, level = None):
        """Remove backup increments starting from ``level``.

        Backups (increments) of backup level higher or equal than ``level`` or higher that the current backup level - in
        case ``level`` is ``None`` - will be removed.  The maximal backup level (:meth:`getMaxBackupLevel()`) will be
        set to the value ``level``.

        :param backupDefinition: Defines backup that shall be removed.  :attr:`BackupDefinition.backupId`,
           :attr:`BackupDefinition.backupType` and :attr:`BackupDefinition.destination` attributes of the passed
           instance has to be initialized.
        :type backupDefinition: :class:`BackupDefinition`
        :param level: The first level that shall be removed.  All backups of levels higher or equal than ``level`` will
           be removed.  If ``None``, backups of levels higher or equal than the one returned by
           :meth:`getMaxBackupLevel()` will be removed.  The value has to be >= 0.
        :type level: ``int``

        :raise ValueError: If ``level`` is outside of required interval or if ``backupDefinition.backupType`` is not
           supported by the implementation.
        :raise NotImplementedError: If incremental backup is not supported.
        :raise OSError: If a system error occurred during removing operation."""



    @abstractmethod
    def getSupportedFeatures(self, backupType = None):
        """Returns a set of supported features, ether all of them or for given ``backupType``.

        :param backupType: The backup type for which the features shall be returned or ``None`` if all supported
           features shall be returned.
        :type backupType: :data:`BackupTypes`

        :return: Supported features for given ``backupType`` or all supported features.
        :rtype: ``set<ArchiverFeatures>``

        :raise ValueError: If the given ``backupType`` is not supported by this service"""



    @abstractmethod
    def getMaxBackupLevel(self, backupId):
        """Determines and returns maximal backup level that can be created.

        :param backupId: ID of the backup for which the level shall be determined.
        :type backupId: ``str``

        :return: The maximal backup level that can be created by :meth:`backupFilesIncrementally()`.
        :rtype: ``int``

        :raise NotImplementedError: If incremental backup is not supported.
        :raise OSError: If a system error occurred."""



    @abstractmethod
    def getStoredBackupIds(self):
        """Returns iterable of archive IDs which has some data stored in a persistent storage.

        See also: :meth:`purgeStoredBackupData()`.

        :return: Iterable of archive names.
        :rtype: ``Iterable<str>``

        :raise OSError: If a system error occurred."""



    @abstractmethod
    def purgeStoredBackupData(self, backupId):
        """Removes internal data from a persistent storage for the passed ``backupId``.

        See also: :meth:`getStoredBackupIds()`.

        :param backupId: ID of the backup of which data shall be purged.
        :type backupId: ``str``

        :raise OSError: If a system error occurred."""



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

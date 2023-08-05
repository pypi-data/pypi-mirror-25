# tar_archiver_provider_base.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2015 Róbert Čerňanský



""":class:`_TarArchiverProviderBase` class."""



__all__ = ["_TarArchiverProviderBase", "_BACKUP_TYPES_TO_EXTENSIONS"]



# {{{ INCLUDES

from abc import *
import os

from AutoArchive._infrastructure.py_additions import event
from AutoArchive._infrastructure.service import IService
from . import BackupTypes, ArchiverFeatures


# }}} INCLUDES



# {{{ CONSTANTS

_BACKUP_TYPES_TO_EXTENSIONS = {BackupTypes.Tar: "tar",
                               BackupTypes.TarGz: "tar.gz",
                               BackupTypes.TarBz2: "tar.bz2",
                               BackupTypes.TarXz: "tar.xz"}

# }}} CONSTANTS



# {{{ CLASSES

# SMELL: Methods that have BackupDefinition as a parameter should be moved to BackupDefinition class (which should be
# renamed to Backup then - it does not represent a physical backup though, maybe the name should be something
# different or split to two classes, one which represents physical backup and other that represents the definition).
class _TarArchiverProviderBase(IService):
    """Base class for tar archiver service providers.

    Abstract constructor of this class, should be called from derived constructors.  It initializes the
    :attr:`workDir_` property.

    :param workDir: Path to a writable directory.  The service will use it as persistent storage.
    :type workDir: ``str``"""

    __PARTIAL_FILE_SUFFIX = "._partial"



    @abstractmethod
    def __init__(self, workDir):
        self.__workDir = workDir



    @abstractproperty
    def supportedBackupTypes(self):
        """Gets a set of backup types supported by this archiver service.

        :rtype: ``set<BackupTypes>``"""

        return frozenset()



    @event
    def fileAdd(filesystemObjectName):
        """Raised when an filesystem object is added to the backup.

        :param filesystemObjectName: Name of the filesystem object.
        :type filesystemObjectName: ``str``"""



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
    def backupFiles(self, backupDefinition, compressionStrength = None, overwriteAtStart = False):
        """Creates a backup.

        :param backupDefinition: Defines the backup that shall be created.  All attributes of the passed instance has
           to be initialized.
        :type backupDefinition: :class:`BackupDefinition`
        :param compressionStrength: Value from interval <MIN_COMPRESSION_STRENGTH, MAX_COMPRESSION_STRENGTH>
           representing the strength of compression.  It has to be non-None only for backup types that supports
           compression and compression strength setting.
        :type compressionStrength: ``int``
        :param overwriteAtStart: If ``True``, backups are overwritten at the start of creation; otherwise they are
           overwritten at the end of creation (new backups are created with temporary name first and renamed when
           completed).
        :type overwriteAtStart: ``bool``

        :return: Path to the created backup.
        :rtype: ``str``

        :raise RuntimeError: If ``compressionStrength`` is non-``None`` and ``backupDefinition.backupType`` does not
           supports compression or compression strength setting.  If an unknown error occurred during backup creation.
        :raise ValueError: If ``compressionStrength`` is outside of required interval or if
           ``backupDefinition.backupType`` is not supported by the implementation.
        :raise OSError: If a system error occurred while making the backup.

        Performs basic checks before the backup creation.

        .. note:: Derived classes should call this base method on the beginning of the overridden method."""

        self.raiseIfUnsupportedBackupType_(backupDefinition.backupType)
        self.raiseIfUnsupportedFeature_(backupDefinition.backupType, compressionStrength)
        self.__raiseIfEmptyIncludeFiles(backupDefinition.includeFiles)



    @abstractmethod
    def backupFilesIncrementally(self, backupDefinition, compressionStrength = None, level = None,
                                 overwriteAtStart = False):
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
        :param overwriteAtStart: If ``True``, backups are overwritten at the start of creation; otherwise they are
               overwritten at the end of creation (new backups are created with temporary name first and renamed when
               completed).
        :type overwriteAtStart: ``bool``

        :return: Path to the created backup.
        :rtype: ``str``

        :raise RuntimeError: If ``compressionStrength`` is non-``None`` and ``backupDefinition.backupType`` does not
           supports compression or compression strength setting.  If an unknown error occurred during backup creation.
        :raise ValueError: If ``compressionStrength`` or ``level`` is outside of required interval or if
           ``backupDefinition.backupType`` is not supported by the implementation.
        :raise NotImplementedError: If incremental backup is not supported.
        :raise OSError: If a system error occurred while making the backup.

        Performs basic checks before the incremental backup creation.

        .. note:: Derived classes should call this base method on the beginning of the overridden method."""

        self.raiseIfUnsupportedBackupType_(backupDefinition.backupType)
        self.raiseIfUnsupportedFeature_(backupDefinition.backupType, compressionStrength, 99)
        self.__raiseIfEmptyIncludeFiles(backupDefinition.includeFiles)



    def removeBackup(self, backupDefinition, keepingId = None):
        """Remove a backup.

        Backup defined by ``backupDefinition`` will be removed.

        :param backupDefinition: Defines backup that shall be removed.  :attr:`BackupDefinition.backupId`,
           :attr:`BackupDefinition.backupType` and :attr:`BackupDefinition.destination` attributes of the passed
           instance has to be initialized.
        :type backupDefinition: :class:`BackupDefinition`
        :param keepingId: The ID under which the backup is currently kept.  ``None`` if it is not kept.
        :type keepingId: ``str``

        :raise ValueError: If ``backupDefinition.backupType`` is not supported by the implementation.
        :raise OSError: If a system error occurred during removing operation."""

        self.raiseIfUnsupportedBackupType_(backupDefinition.backupType)
        os.remove(self.getBackupFilePath_(
            backupDefinition.backupId, backupDefinition.backupType, backupDefinition.destination, keepingId = keepingId))



    def removeBackupIncrements(self, backupDefinition, level = None, keepingId = None):
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
        :param keepingId: The ID under which the backup is currently kept.  ``None`` if it is not kept.
        :type keepingId: ``str``

        :raise ValueError: If ``level`` is outside of required interval or if ``backupDefinition.backupType`` is not
           supported by the implementation.
        :raise NotImplementedError: If incremental backup is not supported.
        :raise OSError: If a system error occurred during removing operation."""

        raise NotImplementedError("Not supported.")



    @classmethod
    def getSupportedFeatures(cls, backupType = None):
        """Returns a set of supported features, either all of them or for given ``backupType``.

        :param backupType: The backup type for which the features shall be returned or ``None`` if all supported
           features shall be returned.
        :type backupType: :data:`BackupTypes`

        :return: Supported features for given ``backupType`` or all supported features.
        :rtype: ``set<ArchiverFeatures>``

        :raise ValueError: If the given ``backupType`` is not supported by this service"""

        return frozenset()



    def getMaxBackupLevel(self, backupId):
        """Determines and returns maximal backup level that can be created.

        :param backupId: ID of the backup for which the level shall be determined.
        :type backupId: ``str``

        :return: The maximal backup level that can be created by :meth:`backupFilesIncrementally()`.
        :rtype: ``int``

        :raise NotImplementedError: If incremental backup is not supported.
        :raise OSError: If a system error occurred."""

        raise NotImplementedError("Not supported.")



    def getStoredBackupIds(self):
        """Returns iterable of archive IDs which has some data stored in a persistent storage.

        See also: :meth:`purgeStoredBackupData()`.

        :return: Iterable of archive names.
        :rtype: ``Iterable<str>``

        :raise OSError: If a system error occurred."""

        return ()



    def purgeStoredBackupData(self, backupId):
        """Removes internal data from a persistent storage for the passed ``backupId``.

        See also: :meth:`getStoredBackupIds()`.

        :param backupId: ID of the backup of which data shall be purged.
        :type backupId: ``str``

        :raise OSError: If a system error occurred."""

        pass



    def doesBackupExist(self, backupDefinition, level = None, keepingId = None):
        """Returns ``True``, if backup exists.

        :param backupDefinition: Defines the backup which existence shall be queried.
        :type backupDefinition: :class:`BackupDefinition`
        :param level: The level of backup of which existence shall be checked.  If ``None``, existence
           of non-incremental backup will be checked.  The value has to be >= 0.
        :type level: ``int``
        :param keepingId: The kept backup with this ID will be checked for existence.  ``None`` if the actual (not kept)
           backup will be checked.
        :type keepingId: ``str``

        :return: ``True`` if the backup exists, ``False`` otherwise.
        :rtype: ``bool``

        :raise ValueError: If ``backupDefinition.backupType`` is not supported by the implementation."""

        self.raiseIfUnsupportedBackupType_(backupDefinition.backupType)
        return os.path.isfile(self.getBackupFilePath_(
            backupDefinition.backupId, backupDefinition.backupType, backupDefinition.destination, level, keepingId))



    def doesAnyBackupLevelExist(self, backupDefinition, fromLevel = 0, keepingId = None):
        """Returns ``True``, if one or more backup levels of a backup defined by ``backupDefinition`` exists.

        :param backupDefinition: Defines the backup which existence shall be queried.
        :type backupDefinition: :class:`BackupDefinition`
        :param fromLevel: The specified backup level and above will be checked for existence. The value has to be >= 0.
        :type fromLevel: ``int``
        :param keepingId: The kept backup with this ID will be checked for existence.  ``None`` if the actual (not kept)
           backup will be checked.
        :type keepingId: ``str``

        :return: ``True`` if any backup level exists, ``False`` otherwise.
        :rtype: ``bool``

        :raise ValueError: If ``backupDefinition.backupType`` is not supported by the implementation."""

        raise NotImplementedError("Not supported.")



    def keepBackup(self, backupDefinition, keepingId, newKeepingId, level = None):
        """Keeps a backup with ``keepingId`` under the ``newKeepingId``.

        See also: :meth:`doesBackupExist()` or :meth:`doesAnyBackupLevelExist()`.

        :param backupDefinition: Defines the backup that shall be kept.
        :type backupDefinition: :class:`BackupDefinition`
        :param keepingId: The ID under which the backup is currently kept.  ``None`` if it is not kept yet.
        :type keepingId: ``str``
        :param newKeepingId: The ID under which the backup is shall be kept.
        :type newKeepingId: ``str``
        :param level: The level of backup of which shall be kept.  If ``None``, non-incremental backup will be kept.
            The value has to be >= 0.
        :type level: ``int``

        :raise ValueError: If ``backupDefinition.backupType`` is not supported by the implementation or if
           ``newKeepingId`` is ``None`` or empty string.
        :raise FileExistsError: If backup with the specified ``newKeepingId`` already exists.
        :raise FileNotFoundError: If backup with the specified ``keepingId`` does not exist.
        :raise OSError: If a system error occurred."""

        self.raiseIfUnsupportedBackupType_(backupDefinition.backupType)
        if not newKeepingId:
            raise ValueError("Parameter 'newKeepingId' has to be non-empty string")

        currentBackupFilePath = self.getBackupFilePath_(
            backupDefinition.backupId, backupDefinition.backupType, backupDefinition.destination, level, keepingId)
        keptBackupFilePath = self.getBackupFilePath_(
            backupDefinition.backupId, backupDefinition.backupType, backupDefinition.destination, level, newKeepingId)

        if os.path.exists(keptBackupFilePath):
            raise FileExistsError(keptBackupFilePath)
        os.replace(currentBackupFilePath, keptBackupFilePath)



    @property
    def workDir_(self):
        """Gets path to the working directory.

        :rtype: ``str``"""

        return self.__workDir



    @staticmethod
    def getBackupFilePath_(backupId, backupType, destination, level = None, keepingId = None):
        """Assembles the backup file name and returns a path to it.

        :param backupId: ID of the backup for which the path shall be returned.
        :type backupId: ``str``
        :param backupType: Type of the backup.
        :type backupType: :data:`BackupTypes`
        :param destination: Path to the directory where the to the backup shall be created.
        :type destination: ``str``
        :param level: Backup level.
        :type level: ``int``
        :param keepingId: Path of the kept backup with this ID will be returned.  ``None`` if path of the actual (not
           kept) backup shall be returned.
        :type keepingId: ``str``

        :return: Path to the backup file.
        :rtype: ``str``"""

        levelToken = "." + str(level) if level else ""
        keepToken = "." + keepingId if keepingId else ""
        return os.path.join(destination, backupId + levelToken + keepToken + "." +
                                         _BACKUP_TYPES_TO_EXTENSIONS[backupType])



    @classmethod
    def getWorkingPath_(cls, properPath):
        return properPath + cls.__PARTIAL_FILE_SUFFIX



    @classmethod
    def raiseIfUnsupportedBackupType_(cls, backupType):
        """Raises an exception if the passed ``backupType`` is not supported by the implementation.

        See also: :attr:`._TarArchiverProviderBase.supportedBackupTypes`.

        :param backupType: The backup type that shall be checked.
        :type backupType: :data:`.BackupTypes`

        :raise ValueError: If the passed ``backupType`` is not supported by the concrete implementation."""

        if backupType not in cls.supportedBackupTypes:
            raise ValueError(str.format("Unsupported backup type: {}", str(backupType)))



    @classmethod
    def raiseIfUnsupportedFeature_(cls, backupType, compressionStrength = None, level = None):
        for feature in cls.__parametersToFeatures(compressionStrength, level):
            if feature not in cls.getSupportedFeatures(backupType):
                raise RuntimeError(str.format("Feature {} is not supported be the backup type {}.",
                                              str(feature), str(backupType)))



    @classmethod
    def __raiseIfEmptyIncludeFiles(cls, includeFiles):
        if not includeFiles:
            raise RuntimeError("Nothing to backup.")



    @staticmethod
    def __parametersToFeatures(compressionStrength = None, level = None):
        features = set()
        if compressionStrength is not None:
            features.add(ArchiverFeatures.CompressionStrength)
        if level is not None:
            features.add(ArchiverFeatures.Incremental)
        return features

# }}} CLASSES

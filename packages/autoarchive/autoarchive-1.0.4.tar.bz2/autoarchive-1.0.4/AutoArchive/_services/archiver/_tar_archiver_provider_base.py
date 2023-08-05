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

from ..._py_additions import *
from ..._archiving import *

# }}} INCLUDES



# {{{ CONSTANTS

_BACKUP_TYPES_TO_EXTENSIONS = {BackupTypes.Tar: "tar",
                               BackupTypes.TarGz: "tar.gz",
                               BackupTypes.TarBz2: "tar.bz2",
                               BackupTypes.TarXz: "tar.xz"}

# }}} CONSTANTS



# {{{ CLASSES

class _TarArchiverProviderBase(IArchiver):
    """Base class for tar archiver service providers.

    Abstract constructor of this class, should be called from derived constructors.  It initializes the
    :attr:`workDir_` property.

    :param workDir: Path to a writable directory.  The service will use it as persistent storage.
    :type workDir: ``str``"""

    __PARTIAL_FILE_SUFFIX = "._partial"



    @abstractmethod
    def __init__(self, workDir):
        self.__workDir = workDir



    # {{{ IArchiver members

    @event
    def fileAdd(filesystemObjectName):
        "See: :meth:`.IArchiver.fileAdd`."



    @event
    def backupOperationError(operation, error, filesystemObjectName = None, unknownErrorString = None):
        "See: :meth:`.IArchiver.backupOperationError`."



    @abstractmethod
    def backupFiles(self, backupDefinition, compressionStrength = None):
        """Performs basic checks before the backup creation.

        .. note:: Derived classes should call this base method on the beginning of the overridden method.

        See also: :meth:`.IArchiver.backupFiles()`."""

        self.raiseIfUnsupportedBackupType_(backupDefinition.backupType)
        self.raiseIfUnsupportedFeature_(backupDefinition.backupType, compressionStrength)
        self.__raiseIfEmptyIncludeFiles(backupDefinition.includeFiles)



    @abstractmethod
    def backupFilesIncrementally(self, backupDefinition, compressionStrength = None, level = None):
        """Performs basic checks before the incremental backup creation.

        .. note:: Derived classes should call this base method on the beginning of the overridden method.

        See also: :meth:`.IArchiver.backupFilesIncrementally()`."""

        self.raiseIfUnsupportedBackupType_(backupDefinition.backupType)
        self.raiseIfUnsupportedFeature_(backupDefinition.backupType, compressionStrength, 99)
        self.__raiseIfEmptyIncludeFiles(backupDefinition.includeFiles)



    def removeBackup(self, backupDefinition):
        "See: :meth:`.IArchiver.removeBackup()`."

        self.raiseIfUnsupportedBackupType_(backupDefinition.backupType)
        os.remove(self.getBackupFilePath_(
            backupDefinition.backupId, backupDefinition.backupType, backupDefinition.destination))



    def removeBackupIncrements(self, backupDefinition, level = None):
        "See: :meth:`.IArchiver.removeBackupIncrements()`."

        raise NotImplementedError("Not supported.")



    @classmethod
    def getSupportedFeatures(cls, backupType = None):
        "See: :meth:`.IArchiver.getSupportedFeatures()`."

        return frozenset()



    def getMaxBackupLevel(self, backupId):
        "See: :meth:`.IArchiver.getMaxBackupLevel()`."

        raise NotImplementedError("Not supported.")



    def getStoredBackupIds(self):
        "See: :meth:`.IArchiver.getMaxBackupLevel()`."

        return ()



    def purgeStoredBackupData(self, backupId):
        "See: :meth:`.IArchiver.purgeStoredBackupData()`."

        pass

    # }}} IArchiver members



    @property
    def workDir_(self):
        """Gets path to the working directory.

        :rtype: ``str``"""

        return self.__workDir



    @staticmethod
    def getBackupFilePath_(backupId, backupType, destination, level = None):
        """Assembles the backup file name and returns a path to it.

        :param backupId: ID of the backup for which the path shall be returned.
        :type backupId: ``str``
        :param backupType: Type of the backup.
        :type backupType: :data:`BackupTypes`
        :param destination: Path to the directory where the to the backup shall be created.
        :type destination: ``str``
        :param level: Backup level.
        :type level: ``int``

        :return: Path to the backup file.
        :rtype: ``str``"""

        levelToken = "." + str(level) if level else ""
        return os.path.join(destination, backupId + levelToken + "." + _BACKUP_TYPES_TO_EXTENSIONS[backupType])



    @classmethod
    def getWorkingPath_(cls, properPath):
        return properPath + cls.__PARTIAL_FILE_SUFFIX



    @classmethod
    def raiseIfUnsupportedBackupType_(cls, backupType):
        """Raises an exception if the passed ``backupType`` is not supported by the implementation.

        See also: :attr:`.IArchiver.supportedBackupTypes`.

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

# archiver_manipulator.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2017 Róbert Čerňanský



""":class:`ArchiverManipulator` class."""



__all__ = ["ArchiverManipulator"]



# {{{ INCLUDES

import os
from datetime import date

from AutoArchive._infrastructure.configuration import ArchiverTypes, Options, OptionsUtils
from AutoArchive._infrastructure.ui import VerbosityLevels
from AutoArchive._services.archiver import BackupTypes, ArchiverFeatures, BackupOperationErrors, BackupDefinition, \
    BackupSubOperations, ArchiverServiceIdentification
from AutoArchive._application.archiving.archive_spec import ArchiveSpecOptions
from .._archive_info import _BackupLevelRestartReasons
from .._archiving_constants import _ArchiverMaps, _RestartStorageVariables
from ._backup_keeping_manipulations import _BackupKeepingManipulations


# }}} INCLUDES



# {{{ CLASSES

class ArchiverManipulator:
    """Performs actions with backups.

    Uses :class:`._TarArchiverProviderBase`-like services to manipulate with or create backups.

    .. note:: ``backupInformationProvider`` is not updated by this class.

    :param backupInformationProvider: Represents the archive that this instance shall be manipulating with.
    :type backupInformationProvider`: :class:`._BackupInformationProvider`
    :param componentUi: Access to user interface.
    :type componentUi: :class:`.CmdlineUi`
    :param storage: Application storage.
    :type storage: :class:`.FileStorage`
    :param serviceAccessor: Access to services.
    :type serviceAccessor: :class:`.ServiceAccessor`

    :raise RuntimeError: If the archiver service could not be created."""

    __ARCHIVER_TYPE_TO_BACKUP_TYPE_MAP = {ArchiverTypes.Tar: BackupTypes.Tar,
                                          ArchiverTypes.TarGz: BackupTypes.TarGz,
                                          ArchiverTypes.TarBz2: BackupTypes.TarBz2,
                                          ArchiverTypes.TarXz: BackupTypes.TarXz,
                                          ArchiverTypes.TarInternal: BackupTypes.Tar,
                                          ArchiverTypes.TarGzInternal: BackupTypes.TarGz,
                                          ArchiverTypes.TarBz2Internal: BackupTypes.TarBz2}

    __OPTION_TO_FEATURE_MAP = {Options.COMPRESSION_LEVEL: ArchiverFeatures.CompressionStrength,
                               Options.INCREMENTAL: ArchiverFeatures.Incremental}



    def __init__(self, backupInformationProvider, componentUi, storage, serviceAccessor):
        self.__backupInformationProvider = backupInformationProvider
        self.__componentUi = componentUi
        self.__serviceAccessor = serviceAccessor
        self.__archiveSpec = self.__backupInformationProvider.archiveSpec
        self.__storagePortion = None
        self.__archiverService = None
        self.__backupOperationStatus = None

        self.__storagePortion = storage.createStoragePortion(realm = self.__archiveSpec[ArchiveSpecOptions.NAME])

        providersIdentifications = self.__serviceAccessor.getProvidersIdentifications(ArchiverServiceIdentification)
        providerIdentification = [pi for pi in providersIdentifications if
                                  pi.providerId == _ArchiverMaps.ARCHIVER_TYPE_TO_SERVICE_MAP[
                                      self.__archiveSpec[Options.ARCHIVER]]][0]
        self.__archiverService = self.__serviceAccessor.getOrCreateService(
            ArchiverServiceIdentification, providerIdentification, self.__archiveSpec[Options.USER_CONFIG_DIR])

        self.__backupKeepingManipulations = _BackupKeepingManipulations(
            self.__archiveSpec, self.__componentUi, self.__archiverService)

        self.__reportUnsupportedOptions()



    def createBackup(self):
        """Runs the :term:`archiver` and creates a :term:`backup`.

        :return: Path to the created backup.
        :rtype: ``str``

        :raise RuntimeError: If the backup operation was aborted due to a fatal error.
        :raise OSError: If a system error occurred while making the backup."""

        backupDefinition = self.__createAndPopulateBackupDefinition()

        self.__backupOperationStatus = True
        self.__archiverService.backupOperationError += self.__onBackupOperationError
        if self.__componentUi.verbosity == VerbosityLevels.Verbose:
            self.__archiverService.fileAdd += self.__onFileAdd

        overwriteAtStart = self.__archiveSpec[Options.OVERWRITE_AT_START]
        compressionLevel = self.__archiveSpec[Options.COMPRESSION_LEVEL] \
            if self.isOptionSupported(Options.COMPRESSION_LEVEL) else None
        try:
            if self.__archiveSpec[Options.INCREMENTAL] and self.isOptionSupported(Options.INCREMENTAL):
                self.__reportBackupLevelRestart()
                self.__reportBackupLevelTooHigh()
                self.__backupKeepingManipulations.keepOldIncrementalBackups(
                    backupDefinition, self.__backupInformationProvider.nextBackupLevel)

                backupFilePath = self.__archiverService.backupFilesIncrementally(
                    backupDefinition, compressionLevel, self.__backupInformationProvider.nextBackupLevel,
                    overwriteAtStart)

                if self.__archiveSpec[Options.REMOVE_OBSOLETE_BACKUPS]:
                    self.__archiverService.removeBackupIncrements(
                        backupDefinition, self.__backupInformationProvider.nextBackupLevel + 1)
            else:
                self.__backupKeepingManipulations.keepOldBackups(backupDefinition)

                backupFilePath = self.__archiverService.backupFiles(
                    backupDefinition, compressionLevel, overwriteAtStart)

        finally:
            if self.__componentUi.verbosity == VerbosityLevels.Verbose:
                self.__archiverService.fileAdd -= self.__onFileAdd
            self.__archiverService.backupOperationError -= self.__onBackupOperationError

        if not self.__backupOperationStatus:
            self.__componentUi.showVerbose(
                "Error(s) occurred during the backup creation. Please check program's output.")

        return backupFilePath



    def saveBackupLevelInfo(self, backupFilePath):
        """Saves all the information required for backup level restarting to the persistent storage.

        .. note:: This method should be called only once after the backup was created.

        :param backupFilePath: Path to the created backup.
        :type backupFilePath: ``str``"""

        if not self.__archiveSpec[Options.INCREMENTAL] or not self.isOptionSupported(Options.INCREMENTAL) or \
           not self.__archiveSpec[Options.RESTARTING]:
            return

        # increase and save restart count
        if self.__backupInformationProvider.restartReason is not _BackupLevelRestartReasons.NoRestart:
            # SMELL: Detect when restarting was enabled and initialize all variables on a single place.
            if not self.__storagePortion.hasVariable(_RestartStorageVariables.RESTART_COUNT):
                self.__storagePortion.saveValue(_RestartStorageVariables.RESTART_COUNT, 0)
            restartCount = int(self.__storagePortion.getValue(_RestartStorageVariables.RESTART_COUNT))
            self.__storagePortion.saveValue(_RestartStorageVariables.RESTART_COUNT, str(restartCount + 1))

        # save last restart date
        today = date.today()
        if self.__backupInformationProvider.nextBackupLevel < 2 or \
            self.__backupInformationProvider.restartReason is not _BackupLevelRestartReasons.NoRestart:

            self.__storagePortion.saveValue(_RestartStorageVariables.LAST_RESTART, today)
            if self.__backupInformationProvider.nextBackupLevel == 0:
                self.__storagePortion.saveValue(_RestartStorageVariables.LAST_FULL_RESTART, today)
                self.__storagePortion.saveValue(_RestartStorageVariables.RESTART_COUNT, "0")

        # save the size of the created backup
        archiveSize = os.path.getsize(backupFilePath)
        self.__storagePortion.saveValue(_RestartStorageVariables.BACKUP_SIZE +
                                        str(self.__backupInformationProvider.nextBackupLevel), archiveSize)

        # >clear stored backup sizes for higher levels
        levelIdx = self.__backupInformationProvider.nextBackupLevel + 1
        while self.__storagePortion.tryRemoveVariable(_RestartStorageVariables.BACKUP_SIZE + str(levelIdx)):
            levelIdx += 1



    def isOptionSupported(self, option):
        """Returns ``True`` if the passed ``option`` is supported by the current configuration of this instance.

        Whether an option is supported or not depends on the archiver type set in the archive specification file
        that is currently attached.

        :param option: The option which shall be tested for support.
        :type option: :class:`.Option`

        :return: ``True`` if the passed ``option`` is supported; ``False`` otherwise.
        :rtype: ``bool``"""

        return self.__OPTION_TO_FEATURE_MAP[option] in self.__archiverService.getSupportedFeatures(
            self.__ARCHIVER_TYPE_TO_BACKUP_TYPE_MAP[self.__archiveSpec[Options.ARCHIVER]]) \
            if option in self.__OPTION_TO_FEATURE_MAP else True



    # SMELL: Should be in a separate class (for stored data manipulations).  Service accessor is already an instance
    # variable.
    @staticmethod
    def tryPurgeStoredArchiveData(archiveName, userConfigDir, storage, serviceAccessor):
        """Deletes all data stored for the archive named ``archiveName`` if any.

        See also: :meth:`._BackupInformationProvider.getStoredArchiveNames()`

        :param archiveName: Name of the archive which data shall be purged.
        :type archiveName: ``str``
        :param userConfigDir: Path to the user configuration directory.
        :type userConfigDir: ``str``
        :param storage: The application storage.
        :type storage: :class:`.IStorage`
        :param serviceAccessor: Service accessor.
        :type serviceAccessor: :class:`.IServiceAccessor`

        :return: ``True`` if data was purged; ``False`` otherwise.
        :rtype: ``bool``

        :raise RuntimeError: If the archiver service could not be created.
        :raise OSError: If an error occurred during the operation of removing data from a physical storage."""

        archiveDataStored = False
        for providerIdentification in serviceAccessor.getProvidersIdentifications(ArchiverServiceIdentification):
            archiverService = serviceAccessor.getOrCreateService(ArchiverServiceIdentification, providerIdentification,
                                                                 userConfigDir)
            archiveDataStored = archiveDataStored or archiveName in archiverService.getStoredBackupIds()
            archiverService.purgeStoredBackupData(archiveName)

        try:
            storage.removeRealm(archiveName)
            return True
        except KeyError:
            return False or archiveDataStored



    # {{{ helpers

    def __onBackupOperationError(self, operation, error, filesystemObjectName = None, unknownErrorString = None):
        if operation == BackupSubOperations.Stat and error == BackupOperationErrors.PermissionDenied:
            self.__showError(str.format("Cannot access \"{}\". Permission denied.", filesystemObjectName))
        elif operation == BackupSubOperations.Open and error == BackupOperationErrors.PermissionDenied:
            self.__showError(str.format("Cannot open file \"{}\". Permission denied.", filesystemObjectName))
        elif operation == (BackupSubOperations.Stat or operation == BackupSubOperations.Open or
                           operation == BackupSubOperations.Read or BackupSubOperations.UnknownFileOperation) and \
             (error == BackupOperationErrors.UnknownError or BackupOperationErrors.UnknownOsError):
            self.__showError(str.format("Error occurred while accessing file \"{}\". {}", filesystemObjectName,
                             unknownErrorString))
        elif operation == BackupSubOperations.Read and error == BackupOperationErrors.FileChanged:
            self.__componentUi.showWarning(str.format("File changed as we read it: \"{}\".", filesystemObjectName))
        elif error == BackupOperationErrors.SocketIgnored:
            self.__componentUi.showWarning(str.format("Socket ignored: \"{}\".", filesystemObjectName))
        elif error == BackupOperationErrors.UnknownTypeIgnored:
            self.__componentUi.showWarning(str.format("Unknown file type ignored: \"{}\".", filesystemObjectName))
        elif operation == BackupSubOperations.Read and error == BackupOperationErrors.DirectoryRenamed:
            self.__componentUi.showVerbose(str.format("Directory has been renamed: \"{}\".", filesystemObjectName))
        elif operation == BackupSubOperations.Finish and error == BackupOperationErrors.SomeFilesChanged:
            self.__componentUi.showWarning("Some files were changed during the backup creation.")
        elif operation == BackupSubOperations.UnknownFileOperation and error == BackupOperationErrors.UnknownOsError:
            self.__showError(str.format("A system error occurred while accessing file \"{}\": {}",
                                        filesystemObjectName, unknownErrorString))
        elif operation == BackupSubOperations.UnknownFileOperation and error == BackupOperationErrors.UnknownError:
            self.__showError(str.format("An error occurred while accessing file \"{}\": {}",
                                        filesystemObjectName, unknownErrorString))
        elif error == BackupOperationErrors.UnknownOsError:
            self.__showError(str.format("A system error occurred: {}", unknownErrorString))
        elif error == BackupOperationErrors.UnknownError:
            self.__showError(str.format("An error occurred: {}", unknownErrorString))
        else:
            self.__showError(str.format("An unknown error occurred: {}, {}, {}, {}!", operation, error,
                                        filesystemObjectName, unknownErrorString))



    def __onFileAdd(self, filesystemObjectName):
        self.__componentUi.showVerbose(filesystemObjectName)



    def __createAndPopulateBackupDefinition(self):
        backupDefinition = BackupDefinition()
        backupDefinition.backupId = self.__archiveSpec[ArchiveSpecOptions.NAME]
        backupDefinition.backupType = self.__ARCHIVER_TYPE_TO_BACKUP_TYPE_MAP[self.__archiveSpec[Options.ARCHIVER]]
        backupDefinition.destination = self.__archiveSpec[Options.DEST_DIR]
        backupDefinition.root = self.__archiveSpec[ArchiveSpecOptions.PATH]
        backupDefinition.includeFiles = self.__archiveSpec[ArchiveSpecOptions.INCLUDE_FILES]
        backupDefinition.excludeFiles = self.__archiveSpec[ArchiveSpecOptions.EXCLUDE_FILES]
        return backupDefinition



    def __reportUnsupportedOptions(self):
        for option in self.__OPTION_TO_FEATURE_MAP:
            if self.__archiveSpec.getRawValue(option) is not None and not self.isOptionSupported(option):
                self.__componentUi.showWarning(str.format(
                    "Option \"{}\" is not supported by the archiver of type \"{}\".",
                    option, OptionsUtils.archiverTypeToStr(self.__archiveSpec[Options.ARCHIVER])))



    def __reportBackupLevelRestart(self):
        """Shows a user message for current :attr:`restartReason`."""

        if self.__backupInformationProvider.restartReason is _BackupLevelRestartReasons.NoRestart:
            return

        if self.__backupInformationProvider.restartReason is _BackupLevelRestartReasons.RestartCountLimitReached:
            self.__componentUi.showWarning("Maximal backup level restart count reached. Restarting to level 0.")
        elif self.__backupInformationProvider.restartReason is _BackupLevelRestartReasons.LastFullRestartAgeLimitReached:
            self.__componentUi.showWarning("Maximal backup level full restart age reached. Restarting to level 0.")
        elif self.__backupInformationProvider.restartReason is _BackupLevelRestartReasons.BackupLevelLimitReached:
            self.__componentUi.showWarning(str.format("Maximal backup level reached. Restarting to level {}.",
                                                     self.__backupInformationProvider.nextBackupLevel))
        elif self.__backupInformationProvider.restartReason is _BackupLevelRestartReasons.LastRestartAgeLimitReached:
            self.__componentUi.showWarning(str.format(
                "Maximal backup level restart age reached. Restarting to level {}.",
                self.__backupInformationProvider.nextBackupLevel))



    def __reportBackupLevelTooHigh(self):
        configuredBackupLevel = self.__archiveSpec[Options.LEVEL]
        nextBackupLevel = self.__backupInformationProvider.nextBackupLevel
        if configuredBackupLevel is not None and configuredBackupLevel > nextBackupLevel:
            self.__componentUi.showWarning(str.format(
                "Backup level value {} is too high. Using level {} instead.", configuredBackupLevel, nextBackupLevel))



    def __showError(self, message):
        self.__componentUi.showError(message)
        self.__backupOperationStatus = False

    # }}} helpers

# }}} CLASSES

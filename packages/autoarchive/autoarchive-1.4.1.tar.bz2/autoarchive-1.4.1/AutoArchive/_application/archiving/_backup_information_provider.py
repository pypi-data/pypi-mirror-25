# _backup_information_provider.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2017 Róbert Čerňanský



""":class:`_BackupInformationProvider` class."""



__all__ = ["_BackupInformationProvider"]



# {{{ INCLUDES

import itertools
from datetime import date, datetime

from AutoArchive._infrastructure.configuration import Options
from AutoArchive._services.archiver import ArchiverFeatures, ArchiverServiceIdentification

from AutoArchive._application.archiving.archive_spec import ArchiveSpecOptions
from ._archive_info import _BackupLevelRestartReasons
from ._archiving_constants import _ArchiverMaps, _RestartStorageVariables

# }}} INCLUDES



# {{{ CLASSES

class _BackupInformationProvider:
    """Provides information about backups.

    :param archiveSpec: Archive specification of the backup that this instance will provide information about.
    :type archiveSpec: :class:`.ArchiveSpec`
    :param storage: Application storage.
    :type storage: :class:`.IStorage`
    :param componentUi: Access to the user interface.
    :type componentUi: :class:`.CmdlineUi`
    :param serviceAccessor: An :class:`.IServiceAccessor` instance.
    :type serviceAccessor: :class:`.IServiceAccessor`

    :raise RuntimeError: If the archiver service could not be created.
    :raise OSError: If a system error occurred."""



    def __init__(self, archiveSpec, componentUi, storage, serviceAccessor):
        self.__serviceAccessor = serviceAccessor

        self.__archiveSpec = archiveSpec
        self.__componentUi = componentUi
        self.__maxBackupLevel = None
        self.__nextBackupLevel = None
        self.__restartReason = None
        self.__restartLevel = None

        # SMELL: Similar initialization is done also in ArchiverManipulator.
        self.__storagePortion = storage.createStoragePortion(realm = self.__archiveSpec[ArchiveSpecOptions.NAME])

        self.__archiverService = self.__getOrCreateArchiverService(self.__archiveSpec[Options.ARCHIVER],
                                                                   self.__archiveSpec[Options.USER_CONFIG_DIR])

        if ArchiverFeatures.Incremental in self.__archiverService.getSupportedFeatures():
            self.__maxBackupLevel = self.__archiverService.getMaxBackupLevel(
                self.__archiveSpec[ArchiveSpecOptions.NAME])
            self.__restartLevel = self.__getRestartLevel()
            self.__nextBackupLevel, self.__restartReason = self.__getNextBackupLevelAndRestartReason()



    @property
    def archiveSpec(self):
        """Gets the archive specification that corresponds to the backup about which this instance provides information.

        :rtype: :class:`.ArchiveSpec`"""

        return self.__archiveSpec



    @property
    def currentBackupLevel(self):
        """Gets the current backup level or ``None``.

        :rtype: ``int``"""

        if self.__maxBackupLevel is not None:
            return self.__maxBackupLevel - 1 if self.__maxBackupLevel > 0 else None
        else:
            return None



    @property
    def nextBackupLevel(self):
        """Gets the backup level that would be created if the backup creation was triggered.

        :rtype: ``int``"""

        return self.__nextBackupLevel



    @property
    def restartReason(self):
        """Gets the reason for upcoming backup level restart.

        :rtype: :attr:`_BackupLevelRestartReasons`"""

        return self.__restartReason



    @property
    def restartLevel(self):
        """Gets a :term:`backup level` to which a next restart would be done.

        :rtype: ``int``"""

        return self.__restartLevel



    def getLastRestartDate(self):
        """Reads the last restart date from the persistent storage and returns it.

        :return: Date of the last backup level restart.
        :rtype: ``datetime.date``"""

        self.getRestartDate(_RestartStorageVariables.LAST_RESTART, self.__storagePortion)



    def getLastFullRestartDate(self):
        """Reads the last full restart date from the persistent storage and returns it.

        :return: Date of the last full backup level restart.
        :rtype: ``datetime.date``"""

        self.getRestartDate(_RestartStorageVariables.LAST_FULL_RESTART, self.__storagePortion)



    @staticmethod
    def getRestartDate(storageVariable, storagePortion):
        """Reads the date of a backup level restart from storage and returns it.

        :param storageVariable: Variable that holds the restart date in the persistent storage.
        :type storageVariable: ``str``
        :param storagePortion: The persistent storage where the variable is located.
        :type storagePortion: :class:`.IStoragePortion`
        :return: A backup level restart date.
        :rtype: ``datetime.date``"""

        if storagePortion.hasVariable(storageVariable):
            return datetime.strptime(storagePortion.getValue(storageVariable), "%Y-%m-%d").date()
        else:
            return None



    # SMELL: Should be in a separate class (StoredBackupInfoProvider?)
    @staticmethod
    def getStoredArchiveNames(userConfigDir, storage, serviceAccessor):
        """Returns iterable of archive names which has some data stored in a persistent storage.

        Persistent storages from which archive names are retrieved are specific to the concrete archiver service.
        A typical storage used by archivers is the application storage (:class:`.IStorage`).

        :param userConfigDir: Path to the user configuration directory.
        :type userConfigDir: ``str``
        :param storage: The application storage.
        :type storage: :class:`.IStorage`
        :param serviceAccessor: Service accessor.
        :type serviceAccessor: :class:`.IServiceAccessor`

        :return: Set of archive names.
        :rtype: ``set<str>``

        :raise RuntimeError: If the archiver service could not be created."""

        archiveNames = set()
        for providerIdentification in serviceAccessor.getProvidersIdentifications(ArchiverServiceIdentification):
            archiverService = serviceAccessor.getOrCreateService(
                ArchiverServiceIdentification, providerIdentification, userConfigDir)
            archiveNames |= set(archiverService.getStoredBackupIds())

        return set(itertools.chain(storage.getRealms(), archiveNames))



    # SMELL: Should be in a separate class (StoredBackupInfoProvider?)
    @staticmethod
    def getBackupLevelForBackup(archiveName, userConfigDir, serviceAccessor):
        """Returns current backup level for the passed ``archiveName``.

        :param archiveName: Name of the archive for which the backup level shall be returned.
        :type archiveName: ``str``
        :param userConfigDir: Path to the user configuration directory.
        :type userConfigDir: ``str``
        :param serviceAccessor: Service accessor.
        :type serviceAccessor: :class:`.IServiceAccessor`

        :return: Current backup level for ``archiveName`` or None
        :rtype: ``int``

        :raise RuntimeError: If the archiver service could not be created.
        :raise OSError: If a system error occurred."""

        backupLevel = None

        for providerIdentification in serviceAccessor.getProvidersIdentifications(ArchiverServiceIdentification):
            if ArchiverFeatures.Incremental in providerIdentification.getSupportedFeatures():
                archiverService = serviceAccessor.getOrCreateService(
                    ArchiverServiceIdentification, providerIdentification, userConfigDir)
                backupLevel = archiverService.getMaxBackupLevel(archiveName)
                if backupLevel > 0:
                    break

        return backupLevel - 1 if backupLevel > 0 else None



    def __getNextBackupLevelAndRestartReason(self):
        configuredBackupLevel = self.__archiveSpec[Options.LEVEL]
        nextBackupLevel = self.__maxBackupLevel \
            if (configuredBackupLevel is None or configuredBackupLevel > self.__maxBackupLevel) \
            else configuredBackupLevel
        restartReason = _BackupLevelRestartReasons.NoRestart

        if self.__archiveSpec[Options.RESTARTING] and configuredBackupLevel is None:
            nextBackupLevel, restartReason = self.__restartBackupLevel(nextBackupLevel)

        return nextBackupLevel, restartReason



    def __restartBackupLevel(self, nextLevel):
        """Restarts the passed ``nextLevel`` backup level for ``backupId`` if needed.

        :param nextLevel: Next backup level if it would not be restarted.
        :type nextLevel: ``int``

        :return: Backup level after restart and the reason for the restart.
        :rtype: ``tuple[int, _BackupLevelRestartReasons]``"""

        # full restart handling
        if nextLevel < 1:
            return nextLevel, _BackupLevelRestartReasons.NoRestart

        if self.__archiveSpec[Options.FULL_RESTART_AFTER_COUNT]:
            if not self.__storagePortion.hasVariable(_RestartStorageVariables.RESTART_COUNT):
                # TODO: Restarting with FULL_RESTART_AFTER_COUNT could have been enabled on to already existing
                # archive which has some levels of backup and which has not enabled restarting before.  In such case
                # it is normal that RESTART_COUNT will not exist in storage.  It should not be an error.  Check also
                # other cases below.
                self.__componentUi.showError("Unable to read the restart count. Setting it to 0.")
                self.__storagePortion.saveValue(_RestartStorageVariables.RESTART_COUNT, 0)
            if int(self.__storagePortion.getValue(_RestartStorageVariables.RESTART_COUNT)) >= \
               self.__archiveSpec[Options.FULL_RESTART_AFTER_COUNT]:
                return 0, _BackupLevelRestartReasons.RestartCountLimitReached

        today = date.today()
        if self.__archiveSpec[Options.FULL_RESTART_AFTER_AGE]:
            if not self.__storagePortion.hasVariable(_RestartStorageVariables.LAST_FULL_RESTART):
                self.__componentUi.showError("Unable to read the last full restart date. Setting it to today.")
                self.__storagePortion.saveValue(_RestartStorageVariables.LAST_FULL_RESTART, today)

            if (today - self.getRestartDate(_RestartStorageVariables.LAST_FULL_RESTART, self.__storagePortion)).days > \
               self.__archiveSpec[Options.FULL_RESTART_AFTER_AGE]:
                return 0, _BackupLevelRestartReasons.LastFullRestartAgeLimitReached

        # standard restart handling
        if nextLevel < 2:
            return nextLevel, _BackupLevelRestartReasons.NoRestart

        if nextLevel > self.__archiveSpec[Options.RESTART_AFTER_LEVEL]:
            return self.restartLevel, _BackupLevelRestartReasons.BackupLevelLimitReached

        if self.__archiveSpec[Options.RESTART_AFTER_AGE]:
            if not self.__storagePortion.hasVariable(_RestartStorageVariables.LAST_RESTART):
                self.__componentUi.showError("Unable to read the last restart date. Setting it to today.")
                self.__storagePortion.saveValue(_RestartStorageVariables.LAST_RESTART, today)

            if (today - self.getRestartDate(_RestartStorageVariables.LAST_RESTART, self.__storagePortion)).days > \
               self.__archiveSpec[Options.RESTART_AFTER_AGE]:
                return self.restartLevel, _BackupLevelRestartReasons.LastRestartAgeLimitReached

        return nextLevel, _BackupLevelRestartReasons.NoRestart



    def __getRestartLevel(self):
        """Returns the :term:`backup level` to which would the backup with ``backupId`` be restarted.

        The restart backup level is determined based on the backup file size.  Full restart is not taken into
        account; the returned value will always be > 0.

        :return: The restart-target backup level.
        :rtype: ``int``"""

        maxRestartLevelSize = self.__archiveSpec[Options.MAX_RESTART_LEVEL_SIZE]

        if not maxRestartLevelSize:
            return 1

        # if no backup was created yet
        if not self.__storagePortion.hasVariable(_RestartStorageVariables.BACKUP_SIZE + "0"):
            return 1

        level0Size = self.__getArchiveSizeOrSetToZero()
        restartLevel = 1
        if level0Size > 0:
            while (restartLevel < self.__maxBackupLevel - 1) and \
                  (self.__getArchiveSizeOrSetToZero(restartLevel) / level0Size) * 100 > maxRestartLevelSize:
                restartLevel += 1

        return restartLevel



    def __getArchiveSizeOrSetToZero(self, level = 0):
        archiveSize = 0
        backupSizeVariable = _RestartStorageVariables.BACKUP_SIZE + str(level)
        if self.__storagePortion.hasVariable(backupSizeVariable):
            archiveSize = int(self.__storagePortion.getValue(backupSizeVariable))
        else:
            self.__componentUi.showWarning(str.format("Unable to obtain size of the level {} backup file.", level))
            self.__storagePortion.saveValue(backupSizeVariable, 0)
        return archiveSize



    def __getOrCreateArchiverService(self, archiverType, workDir):
        providersIdentifications = self.__serviceAccessor.getProvidersIdentifications(ArchiverServiceIdentification)
        providerIdentification = [pi for pi in providersIdentifications
                                  if pi.providerId == _ArchiverMaps.ARCHIVER_TYPE_TO_SERVICE_MAP[archiverType]][0]
        return self.__serviceAccessor.getOrCreateService(ArchiverServiceIdentification, providerIdentification, workDir)

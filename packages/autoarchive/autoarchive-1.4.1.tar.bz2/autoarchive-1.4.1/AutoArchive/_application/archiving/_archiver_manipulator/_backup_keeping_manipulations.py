# _backup_keeping_manipulations.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2017 Róbert Čerňanský



""":class:`_BackupKeepingManipulations` class."""



__all__ = ["_BackupKeepingManipulations"]



# {{{ INCLUDES

from AutoArchive._infrastructure.configuration import Options
from ._keeping_id_operations import _KeepingIdOperations

# }}} INCLUDES



# {{{ CLASSES

# SMELL: Incremental backups removal logic is in the service layer while the backup keeping removal logic is here
# in the application level.  Maybe _TarArchiverProviderBase.removeBackupIncrements should be implemented in the
# application level and removeBackup should have parameter level.
class _BackupKeepingManipulations:
    """Operations for keeping old backups.

    :param archiveSpec: Archive specification of the backup that this instance will operate on.
    :type archiveSpec: :class:`.ArchiveSpec`
    :param componentUi: Component UI instance.
    :type componentUi: :class:`.CmdlineUi`
    :param archiverService: Archiver service to use for operations with the backup.
    :type archiverService: :class:`._TarArchiverProviderBase`"""

    def __init__(self, archiveSpec, componentUi, archiverService):
        self.__archiveSpec = archiveSpec
        self.__componentUi = componentUi
        self.__archiverService = archiverService



    # SMELL: backupDefinition has to be populated from the same _ArchiveSpec instance as passed to the constructor.
    def keepOldBackups(self, backupDefinition):
        """Keeps old backups according configuration settings.

        :param backupDefinition: Provides information about backup which shall be kept.  It has to be populated
           from the same :class:`.ArchiveSpec` instance as passed to the constructor.
        :type backupDefinition: :class:`.BackupDefinition`"""

        if self.__archiveSpec[Options.KEEP_OLD_BACKUPS]:
            numberOfOldBackups = self.__archiveSpec[Options.NUMBER_OF_OLD_BACKUPS]

            if numberOfOldBackups > _KeepingIdOperations.maxKeepingIdAsInt + 1:
                self.__componentUi.showWarning(str.format(
                    "Configured number of old backups ({}) exceed maximal possible value ({}). Using the maximal " +
                    "possible value.", numberOfOldBackups, _KeepingIdOperations.maxKeepingIdAsInt + 1))
                numberOfOldBackups = _KeepingIdOperations.maxKeepingIdAsInt + 1

            if self.__archiverService.doesBackupExist(backupDefinition):
                if numberOfOldBackups > 0:
                    self.__componentUi.showInfo("Keeping already existing backups.")
                    try:
                        self.__shiftBackup(backupDefinition, numberOfOldBackups)
                    except FileExistsError:
                        self.__componentUi.showError(str.format("Unable to create file \"{}\" while keeping a backup."))
                else:
                    self.__componentUi.showWarning("Keeping of old backups is enabled but the number to keep is " +
                                                   "0. No backups will be kept.")
            self.__removeKeptObsoleteBackups(backupDefinition, numberOfOldBackups)



    def keepOldIncrementalBackups(self, backupDefinition, fromLevel):
        """Keeps old incremental backups according configuration settings.

        :param backupDefinition: Provides information about backup which shall be kept.  It has to be populated
           from the same :class:`.ArchiveSpec` instance as passed to the constructor.
        :type backupDefinition: :class:`.BackupDefinition`"""

        if self.__archiveSpec[Options.KEEP_OLD_BACKUPS]:
            numberOfOldBackups = self.__archiveSpec[Options.NUMBER_OF_OLD_BACKUPS]

            if numberOfOldBackups > _KeepingIdOperations.maxKeepingIdAsInt + 1:
                self.__componentUi.showWarning(str.format(
                    "Configured number of old backups ({}) exceed maximal possible value ({}). Using the maximal " +
                    "possible value.", numberOfOldBackups, _KeepingIdOperations.maxKeepingIdAsInt + 1))
                numberOfOldBackups = _KeepingIdOperations.maxKeepingIdAsInt + 1

            if self.__archiverService.doesAnyBackupLevelExist(backupDefinition, fromLevel):
                if numberOfOldBackups > 0:
                    self.__componentUi.showInfo("Keeping already existing backups.")
                    try:
                        self.__shiftIncrementalBackup(backupDefinition, numberOfOldBackups, fromLevel)
                    except FileExistsError:
                        self.__componentUi.showError(str.format("Unable to create file \"{}\" while keeping a backup."))
                else:
                    self.__componentUi.showWarning("Keeping of old backups is enabled but the number to keep is " +
                                                   "0. No backups will be kept.")
            self.__removeKeptObsoleteIncrementalBackups(backupDefinition, numberOfOldBackups)



    def __shiftBackup(self, backupDefinition, numberOfOldBackups, keepingId = None):
        newKeepingId = _KeepingIdOperations.getNextKeepingId(keepingId)
        currentNumberOfOldBackups = _KeepingIdOperations.keepingIdToInt(newKeepingId) + 1
        if self.__archiverService.doesBackupExist(backupDefinition, keepingId = newKeepingId):
            if currentNumberOfOldBackups < numberOfOldBackups:
                self.__shiftBackup(backupDefinition, numberOfOldBackups, newKeepingId)
            elif currentNumberOfOldBackups == numberOfOldBackups:
                self.__componentUi.showInfo(str.format("Removing kept backup with keeping ID \"{}\".", newKeepingId))
                self.__archiverService.removeBackup(backupDefinition, newKeepingId)

        if _KeepingIdOperations.keepingIdToInt(newKeepingId) + 1 <= numberOfOldBackups:
            self.__archiverService.keepBackup(backupDefinition, keepingId, newKeepingId)



    def __removeKeptObsoleteBackups(self, backupDefinition, numberOfOldBackups):
        if self.__archiveSpec[Options.REMOVE_OBSOLETE_BACKUPS]:
            obsoleteKeepingId = _KeepingIdOperations.intToKeepingId(numberOfOldBackups)
            for keepingIdNumber in range(_KeepingIdOperations.keepingIdToInt(obsoleteKeepingId),
                                         _KeepingIdOperations.maxKeepingIdAsInt):
                keepingId = _KeepingIdOperations.intToKeepingId(keepingIdNumber)
                if self.__archiverService.doesBackupExist(backupDefinition, keepingId = keepingId):
                    self.__componentUi.showInfo(str.format(
                        "Removing obsolete kept backup with keeping ID \"{}\".", keepingId))
                    self.__archiverService.removeBackup(backupDefinition, keepingId)



    def __shiftIncrementalBackup(self, backupDefinition, numberOfOldBackups, fromLevel, keepingId = None):
        newKeepingId = _KeepingIdOperations.getNextKeepingId(keepingId)
        currentNumberOfOldBackups = _KeepingIdOperations.keepingIdToInt(newKeepingId) + 1
        firstExistingBackupLevel = self.__findFirstExistingBackupLevel(backupDefinition, 0, newKeepingId)
        if firstExistingBackupLevel is not None:
            if currentNumberOfOldBackups < numberOfOldBackups:
                self.__shiftIncrementalBackup(backupDefinition, numberOfOldBackups, firstExistingBackupLevel,
                                              newKeepingId)
            elif currentNumberOfOldBackups == numberOfOldBackups:
                self.__componentUi.showInfo(str.format("Removing kept incremental backup with keeping ID \"{}\".",
                                                       newKeepingId))
                self.__archiverService.removeBackupIncrements(backupDefinition, firstExistingBackupLevel, newKeepingId)

        if _KeepingIdOperations.keepingIdToInt(newKeepingId) + 1 <= numberOfOldBackups:
            for level in self.__iterateExistingBackupLevels(backupDefinition, fromLevel, keepingId):
                self.__archiverService.keepBackup(backupDefinition, keepingId, newKeepingId, level)



    def __removeKeptObsoleteIncrementalBackups(self, backupDefinition, numberOfOldBackups):
        if self.__archiveSpec[Options.REMOVE_OBSOLETE_BACKUPS]:
            obsoleteKeepingId = _KeepingIdOperations.intToKeepingId(numberOfOldBackups)
            for keepingIdNumber in range(_KeepingIdOperations.keepingIdToInt(obsoleteKeepingId),
                                         _KeepingIdOperations.maxKeepingIdAsInt):
                keepingId = _KeepingIdOperations.intToKeepingId(keepingIdNumber)
                firstExistingBackupLevel = self.__findFirstExistingBackupLevel(backupDefinition, 0, keepingId)
                if firstExistingBackupLevel is not None:
                    self.__componentUi.showInfo(str.format(
                        "Removing obsolete kept incremental backup with keeping ID \"{}\".", keepingId))
                    self.__archiverService.removeBackupIncrements(backupDefinition, firstExistingBackupLevel, keepingId)



    def __findFirstExistingBackupLevel(self, backupDefinition, fromLevel, keepingId = None):
        level = None
        if self.__archiverService.doesAnyBackupLevelExist(backupDefinition, fromLevel, keepingId):
            level = fromLevel
            # SMELL: Prevent endless loop? (Which can happen if backups are removed in the meantime.)
            # SMELL: Low performance.
            while not self.__archiverService.doesBackupExist(backupDefinition, level, keepingId):
                level += 1
        return level



    def __iterateExistingBackupLevels(self, backupDefinition, fromLevel, keepingId = None):
        level = self.__findFirstExistingBackupLevel(backupDefinition, fromLevel, keepingId)
        while self.__archiverService.doesBackupExist(backupDefinition, level, keepingId):
            yield level
            level += 1

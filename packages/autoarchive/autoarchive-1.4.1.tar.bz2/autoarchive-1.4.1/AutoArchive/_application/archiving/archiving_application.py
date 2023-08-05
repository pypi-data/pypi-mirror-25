# archiving_application.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2016 Róbert Čerňanský



""":class:`ArchivingApplication`."""



__all__ = ["ArchivingApplication"]



# {{{ INCLUDES

import itertools
from datetime import date

from AutoArchive._infrastructure.utils import Utils
from AutoArchive._infrastructure.py_additions import Enum
from AutoArchive._infrastructure.ui import UiMessageKinds, VerbosityLevels, MultiFieldLine, DisplayField, \
    FieldStretchiness
from AutoArchive._infrastructure.configuration import Options, OptionsUtils
from AutoArchive._services.external_command_executor import ExternalCommandExecutorServiceIdentification
from ._command_executor import _CommandExecutor
from ._archive_info import _BackupLevelRestartReasons
from ._archiving import _Archiving

# }}} INCLUDES



# {{{ CLASSES

class ArchivingApplication:
    """Takes care of executing user actions - application main use cases.

    :param componentUi: Access to user interface.
    :type componentUi: :class:`.CmdlineUi`
    :param applicationContext: Application context.
    :type applicationContext: :class:`.ApplicationContext`
    :param serviceAccessor: Access to services.
    :type serviceAccessor: :class:`.IServiceAccessor`"""

    #: Enumerates statuses how a backup operation can finish.
    __ActionResults = Enum(

        #: Backup operation finished successfully.
        "Successful",

        #: Backup operation finished successfully with some issues (warnings).
        "Issues",

        #: Backup operation failed.
        "Failed")



    def __init__(self, componentUi, applicationContext, serviceAccessor):
        self.__componentUi = componentUi
        self.__serviceAccessor = serviceAccessor

        self.__appEnvironment = applicationContext.appEnvironment
        self.__configuration = applicationContext.configuration

        self.__commandExecutor = _CommandExecutor(self.__configuration, self.__serviceAccessor.getOrCreateService(
            ExternalCommandExecutorServiceIdentification, None), self.__componentUi)
        self.__archiving = _Archiving(componentUi, applicationContext, self.__serviceAccessor, self.__commandExecutor)

        self.__actionResult = self.__ActionResults.Successful

    # {{{ helpers


    # {{{ create action

    def executeCreateAction(self, selectedArchiveSpecs):
        """Executes create backup(s) action.

        Takes ``selectedArchiveSpecs`` and for each it creates a backup.  If ``selectedArchiveSpecs`` is empty or
        :attr:`.Options.ALL` is set to ``True`` then backups for all knows archives (typically all archive
        specification files in :attr:`.Options.ARCHIVE_SPECS_DIR` directory) plus those in ``selectedArchiveSpecs``
        are created.

        :param selectedArchiveSpecs: :term:`archive specification files <archive specification file>` for which backups
           shall be created.
        :type selectedArchiveSpecs: ``Sequence<ArchiveSpecInfo>``"""
        
        selectedArchiveSpecs = self.__appendAllArchiveSpecsIfSelected(selectedArchiveSpecs)
        self.__actionResult = self.__ActionResults.Successful
        self.__componentUi.messageShown += self.__onMessageShown

        try:
            self.__commandExecutor.executeBeforeAllCommand()
        except OSError as ex:
            self.__componentUi.showError(ex.args[0])
            return

        for specName, specFile in selectedArchiveSpecs:
            processingArchSpec = specName or specFile
            self.__componentUi.setProcessingArchSpec(processingArchSpec)

            if self.__componentUi.verbosity == VerbosityLevels.Verbose:
                self.__componentUi.showVerbose(str.format("\nProcessing \"{}\"...", processingArchSpec))

            # create the archive
            self.__archiving.makeBackup(specFile)

        try:
            self.__commandExecutor.executeAfterAllCommand()
        except OSError as ex:
            self.__componentUi.showError(ex.args[0])
            return

        self.__componentUi.setProcessingArchSpec(None)
        self.__componentUi.messageShown -= self.__onMessageShown

        # print results
        if self.__componentUi.verbosity == VerbosityLevels.Verbose:
            self.__componentUi.showVerbose("")
            if self.__actionResult == self.__ActionResults.Successful:
                self.__componentUi.showVerbose("Backup creation completed successfully.")
            elif self.__actionResult == self.__ActionResults.Issues:
                self.__componentUi.showVerbose("Backup creation completed successfully. One or more warnings were " +
                                               "shown. Check program's output for details.")
            else:
                self.__componentUi.showVerbose("Backup creation for one or more archives finished with error(s)! " +
                                               "Check program's output for details.")

        return self.__actionResult == self.__ActionResults.Successful

    # }}} create action



    # {{{ list action

    def executeListAction(self, selectedArchiveSpecs):
        """Lists information about :term:`selected <selected archive>` and :term:`orphaned <orphaned archive>` archives
        to standard output.

        Similarly to :meth:`executeCreateAction` archives in ``selectedArchiveSpecs`` are listed.  If it is empty or
        :attr:`.Options.ALL` is ``True`` then all archives plus selected are listed.  Orphaned archives are always
        listed.

        List of orphaned archives is obtained by following operation: from the list of
        :term:`stored archives <stored archive>` is subtracted the unique list of valid selected archives and
        valid :term:`configured archives <configured archive>`.

        Output has two possible formats depending on the :attr:`.Options.VERBOSE` option.

        :param selectedArchiveSpecs: :term:`archive specification files <archive specification file>` which shall be
           listed.
        :type selectedArchiveSpecs: ``Sequence<ArchiveSpecInfo>``"""

        archiveSpecs = self.__appendAllArchiveSpecsIfSelected(selectedArchiveSpecs)
        self.__actionResult = self.__ActionResults.Successful
        self.__componentUi.messageShown += self.__onMessageShown

        orphanedArchives = frozenset(self.__getOrphanedArchives(archiveSpecs))

        for archiveSpecInfo in archiveSpecs:
            processingArchSpec = archiveSpecInfo.name or archiveSpecInfo.path
            self.__componentUi.setProcessingArchSpec(processingArchSpec)

            # if the archive is orphaned do not even try to get information about it because it most certainly will
            # fail and an error will be shown which is undesirable
            if processingArchSpec in orphanedArchives:
                continue

            archiveInfo = self.__archiving.getArchiveInfo(archiveSpecInfo.path)
            if archiveInfo is None:
                self.__actionResult = self.__ActionResults.Failed
                continue

            if self.__componentUi.verbosity == VerbosityLevels.Verbose:
                self.__showVerboseArchiveInfo(archiveInfo)
            else:
                self.__showStandardArchiveInfo(archiveInfo)
        self.__componentUi.setProcessingArchSpec(None)

        archiveSpecsNames = {spec.name for spec in archiveSpecs}
        for orphanedArchiveName in orphanedArchives:
            self.__componentUi.setProcessingArchSpec(orphanedArchiveName)

            # if user passed some arguments (selected some archives) and option ALL is not enabled then we will going
            # to list only those orphaned archives which were specified (as arguments)
            if (len(selectedArchiveSpecs) > 0 and not self.__configuration[Options.ALL]) and \
               (orphanedArchiveName not in archiveSpecsNames):
                continue

            archiveInfo = self.__archiving.getStoredArchiveInfo(orphanedArchiveName)

            if self.__componentUi.verbosity == VerbosityLevels.Verbose:
                self.__showVerboseArchiveInfo(archiveInfo, True)
            else:
                self.__showStandardArchiveInfo(archiveInfo, True)
        self.__componentUi.setProcessingArchSpec(None)

        self.__componentUi.messageShown -= self.__onMessageShown

        return self.__actionResult == self.__ActionResults.Successful



    def __showStandardArchiveInfo(self, archiveInfo, orphaned = False):
        name = DisplayField(self.__bracket(archiveInfo.name, orphaned), 0.087, FieldStretchiness.Medium)
        path = DisplayField(self.__question(archiveInfo.path, True), 0.447, FieldStretchiness.Normal)
        destDir = DisplayField(archiveInfo.destDir, 0.448, FieldStretchiness.Normal)
        levels = DisplayField(self.__formatLevelsString(archiveInfo), 0.015, FieldStretchiness.Low)

        self.__componentUi.presentMultiFieldLine(MultiFieldLine([name, path, destDir, levels], 1000))



    def __showVerboseArchiveInfo(self, archiveInfo, orphaned = False):
        archiveInfoMsg = str.format("Name: {}\n", self.__bracket(archiveInfo.name, orphaned))
        archiveInfoMsg += str.format("Root: {}\n", self.__question(archiveInfo.path, True))
        archiveInfoMsg += str.format("Archiver type: {}\n", OptionsUtils.archiverTypeToStr(archiveInfo.archiverType))
        archiveInfoMsg += str.format("Destination directory: {}\n", archiveInfo.destDir)
        archiveInfoMsg += str.format("Current backup level/next/max.: {}\n", self.__formatLevelsString(archiveInfo))
        archiveInfoMsg += str.format(
            "Target backup level for non-full restart: {}\n",
            self.__bracket(self.__question(archiveInfo.restartLevel, archiveInfo.incremental is not None),
                           not archiveInfo.incremental or not archiveInfo.restarting))
        archiveInfoMsg += str.format(
            "Upcoming restart reason: {}\n",
            self.__bracket(self.__question(self.__reasonToStr(archiveInfo.restartReason),
                                           archiveInfo.incremental is not None),
                           not archiveInfo.incremental or not archiveInfo.restarting))
        archiveInfoMsg += str.format("Restart count/max.: {}/{}\n",
                                     self.__bracket(self.__dash(archiveInfo.restartCount),
                                                    not archiveInfo.incremental or not archiveInfo.restarting),
                                     self.__bracket(self.__dash(archiveInfo.fullRestartAfterCount),
                                                    not archiveInfo.incremental or not archiveInfo.restarting))
        age = (date.today() - archiveInfo.lastRestart).days if archiveInfo.lastRestart is not None else None
        archiveInfoMsg += str.format("Days since last restart/max.: {}/{}\n",
                                     self.__bracket(self.__dash(age), not archiveInfo.incremental or
                                                                      not archiveInfo.restarting),
                                     self.__bracket(self.__dash(archiveInfo.restartAfterAge),
                                                    not archiveInfo.incremental or not archiveInfo.restarting))
        age = (date.today() - archiveInfo.lastFullRestart).days if archiveInfo.lastFullRestart is not None else None
        archiveInfoMsg += str.format("Days since last full restart/max.: {}/{}\n",
                                     self.__bracket(self.__dash(age), not archiveInfo.incremental or
                                                                      not archiveInfo.restarting),
                                     self.__bracket(self.__dash(archiveInfo.fullRestartAfterAge),
                                                    not archiveInfo.incremental or not archiveInfo.restarting))
        self.__componentUi.showVerbose(archiveInfoMsg)



    def __formatLevelsString(self, archiveInfo):
        levels = str.format(
            "{}/{}/{}",
            self.__bracket(self.__dash(archiveInfo.backupLevel), not archiveInfo.incremental),
            self.__bracket(self.__question(archiveInfo.nextBackupLevel,
                                           archiveInfo.incremental is not None and archiveInfo.backupLevel is not None),
                           not archiveInfo.incremental),
            self.__bracket(self.__dash(archiveInfo.restartAfterLevel), not archiveInfo.incremental or
                                                                       not archiveInfo.restarting))
        return levels



    @staticmethod
    def __bracket(token, condition):
        leftBracket = ""
        rightBracket = ""
        if condition and token is not None:
            leftBracket = "["
            rightBracket = "]"
        return str.format("{leftBracket}{token}{rightBracket}", leftBracket = leftBracket, token = token,
                          rightBracket = rightBracket)



    @staticmethod
    def __dash(value):
        if value is None:
            return "-"
        else:
            return value



    @classmethod
    def __question(cls, value, condition):
        if condition and value is None:
            return "?"
        else:
            return cls.__dash(value)



    @classmethod
    def __reasonToStr(cls, reason):
        if reason is _BackupLevelRestartReasons.NoRestart:
            reasonStr = "No restart scheduled for the next backup."
        elif reason is _BackupLevelRestartReasons.RestartCountLimitReached:
            reasonStr = "Maximal restart count reached."
        elif reason is _BackupLevelRestartReasons.LastFullRestartAgeLimitReached:
            reasonStr = "Maximal age without full restart reached."
        elif reason is _BackupLevelRestartReasons.BackupLevelLimitReached:
            reasonStr = "Maximal backup level reached."
        elif reason is _BackupLevelRestartReasons.LastRestartAgeLimitReached:
            reasonStr = "Maximal age without a restart reached."
        elif reason is None:
            reasonStr = None
        else:
            reasonStr = "Unknown reason."
        return reasonStr

    # }}} list action



    # {{{ purge action

    def executePurgeAction(self, selectedArchiveSpecs):
        """Removes all stored information about specified orphaned archives.

        If ``selectedArchiveSpecs`` is empty or :attr:`.Options.ALL` is ``True`` then all orphaned archives are
        processed.

        :param selectedArchiveSpecs: :term:`archive specification files <archive specification file>` which shall be
           purged.
        :type selectedArchiveSpecs: ``Sequence<ArchiveSpecInfo>``"""

        def reportPurgedArchive(processingArchSpec):
            if self.__componentUi.verbosity == VerbosityLevels.Verbose:
                self.__componentUi.showVerbose(str.format("Purging {}.", processingArchSpec))



        result = True

        archiveSpecs = self.__appendAllArchiveSpecsIfSelected(selectedArchiveSpecs)
        orphanedArchives = frozenset(self.__getOrphanedArchives(archiveSpecs))
        knownValidArchiveNames = frozenset(self.__getKnownValidArchiveNames(selectedArchiveSpecs))
        try:
            # names of archive specs which were selected by a name, not by path to .aa file
            archiveSpecNamesSelectedByName = [asi.name for asi in selectedArchiveSpecs if asi.name is not None]
            for archiveSpecName in archiveSpecNamesSelectedByName:
                self.__componentUi.setProcessingArchSpec(archiveSpecName)
                if archiveSpecName in orphanedArchives:
                    reportPurgedArchive(archiveSpecName)
                    self.__archiving.purgeStoredArchiveData(archiveSpecName)
                elif archiveSpecName in knownValidArchiveNames:
                    self.__componentUi.showWarning("Archive is not orphaned. Not purging.")
                    result = False
                else:
                    self.__componentUi.showInfo("Nothing to purge.")
            self.__componentUi.setProcessingArchSpec(None)

            if self.__configuration[Options.ALL]:
                for orphanedArchive in orphanedArchives:
                    self.__componentUi.setProcessingArchSpec(orphanedArchive)

                    # archives specified via name arguments were purged in the loop above so exclude them here
                    if orphanedArchive not in archiveSpecNamesSelectedByName:

                        reportPurgedArchive(orphanedArchive)
                        self.__archiving.purgeStoredArchiveData(orphanedArchive)

                self.__componentUi.setProcessingArchSpec(None)
        except OSError as ex:
            self.__componentUi.showError(str.format("Purge failed: {}", ex.strerror))
            result = False

        return result

    # }}} purge action



    def __onMessageShown(self, messageKind):
        "Sets the backup status."

        # SMELL: Split status evaluation and message presentation.
        if messageKind == UiMessageKinds.Warning and self.__actionResult != self.__ActionResults.Failed:
            self.__actionResult = self.__ActionResults.Issues
        elif messageKind == UiMessageKinds.Error:
            self.__actionResult = self.__ActionResults.Failed



    def __getOrphanedArchives(self, selectedArchiveSpecs):
        knownValidArchiveNames = frozenset(self.__getKnownValidArchiveNames(selectedArchiveSpecs))
        return (name
                for name in self.__archiving.getStoredArchiveNames()
                if name not in knownValidArchiveNames)



    @Utils.uniq
    def __getKnownValidArchiveNames(self, selectedArchiveSpecs):
        selectedArchiveSpecFiles = (archSpecInf.path
                                    for archSpecInf in selectedArchiveSpecs)
        configuredArchiveSpecsFiles = (archSpecInf.path
                                       for archSpecInf in self.__archiving.getArchiveSpecs())
        return self.__archiving.filterValidSpecFiles(
            itertools.chain(selectedArchiveSpecFiles, configuredArchiveSpecsFiles))



    def __appendAllArchiveSpecsIfSelected(self, selectedArchiveSpecs):

        @Utils.uniq
        def getAllUniqueArchiveSpecs():
            for archiveSpecInfo in selectedArchiveSpecs:
                yield archiveSpecInfo

            try:
                empty = True
                for archiveSpecInfo in self.__archiving.getArchiveSpecs():
                    empty = False
                    yield archiveSpecInfo
                if empty:
                    self.__componentUi.showWarning("No configured archive specification files were found.")
            except RuntimeError as ex:
                self.__componentUi.showError(str.format(
                            "An error occurred while obtaining the list of all archive specification files: {}", ex))



        if len(selectedArchiveSpecs) == 0 or self.__configuration[Options.ALL]:
            return tuple(getAllUniqueArchiveSpecs())
        else:
            return selectedArchiveSpecs

    # }}} helpers

# }}} CLASSES

# _user_action_executor.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2012 Róbert Čerňanský



""":class:`_UserActionExecutor` class."""



__all__ = ["_UserActionExecutor"]



# {{{ INCLUDES

import os
import subprocess
import itertools
from datetime import date

from ...._utils import *
from ...._py_additions import *
from ...._mainf import *
from ...._configuration import *
from ...._archiving import *
from .. import *

# }}} INCLUDES



# {{{ CLASSES

class _UserActionExecutor:
    """Takes care of execution of a user action specified on the command line.

    :param interfaceAccessor: An :class:`.IInterfaceAccessor` instance.
    :type interfaceAccessor: :class:`.IInterfaceAccessor`"""

    #: Enumerates statuses how a backup operation can finish.
    __ActionResults = Enum(

        #: Backup operation finished successfully.
        "Successful",

        #: Backup operation finished successfully with some issues (warnings).
        "Issues",

        #: Backup operation failed.
        "Failed")



    def __init__(self, interfaceAccessor):
        self.__interfaceAccessor = interfaceAccessor
        self.__appConfig = self.__interfaceAccessor.getComponentInterface(IAppConfig)
        self.__componentUi = self.__interfaceAccessor.getComponentInterface(IComponentUi)
        self.__archiving = self.__interfaceAccessor.getComponentInterface(IArchiving)
        self.__appEnvironment = None
        self.__action = None
        self.__processedArchSpec = None
        self.__selectedArchiveSpecs = None
        self.__actionResult = self.__ActionResults.Successful

        mainfContext = self.__interfaceAccessor.getComponentInterface(IMainfContext)
        self.__appEnvironment = mainfContext.appEnvironment

        self.__action = self.__getUserAction()



    @property
    def action(self):
        """Gets the user action.

        :rtype: ``str``"""

        return self.__action



    @property
    def processedArchSpec(self):
        """Gets currently processed :term:`archive specification file`.

        .. note:: The returned value can be either the archive specification file name or path to it.

        :rtype archSpec: ``str``"""

        return self.__processedArchSpec



    def execute(self):
        """Executes the user action.

        :return: ``True`` if the action execution was successful; ``False`` otherwise."""

        if not self.__validateUserAction(self.action):
            return False

        self.__setSelectedArchiveSpecs()

        if self.action == CmdlineCommands.CREATE:
            return self.__executeCreateAction()
        elif self.action == CmdlineCommands.LIST:
            return self.__executeListAction()
        elif self.action == CmdlineCommands.PURGE:
            return self.__executePurgeAction()



    # {{{ helpers

    def __getUserAction(self):
        optparseValues = self.__appEnvironment.options
        for optParseOption in optparseValues.__dict__:
            if optparseValues.__dict__[optParseOption]:
                if CmdlineCommandsUtils.isExistingCommand(optParseOption):
                    return optParseOption
        return CmdlineCommands.CREATE



    def __validateUserAction(self, action):
        if action == CmdlineCommands.CREATE:
            if len(self.__appEnvironment.arguments) == 0 and not self.__appConfig[Options.ALL]:

                self.__componentUi.showError("No archive specification given. Please pass the name or path to an " +
                                             "archive specification file as the program's argument; or use option " +
                                             "--all if you want to process all configured archive specifications.")
                return False

        elif action == CmdlineCommands.PURGE:
            if len(self.__appEnvironment.arguments) == 0 and not self.__appConfig[Options.ALL]:

                self.__componentUi.showError("No archive name given. Please pass the name of an archive as the " +
                                             "program's argument or use option --all if you want to purge all " +
                                             "orphaned archive data.")
                return False

        return True



    # {{{ create action

    def __executeCreateAction(self):
        self.__actionResult = self.__ActionResults.Successful
        self.__componentUi.messageShown += self.__onMessageShown

        for specName, specFile in self.__selectedArchiveSpecs:
            self.__processedArchSpec = specName or specFile

            if self.__componentUi.verbosity == VerbosityLevels.Verbose:
                self.__componentUi.showVerbose(str.format("\nProcessing \"{}\"...", self.__processedArchSpec))

            # create the archive
            self.__archiving.makeBackup(specFile)

        self.__processedArchSpec = None
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

    def __executeListAction(self):
        self.__actionResult = self.__ActionResults.Successful
        self.__componentUi.messageShown += self.__onMessageShown

        orphanedArchives = frozenset(self.__getOrphanedArchives())

        for archiveSpecInfo in self.__selectedArchiveSpecs:
            self.__processedArchSpec = archiveSpecInfo.name or archiveSpecInfo.path

            # if the archive is orphaned do not even try to get information about it because it most certainly will
            # fail and an error will be shown which is undesirable
            if self.__processedArchSpec in orphanedArchives:
                continue

            archiveInfo = self.__archiving.getArchiveInfo(archiveSpecInfo.path)
            if archiveInfo is None:
                self.__actionResult = self.__ActionResults.Failed
                continue

            if self.__componentUi.verbosity == VerbosityLevels.Verbose:
                self.__showVerboseArchiveInfo(archiveInfo)
            else:
                self.__showStandardArchiveInfo(archiveInfo)
        self.__processedArchSpec = None

        selectedArchiveSpecsNames = {spec.name for spec in self.__selectedArchiveSpecs}
        for orphanedArchiveName in orphanedArchives:
            self.__processedArchSpec = orphanedArchiveName

            # if user passed some arguments and option ALL is not enabled then we will going to list only those
            # orphaned archives which were specified (as arguments)
            if (len(self.__appEnvironment.arguments) > 0 and not self.__appConfig[Options.ALL]) and \
               (orphanedArchiveName not in selectedArchiveSpecsNames):
                continue

            archiveInfo = self.__archiving.getStoredArchiveInfo(orphanedArchiveName)

            if self.__componentUi.verbosity == VerbosityLevels.Verbose:
                self.__showVerboseArchiveInfo(archiveInfo, True)
            else:
                self.__showStandardArchiveInfo(archiveInfo, True)
        self.__processedArchSpec = None

        self.__componentUi.messageShown -= self.__onMessageShown

        return self.__actionResult == self.__ActionResults.Successful



    def __showStandardArchiveInfo(self, archiveInfo, orphaned = False):
        from .cmdline_ui_component import CmdlineUiComponent

        termWidth = self.__getTermWidth()
        levels = self.__formatLevelsString(archiveInfo)
        usableWidth = termWidth - (3 + len(levels))
        pathWidth = int(usableWidth * 0.4)
        nameWidth = int(usableWidth * 0.2)
        archiveInfoMsg = str.format(
            "{name:<{nameWidth}} {path:<{pathWidth}} {destDir:<{pathWidth}} {levels}",
            name = self.__bracket(CmdlineUiComponent._shortenString(archiveInfo.name, nameWidth), orphaned),
            path = CmdlineUiComponent._shortenString(self.__question(archiveInfo.path, True), pathWidth),
            destDir = CmdlineUiComponent._shortenString(archiveInfo.destDir, pathWidth),
            levels = levels,
            nameWidth = nameWidth,
            pathWidth = pathWidth)
        self.__componentUi.presentLine(archiveInfoMsg)



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
        if reason is BackupLevelRestartReasons.NoRestart:
            reasonStr = "No restart scheduled for the next backup."
        elif reason is BackupLevelRestartReasons.RestartCountLimitReached:
            reasonStr = "Maximal restart count reached."
        elif reason is BackupLevelRestartReasons.LastFullRestartAgeLimitReached:
            reasonStr = "Maximal age without full restart reached."
        elif reason is BackupLevelRestartReasons.BackupLevelLimitReached:
            reasonStr = "Maximal backup level reached."
        elif reason is BackupLevelRestartReasons.LastRestartAgeLimitReached:
            reasonStr = "Maximal age without a restart reached."
        elif reason is None:
            reasonStr = None
        else:
            reasonStr = "Unknown reason."
        return reasonStr



    @staticmethod
    def __getTermWidth():

        def getWinWidth(fd):
            try:
                import struct, fcntl, termios
                expectStruct = struct.pack("hh", 0, 0)
                width = struct.unpack("hh", fcntl.ioctl(fd, termios.TIOCGWINSZ, expectStruct))[1]
            except IOError:
                width = None
            return width



        # try get terminal width from standard file descriptors using ioctl
        for stdFd in (1, 2, 0):
            width = getWinWidth(stdFd)
            if width:
                return width

        # try get terminal width from controlling terminal file descriptor using ioctl
        try:
            with open(os.ctermid()) as termFd:
                return getWinWidth(termFd)
        except IOError:
            pass

        # try environment variable
        if "COLUMNS" in os.environ.keys():
            return os.environ["COLUMNS"]

        # try call external program stty
        status, output = subprocess.getstatusoutput("stty size")
        if status == 0:
            splitOutput = output.split()
            if len(splitOutput) == 2:
                try:
                    return int(splitOutput[1])
                except ValueError:
                    pass

        return 80

    # }}} list action



    # {{{ purge action

    def __executePurgeAction(self):

        def reportPurgedArchive():
            if self.__componentUi.verbosity == VerbosityLevels.Verbose:
                self.__componentUi.showVerbose(str.format("Purging {}.", self.__processedArchSpec))



        result = True

        orphanedArchives = frozenset(self.__getOrphanedArchives())
        knownValidArchiveNames = frozenset(self.__getKnownValidArchiveNames())
        try:
            for argument in self.__getArchiveNameArguments():
                self.__processedArchSpec = argument
                if argument in orphanedArchives:
                    reportPurgedArchive()
                    self.__archiving.purgeStoredArchiveData(argument)
                elif argument in knownValidArchiveNames:
                    self.__componentUi.showWarning("Archive is not orphaned. Not purging.")
                    result = False
                else:
                    self.__componentUi.showInfo("Nothing to purge.")
            self.__processedArchSpec = None

            if self.__appConfig[Options.ALL]:
                for orphanedArchive in orphanedArchives:
                    self.__processedArchSpec = orphanedArchive

                    # archives specified via name arguments were purged in the loop above so exclude them here
                    if orphanedArchive not in self.__getArchiveNameArguments():

                        reportPurgedArchive()
                        self.__archiving.purgeStoredArchiveData(orphanedArchive)

                self.__processedArchSpec = None
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



    def __setSelectedArchiveSpecs(self):

        @_Utils.uniq
        def getSelectedArchiveSpecs():
            archiveSpecsDir = self.__appConfig[Options.ARCHIVE_SPECS_DIR]

            for archiveName in self.__getArchiveNameArguments():
                yield ArchiveSpecInfo(archiveName,
                                      os.path.join(archiveSpecsDir, archiveName + ConfigConstants.ARCHIVE_SPEC_EXT))

            for archiveSpec in self.__getArchiveSpecPathArguments():
                yield ArchiveSpecInfo(None, archiveSpec)

            if len(self.__appEnvironment.arguments) == 0 or self.__appConfig[Options.ALL]:

                try:
                    empty = True
                    for archiveSpecInfo in self.__appConfig.getArchiveSpecs():
                        empty = False
                        yield archiveSpecInfo
                    if empty:
                        self.__componentUi.showWarning("No configured archive specification files were found.")
                except RuntimeError as ex:
                    self.__componentUi.showError(str.format(
                            "An error occurred while obtaining the list of all archive specification files: {}", ex))



        self.__selectedArchiveSpecs = tuple(getSelectedArchiveSpecs())



    def __getArchiveNameArguments(self):
        return (arg
                for arg in self.__appEnvironment.arguments
                if os.path.splitext(arg)[1] != ConfigConstants.ARCHIVE_SPEC_EXT)



    def __getArchiveSpecPathArguments(self):
        return (arg
                for arg in self.__appEnvironment.arguments
                if os.path.splitext(arg)[1] == ConfigConstants.ARCHIVE_SPEC_EXT)



    def __getOrphanedArchives(self):
        knownValidArchiveNames = frozenset(self.__getKnownValidArchiveNames())
        return (name
                for name in self.__archiving.getStoredArchiveNames()
                if name not in knownValidArchiveNames)



    @_Utils.uniq
    def __getKnownValidArchiveNames(self):
        selectedArchiveSpecFiles = (archSpecInf.path
                                    for archSpecInf in self.__selectedArchiveSpecs)
        configuredArchiveSpecsFiles = (archSpecInf.path
                                       for archSpecInf in self.__appConfig.getArchiveSpecs())
        return self.__archiving.filterValidSpecFiles(
            itertools.chain(selectedArchiveSpecFiles, configuredArchiveSpecsFiles))

    # }}} helpers

# }}} CLASSES

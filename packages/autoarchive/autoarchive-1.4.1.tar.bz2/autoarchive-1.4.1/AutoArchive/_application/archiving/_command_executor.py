# _command_executor.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2016 Róbert Čerňanský



""":class:`_CommandExecutor` class."""



__all__ = ["_CommandExecutor"]



# {{{ INCLUDES

import shlex

from AutoArchive._infrastructure.ui import VerbosityLevels
from AutoArchive._infrastructure.configuration import Options

# }}} INCLUDES



# {{{ CLASSES

class _CommandExecutor:
    def __init__(self, configuration, externalCommandExecutor, componentUi):
        self.__configuration = configuration
        self.__externalCommandExecutor = externalCommandExecutor
        self.__componentUi = componentUi



    def executeBeforeCommand(self, archiveSpec):
        self.__executeCommand(archiveSpec[Options.COMMAND_BEFORE_BACKUP])



    def executeAfterCommand(self, archiveSpec):
        self.__executeCommand(archiveSpec[Options.COMMAND_AFTER_BACKUP])



    def executeBeforeAllCommand(self):
        self.__executeCommand(self.__configuration[Options.COMMAND_BEFORE_ALL_BACKUPS])



    def executeAfterAllCommand(self):
        self.__executeCommand(self.__configuration[Options.COMMAND_AFTER_ALL_BACKUPS])



    def __executeCommand(self, commandString):
        if commandString is not None and commandString != "":
            command = shlex.split(commandString)
            self.__informVerboseUser(commandString)
            self.__externalCommandExecutor.commandMessage += self.__onCommandMessage
            self.__externalCommandExecutor.execute(command[0], command[1:] if len(command) > 1 else None)
            self.__externalCommandExecutor.commandMessage -= self.__onCommandMessage



    def __onCommandMessage(self, command, message, isError):
        if isError:
            self.__componentUi.showWarning(message)
        elif self.__componentUi.verbosity != VerbosityLevels.Quiet:
            self.__componentUi.presentLine(message)



    def __informVerboseUser(self, commandString):
        if self.__componentUi.verbosity == VerbosityLevels.Verbose:
            self.__componentUi.showVerbose(str.format("Executing command '{}'", commandString))

# }}} CLASSES

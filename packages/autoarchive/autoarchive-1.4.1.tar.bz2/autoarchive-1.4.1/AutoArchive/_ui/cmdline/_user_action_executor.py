# _user_action_executor.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2017 Róbert Čerňanský



""":class:`UserActionExecutor` class."""



__all__ = ["UserActionExecutor"]



# {{{ INCLUDES

import os

from AutoArchive._infrastructure.utils import Utils
from AutoArchive._infrastructure.configuration import Options
from AutoArchive._application.archiving.archive_spec import ArchiveSpecInfo, ConfigConstants
from ._cmdline_commands import CmdlineCommands, _CmdlineCommandsUtils

# }}} INCLUDES



# {{{ CLASSES

class UserActionExecutor:
    """Takes care of execution of a user action specified on the command line.

    :param componentUi: Access to user interface.
    :type componentUi: :class:`.CmdlineUi`
    :param applicationContext: Application context.
    :type applicationContext: :class:`.ApplicationContext`
    :param archivingApplication: The application interface.
    :type archivingApplication: :class:`.ArchivingApplication`"""

    def __init__(self, componentUi, applicationContext, archivingApplication):
        self.__componentUi = componentUi
        self.__archivingApplication = archivingApplication
        self.__configuration = applicationContext.configuration
        self.__appEnvironment = applicationContext.appEnvironment
        self.__action = self.__getUserAction()



    def execute(self):
        """Executes an action defined for the specified command for specified
        :term:`archive specification files <archive specification file>`.

        Command is read from the :attr:`.ApplicationContext.appEnvironment.options`.  If ``options`` has an attribute
        that matches one of the :class:`.CmdlineCommands` and the value of that attribute is ``True`` then the action
        for the matching command is executed.  If there is no such attribute, then the default action ``create`` is
        executed.

        Archive specification files can be specified by following ways:

          - By archive names passed in :attr:`.ApplicationContext.appEnvironment.arguments`.

            Archive name can not contain the string defined by :attr:`.ConfigConstants.ARCHIVE_SPEC_EXT` at the end
            otherwise it would be taken as the path to an archive specification file.  Archive specification files
            corresponding to the names are looked up in the path defined by :attr:`.Options.ARCHIVE_SPECS_DIR` option.

          - By paths to archive specification files passed in :attr:`.ApplicationContext.appEnvironment.arguments`.

            A path must end with the string defined by :attr:`.ConfigConstants.ARCHIVE_SPEC_EXT`.

        :return: ``True`` if the action execution was successful; ``False`` otherwise."""

        if not self.__validateUserAction(self.__action):
            return False

        selectedArchiveSpecs = self.__retrieveSelectedArchiveSpecs()

        if self.__action == CmdlineCommands.CREATE:
            return self.__archivingApplication.executeCreateAction(selectedArchiveSpecs)
        elif self.__action == CmdlineCommands.LIST:
            return self.__archivingApplication.executeListAction(selectedArchiveSpecs)
        elif self.__action == CmdlineCommands.PURGE:
            return self.__archivingApplication.executePurgeAction(selectedArchiveSpecs)



    # {{{ helpers

    def __getUserAction(self):
        optparseValues = self.__appEnvironment.options
        for optParseOption in optparseValues.__dict__:
            if optparseValues.__dict__[optParseOption]:
                if _CmdlineCommandsUtils.isExistingCommand(optParseOption):
                    return optParseOption
        return CmdlineCommands.CREATE



    def __validateUserAction(self, action):
        if action == CmdlineCommands.CREATE:
            if len(self.__appEnvironment.arguments) == 0 and not self.__configuration[Options.ALL]:
                self.__componentUi.showError("No archive specification given. Please pass the name or path to an " +
                                             "archive specification file as the program's argument; or use option " +
                                             "--all if you want to process all configured archive specifications.")
                return False

        elif action == CmdlineCommands.PURGE:
            if len(self.__appEnvironment.arguments) == 0 and not self.__configuration[Options.ALL]:

                self.__componentUi.showError("No archive name given. Please pass the name of an archive as the " +
                                             "program's argument or use option --all if you want to purge all " +
                                             "orphaned archive data.")
                return False

        return True



    def __retrieveSelectedArchiveSpecs(self):

        @Utils.uniq
        def getSelectedArchiveSpecs():
            archiveSpecsDir = self.__configuration[Options.ARCHIVE_SPECS_DIR]

            for archiveName in self.__getArchiveNameArguments():
                yield ArchiveSpecInfo(archiveName,
                                      os.path.join(archiveSpecsDir, archiveName + ConfigConstants.ARCHIVE_SPEC_EXT))

            for archiveSpec in self.__getArchiveSpecPathArguments():
                yield ArchiveSpecInfo(None, archiveSpec)



        return tuple(getSelectedArchiveSpecs())



    def __getArchiveNameArguments(self):
        return (arg
                for arg in self.__appEnvironment.arguments
                if os.path.splitext(arg)[1] != ConfigConstants.ARCHIVE_SPEC_EXT)



    def __getArchiveSpecPathArguments(self):
        return (arg
                for arg in self.__appEnvironment.arguments
                if os.path.splitext(arg)[1] == ConfigConstants.ARCHIVE_SPEC_EXT)

    # }}} helpers

# }}} CLASSES

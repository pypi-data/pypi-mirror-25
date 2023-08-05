# cmdline_ui_component.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2012 Róbert Čerňanský



""":class:`CmdlineUiComponent` class."""



__all__ = ["CmdlineUiComponent"]



# {{{ INCLUDES

import sys
import os

from ...._py_additions import *
from ...._mainf import *
from ...._configuration import *
from .. import *
from ._user_action_executor import *

# }}} INCLUDES



# {{{ CLASSES

class CmdlineUiComponent(IComponent, IComponentUi):
    """Implementation of the command-line user interface.

    Class serves as the component of :term:`Mainf` framework and uses the :meth:`run()` method as an entry point for
    executing user actions specified on the command-line.  It implements the :class:`.IComponentUi` such that it uses
    standard output and standard error as the user interface.  The instance is exposed as
    :class:`.IComponentInterface`."""

    #: Maximal length of the archive name in output messages.
    __MAX_NAME_LENGTH = 10



    # {{{ IComponent implementation

    def __init__(self, interfaceAccessor):
        self.__interfaceAccessor = interfaceAccessor
        self.__appConfig = self.__interfaceAccessor.getComponentInterface(IAppConfig)
        self.__appEnvironment = None
        self.__userActionExecutor = None

        # overall backup result
        self.__backupStatus = None



    def run(self):
        """Executes an action defined for the specified command.

        Command is read from the :attr:`.IMainfContext.appEnvironment.options`.  If ``options`` has an attribute that
        matches one of the :class:`.CmdlineCommands` and the value of that attribute is ``True`` then the action for
        the matching command is executed.  If there is no such attribute, then the default action ``create`` is
        executed.

        :attr:`.CmdlineCommands.CREATE` command triggers the ``Create`` action.  It takes all specified
        :term:`archive specification files <archive specification file>` and for each it creates a backup using
        :term:`Archiving` component.  Archive specification files can be specified by following ways:

          - By archive names passed in :attr:`.IMainfContext.appEnvironment.arguments`.

            Archive name can not contain the string defined by :attr:`.ConfigConstants.ARCHIVE_SPEC_EXT` at the end
            otherwise it would be taken as the path to an archive specification file.  Archive specification files
            corresponding to the names are looked up in the path defined by :attr:`.Options.ARCHIVE_SPECS_DIR` option.

          - By paths to archive specification files passed in :attr:`.IMainfContext.appEnvironment.arguments`.

            A path must end with the string defined by :attr:`.ConfigConstants.ARCHIVE_SPEC_EXT`.

          - By passing empty :attr:`.IMainfContext.appEnvironment.arguments` and setting the option
            :attr:`.Options.ALL` to ``True``.

            In this case the action shall be executed for all known archives as served by Configuration component
            (typically all archive specification files in :attr:`.Options.ARCHIVE_SPECS_DIR` directory).

        :attr:`.CmdlineCommands.LIST` command triggers the ``List`` action.  It lists information about
        :term:`selected <selected archive>` and :term:`orphaned <orphaned archive>` archives to standard output.
        Archives can be specified by the same way as for the ``Create`` action except the last point where the ``List``
        action does not require the option :attr:`.Options.ALL` to be ``True``.  Orphaned archives are always listed.

        List of orphaned archives is obtained by following operation: from the list of
        :term:`stored archives <stored archive>` (as served by :term:`Archiving` component) is subtracted the unique
        list of valid selected archives and valid :term:`configured archives <configured archive>`.

        Output has two possible formats depending on the :attr:`.Options.VERBOSE` option.

        :attr:`.CmdlineCommands.PURGE` command triggers the ``Purge`` action.  It removes all stored information about
        specified orphaned archives.

        Orphaned archives names can be passed in :attr:`.IMainfContext.appEnvironment.arguments` or if
        :attr:`.Options.ALL` is ``True`` then all orphaned archives are processed.

        See also: :meth:`.IComponent.run`."""

        mainfContext = self.__interfaceAccessor.getComponentInterface(IMainfContext)
        self.__appEnvironment = mainfContext.appEnvironment

        self.__interfaceAccessor.registerComponentInterface(IComponentUi, self)

        self.__userActionExecutor = _UserActionExecutor(self.__interfaceAccessor)
        return self.__userActionExecutor.execute()

    # }}} IComponent implementation



    # {{{ IComponentUi implementation

    @event
    def messageShown(messageKind):
        "See: :meth:`.IComponentUi.messageShown`."

        pass



    @property
    def verbosity(self):
        "See: :attr:`.IComponentUi.verbosity`."

        if self.__appConfig[Options.QUIET]:
            return VerbosityLevels.Quiet
        elif self.__appConfig[Options.VERBOSE]:
            return VerbosityLevels.Verbose
        return VerbosityLevels.Normal



    def showVerbose(self, msg):
        "See: :meth:`.IComponentUi.showVerbose`."

        if self.verbosity == VerbosityLevels.Verbose:
            self.__printStandardMsg(msg)
        self.messageShown(UiMessageKinds.Verbose)



    def showNotification(self, msg):
        "See: :meth:`.IComponentUi.showNotification`."

        if self.verbosity != VerbosityLevels.Quiet:
            self.__printStandardMsg(msg)
        self.messageShown(UiMessageKinds.Notification)



    def showInfo(self, msg):
        "See: :meth:`.IComponentUi.showInfo`."

        if self.verbosity != VerbosityLevels.Quiet:
            self.__printStandardMsg(msg, self.__userActionExecutor.processedArchSpec)
        self.messageShown(UiMessageKinds.Info)



    def showWarning(self, msg):
        "See: :meth:`.IComponentUi.showWarning`."

        if self.verbosity != VerbosityLevels.Quiet:
            self.__printAttentionMsg("Warning", msg)
        self.messageShown(UiMessageKinds.Warning)



    def showError(self, msg):
        "See: :meth:`.IComponentUi.showError`."

        self.__printAttentionMsg("Error", msg)
        self.messageShown(UiMessageKinds.Error)



    def presentLine(self, line):
        "See: :meth:`.IComponentUi.presentLine`."

        self.__printStandardMsg(line)

    # }}} IComponentUi implementation



    # {{{ helpers

    @classmethod
    def __printStandardMsg(cls, msg, currentArchSpec = None):
        archSpecToken = str.format(
            "[{}] ", cls.__getArchSpecToken(currentArchSpec)) if currentArchSpec is not None else ""
        print(str.format("{}{}", archSpecToken, msg))



    def __printAttentionMsg(self, attentionString, msg):
        archSpecToken = str.format(
            " [{}] ", self.__getArchSpecToken(self.__userActionExecutor.processedArchSpec)) \
            if self.__userActionExecutor.processedArchSpec is not None else " "
        sys.stderr.write(str.format(
                "{executableName}: {attentionString}!{archSpecToken}{msg}\n",
                executableName = self.__appEnvironment.executableName,
                attentionString = attentionString,
                archSpecToken = archSpecToken,
                msg = msg))



    @classmethod
    def __getArchSpecToken(cls, currentArchSpec):
        if os.path.split(currentArchSpec)[0]:
            return os.path.join(cls._shortenString(os.path.split(currentArchSpec)[0], cls.__MAX_NAME_LENGTH),
                                os.path.basename(currentArchSpec))
        else:
            return currentArchSpec



    @staticmethod
    def _shortenString(token, length):
        halfLength = length // 2
        return token[:halfLength] + "~" + token[-halfLength - ((length % 2) - 1):] if len(token) > length else token

    # }}} helpers

# }}} CLASSES

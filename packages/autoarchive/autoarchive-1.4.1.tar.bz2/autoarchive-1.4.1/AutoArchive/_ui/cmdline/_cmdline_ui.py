# _cmdline_ui.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2014 Róbert Čerňanský



""":class:`CmdlineUi` class."""



__all__ = ["CmdlineUi"]



# {{{ INCLUDES

import sys
import os
import subprocess

from AutoArchive._infrastructure.py_additions import event
from AutoArchive._infrastructure.ui import VerbosityLevels, UiMessageKinds
from AutoArchive._infrastructure.configuration import Options


# }}} INCLUDES



# {{{ CLASSES

class CmdlineUi:
    """Implementation of the command-line user interface.

    Provides basic methods for showing messages of various importance to a user.  It uses standard output and standard
    error as the user interface.

    :param appEnvironment: Application environment.
    :type appEnvironment: :class:`.AppEnvironment`
    :param configuration: Application configuration.
    :type configuration: :class:`.IConfiguration`"""

    #: Maximal length of the archive name in output messages.
    __MAX_NAME_LENGTH = 10



    def __init__(self, appEnvironment, configuration):
        self.__configuration = configuration
        self.__appEnvironment = appEnvironment

        # currently processed archive specification file
        self.__processingArchSpec = None



    @event
    def messageShown(messageKind):
        """Fired after a user message was shown.

        Event is fired when one of the message kinds from :data:`UiMessageKinds` enum was shown or would be shown (but
        was suppressed due to the verbosity level).

        :param messageKind: Kind of the message that was shown.
        :type messageKind: :data:`UiMessageKinds`"""

        pass



    @property
    def verbosity(self):
        """Gets the verbosity level.

        If verbosity level is :data:`VerbosityLevels.Quiet` only messages of kind :data:`UiMessageKinds.Error` are
        shown.  For level :data:`VerbosityLevels.Normal` all messages kinds except :data:`UiMessageKinds.Verbose`
        are shown.  For level :data:`VerbosityLevels.Verbose` all message kinds are shown.

        :rtype: :data:`VerbosityLevels`"""

        if self.__configuration[Options.QUIET]:
            return VerbosityLevels.Quiet
        elif self.__configuration[Options.VERBOSE]:
            return VerbosityLevels.Verbose
        return VerbosityLevels.Normal



    def setProcessingArchSpec(self, archSpec):
        """Sets currently processed :term:`archive specification file`.

        :param archSpec: The archive specification file name or path to it.
        :type archSpec: ``str``"""

        self.__processingArchSpec = archSpec



    def showVerbose(self, msg):
        """Show a verbose-type message (:data:`UiMessageKinds.Verbose`) to the user.

        Verbose messages should be shown only if user enables it.  Although this method can be called regardless of
        current verbosity level, the concrete implementation can decide whether it will be shown or not if verbosity
        level is 0.  It is not recommended to call this method if verbosity level is 0 due to performance reasons.
        Current verbosity level can be obtained via :attr:`verbosity` property.

        See also: :attr:`verbosity`.

        :param msg: The message that should be shown to the user.
        :type msg: ``str``"""

        if self.verbosity == VerbosityLevels.Verbose:
            self.__printStandardMsg(msg)
        self.messageShown(UiMessageKinds.Verbose)



    def showNotification(self, msg):
        """Show an unintrusive notification message (:data:`UiMessageKinds.Notification`) to the user.

        .. note:: If user interface implementation does not have means to support notifications then it should be
           presented to the user similarly as :meth:`showInfo`.

        See also: :attr:`verbosity`.

        :param msg: The message that should be shown to the user.
        :type msg: ``str``"""

        if self.verbosity != VerbosityLevels.Quiet:
            self.__printStandardMsg(msg)
        self.messageShown(UiMessageKinds.Notification)



    def showInfo(self, msg):
        """Show an information message (:data:`UiMessageKinds.Info`) to the user.

        See also: :attr:`verbosity`.

        :param msg: The message that should be shown to the user.
        :type msg: ``str``"""

        if self.verbosity != VerbosityLevels.Quiet:
            self.__printStandardMsg(msg, self.__processingArchSpec)
        self.messageShown(UiMessageKinds.Info)



    def showWarning(self, msg):
        """Show a warning message (:data:`UiMessageKinds.Warning`) to the user.

        See also: :attr:`verbosity`.

        :param msg: The message that should be shown to the user.
        :type msg: ``str``"""

        if self.verbosity != VerbosityLevels.Quiet:
            self.__printAttentionMsg("Warning", msg)
        self.messageShown(UiMessageKinds.Warning)



    def showError(self, msg):
        """Show an error message to (:data:`UiMessageKinds.Error`) the user.

        See also: :attr:`verbosity`.

        :param msg: The message that should be shown to the user.
        :type msg: ``str``"""

        self.__printAttentionMsg("Error", msg)
        self.messageShown(UiMessageKinds.Error)



    def presentLine(self, line):
        """Present a line of text to the user.

        .. note:: The verbosity level has no effect on presenting the line.

        :param line: The text that shall be presented to the user.
        :type line: ``str``"""

        self.__printStandardMsg(line)



    def presentMultiFieldLine(self, multiFieldLine):
        """Present a line consisting of multiple fields of text to the user.

        .. note:: The verbosity level has no effect on presenting the line.

        :param multiFieldLine: Line that shall be presented.
        :type multiFieldLine: :class:`.MultiFieldLine`"""

        physicalWidth = self.__getTermWidth()
        widths = multiFieldLine.computeFieldWidths(physicalWidth)
        widthIdx = 0
        line = ""
        for field in multiFieldLine.fields:
            width = widths[widthIdx] - 1 if widthIdx < (len(multiFieldLine.fields) - 1) else widths[widthIdx]
            paddedText = str.format("{text:<{width}} ", text = self._shortenString(field.text, width), width = width)
            line += paddedText
            widthIdx += 1

        self.__printStandardMsg(line[:-1])



    # {{{ helpers

    @classmethod
    def __printStandardMsg(cls, msg, currentArchSpec = None):
        archSpecToken = str.format(
            "[{}] ", cls.__getArchSpecToken(currentArchSpec)) if currentArchSpec is not None else ""
        print(str.format("{}{}", archSpecToken, msg))



    def __printAttentionMsg(self, attentionString, msg):
        archSpecToken = str.format(
            " [{}] ", self.__getArchSpecToken(self.__processingArchSpec)) \
            if self.__processingArchSpec is not None else " "
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
            winWidth = getWinWidth(stdFd)
            if winWidth:
                return winWidth

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

    # }}} helpers

# }}} CLASSES

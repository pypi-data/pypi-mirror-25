# _external_command_executor.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2014 Róbert Čerňanský



""":class:`ExternalCommandExecutor` class."""



__all__ = ["ExternalCommandExecutor"]



# {{{ INCLUDES

import subprocess
import select

from AutoArchive._infrastructure.py_additions import event
from AutoArchive._infrastructure.service import IService


# }}} INCLUDES



# {{{ CLASSES

class ExternalCommandExecutor(IService):
    """Executes external commands."""

    def __init__(self):
        pass



    @event
    def commandMessage(command, message, isError):
        """Raised when the external command produces a message on standard error.

        :param command: Command name or path that produced the message.
        :type command: ``str``
        :param message: Message that the command produced.
        :type message: ``str``
        :param isError: ``true`` if the message was sent to standard error, ``false`` otherwise.
        :type isError: ``bool``"""



    def execute(self, command, arguments = None, environment = None):
        """Executes passed command.

        Commands standard output and standard error messages are propagated through ``commandMessage`` event.

        :raise OSError: If a system error occurred during command execution.
        :raise ChildProcessError: If the command exit code is non zero.

        Executes given command as a child process.

        Both standard output and standard error are captured and propagated via :meth:`commandMessage` event.  The
        order of messages written to standard output vs. standard error is not guaranteed to be preserved.

        See also: :meth:`ExternalCommandExecutor.execute()`."""

        if arguments is None:
            arguments = []
        try:
            commandProcess = subprocess.Popen([command] + arguments, stdout = subprocess.PIPE,
                                              stderr = subprocess.PIPE, env = environment,
                                              universal_newlines = True)
            self.__processCommandOutput(command, commandProcess)
        except OSError as ex:
            raise OSError(str.format("Error while executing command '{}'.", [command] + arguments),
                          command, ex)





    def __processCommandOutput(self, command, commandProcess):
        # capture program's standard output and standard error and informs about captured messages; note that
        # the order of messages written to stdout vs. messages written to stderr might not be preserved
        while True:
            readyStreams = select.select((commandProcess.stdout, commandProcess.stderr), (), ())[0]
            streamActive = False
            for readyStream in readyStreams:
                line = readyStream.readline()
                if line:
                    streamActive = True
                    self.commandMessage(command, line[:-1], readyStream is not commandProcess.stdout)
            if commandProcess.poll() is not None and not streamActive:
                break

        if commandProcess.returncode:
            self.__handleCommandExitCode(command, commandProcess.returncode)



    @staticmethod
    def __handleCommandExitCode(command, exitCode):
        if exitCode != 0:
            raise ChildProcessError(str.format("Command did not finished successfully: '{}', exit code: {}.",
                                               command, exitCode), command)

# }}} CLASSES

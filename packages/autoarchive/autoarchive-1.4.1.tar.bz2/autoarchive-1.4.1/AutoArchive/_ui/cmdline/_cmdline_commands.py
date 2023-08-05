# _cmdline_commands.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2014 Róbert Čerňanský



""":class:`CmdlineCommands` and :class:`_CmdlineCommandsUtils` static classes."""



# {{{ INCLUDES

from abc import *

# }}} INCLUDES



# {{{ CLASSES

# all command name constants defined in this class has to have uppercase names; there can not be any other constants
# defined that has uppercase names and are type of str, besides those representing command names
class CmdlineCommands(metaclass = ABCMeta):
    """Constants for command-line command names.

    Command-line commands are used to invoke program operations via a command-line argument.  For example: ``--create``
    will invoke a backup creation.

    .. note:: It is not allowed to change values of these constants."""

    # {{{ command constants

    #: Create :term:`backup` for a given :term:`archive specification file`.
    CREATE = "create"

    #: List all archive specification files.
    LIST = "list"

    #: Purge orphaned archive data.
    PURGE = "purge"

    # }}} command constants



    @abstractmethod
    def __init__(self):
        pass



class _CmdlineCommandsUtils(metaclass = ABCMeta):
    "Various utility methods working with :class:`CmdlineCommands`."

    @abstractmethod
    def __init__(self):
        pass



    @staticmethod
    def getAllCommands():
        """Iterator over all known commands.

        :return: All options defined in :class:`CmdlineCommands`.
        :rtype: ``Iterable<str>``"""

        for member in CmdlineCommands.__dict__:
            if member.isupper and isinstance(CmdlineCommands.__dict__[member], str):
                yield CmdlineCommands.__dict__[member]



    @classmethod
    def isExistingCommand(cls, commandName):
        """Check whether a command with name ``commandName`` does exists in :class:`_CmdlineCommandsUtils`.

        :param commandName: Name of the command which existence shall be checked.
        :type commandName: ``str``

        :return: ``True`` if option with name ``commandName`` exists; ``False`` otherwise.
        :rtype: ``bool``"""

        try:
            next(filter(lambda cmd: cmd == commandName, cls.getAllCommands()))
            return True
        except StopIteration:
            return False

# }}} CLASSES

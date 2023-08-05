# _cmdline_arguments_processor.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2014 Róbert Čerňanský



""":class:`_CmdlineArgumentsProcessor` class."""



__all__ = ["_CmdlineArgumentsProcessor"]



# {{{ INCLUDES

from AutoArchive._infrastructure.utils import Utils
from . import OptionsUtils

# }}} INCLUDES



# {{{ CLASSES

class _CmdlineArgumentsProcessor:
    """Processes command-line arguments and populates :class:`.IConfiguration` instance.

    :param optparseValues: Command-line options and their values.
    :type optparseValues: :class:`optparse.Values`"""

    def __init__(self, optparseValues):
        self.__optparseValues = optparseValues



    def populateConfiguration(self, configuration):
        """Populates ``configuration`` with options specified on the command line.

        .. note:: Options that are not defined in the :class:`.Options` class are skipped; it is assumed that they are
           commands for command-line UI.

        :param configuration: Configuration that should be populated.
        :type configuration: :class:`._Configuration`"""

        for optParseOption in self.__optparseValues.__dict__:
            if self.__optparseValues.__dict__[optParseOption] is not None:
                option = optParseOption.replace("_", "-")
                try:
                    if OptionsUtils.isExistingOption(option):
                        configuration._addOrReplaceOption(option, str(self.__optparseValues.__dict__[optParseOption]))
                except ValueError:
                    Utils.fatalExit(str.format(
                            "Wrong value \"{}\" of the option \"{}\" specified on the command line.",
                            self.__optparseValues.__dict__[optParseOption], option))

# }}} CLASSES

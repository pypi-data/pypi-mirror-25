# _cmdline_arguments_processor.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2011 Róbert Čerňanský



""":class:`_CmdlineArgumentsProcessor` class."""



__all__ = ["_CmdlineArgumentsProcessor"]



# {{{ INCLUDES

from .. import *

# }}} INCLUDES



# {{{ CLASSES

class _CmdlineArgumentsProcessor:
    """Processes command-line arguments and populates :class:`.IConfiguration` instance.

    :param optparseValues: Command-line options and their values.
    :type optparseValues: :class:`optparse.Values`"""

    def __init__(self, optparseValues):
        self.__optparseValues = optparseValues



    def populateConfiguration(self, appConfig):
        """Populates ``appConfig`` with options specified on the command line.

        .. note:: Options that are not defined in the :class:`.Options` class are skipped; it is assumed that they are
           commands for command-line UI.

        :param appConfig: Configuration that should be populated.
        :type appConfig: :class:`._AppConfig`"""

        for optParseOption in self.__optparseValues.__dict__:
            if self.__optparseValues.__dict__[optParseOption] is not None:
                try:
                    option = optParseOption.replace("_", "-")
                    if OptionsUtils.isExistingOption(option):
                        appConfig._addOrReplaceOption(option, str(self.__optparseValues.__dict__[optParseOption]))
                except ValueError:
                    _Utils.fatalExit(str.format(
                            "Wrong value \"{}\" of the option \"{}\" specified on the command line.",
                            self.__optparseValues.__dict__[optParseOption], option))

# }}} CLASSES

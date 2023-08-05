# _config_file_processor.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2014 Róbert Čerňanský



""":class:`_ConfigFileProcessor` class."""



__all__ = ["_ConfigFileProcessor"]



# {{{ INCLUDES

import configparser
import os.path

from AutoArchive._infrastructure.utils import Utils
from . import Options

# }}} INCLUDES



# {{{ CLASSES

class _ConfigFileProcessor:
    """Processes configuration files and populates :class:`.IConfiguration` instance.

    :param appEnvironment: :class:`.AppEnvironment` instance.
    :type appEnvironment: :class:`.AppEnvironment`
    :param factoryUserConfigDir: Pre-defined path to the :term:`user configuration directory`.
    :type factoryUserConfigDir: ``str``
    :param factoryUserConfigFileProvider: Function that returns path to the :term:`user configuration file` based on
       the passed configuration directory.
    :type factoryUserConfigFileProvider: ``function{str, =>str}``
    :param userConfigDir: Path to the user configuration directory.
    :type userConfigDir: ``str``
    :param userConfigFile: Path to the user configuration file.
    :type userConfigFile: ``str``"""

    # system configuration file - full path
    __SYSTEM_CONFIG_FILE = os.path.join("/etc/aa/aa.conf")

    __SECTION_GENERAL = "General"
    __SECTION_ARCHIVE = "Archive"

    # options not suitable for a configuration file
    __INVALID_OPTIONS = frozenset(str(opt)
                                  for opt in (Options.LEVEL,
                                              Options.ALL,
                                              Options.NO_INCREMENTAL,
                                              Options.NO_RESTARTING,
                                              Options.NO_REMOVE_OBSOLETE_BACKUPS,
                                              Options.NO_KEEP_OLD_BACKUPS,
                                              Options.NO_ALL,
                                              Options.NO_OVERWRITE_AT_START))

    # options not suitable for the global configuration file
    __INVALID_OPTIONS_GLOBAL = frozenset()

    # options not suitable for the user configuration file
    __INVALID_OPTIONS_USER = frozenset(str(opt)
                                       for opt in (Options.USER_CONFIG_FILE,
                                                   Options.USER_CONFIG_DIR))



    def __init__(self, appEnvironment, factoryUserConfigDir, factoryUserConfigFileProvider, userConfigDir = None,
                 userConfigFile = None):
        self.__appEnvironment = appEnvironment
        self.__factoryUserConfigDir = factoryUserConfigDir
        self.__factoryUserConfigFileProvider = factoryUserConfigFileProvider
        self.__userConfigDir = userConfigDir
        self.__userConfigFile = userConfigFile



    def populateConfiguration(self, configuration):
        """Populates ``configuration`` with options.

        :param configuration: Configuration that should be populated.
        :type configuration: :class:`._Configuration`"""

        supportedSections = {self.__SECTION_GENERAL, self.__SECTION_ARCHIVE}

        # process system configuration file
        self.__processConfigFile(
            self.__SYSTEM_CONFIG_FILE, configuration, supportedSections,
            self.__INVALID_OPTIONS | self.__INVALID_OPTIONS_GLOBAL)

        # process user configuration file
        userConfigDir = self.__userConfigDir or configuration[Options.USER_CONFIG_DIR] or self.__factoryUserConfigDir
            
        userConfigFile = self.__userConfigFile or configuration[Options.USER_CONFIG_FILE] or \
                self.__factoryUserConfigFileProvider(userConfigDir)

        self.__processConfigFile(
            userConfigFile, configuration, supportedSections, self.__INVALID_OPTIONS | self.__INVALID_OPTIONS_USER)



    def __processConfigFile(self, configFile, configuration, supportedSections, invalidOptions):
        configParser = configparser.ConfigParser(interpolation = None)
        try:
            configParser.read(configFile)
        except (configparser.MissingSectionHeaderError, configparser.ParsingError) as ex:
            Utils.fatalExit(ex)
        except UnicodeDecodeError as ex:
            Utils.fatalExit(str.format("Unable to parse file \"{}\" [{}].", configFile, ex))

        if len(supportedSections.union(configParser.sections())) > len(supportedSections):
            Utils.fatalExit(str.format(
                    "One or more invalid sections found in the configuration file \"{}\".", configFile),
                             self.__appEnvironment.executableName)

        self.__addOptionsFromSection(self.__SECTION_GENERAL, configuration, configParser, configFile, invalidOptions)
        self.__addOptionsFromSection(self.__SECTION_ARCHIVE, configuration, configParser, configFile, invalidOptions)



    def __addOptionsFromSection(self, section, configuration, configParser, configFile, invalidOptions):
        if configParser.has_section(section):
            for configOption in configParser.options(section):
                try:
                    if configOption in invalidOptions:
                        raise KeyError("Not suitable for a config. file")
                    value = configParser.get(section, configOption)
                    configuration._addOrReplaceOption(configOption, value)
                except KeyError:
                    Utils.fatalExit(str.format(
                            "Invalid option \"{}\" in the configuration file \"{}\".", configOption, configFile),
                                     self.__appEnvironment.executableName)
                except ValueError:
                    Utils.fatalExit(str.format(
                            "Wrong value \"{}\" of the option \"{}\" in the configuration file \"{}\".",
                            value, configOption, configFile), self.__appEnvironment.executableName)

# }}} CLASSES

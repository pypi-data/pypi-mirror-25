# _configuration_factory.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2017 Róbert Čerňanský



""":class:`ConfigurationFactory` class."""



__all__ = ["ConfigurationFactory"]



# {{{ INCLUDES

import os

from AutoArchive._infrastructure.utils import Utils
from AutoArchive._infrastructure.configuration import ArchiverTypes
from . import Options, OptionsUtils
from ._configuration import *
from ._cmdline_arguments_processor import _CmdlineArgumentsProcessor
from ._config_file_processor import _ConfigFileProcessor

# }}} INCLUDES



# {{{ CLASSES

# SMELL: Creation of archive specifications directory should perhaps go to Archiving?
class ConfigurationFactory():
    """Support of configuration options and a persistent storage.

    During :meth:`makeConfiguration` call it creates :class:`.IConfiguration` implementation instance.  It also
    creates :term:`user configuration directory` and :term:`archive specifications directory` if either of them does
    not exists.

    The :class:`.ConfigurationBase`-like class provides access to configuration options.  It is instantiated and
    populated during :meth:`makeConfiguration` call from :attr:`.ApplicationContext.appEnvironment.options`
    (command-line options) and from configuration files.  The :term:`system configuration file` is "/etc/aa/aa.conf".
    The :term:`user configuration file` location is determined by values of :attr:`.Options.USER_CONFIG_FILE` and
    :attr:`.Options.USER_CONFIG_DIR` options.  The :term:`user configuration directory` is automatically created if
    it does not exists.  The format of configuration files is defined by the standard :mod:`configparser` module
    (without interpolation).

    The :class:`.ConfigurationBase` implementation instance is populated in the way that same options specified in
    multiple sources overrides each other so that the order of precedence from highest to lowest is following:
    command-line, user configuration file, system configuration file.  However the implementation recognizes certain
    types of options that does not follow this rule (see :meth:`.ConfigurationBase.__getitem__()`).

    Some of the options, if not specified in neither of possible sources, has some predefined default value.  The list
    of these options with their predefined value follows:

    * :attr:`.Options.ARCHIVER`\ : :attr:`.ArchiverTypes.TarGz`
    * :attr:`.Options.DEST_DIR`\ : ``os.curdir``
    * :attr:`.Options.RESTART_AFTER_LEVEL`\ : 10
    * :attr:`.Options.ARCHIVE_SPECS_DIR`\ : :attr:`.Options.USER_CONFIG_DIR` + "archive_specs"
    * :attr:`.Options.USER_CONFIG_FILE`\ : :attr:`.Options.USER_CONFIG_DIR` + "aa.conf"
    * :attr:`.Options.USER_CONFIG_DIR`\ : "~/.config/aa"
    * :attr:`.Options.NUMBER_OF_OLD_BACKUPS`\ : 1
    * options of type ``bool``\ : ``False``"""

    # user configuration directory
    __FACTORY_USER_CONFIG_DIR = os.path.expanduser("~/.config/aa")

    # configuration file name
    __CONFIG_FILE_NAME = "aa.conf"



    @classmethod
    def makeConfiguration(cls, appEnvironment):
        """Creates and populates configuration.

        :param appEnvironment: Application environment.
        :type appEnvironment: :class:`.AppEnvironment`"""

        configuration = cls.__createAndPopulateConfig(appEnvironment)

        userDirectoryCreated = cls.__createUserConfigDirectory(configuration)
        cls.__createArchiveSpecsDirectory(configuration, userDirectoryCreated)

        return configuration



    # {{{ helpers

    @classmethod
    def __createAndPopulateConfig(cls, appEnvironment):

        optparseValues = appEnvironment.options
        cmdlineArgumentsProcessor = _CmdlineArgumentsProcessor(optparseValues)

        cmdlineUserConfigDir, cmdlineUserConfigFile = cls.__getUserPathsFromCmdline(
            cmdlineArgumentsProcessor, appEnvironment)

        # create IConfiguration which will be registered to Component Accessor
        configuration = _Configuration()

        cls.__prePopulateWithDefaults(configuration)

        # populate configuration with config. file options
        configFileProcessor = _ConfigFileProcessor(
            appEnvironment, cls.__FACTORY_USER_CONFIG_DIR,
            lambda usrDir: os.path.join(usrDir, cls.__CONFIG_FILE_NAME),
            cmdlineUserConfigDir, cmdlineUserConfigFile)
        configFileProcessor.populateConfiguration(configuration)

        # populate configuration with command line options
        cmdlineArgumentsProcessor.populateConfiguration(configuration)

        cls.__postPopulateWithDefaults(configuration)

        return configuration



    @staticmethod
    def __getUserPathsFromCmdline(cmdlineArgumentsProcessor, appEnvironment):

        # create temporary IConfiguration and populate it with command line options
        cmdlineConfiguration = _Configuration()
        cmdlineArgumentsProcessor.populateConfiguration(cmdlineConfiguration)

        # determine and create user config directory if it does not exists
        cmdlineUserConfigDir = cmdlineConfiguration[Options.USER_CONFIG_DIR]

        # get user config file passed as an command-line option, if any and show error if it does not exists
        cmdlineUserConfigFile = cmdlineConfiguration[Options.USER_CONFIG_FILE]
        if cmdlineUserConfigFile:
            if not os.path.isfile(cmdlineUserConfigFile):
                Utils.printError(str.format("Configuration file \"{}\" does not exists.",
                                             cmdlineUserConfigFile), appEnvironment.executableName)

        return cmdlineUserConfigDir, cmdlineUserConfigFile



    @staticmethod
    def __prePopulateWithDefaults(configuration):
        configuration._addOrReplaceOption(str(Options.ARCHIVER), OptionsUtils.archiverTypeToStr(ArchiverTypes.TarGz))
        configuration._addOrReplaceOption(str(Options.DEST_DIR), os.curdir)
        configuration._addOrReplaceOption(str(Options.RESTART_AFTER_LEVEL), 10)
        configuration._addOrReplaceOption(str(Options.NUMBER_OF_OLD_BACKUPS), 1)



    @classmethod
    def __postPopulateWithDefaults(cls, configuration):
        cls.__addOptionIfNone(configuration, Options.USER_CONFIG_DIR, cls.__FACTORY_USER_CONFIG_DIR)

        cls.__addOptionIfNone(
            configuration, Options.USER_CONFIG_FILE, os.path.join(
                configuration[Options.USER_CONFIG_DIR], cls.__CONFIG_FILE_NAME))

        cls.__addOptionIfNone(
            configuration, Options.ARCHIVE_SPECS_DIR, os.path.join(
                configuration[Options.USER_CONFIG_DIR], "archive_specs"))



    @staticmethod
    def __addOptionIfNone(configuration, option, value):
        if configuration.getRawValue(option) is None:
            configuration._addOrReplaceOption(str(option), value)



    @staticmethod
    def __createUserConfigDirectory(configuration):
        userConfigDir = configuration[Options.USER_CONFIG_DIR]
        if not os.path.exists(userConfigDir):
            try:
                if not configuration[Options.QUIET]:
                    Utils.printWarning(str.format(
                            "User configuration directory does not exists. Creating \"{}\".", userConfigDir))
                os.makedirs(userConfigDir)
                return True
            except OSError as ex:
                Utils.printError(str.format(
                        "Unable to create user configuration directory: \"{}\". The reason is: {}",
                        userConfigDir, ex.strerror))

        return False



    @staticmethod
    def __createArchiveSpecsDirectory(configuration, userDirectoryCreated):
        userConfigDir = configuration[Options.USER_CONFIG_DIR]
        archiveSpecsDirectory = configuration[Options.ARCHIVE_SPECS_DIR]
        if not os.path.exists(archiveSpecsDirectory):
            try:

                # show warning only if we are not quiet and if the user configuration directory was not just created;
                # or in case it was just created the archive specifications directory is not its subdirectory
                if not configuration[Options.QUIET] and \
                   (not userDirectoryCreated or
                    not os.path.commonprefix((userConfigDir, archiveSpecsDirectory)) == userConfigDir):

                    Utils.printWarning(str.format(
                            "Archive specifications directory does not exists. Creating \"{}\".",
                            archiveSpecsDirectory))

                os.makedirs(archiveSpecsDirectory)

            except OSError as ex:
                Utils.printError(str.format(
                        "Unable to create archive specifications directory: \"{}\". The reason is: {}",
                        archiveSpecsDirectory, ex.strerror))

    # }}} helpers

# }}} CLASSES

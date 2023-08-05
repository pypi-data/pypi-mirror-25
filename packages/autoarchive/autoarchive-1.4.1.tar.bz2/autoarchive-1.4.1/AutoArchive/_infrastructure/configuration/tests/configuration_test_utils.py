# configuration_test_utils.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2017 Róbert Čerňanský



""":class:`ConfigurationTestUtils` class."""



__all__ = ["ConfigurationTestUtils"]



# {{{ INCLUDES

from abc import ABCMeta, abstractmethod
import os
import shutil
from optparse import OptionParser
import tempfile

from mock import MagicMock

from AutoArchive._infrastructure._app_environment import AppEnvironment
from AutoArchive._infrastructure.configuration import Options, ConfigurationBase
from AutoArchive._infrastructure.configuration._configuration_factory import ConfigurationFactory
from AutoArchive.tests import ComponentTestUtils

# }}} INCLUDES



# {{{ CLASSES

class ConfigurationTestUtils(metaclass = ABCMeta):
    """Utility methods for Configuration component tests."""

    # Name of the default storage realm used if the realm is not specified.
    __DEFAULT_REALM = "TestDefaultRealm"

    # Name of the default storage section used if the section is not specified.
    DEFAULT_SECTION = "TestDefaultSection"

    # Subdirectory where the storage place its files.
    __STORAGE_SUBDIR = "storage"



    @abstractmethod
    def __init__(self):
        pass



    @staticmethod
    def createConfigurationMock(options = None):
        """Creates a mock of :class:`ConfigurationBase` and initializes it with passed arguments.

        :param options: Dictionary of option: value with which the mock will be initialized.
        :type options: ``dict<Option, object>``

        :return: Mock of the :class:`ConfigurationBase`.
        :rtype: :class:`mock.Mock<ConfigurationBase>`"""

        def getItemSideEffect(option):
            try:
                return options[option]
            except KeyError:
                return None



        if options is None:
            options = {}

        mockConfiguration = MagicMock(spec_set = ConfigurationBase)
        mockConfiguration.__getitem__.side_effect = getItemSideEffect
        mockConfiguration.getRawValue.side_effect = getItemSideEffect

        return mockConfiguration



    @staticmethod
    def makeUserConfigDirectory():
        """Creates the user configuration directory and stores its path in the :class:`.ComponentTestContext` instance.

        :raise RuntimeError: If the user configuration directory was already created, i. e. the
           :attr:`.ComponentTestContext.userConfigDir` is not ``None``."""

        if ComponentTestUtils.getComponentTestContext().userConfigDir is not None:
            raise RuntimeError("User configuration directory already created.")

        ComponentTestUtils.getComponentTestContext().userConfigDir = tempfile.mkdtemp(
            prefix = "user_config", dir = ComponentTestUtils.getComponentTestContext().workDir)



    @staticmethod
    def removeUserConfigDirectory():
        """Removes the user configuration directory and its path from the :class:`.ComponentTestContext` instance."""

        shutil.rmtree(ComponentTestUtils.getComponentTestContext().userConfigDir)
        ComponentTestUtils.getComponentTestContext().userConfigDir = None



    @staticmethod
    def makeArchiveSpecsDirectory():
        """Creates the arch. spec. files directory and stores its path in the :class:`.ComponentTestContext` instance.

        :raise RuntimeError: If the user configuration directory was already created, i. e. the
           :attr:`.ComponentTestContext.userConfigDir` is not ``None``."""

        if ComponentTestUtils.getComponentTestContext().archiveSpecsDir is not None:
            raise RuntimeError("Archive specification files directory already created.")

        ComponentTestUtils.getComponentTestContext().archiveSpecsDir = tempfile.mkdtemp(
            prefix = "archive_specs_test", dir = ComponentTestUtils.getComponentTestContext().workDir)



    @staticmethod
    def removeArchiveSpecsDirectory():
        """Removes the arch. spec. files directory and its path from the :class:`.ComponentTestContext` instance."""

        shutil.rmtree(ComponentTestUtils.getComponentTestContext().archiveSpecsDir)
        ComponentTestUtils.getComponentTestContext().archiveSpecsDir = None



    @classmethod
    def _setUpClassConfigurationComponent(cls):
        ComponentTestUtils.setUpClassComponent()

        # although it is not necessary to create the directory since the class will create it we just reusing
        # the utility method here
        ConfigurationTestUtils.makeUserConfigDirectory()

        os.mkdir(os.path.join(ComponentTestUtils.getComponentTestContext().userConfigDir, cls.__STORAGE_SUBDIR))

        # although it is not necessary to create the directory since the class will create it we just reusing
        # the utility method here
        cls.makeArchiveSpecsDirectory()



    @classmethod
    def _tearDownClassConfigurationComponent(cls):
        cls.removeArchiveSpecsDirectory()
        os.rmdir(os.path.join(ComponentTestUtils.getComponentTestContext().userConfigDir, cls.__STORAGE_SUBDIR))
        ConfigurationTestUtils.removeUserConfigDirectory()

        ComponentTestUtils.tearDownClassComponent()



    @classmethod
    def _setUpConfigurationComponent(cls, options = None, userConfigFile = None):
        parser = OptionParser()
        parser.add_option(cls._makeCmdlineOption(Options.USER_CONFIG_DIR))
        cmdline = [cls._makeCmdlineOption(Options.USER_CONFIG_DIR) + "=" +
                   ComponentTestUtils.getComponentTestContext().userConfigDir]
        if userConfigFile:
            parser.add_option(cls._makeCmdlineOption(Options.USER_CONFIG_FILE))
            cmdline.append(cls._makeCmdlineOption(Options.USER_CONFIG_FILE) + "=" + userConfigFile)
        parser.add_option(cls._makeCmdlineOption(Options.ARCHIVE_SPECS_DIR))
        cmdline.append(cls._makeCmdlineOption(Options.ARCHIVE_SPECS_DIR) + "=" +
                       ComponentTestUtils.getComponentTestContext().archiveSpecsDir)
        options = parser.parse_args(cmdline, options)[0]

        appEnvironment = AppEnvironment("test_aa", options, [])

        return ConfigurationFactory.makeConfiguration(appEnvironment)



    @classmethod
    def _tearDownConfigurationComponent(cls):
        pass



    @staticmethod
    def _makeCmdlineOption(option):
        return "--" + str(option)

# }}} CLASSES

# test_configuration.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2014 Róbert Čerňanský



""":class:`TestConfiguration` class."""



__all__ = ["TestConfiguration"]



# {{{ INCLUDES

import unittest
import os
from optparse import OptionParser

from AutoArchive._infrastructure.configuration import Options
from AutoArchive.tests import ComponentTestUtils
from .configuration_test_utils import ConfigurationTestUtils

# }}} INCLUDES



# {{{ CLASSES

class TestConfiguration(unittest.TestCase):
    """Test of :class:`.IConfiguration` provided interface."""

    # Each test should call __setUpConfiguration() method; if called with non-None configFileContent argument
    # then the test has to call __removeUserConfigFile() at the end of the its method.



    # Name of the user configuration file.
    __USER_CONFIG_FILE = "test_aa.conf"



    @classmethod
    def setUpClass(cls):
        ConfigurationTestUtils._setUpClassConfigurationComponent()



    @classmethod
    def tearDownClass(cls):
        ConfigurationTestUtils._tearDownClassConfigurationComponent()



    def setUp(self):
        self.__parser = OptionParser()



    def tearDown(self):
        ConfigurationTestUtils._tearDownConfigurationComponent()



    # {{{ __getitem__() tests

    def test_getItemBool(self):
        """Tests the __getitem__() method for a ``bool`` value.

        Sets a ``bool``\-type option through the command line and verifies that its retrieved value is ``True``.  Also
        verifies that for an another ``bool`` option, not set at all, the returned value is ``False`` since for ``bool``
        options ``None`` should be converted to ``False``."""

        self.__parser.add_option(ConfigurationTestUtils._makeCmdlineOption(Options.INCREMENTAL), action = "store_true")
        cmdline = [ConfigurationTestUtils._makeCmdlineOption(Options.INCREMENTAL)]
        configuration = self.__setUpConfiguration(cmdline)

        # test that the INCREMENTAL option was set to True
        self.assertTrue(configuration[Options.INCREMENTAL])

        # test that the RESTARTING option, which was not specified at all, was set to False (instead of None)
        self.assertFalse(configuration[Options.RESTARTING])



    def test_getItemInt(self):
        """Tests the __getitem__() method for an ``int`` value.

        Sets an ``int``\-type option through the command line and verifies that its retrieved value is equal to the one
        that was set."""

        LEVEL = 99

        self.__parser.add_option(ConfigurationTestUtils._makeCmdlineOption(Options.LEVEL), type = "int")
        cmdline = [ConfigurationTestUtils._makeCmdlineOption(Options.LEVEL) + "=" + str(LEVEL)]
        configuration = self.__setUpConfiguration(cmdline)

        # test that the LEVEL option was set to LEVEL value
        self.assertEqual(configuration[Options.LEVEL], LEVEL)

        # test that the RESTART_AFTER_AGE option, which was not specified at all, was set to None
        self.assertIsNone(configuration[Options.RESTART_AFTER_AGE])



    def test_getItemStr(self):
        """Tests the __getitem__() method for a ``str`` value.

        Sets an ``str``\-type option through the command line and verifies that its retrieved value is equal to the one
        that was set."""

        DEST_DIR = "TEST_DEST_DIR"

        self.__parser.add_option(ConfigurationTestUtils._makeCmdlineOption(Options.DEST_DIR))
        cmdline = [ConfigurationTestUtils._makeCmdlineOption(Options.DEST_DIR) + "=" + DEST_DIR]
        configuration = self.__setUpConfiguration(cmdline)

        # test that the DEST_DIR option was set to DEST_DIR value
        self.assertEqual(configuration[Options.DEST_DIR], DEST_DIR)



    def test_getItemNegationForm(self):
        """Tests the __getitem__() method for an option with negation form defined.

        Sets an option in its *normal form* and its *negation form*, both through the command line.  Verifies that
        its retrieved value is ``False`` since the *negation form* has precedence over the *normal form*."""

        self.__parser.add_option(ConfigurationTestUtils._makeCmdlineOption(Options.INCREMENTAL), action = "store_true")
        cmdline = [ConfigurationTestUtils._makeCmdlineOption(Options.INCREMENTAL)]
        self.__parser.add_option(ConfigurationTestUtils._makeCmdlineOption(Options.NO_INCREMENTAL),
                                 action = "store_true")
        cmdline.append(ConfigurationTestUtils._makeCmdlineOption(Options.NO_INCREMENTAL))
        configuration = self.__setUpConfiguration(cmdline)

        # test that the INCREMENTAL option was set to False
        self.assertFalse(configuration[Options.INCREMENTAL])



    def test_getItemForceForm(self):
        """Tests the __getitem__() method for an option with force form defined.

        Sets an option in its *negation form* and its *force form*, both through the command line.  Verifies that
        its retrieved value is ``True`` since the *force form* has precedence over the *negation form*."""

        self.__parser.add_option(ConfigurationTestUtils._makeCmdlineOption(Options.NO_INCREMENTAL),
                                 action = "store_true")
        cmdline = [ConfigurationTestUtils._makeCmdlineOption(Options.NO_INCREMENTAL)]
        self.__parser.add_option(ConfigurationTestUtils._makeCmdlineOption(Options.FORCE_INCREMENTAL),
                                 action = "store_true")
        cmdline.append(ConfigurationTestUtils._makeCmdlineOption(Options.FORCE_INCREMENTAL))
        configuration = self.__setUpConfiguration(cmdline)

        # test that the INCREMENTAL option was forced to True
        self.assertTrue(configuration[Options.INCREMENTAL])



    def test_getItemUserConfig(self):
        """Tests the __getitem__() method for an option initialized from the user configuration file.

        Sets an option through the user configuration file and verifies that its retrieved value is equal to the one
        that was set."""

        FULL_RESTART_AFTER_AGE = 99

        # setup the user configuration file
        configFileContent = str.format("""\
[Archive]
full-restart-after-age = {}
""", FULL_RESTART_AFTER_AGE)
        configuration = self.__setUpConfiguration(configFileContent = configFileContent)

        # test that the FULL_RESTART_AFTER_AGE option was set to the command line value
        self.assertEqual(configuration[Options.FULL_RESTART_AFTER_AGE], FULL_RESTART_AFTER_AGE)

        self.__removeUserConfigFile()



    def test_getItemCmdlinePrecedence(self):
        """Tests the __getitem__() method for precedence of options specified on a command line.

        Sets an option through command line and through the user configuration file.  Verifies that its retrieved value
        is equal to the one that was set through the command line because command line values overrides configuration
        file values."""

        CMDLINE_FULL_RESTART_AFTER_AGE = 98
        CONFIG_FULL_RESTART_AFTER_AGE = 99

        # setup command line options
        self.__parser.add_option(ConfigurationTestUtils._makeCmdlineOption(Options.FULL_RESTART_AFTER_AGE),
                                 type = "int")
        cmdline = [ConfigurationTestUtils._makeCmdlineOption(Options.FULL_RESTART_AFTER_AGE) + "=" +
                   str(CMDLINE_FULL_RESTART_AFTER_AGE)]

        # setup the user configuration file
        configFileContent = str.format("""\
[Archive]
full-restart-after-age = {}
""", CONFIG_FULL_RESTART_AFTER_AGE)
        configuration = self.__setUpConfiguration(cmdline, configFileContent)

        # test that the FULL_RESTART_AFTER_AGE option was set to the command line value
        self.assertEqual(configuration[Options.FULL_RESTART_AFTER_AGE], CMDLINE_FULL_RESTART_AFTER_AGE)

        self.__removeUserConfigFile()



    def test_getItemCmdlinePrecedenceForceForm(self):
        """Tests the __getitem__() method for precedence of an option specified on a command line and force in config.

        Sets an option through command line and its *force form* through the user configuration file.  Even the
        command line options overrides those from configuration file, the *force form* should win in cases like
        this because for parsers it is *not* the same option (e. g. one is ``--compression-level`` and the other is
        ``--force-compression-level``) so they do not override each other."""

        CMDLINE_COMPRESSION_LEVEL = 98
        CONFIG_FORCE_COMPRESSION_LEVEL = 99

        # setup command line options
        self.__parser.add_option(ConfigurationTestUtils._makeCmdlineOption(Options.COMPRESSION_LEVEL),
                                 type = "int")
        cmdline = [ConfigurationTestUtils._makeCmdlineOption(Options.COMPRESSION_LEVEL) + "=" +
                   str(CMDLINE_COMPRESSION_LEVEL)]

        # setup the user configuration file
        configFileContent = str.format("""\
[Archive]
force-compression-level = {}
""", CONFIG_FORCE_COMPRESSION_LEVEL)
        configuration = self.__setUpConfiguration(cmdline, configFileContent)

        # test that the COMPRESSION_LEVEL option was set to the force value from the configuration file
        self.assertEqual(configuration[Options.COMPRESSION_LEVEL], CONFIG_FORCE_COMPRESSION_LEVEL)

        self.__removeUserConfigFile()

    # }}} __getitem__() tests



    # {{{ getRawValue() tests

    def test_getRawValue(self):
        """Tests the getRawValue() method.

        Sets an option in its *negation form* and its *force form*, both through the command line.  Verifies that
        retrieved value for its *normal form* is ``None`` and for its *negation form* and its *force form* is
        ``True``."""

        self.__parser.add_option(ConfigurationTestUtils._makeCmdlineOption(Options.NO_INCREMENTAL),
                                 action = "store_true")
        cmdline = [ConfigurationTestUtils._makeCmdlineOption(Options.NO_INCREMENTAL)]
        self.__parser.add_option(ConfigurationTestUtils._makeCmdlineOption(Options.FORCE_INCREMENTAL),
                                 action = "store_true")
        cmdline.append(ConfigurationTestUtils._makeCmdlineOption(Options.FORCE_INCREMENTAL))
        configuration = self.__setUpConfiguration(cmdline)

        # test the raw values of all forms of the INCREMENTAL option
        self.assertIsNone(configuration.getRawValue(Options.INCREMENTAL))
        self.assertTrue(configuration.getRawValue(Options.NO_INCREMENTAL))
        self.assertTrue(configuration.getRawValue(Options.FORCE_INCREMENTAL))

    # }}} getRawValue() tests



    # {{{ helpers

    def __setUpConfiguration(self, cmdline = None, configFileContent = None):
        if cmdline is None: cmdline = []

        options = self.__parser.parse_args(cmdline)[0]
        configFilePath = self.__createUserConfigFile(configFileContent) if configFileContent else None

        return ConfigurationTestUtils._setUpConfigurationComponent(options, configFilePath)



    @classmethod
    def __createUserConfigFile(cls, content):
        configFilePath = os.path.join(ComponentTestUtils.getComponentTestContext().userConfigDir,
                                      cls.__USER_CONFIG_FILE)
        with open(configFilePath, "w") as configFile:
            configFile.write(content)
        return configFilePath



    @classmethod
    def __removeUserConfigFile(cls):
        os.remove(os.path.join(ComponentTestUtils.getComponentTestContext().userConfigDir, cls.__USER_CONFIG_FILE))

    # }}} helpers

# }}} CLASSES

# test_icomponent_ui.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2012 Róbert Čerňanský



""":class:`TestIComponentUi`."""



__all__ = ["TestIComponentUi"]



# {{{ INCLUDES

import unittest
from mock import Mock, patch

import sys
import io

from ...._mainf import *
from ...._configuration import *
from .. import *

from ....tests import *
from .cmdline_ui_test_utils import *

# }}} INCLUDES



# {{{ CLASSES

class TestIComponentUi(unittest.TestCase):
    """Test of :class:`.IComponentUi` provided interface."""

    __TEST_MESSAGE = "test message"



    @classmethod
    def setUpClass(cls):
        CmdlineUiTestUtils._setUpClassCmdlineUiComponent()



    @classmethod
    def tearDownClass(cls):
        CmdlineUiTestUtils._tearDownClassCmdlineUiComponent()



    def setUp(self):
        CmdlineUiTestUtils._setUpCommon()
        CmdlineUiTestUtils._setUpCmdlineUiComponent(
            {Options.USER_CONFIG_DIR: ComponentTestUtils.getComponentTestContext().userConfigDir})

        self.__runCmdlineUiComponent()

        sys.stdout = io.StringIO()
        sys.stderr = io.StringIO()



    def tearDown(self):
        sys.stderr = sys.__stderr__
        sys.stdout = sys.__stdout__

        CmdlineUiTestUtils._tearDownCmdlineUiComponent()
        CmdlineUiTestUtils._tearDownCommon()



    def test_showVerbose(self):
        """Tests the showVerbose() method.

        Configures option for verbosity to True, subscribes to :meth:`.ICmdlineUi.messageShown` event and shows
        a verbose message.  Checks that the message was shown and the event was fired."""

        # ignore standard setup and make a new one with changed options
        CmdlineUiTestUtils._tearDownCmdlineUiComponent()
        CmdlineUiTestUtils._setUpCmdlineUiComponent(
            {Options.USER_CONFIG_DIR: ComponentTestUtils.getComponentTestContext().userConfigDir,
             Options.VERBOSE: True})
        self.__runCmdlineUiComponent()

        cmdlineUi = CmdlineUiTestUtils._mockInterfaceAccessor.getComponentInterface(IComponentUi)
        mockOnMessageShown = Mock()
        cmdlineUi.messageShown += mockOnMessageShown
        cmdlineUi.showVerbose(self.__TEST_MESSAGE)

        self.assertTrue(sys.stdout.getvalue().find(self.__TEST_MESSAGE) != -1, "Message was not shown.")
        self.assertEqual(mockOnMessageShown.call_count, 1, "MessageShown event not fired or fired more than once.")



    def test_showVerboseFalse(self):
        """Tests the showVerbose() method with verbosity turned off.

        Subscribes to :meth:`ICmdlineUi.messageShown` event and shows a verbose message.  Checks that the message was
        _not_ shown (because by default the verbosity is turned off) and the event was fired."""

        cmdlineUi = CmdlineUiTestUtils._mockInterfaceAccessor.getComponentInterface(IComponentUi)
        mockOnMessageShown = Mock()
        cmdlineUi.messageShown += mockOnMessageShown
        cmdlineUi.showVerbose(self.__TEST_MESSAGE)

        self.assertTrue(sys.stdout.getvalue().find(self.__TEST_MESSAGE) == -1, "Message was shown.")
        self.assertEqual(mockOnMessageShown.call_count, 1, "MessageShown event not fired or fired more than once.")



    def test_showVerboseQuiet(self):
        """Tests the showVerbose() method with both verbosity and quietness turned on.

        Configures options for verbosity and quietness to True, subscribes to :meth:`.ICmdlineUi.messageShown` event
        and shows a verbose message.  Checks that the message was _not_ shown (because 'quiet' overrides 'verbose')
        and the event was fired."""

        # ignore standard setup and make a new one with changed options
        CmdlineUiTestUtils._tearDownCmdlineUiComponent()
        CmdlineUiTestUtils._setUpCmdlineUiComponent(
            {Options.USER_CONFIG_DIR: ComponentTestUtils.getComponentTestContext().userConfigDir,
             Options.VERBOSE: True,
             Options.QUIET: True})
        self.__runCmdlineUiComponent()

        cmdlineUi = CmdlineUiTestUtils._mockInterfaceAccessor.getComponentInterface(IComponentUi)
        mockOnMessageShown = Mock()
        cmdlineUi.messageShown += mockOnMessageShown
        cmdlineUi.showVerbose(self.__TEST_MESSAGE)

        self.assertTrue(sys.stdout.getvalue().find(self.__TEST_MESSAGE) == -1, "Message was shown.")
        self.assertEqual(mockOnMessageShown.call_count, 1, "MessageShown event not fired or fired more than once.")



    def test_showNotification(self):
        """Tests the showNotification() method.

        Subscribes to :meth:`ICmdlineUi.messageShown` event and shows a notification message.  Checks that the message
        was shown and the event was fired."""

        cmdlineUi = CmdlineUiTestUtils._mockInterfaceAccessor.getComponentInterface(IComponentUi)
        mockOnMessageShown = Mock()
        cmdlineUi.messageShown += mockOnMessageShown
        cmdlineUi.showNotification(self.__TEST_MESSAGE)

        self.assertTrue(sys.stdout.getvalue().find(self.__TEST_MESSAGE) != -1, "Message was not shown.")
        self.assertEqual(mockOnMessageShown.call_count, 1, "MessageShown event not fired or fired more than once.")



    def test_showInfo(self):
        """Tests the showInfo() method.

        Subscribes to :meth:`ICmdlineUi.messageShown` event and shows an info message.  Checks that the message
        was shown and the event was fired."""

        cmdlineUi = CmdlineUiTestUtils._mockInterfaceAccessor.getComponentInterface(IComponentUi)
        mockOnMessageShown = Mock()
        cmdlineUi.messageShown += mockOnMessageShown
        cmdlineUi.showInfo(self.__TEST_MESSAGE)

        self.assertTrue(sys.stdout.getvalue().find(self.__TEST_MESSAGE) != -1, "Message was not shown.")
        self.assertEqual(mockOnMessageShown.call_count, 1, "MessageShown event not fired or fired more than once.")



    def test_showWarning(self):
        """Tests the showWarning() method.

        Subscribes to :meth:`ICmdlineUi.messageShown` event and shows a warning message.  Checks that the message
        was shown and the event was fired."""

        cmdlineUi = CmdlineUiTestUtils._mockInterfaceAccessor.getComponentInterface(IComponentUi)
        mockOnMessageShown = Mock()
        cmdlineUi.messageShown += mockOnMessageShown
        cmdlineUi.showWarning(self.__TEST_MESSAGE)

        self.assertTrue(sys.stderr.getvalue().find(self.__TEST_MESSAGE) != -1, "Message was not shown.")
        self.assertEqual(mockOnMessageShown.call_count, 1, "MessageShown event not fired or fired more than once.")



    def test_showWarningQuiet(self):
        """Tests the showWarning() method with :attr:`Options.QUIET` option turned on.

        Subscribes to :meth:`ICmdlineUi.messageShown` event and shows a warning message.  Checks that the message
        was _not_ shown and the event was fired."""

        # ignore standard setup and make a new one with changed options
        CmdlineUiTestUtils._tearDownCmdlineUiComponent()
        CmdlineUiTestUtils._setUpCmdlineUiComponent(
            {Options.USER_CONFIG_DIR: ComponentTestUtils.getComponentTestContext().userConfigDir,
             Options.QUIET: True})
        self.__runCmdlineUiComponent()

        cmdlineUi = CmdlineUiTestUtils._mockInterfaceAccessor.getComponentInterface(IComponentUi)
        mockOnMessageShown = Mock()
        cmdlineUi.messageShown += mockOnMessageShown
        cmdlineUi.showWarning(self.__TEST_MESSAGE)

        self.assertTrue(sys.stderr.getvalue().find(self.__TEST_MESSAGE) == -1, "Message was shown.")
        self.assertEqual(mockOnMessageShown.call_count, 1, "MessageShown event not fired or fired more than once.")



    def test_showError(self):
        """Tests the showError() method.

        Subscribes to :meth:`ICmdlineUi.messageShown` event and shows an error message.  Checks that the message
        was shown and the event was fired."""

        cmdlineUi = CmdlineUiTestUtils._mockInterfaceAccessor.getComponentInterface(IComponentUi)
        mockOnMessageShown = Mock()
        cmdlineUi.messageShown += mockOnMessageShown
        cmdlineUi.showError(self.__TEST_MESSAGE)

        self.assertTrue(sys.stderr.getvalue().find(self.__TEST_MESSAGE) != -1, "Message was not shown.")
        self.assertEqual(mockOnMessageShown.call_count, 1, "MessageShown event not fired or fired more than once.")



    def __runCmdlineUiComponent(self):
        mockUserActionExecutor = Mock()
        mockUserActionExecutor.processedArchSpec = "test_arch_spec"
        patchUserActionExecutor = Mock()
        patchUserActionExecutor.return_value = mockUserActionExecutor
        with patch("AutoArchive._ui._cmdline._core.cmdline_ui_component._UserActionExecutor", patchUserActionExecutor):
            CmdlineUiTestUtils._cmdlineUiComponent.run()

# }}} CLASSES

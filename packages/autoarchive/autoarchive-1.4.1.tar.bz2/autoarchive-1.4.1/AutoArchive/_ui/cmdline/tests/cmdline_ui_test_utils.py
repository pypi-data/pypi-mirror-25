# cmdline_ui_test_utils.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2014 Róbert Čerňanský



""":class:`CmdlineUiTestUtils` class."""



__all__ = ["CmdlineUiTestUtils"]



# {{{ INCLUDES

from abc import ABCMeta, abstractmethod
from optparse import Values

from mock import Mock

from AutoArchive._infrastructure._application_context import ApplicationContext
from AutoArchive._infrastructure._app_environment import AppEnvironment
from AutoArchive._application.archiving import ArchivingApplication
from .._user_action_executor import UserActionExecutor
from .._cmdline_ui import CmdlineUi
from .._cmdline_commands import CmdlineCommands
from AutoArchive.tests import ComponentTestUtils
from AutoArchive._infrastructure.configuration.tests import ConfigurationTestUtils


# }}} INCLUDES



# {{{ CLASSES

class CmdlineUiTestUtils(metaclass = ABCMeta):
    """Utility methods for Cmdline UI component tests."""

    _cmdlineUi = None
    _archivingApplicationMock = None



    @abstractmethod
    def __init__(self):
        pass



    @classmethod
    def _setUpClassCmdlineUiComponent(cls):
        ComponentTestUtils.setUpClassComponent()



    @classmethod
    def _tearDownClassCmdlineUiComponent(cls):
        ComponentTestUtils.tearDownClassComponent()



    @classmethod
    def _setUpCommon(cls):
        pass



    @classmethod
    def _tearDownCommon(cls):
        pass



    @classmethod
    def _setUpCmdlineUiComponent(cls, options = None):
        """Sets-up the environment for :term:`CmdlineUi` and creates it.

        :param options: Configuration options.
        :type options: ``dict<Option, object>``
        :param command: The command that shall be executed (normally - within the non-test environment - specified by
            the user using the UI).
        :type command: :class:`.CmdlineCommands`
        :param arguments: Program arguments.
        :type arguments: ``list<str>``"""

        appEnvironment = AppEnvironment("test_aa", Values(), [])
        configurationMock = ConfigurationTestUtils.createConfigurationMock(options)
        cls._cmdlineUi = CmdlineUi(appEnvironment, configurationMock)



    @classmethod
    def _tearDownCmdlineUiComponent(cls):
        cls._mockArchiving = None
        cls._cmdlineUi = None



    @classmethod
    def _setUpUserActionExecutor(cls, options = None, command = None, arguments = None):
        """Sets-up the environment for :term:`UserActionExecutor` and creates it.

        :param options: Configuration options.
        :type options: ``dict<Option, object>``
        :param command: The command that shall be executed (normally - within the non-test environment - specified by
            the user using the UI).
        :type command: :class:`.CmdlineCommands`
        :param arguments: Program arguments.
        :type arguments: ``list<str>``"""

        if arguments is None: arguments = []

        values = Values()
        if command == CmdlineCommands.LIST:
            values.list = True
        elif command == CmdlineCommands.PURGE:
            values.purge = True

        appEnvironment = AppEnvironment("test_aa", values, arguments)
        configurationMock = ConfigurationTestUtils.createConfigurationMock(options)
        applicationContextMock = Mock(spec_set = ApplicationContext)
        applicationContextMock.appEnvironment = appEnvironment
        applicationContextMock.configuration = configurationMock

        cls._archivingApplicationMock = Mock(spec_set = ArchivingApplication)

        return UserActionExecutor(Mock(spec_set = CmdlineUi), applicationContextMock, cls._archivingApplicationMock)



    @classmethod
    def _tearDownUserActionExecutor(cls):
        cls._archivingApplicationMock = None

# }}} CLASSES

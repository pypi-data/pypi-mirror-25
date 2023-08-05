# cmdline_ui_test_utils.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2012 Róbert Čerňanský



""":class:`CmdlineUiTestUtils` class."""



__all__ = ["CmdlineUiTestUtils"]



# {{{ INCLUDES

from mock import Mock

from abc import *
from optparse import Values

from ...._app_environment import *
from ...._mainf import *
from ...._configuration import *
from ...._archiving import *
from .. import *
from .._core import CmdlineUiComponent

from ....tests import *
from ...._mainf.tests import MainfTestUtils
from ...._configuration.tests import ConfigurationTestUtils
from ...._archiving.tests import ArchivingTestUtils

# }}} INCLUDES



# {{{ CLASSES

class CmdlineUiTestUtils(metaclass = ABCMeta):
    """Utility methods for Cmdline UI component tests."""

    _mockInterfaceAccessor = None
    _mockArchiving = None
    _cmdlineUiComponent = None



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
        cls._mockInterfaceAccessor = MainfTestUtils.createMockInterfaceAccessor({})

        mockMainfContext = Mock(spec_set = IMainfContext)
        cls._mockInterfaceAccessor.registerComponentInterface(IMainfContext, mockMainfContext)



    @classmethod
    def _tearDownCommon(cls):
        cls._mockInterfaceAccessor = None



    @classmethod
    def _setUpCmdlineUiComponent(cls, options = None, archiveSpecs = None, command = None, arguments = None,
                                 configuredArchiveNames = None, storedArchiveNames = None):
        """Sets-up the environment for :term:`CmdlineUiComponent` and creates it.

        :param options: Configuration options.
        :type options: ``dict<Option, object>``
        :param archiveSpecs: Archive specification files as shall be known to :term:`Configuration component`.
        :type archiveSpecs: ``Iterable<ArchiveSpecInfo>``
        :param command: The command that shall be executed (normally - within the non-test environment - specified by
            the user using the UI).
        :type command: :class:`.CmdlineCommands`
        :param arguments: Program arguments.
        :type arguments: ``list<str>``
        :param configuredArchiveNames: Names of archives that shall be considered as correctly :term:`configured` by
            :term:`Archiving component`.
        :type configuredArchiveNames: ``Iterable<str>``
        :param storedArchiveNames: Names of archives that shall be considered as :term:`stored` by
            :term:`Archiving component`.
        :type storedArchiveNames: ``Iterable<str>``"""

        if arguments is None: arguments = []

        mockAppConfig = ConfigurationTestUtils.createMockAppConfig(options, archiveSpecs)
        cls._mockInterfaceAccessor.registerComponentInterface(IAppConfig, mockAppConfig)

        values = Values()
        if command == CmdlineCommands.LIST:
            values.list = True
        elif command == CmdlineCommands.PURGE:
            values.purge = True
        mockMainfContext = cls._mockInterfaceAccessor.getComponentInterface(IMainfContext)
        mockMainfContext.appEnvironment = _AppEnvironment("test_aa", values, arguments)

        cls._mockArchiving = ArchivingTestUtils.createMockArchiving(configuredArchiveNames, storedArchiveNames)
        cls._mockInterfaceAccessor.registerComponentInterface(IArchiving, cls._mockArchiving)

        cls._cmdlineUiComponent = CmdlineUiComponent(cls._mockInterfaceAccessor)



    @classmethod
    def _tearDownCmdlineUiComponent(cls):
        cls._mockInterfaceAccessor.unregisterComponentInterface(IAppConfig)
        cls._mockInterfaceAccessor.unregisterComponentInterface(IArchiving)
        cls._mockArchiving = None
        cls._cmdlineUiComponent = None

# }}} CLASSES

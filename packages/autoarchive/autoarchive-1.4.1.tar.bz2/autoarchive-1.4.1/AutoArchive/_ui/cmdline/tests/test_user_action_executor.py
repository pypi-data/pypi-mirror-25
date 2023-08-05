# test_user_action_executor.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2017 Róbert Čerňanský



""":class:`TestUserActionExecutor`."""



__all__ = ["TestUserActionExecutor"]



# {{{ INCLUDES

import unittest
import os

from AutoArchive._infrastructure.configuration import Options
from AutoArchive._application.archiving.archive_spec import ArchiveSpecInfo, ConfigConstants
from .._cmdline_commands import CmdlineCommands
from AutoArchive._infrastructure.configuration.tests import ConfigurationTestUtils
from AutoArchive.tests import ComponentTestUtils
from .cmdline_ui_test_utils import CmdlineUiTestUtils

# }}} INCLUDES



# {{{ CLASSES

class TestUserActionExecutor(unittest.TestCase):
    """Test of :class:`.UserActionExecutor`."""

    @classmethod
    def setUpClass(cls):
        CmdlineUiTestUtils._setUpClassCmdlineUiComponent()



    @classmethod
    def tearDownClass(cls):
        CmdlineUiTestUtils._tearDownClassCmdlineUiComponent()



    def setUp(self):
        CmdlineUiTestUtils._setUpCommon()



    def tearDown(self):
        CmdlineUiTestUtils._tearDownCommon()



    def test_executeCreateSpecific(self):
        """Tests the :meth:`.UserActionExecutor.execute()` method for Create action for a specific archive.

        Simulate passing a single argument (the name of the archive).  This shall invoke Create action for the
        specified archive name upon call of the tested method.  Checks that the tested method returns ``True`` and
        the :meth:`.ArchivingApplication.executeCreateAction()` was called with correct :class:`.ArchiveSpecInfo`."""

        ARCHIVE_NAME = "test_archive"

        # empty archive specifications directory should exists when the test method executes so let's create it
        ConfigurationTestUtils.makeArchiveSpecsDirectory()

        userActionExecutor = CmdlineUiTestUtils._setUpUserActionExecutor(
                {Options.ARCHIVE_SPECS_DIR: ComponentTestUtils.getComponentTestContext().archiveSpecsDir},
                arguments = [ARCHIVE_NAME])

        success = userActionExecutor.execute()

        self.assertTrue(success)
        CmdlineUiTestUtils._archivingApplicationMock.executeCreateAction.assert_called_once_with(
            (ArchiveSpecInfo(ARCHIVE_NAME, os.path.join(ComponentTestUtils.getComponentTestContext().archiveSpecsDir,
                                                       ARCHIVE_NAME + ConfigConstants.ARCHIVE_SPEC_EXT)),))

        ConfigurationTestUtils.removeArchiveSpecsDirectory()



    def test_executeCreateNoneSelected(self):
        """Tests the :meth:`.UserActionExecutor.execute()` method for Create action for no selected archives.

        Simulate passing no arguments while :attr:`.Options.ALL` option is set to ``True``.  Checks that the tested
        method returns ``True`` and the :meth:`.ArchivingApplication.executeCreateAction()` was called with
        an empty sequence."""

        userActionExecutor = CmdlineUiTestUtils._setUpUserActionExecutor({Options.ALL: True})

        success = userActionExecutor.execute()

        self.assertTrue(success)
        CmdlineUiTestUtils._archivingApplicationMock.executeCreateAction.assert_called_once_with(())



    def test_executeCreateNoArchives(self):
        """Tests the :meth:`.UserActionExecutor.execute()` method for Create action for missing archive specification.

        Simulate passing no arguments while not enabling the :attr:`.Options.ALL` option.  This shall produce an error
        because there is no archive specified at all.  Checks that the tested method returns ``False`` and the
        :meth:`.ArchivingApplication.executeCreateAction()` was _not_ called."""

        userActionExecutor = CmdlineUiTestUtils._setUpUserActionExecutor()

        success = userActionExecutor.execute()

        self.assertFalse(success)
        self.assertFalse(CmdlineUiTestUtils._archivingApplicationMock.executeCreateAction.called)



    def test_executeListNoArchives(self):
        """Tests the :meth:`.UserActionExecutor.execute()` method for List action with missing archive specification.

        Simulate passing no arguments while not enabling the :attr:`.Options.ALL` option.  Checks that the tested
        method returns ``True`` and the :meth:`.ArchivingApplication.executeListAction()` was called with
        an empty sequence."""

        userActionExecutor = CmdlineUiTestUtils._setUpUserActionExecutor(command = CmdlineCommands.LIST)

        success = userActionExecutor.execute()

        self.assertTrue(success)
        CmdlineUiTestUtils._archivingApplicationMock.executeListAction.assert_called_once_with(())



    def test_executePurge(self):
        """Tests the :meth:`.UserActionExecutor.execute()` method for Purge action for a specific archive.

        Simulate passing a single argument (the name of the obsolete archive).  Checks that the tested method returns
        ``True`` and the :meth:`.ArchivingApplication.executePurgeAction()` was called."""

        # empty archive specifications directory should exists when the test method executes so let's create it
        ConfigurationTestUtils.makeArchiveSpecsDirectory()

        userActionExecutor = CmdlineUiTestUtils._setUpUserActionExecutor(
                {Options.ARCHIVE_SPECS_DIR: ComponentTestUtils.getComponentTestContext().archiveSpecsDir},
                command = CmdlineCommands.PURGE,
                arguments = ["any string"])

        success = userActionExecutor.execute()

        self.assertTrue(success)
        self.assertTrue(CmdlineUiTestUtils._archivingApplicationMock.executePurgeAction.called)

        ConfigurationTestUtils.removeArchiveSpecsDirectory()

# }}} CLASSES

# test_icomponent.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2012 Róbert Čerňanský



""":class:`TestIComponent`."""



__all__ = ["TestIComponent"]



# {{{ INCLUDES

import unittest

import sys
import os
import io

from ...._configuration import *
from .. import *

from ....tests import *
from ...._archiving.tests import ArchivingTestUtils
from .cmdline_ui_test_utils import *

# }}} INCLUDES



# {{{ CLASSES

class TestIComponent(unittest.TestCase):
    """Test of :class:`.IComponent` provided interface."""

    # Attention! Tests included in this class has to call CmdlineUiTestUtils._setUpClassCmdlineUiComponent() method.



    @classmethod
    def setUpClass(cls):
        CmdlineUiTestUtils._setUpClassCmdlineUiComponent()



    @classmethod
    def tearDownClass(cls):
        CmdlineUiTestUtils._tearDownClassCmdlineUiComponent()



    def setUp(self):
        CmdlineUiTestUtils._setUpCommon()



    def tearDown(self):
        CmdlineUiTestUtils._tearDownCmdlineUiComponent()
        CmdlineUiTestUtils._tearDownCommon()



    def test_runCreateSpecific(self):
        """Tests the :meth:`.IComponent.run()` method for Create action for a specific archive.

        Simulate passing a single argument (the name of the archive).  This shall invoke Create action for the
        specified archive name upon call of the tested method.  Checks that the tested method returns ``True`` and
        the :meth:`.IArchiving.makeBackup()` was called with path to the :term:`archive specification file`
        corresponding to the specified archive name."""

        ARCHIVE_NAME = "test_archive"

        # empty archive specifications directory should exists when the test method executes so let's create it
        ArchivingTestUtils.makeArchiveSpecsDirectory()

        CmdlineUiTestUtils._setUpCmdlineUiComponent(
                {Options.ARCHIVE_SPECS_DIR: ComponentTestUtils.getComponentTestContext().archiveSpecsDir},
                arguments = [ARCHIVE_NAME])

        success = CmdlineUiTestUtils._cmdlineUiComponent.run()
        self.assertTrue(success)
        CmdlineUiTestUtils._mockArchiving.makeBackup.assert_called_once_with(
            os.path.join(ComponentTestUtils.getComponentTestContext().archiveSpecsDir,
                         ARCHIVE_NAME + ConfigConstants.ARCHIVE_SPEC_EXT))

        ArchivingTestUtils.removeArchiveSpecsDirectory()



    def test_runCreateAll(self):
        """Tests the :meth:`.IComponent.run()` method for Create action for all configured archives.

        Sets up the configuration with two archives and enable :attr:`.Options.ALL` option.  Simulate passing no
        arguments.  This shall invoke Create action for all the configured archives upon call of the tested method.
        Checks that the tested method returns ``True`` and the :meth:`.IArchiving.makeBackup()` was called for each
        configured archive."""

        ARCHIVE_SPECS = (ArchiveSpecInfo("test_arch_spec1", "path_to/test_arch_spec1"),
                         ArchiveSpecInfo("test_arch_spec2", "path_to/test_arch_spec2"))

        CmdlineUiTestUtils._setUpCmdlineUiComponent({Options.ALL: True}, ARCHIVE_SPECS)

        success = CmdlineUiTestUtils._cmdlineUiComponent.run()
        self.assertTrue(success)
        self.assertEqual([((ARCHIVE_SPECS[0].path,),), ((ARCHIVE_SPECS[1].path,),)],
                         CmdlineUiTestUtils._mockArchiving.makeBackup.call_args_list)



    def test_runCreateNoArchives(self):
        """Tests the :meth:`.IComponent.run()` method for Create action for missing archive specification.

        Simulate passing no arguments while not enabling the :attr:`.Options.ALL` option.  This shall produce an error
        because there is no archive specified at all.  Checks that the tested method returns ``False`` and the
        :meth:`.IArchiving.makeBackup()` was _not_ called."""

        CmdlineUiTestUtils._setUpCmdlineUiComponent()

        success = CmdlineUiTestUtils._cmdlineUiComponent.run()
        self.assertFalse(success)
        self.assertFalse(CmdlineUiTestUtils._mockArchiving.makeBackup.called)



    def test_runList(self):
        """Tests the :meth:`.IComponent.run()` method for List action.

        Simulate passing the ``list`` command and no argument.  This shall invoke the List action for all archives
        (both :term:`configured <configured archive>` and :term:`orphaned <orphaned archive>` ones).  Also sets up the
        configuration with a single archive and :class:`.IArchiving` mock with a single :term:`stored archive` to
        simulate that there is an existing configured archive and also an orphaned one.  Checks that the tested method
        returns ``True`` and the standard output contains names of both archives."""

        CONFIGURED_ARCH_SPEC = "path_to/test_arch_spec1.aa"
        ORPHANED_ARCHIVE_NAME = "test_orphaned_archive"

        # 'ArchiveSpecInfo.name' is not actually used because IArchiving mock creates it from the path
        CmdlineUiTestUtils._setUpCmdlineUiComponent(
            {Options.VERBOSE: True},
            [ArchiveSpecInfo("test_configured_archive", CONFIGURED_ARCH_SPEC)],
            CmdlineCommands.LIST,
            storedArchiveNames = [ORPHANED_ARCHIVE_NAME])

        uiStdout = io.StringIO()
        sys.stdout = uiStdout
        try:
            success = CmdlineUiTestUtils._cmdlineUiComponent.run()
        finally:
            sys.stdout = sys.__stdout__
        self.assertTrue(success)
        self.assertTrue(uiStdout.getvalue().find(os.path.basename(CONFIGURED_ARCH_SPEC).replace(
            ConfigConstants.ARCHIVE_SPEC_EXT, "")) != -1, "Configured archive was not listed.")
        self.assertTrue(uiStdout.getvalue().find("[" + ORPHANED_ARCHIVE_NAME + "]") != -1,
                        "Orphaned archive was not listed.")



    def test_runPurgeSpecific(self):
        """Tests the :meth:`.IComponent.run()` method for Purge action for specific archives.

        Simulate passing the ``purge`` command and two archive names as arguments - one
        :term:`configured <configured archive>` and other :term:`orphaned archive`.  This shall invoke the Purge action
        for both archives but only the orphaned one should be purged.  Checks that the tested method returns ``True``
        (because one of the archives was not purged) and the purge API was called for the orphaned archive only."""

        CONFIGURED_ARCHIVE_NAME = "test_configured_archive"
        ORPHANED_ARCHIVE_NAMES = ("test_orphaned_archive1", "test_orphaned_archive2")

        # empty archive specifications directory should exists when the test method executes so let's create it
        ArchivingTestUtils.makeArchiveSpecsDirectory()

        CmdlineUiTestUtils._setUpCmdlineUiComponent(
            {Options.ARCHIVE_SPECS_DIR: ComponentTestUtils.getComponentTestContext().archiveSpecsDir},
            command = CmdlineCommands.PURGE,
            arguments = [CONFIGURED_ARCHIVE_NAME, ORPHANED_ARCHIVE_NAMES[0]],
            configuredArchiveNames = [CONFIGURED_ARCHIVE_NAME],
            storedArchiveNames = ORPHANED_ARCHIVE_NAMES)

        success = CmdlineUiTestUtils._cmdlineUiComponent.run()
        self.assertFalse(success)
        CmdlineUiTestUtils._mockArchiving.purgeStoredArchiveData.assert_called_once_with(ORPHANED_ARCHIVE_NAMES[0])

        ArchivingTestUtils.removeArchiveSpecsDirectory()



    def test_runPurgeAll(self):
        """Tests the :meth:`.IComponent.run()` method for Purge action for all archives.

        Simulate passing the ``purge`` command and no arguments.  This shall invoke the Purge action for all
        :term:`orphaned archives <orphaned archive>`.  The configuration and :class:`.IArchiving` mock are configured
        to simulate environment with a single :term:`configured <configured archive>` and two orphaned archives.
        Checks that the tested method returns ``True`` and the purge API was called for orphaned archives only."""

        CONFIGURED_ARCHIVE_NAME = "test_configured_archive"

        # set the file name according to the archive name because that's the limitation of IArchiving mock
        CONFIGURED_ARCH_SPEC = "path_to/" + CONFIGURED_ARCHIVE_NAME + ConfigConstants.ARCHIVE_SPEC_EXT

        ORPHANED_ARCHIVE_NAMES = ("test_orphaned_archive1", "test_orphaned_archive2")

        CmdlineUiTestUtils._setUpCmdlineUiComponent(
            {Options.ALL: True},
            [ArchiveSpecInfo(CONFIGURED_ARCHIVE_NAME, CONFIGURED_ARCH_SPEC)],
            command = CmdlineCommands.PURGE,
            configuredArchiveNames = [CONFIGURED_ARCHIVE_NAME],
            storedArchiveNames = ORPHANED_ARCHIVE_NAMES)

        success = CmdlineUiTestUtils._cmdlineUiComponent.run()
        self.assertTrue(success)
        self.assertCountEqual([((ORPHANED_ARCHIVE_NAMES[0],),), ((ORPHANED_ARCHIVE_NAMES[1],),)],
                              CmdlineUiTestUtils._mockArchiving.purgeStoredArchiveData.call_args_list)

# }}} CLASSES

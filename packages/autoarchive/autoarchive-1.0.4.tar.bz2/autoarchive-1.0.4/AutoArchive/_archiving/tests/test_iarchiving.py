# test_iarchiving.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2015 Róbert Čerňanský



""":class:`TestIArchivingMakeBackupArchiveTypes`,
:class:`TestIArchivingMakeBackupShowFinalError`,
:class:`TestIArchivingMakeBackupIncremental`, :class:`TestIArchivingMakeBackupRestarting`,
:class:`TestIArchivingMakeBackupOptionsPriority`, :class:`TestIArchivingConfiguredArchiveInfo` and
:class:`TestIArchivingStoredArchiveInfo` classes."""



__all__ = ["TestIArchivingMakeBackupArchiveTypes",
           "TestIArchivingMakeBackupShowFinalError",
           "TestIArchivingMakeBackupIncremental", "TestIArchivingMakeBackupRestarting",
           "TestIArchivingMakeBackupOptionsPriority", "TestIArchivingConfiguredArchiveInfo",
           "TestIArchivingStoredArchiveInfo"]



# {{{ INCLUDES

import unittest
import mock

import os
import itertools
import re
from datetime import datetime, timedelta

from ..._mainf import *
from ..._configuration import *
from .. import *
from .._core import ArchivingComponent

from ...tests import *
from ..._mainf.tests import MainfTestUtils
from ..._configuration.tests import ConfigurationTestUtils
from AutoArchive._services.archiver.tests import ArchiverTestUtils
from .archiving_test_utils import *

# }}} INCLUDES



# {{{ CLASSES

# {{{ makeBackup() tests

class TestIArchivingMakeBackupArchiveTypes(unittest.TestCase):
    """Test of :meth:`.IArchiving.makeBackup()` method for SPI usage for all supported archiver types."""



    @classmethod
    def setUpClass(cls):
        ArchivingTestUtils._setUpClassArchivingComponent()



    @classmethod
    def tearDownClass(cls):
        ArchivingTestUtils._tearDownClassArchivingComponent()



    def setUp(self):
        ArchivingTestUtils._setUpArchivingComponent()



    def tearDown(self):
        ArchivingTestUtils._tearDownArchivingComponent()



    # {{{ makeBackup() tests for archive types

    def test_makeBackupTar(self):
        "Tests the makeBackup() method with Tar archive type."

        self.__testMakeBackup(ArchiverTypes.Tar)



    def test_makeBackupTarGz(self):
        "Tests the makeBackup() method with TarGz archive type."

        self.__testMakeBackup(ArchiverTypes.TarGz)



    def test_makeBackupTarBz2(self):
        "Tests the makeBackup() method with TarBz2 archive type."

        self.__testMakeBackup(ArchiverTypes.TarBz2)



    def test_makeBackupTarXz(self):
        "Tests the makeBackup() method with TarXz archive type."

        self.__testMakeBackup(ArchiverTypes.TarXz)



    def test_makeBackupTarInternal(self):
        "Tests the makeBackup() method with TarInternal archive type."

        self.__testMakeBackup(ArchiverTypes.TarInternal)



    def test_makeBackupTarGzInternal(self):
        "Tests the makeBackup() method with TarGzInternal archive type."

        self.__testMakeBackup(ArchiverTypes.TarGzInternal)



    def test_makeBackupTarBz2Internal(self):
        "Tests the makeBackup() method with TarBz2Internal archive type."

        self.__testMakeBackup(ArchiverTypes.TarBz2Internal)

    # }}} makeBackup() tests for archive types



    # {{{ helpers for makeBackup() tests for archiver type

    def __testMakeBackup(self, archiver):
        """Tests the makeBackup() method with specified archive type."""

        archiverMock = ArchiverTestUtils.createArchiverMock()

        ArchivingTestUtils._createBackup(archiverMock, archiverType = archiver)

        self.assertTrue(archiverMock.backupFiles.called)
        self.assertEqual(ArchivingTestUtils._ARCHIVER_TYPE_TO_BACKUP_TYPE_MAP[archiver],
                         archiverMock.backupFiles.call_args[0][0].backupType)

    # }}} helpers for makeBackup() tests for archiver type



class TestIArchivingMakeBackupShowFinalError(unittest.TestCase):
    """Test of :meth:`.IArchiving.makeBackup()` method for showing final error message."""

    @classmethod
    def setUpClass(cls):
        ArchivingTestUtils._setUpClassArchivingComponent()



    @classmethod
    def tearDownClass(cls):
        ArchivingTestUtils._tearDownClassArchivingComponent()



    def setUp(self):
        ArchivingTestUtils._setUpArchivingComponent()



    def tearDown(self):
        ArchivingTestUtils._tearDownArchivingComponent()



    # {{{ makeBackup() tests for show final error

    def test_makeBackupShowFinalError(self):
        """Tests the makeBackup() method for showing final error message for failed backup creation.

        Sets up the archiver service so it simulates an error upon backup creation.  Checks that the final verbose
        message saying that an error occurred was shown."""

        archiverMock = ArchiverTestUtils.createArchiverMock()
        interfaceAccessorMock = MainfTestUtils.createMockInterfaceAccessor({})

        ArchivingTestUtils._createBackup(archiverMock, errorOccur = True,
                                         interfaceAccessorMock = interfaceAccessorMock)

        mockComponentUi = interfaceAccessorMock.getComponentInterface(IComponentUi)
        errorCallsArgs = (methodCall[1]
                          for methodCall in mockComponentUi.method_calls
                          if methodCall[0] == "showVerbose")
        creationFailedCallsArgs = itertools.dropwhile(
            lambda callArg: re.search("error\(s\) occurred during", callArg[0], re.IGNORECASE) is None, errorCallsArgs)

        # we expect that the "creation failed" message will be shown
        self.assertIsNotNone(next(creationFailedCallsArgs, None),
                             "The error message \"error(s) occurred\" was not shown.")

    # }}} makeBackup() tests for show final error



class TestIArchivingMakeBackupIncremental(unittest.TestCase):
    "Test of :meth:`.IArchiving.makeBackup()` method for the incremental backup."

    @classmethod
    def setUpClass(cls):
        ArchivingTestUtils._setUpClassArchivingComponent()



    @classmethod
    def tearDownClass(cls):
        ArchivingTestUtils._tearDownClassArchivingComponent()



    def setUp(self):
        ArchivingTestUtils._setUpArchivingComponent()



    def tearDown(self):
        ArchivingTestUtils._tearDownArchivingComponent()



    # {{{ makeBackup() tests for incremental archiving

    def test_makeBackupIncremental(self):
        """Tests the makeBackup() method to create an incremental archive.

        Calls an incremental backup creation and check that the right service method was called and the passed backup
        level value was the same as the maximal backup level was set to."""

        MAX_BACKUP_LEVEL = 10

        archiverMock = ArchiverTestUtils.createArchiverMock()

        # call the backup creation
        ArchivingTestUtils._createIncrementalBackup(archiverMock, maxBackupLevel = MAX_BACKUP_LEVEL)

        # check that the backupFilesIncrementally() was called and that it was called with correct value of the
        # backup level argument
        self.assertTrue(archiverMock.backupFilesIncrementally.called)
        self.assertEqual(MAX_BACKUP_LEVEL, archiverMock.backupFilesIncrementally.call_args[0][2])



    def test_makeBackupIncrementalLevel(self):
        """Tests the makeBackup() method to create an incremental backup of a specified level.

        Sets-up the service so it returns maximal backup level 2.  Calls an incremental backup creation of the level 1.
        Checks that the right service method was called with the same backup level."""

        MAX_BACKUP_LEVEL = 2
        BACKUP_LEVEL = MAX_BACKUP_LEVEL - 1

        archiverMock = ArchiverTestUtils.createArchiverMock()

        # call the backup creation
        ArchivingTestUtils._createIncrementalBackup(archiverMock, {Options.LEVEL: BACKUP_LEVEL}, MAX_BACKUP_LEVEL)

        # check that the backupFilesIncrementally() was called with correct value of the backup level argument
        self.assertEqual(BACKUP_LEVEL, archiverMock.backupFilesIncrementally.call_args[0][2])



    def test_makeBackupIncrementalLevelTooHigh(self):
        """Tests the makeBackup() method to create an incremental backup of specified level which is too high.

        Sets-up the service so it returns maximal backup level 2.  Calls an incremental backup creation of the level 3.
        Checks that the right service method was called with the same backup level as the maximal.  Also checks that
        the message that the backup level is too high was shown."""

        MAX_BACKUP_LEVEL = 2
        BACKUP_LEVEL = MAX_BACKUP_LEVEL + 1

        archiverMock = ArchiverTestUtils.createArchiverMock()
        interfaceAccessorMock = MainfTestUtils.createMockInterfaceAccessor({})

        # call the backup creation
        ArchivingTestUtils._createIncrementalBackup(archiverMock, {Options.LEVEL: BACKUP_LEVEL}, MAX_BACKUP_LEVEL,
                                                    interfaceAccessorMock = interfaceAccessorMock)

        # check that the backupFilesIncrementally() was called with correct value of the backup level argument
        self.assertEqual(MAX_BACKUP_LEVEL, archiverMock.backupFilesIncrementally.call_args[0][2])

        # check that warning message that the level is too high was shown
        mockComponentUi = interfaceAccessorMock.getComponentInterface(IComponentUi)
        warningCallsArgs = (methodCall[1]
                            for methodCall in mockComponentUi.method_calls
                            if methodCall[0] == "showWarning")
        socketIgnoredCallsArgs = itertools.dropwhile(
            lambda callArg: re.search("level.*too.*high", callArg[0], re.IGNORECASE) is None, warningCallsArgs)
        self.assertIsNotNone(next(socketIgnoredCallsArgs, None),
                             "A warning message that the level is too high was not shown.")



    def test_makeBackupIncrementalRemoveObsolete(self):
        """Tests the makeBackup() method for removal of obsolete backups.

        Enables option for obsolete backups removal and sets-up service so that maximal backup level is 2.  Calls an
        incremental backup creation of level 1.  Asserts that a service method for backup removal was called with
        correct "level" parameter."""

        MAX_BACKUP_LEVEL = 2
        BACKUP_LEVEL = MAX_BACKUP_LEVEL - 1

        archiverMock = ArchiverTestUtils.createArchiverMock()

        options = {
            Options.LEVEL: BACKUP_LEVEL,
            Options.REMOVE_OBSOLETE_BACKUPS: True
        }

        # call the backup creation
        ArchivingTestUtils._createIncrementalBackup(archiverMock, options, MAX_BACKUP_LEVEL)

        # check that the removeBackupIncrements() was called with correct value of the backup level argument
        self.assertEqual(BACKUP_LEVEL + 1, archiverMock.removeBackupIncrements.call_args[0][1])

    # }}} makeBackup() tests for incremental archiving



class TestIArchivingMakeBackupRestarting(unittest.TestCase):
    "Test of :meth:`.IArchiving.makeBackup()` method for the backup level restarting."



    @classmethod
    def setUpClass(cls):
        ArchivingTestUtils._setUpClassArchivingComponent()



    @classmethod
    def tearDownClass(cls):
        ArchivingTestUtils._tearDownClassArchivingComponent()



    def setUp(self):
        self.__archiveSpecFilePath = None
        self.__irrelevantFilePath = None
        self.__storageState = {}

        ArchivingTestUtils._setUpArchivingComponent()

        self.__irrelevantFilePath = ArchivingTestUtils._createIrrelevantFile()
        self.__archiveSpecFilePath = ArchivingTestUtils._makeArchiveSpecFile()



    def tearDown(self):
        ArchivingTestUtils._removeIrrelevantFile()

        ArchivingTestUtils._tearDownArchivingComponent()



    # {{{ makeBackup() tests for backup level restarting

    def test_makeBackupRestartAfterLevel(self):
        """Tests the makeBackup() method for restarting a level after a specific level was reached.

        Configures that the backup level shall be restarted after level 2.  Creates four incremental backups expecting
        that at fourth time the level will be restarted to 1.  Checks that the service method was called to create
        backup of level 1."""

        RESTART_AFTER_LEVEL = 2

        archiverMock = ArchiverTestUtils.createArchiverMock()

        options = {
            Options.RESTART_AFTER_LEVEL: RESTART_AFTER_LEVEL
        }

        # call the backup creation for RESTART_AFTER_LEVEL + 2 times so it should be restarted
        self.__createRestartableArchives(archiverMock, options, RESTART_AFTER_LEVEL + 2)

        # check that the last call of backupFilesIncrementally() was with backup level 1
        self.assertEqual(1, archiverMock.backupFilesIncrementally.call_args[0][2],
                         "The backup creation on the service was not called with expected backup level.")



    def test_makeBackupRestartAfterDays(self):
        """Tests the makeBackup() method for restarting a level after a specific number of days passed.

        Configures that the backup level shall be restarted after 3 days.  Creates a level 0, level 1 and level 2
        backups.  Modify value of last restart in the storage mock so that it is older than 3 days.  Calls the backup
        creation once more attempting to create the backup of level 3 but it should be restarted.  Checks that the
        service method was called to create backup of level 1."""

        RESTART_AFTER_AGE = 3

        NUMBER_OF_CREATED_LEVELS = 3

        STORAGE_LAST_RESTART = "archiving-last-restart"

        archiverMock = ArchiverTestUtils.createArchiverMock()

        options = {
            Options.RESTART_AFTER_LEVEL: 100, # has to be greater than NUMBER_OF_CREATED_LEVELS
            Options.RESTART_AFTER_AGE: RESTART_AFTER_AGE
        }

        # call the backup creation for NUMBER_OF_CREATED_LEVELS times
        self.__createRestartableArchives(archiverMock, options, NUMBER_OF_CREATED_LEVELS,
                                         archiveSpecFile = self.__archiveSpecFilePath)

        # decrease last restart date by RESTART_AFTER_AGE + 1 days

        # >beware that how the date of the last restart is stored is internal to the Archiving component so the
        # >following code may break without the interface change; well, not great but much better than to let this test
        # >to wait couple of days

        # >from the name of the archive specification file we get the realm
        realm = os.path.basename(self.__archiveSpecFilePath)

        # >get the last restart date, decrease it and store back
        lastRestartStr = self.__storageState[realm][ConfigurationTestUtils.DEFAULT_SECTION][STORAGE_LAST_RESTART]
        lastRestart = datetime.strptime(lastRestartStr, "%Y-%m-%d").date()
        self.__storageState[realm][ConfigurationTestUtils.DEFAULT_SECTION][STORAGE_LAST_RESTART] = \
            str(lastRestart - timedelta(RESTART_AFTER_AGE + 1))

        jointOptions = {
            Options.RESTARTING: True
        }
        jointOptions.update(options)

        # call the backup creation one more time with max. backup level set to NUMBER_OF_CREATED_LEVELS
        ArchivingTestUtils._createIncrementalBackup(archiverMock, jointOptions, NUMBER_OF_CREATED_LEVELS,
                                                    self.__storageState, self.__archiveSpecFilePath)

        # check that the last call of backupFilesIncrementally() was with backup level 1
        self.assertEqual(1, archiverMock.backupFilesIncrementally.call_args[0][2],
                         "The backup creation on the service was not called with expected backup level.")



    def test_makeBackupFullRestartAfterCount(self):
        """Tests the makeBackup() method for full level restarting after a specific number of restarts.

        Configures values for backup level restart and full backup level restart.  Creates number of backups so that
        the level shall be fully restarted.  Checks that the service method was called to create backup of level 0."""

        RESTART_AFTER_LEVEL = 1
        FULL_RESTART_AFTER_COUNT = 1

        archiverMock = ArchiverTestUtils.createArchiverMock()

        options = {
            Options.RESTART_AFTER_LEVEL: RESTART_AFTER_LEVEL,
            Options.FULL_RESTART_AFTER_COUNT: FULL_RESTART_AFTER_COUNT
        }

        # call the backup creation for number of times required to full restart; for the first time the level is
        # restarted after RESTART_AFTER_LEVEL + 1 backups are created; later on the level is restarted after each
        # backup creation (because the max. backup level is already higher than RESTART_AFTER_LEVEL), so we need to
        # make FULL_RESTART_AFTER_COUNT additional backups; finally yet one additional backup creation shall do the
        # _full_ restart
        self.__createRestartableArchives(archiverMock, options, RESTART_AFTER_LEVEL + FULL_RESTART_AFTER_COUNT + 2)

        # check that the last call of backupFilesIncrementally() was with backup level 0
        self.assertEqual(0, archiverMock.backupFilesIncrementally.call_args[0][2],
                         "The backup creation on the service was not called with expected backup level.")



    def test_makeBackupFullRestartAfterDays(self):
        """Tests the makeBackup() method for full restarting a level after a specific number of days passed.

        Configures that the backup level shall be fully restarted after 3 days.  Creates a level 0 and level 1
        archives.  Modify value of last full restart in the storage mock so that it is older than 3 days.  Removes all
        created backup files and creates a one more backup which should be level 0 due to full restarting.  Checks that
        the backup file of level 0 was created."""

        FULL_RESTART_AFTER_AGE = 3

        NUMBER_OF_CREATED_LEVELS = 3

        STORAGE_LAST_FULL_RESTART = "archiving-last-full-restart"

        archiverMock = ArchiverTestUtils.createArchiverMock()

        options = {
            Options.RESTART_AFTER_LEVEL: 100, # has to be greater than NUMBER_OF_CREATED_LEVELS
            Options.FULL_RESTART_AFTER_AGE: FULL_RESTART_AFTER_AGE
        }

        # call the backup creation for NUMBER_OF_CREATED_LEVELS times
        self.__createRestartableArchives(archiverMock, options, NUMBER_OF_CREATED_LEVELS,
                                         archiveSpecFile = self.__archiveSpecFilePath)

        # decrease last full restart date by FULL_RESTART_AFTER_AGE + 1 days

        # >beware that how the date of the last full restart is stored is internal to the Archiving component so the
        # >following code may break without the interface change; well, not great but much better than to let this test
        # >to wait couple of days

        # >from the name of the archive specification file we get the realm
        realm = os.path.basename(self.__archiveSpecFilePath)

        # >get the last full restart date, decrease it and store back
        lastRestartStr = self.__storageState[realm][ConfigurationTestUtils.DEFAULT_SECTION][STORAGE_LAST_FULL_RESTART]
        lastRestart = datetime.strptime(lastRestartStr, "%Y-%m-%d").date()
        self.__storageState[realm][ConfigurationTestUtils.DEFAULT_SECTION][STORAGE_LAST_FULL_RESTART] = \
            str(lastRestart - timedelta(FULL_RESTART_AFTER_AGE + 1))

        jointOptions = {
            Options.RESTARTING: True
        }
        jointOptions.update(options)

        # call the backup creation one more time with max. backup level set to NUMBER_OF_CREATED_LEVELS
        ArchivingTestUtils._createIncrementalBackup(archiverMock, jointOptions, NUMBER_OF_CREATED_LEVELS,
                                                    self.__storageState, self.__archiveSpecFilePath)

        # check that the last call of backupFilesIncrementally() was with backup level 0
        self.assertEqual(0, archiverMock.backupFilesIncrementally.call_args[0][2],
                         "The backup creation on the service was not called with expected backup level.")



    def test_makeBackupMaxRestartLevelSize_NotAllowed(self):
        """Tests the makeBackup() method for restarting to a higher level due to max. size reached.

        Configures that the backup level shall be restarted after level 2 and that the size of the target level can not
        exceed 60% of level 0 backup size.  Creates a level 0 backup then the level 1 backup with the service mock
        set up so that it creates (backup) file bigger than 60% of the level 0 (backup) file.  Finally, creates two
        more backups so that level is restarted.  Checks that the service method was called to create backup of level 2
        (which means that it was not allowed to restart to level 1)."""

        LEVEL0_SIZE = 10
        MAX_RESTART_LEVEL_SIZE = 60
        BACKUP_ID = "test backup"

        # create files which will represent backup files of particular levels
        # >create level 0 backup file of size LEVEL0_SIZE
        level0Backup = os.path.join(ComponentTestUtils.getComponentTestContext().workDir, BACKUP_ID + ".0")
        with open(level0Backup, "wb") as level0BackupStream:
            level0BackupStream.write(b"x" * LEVEL0_SIZE)

        # >create level 1 backup file which size is MAX_RESTART_LEVEL_SIZE + 15 percent of the level 0 size
        level1Backup = os.path.join(ComponentTestUtils.getComponentTestContext().workDir, BACKUP_ID + ".1")
        with open(level1Backup, "wb") as level1BackupStream:
            level1BackupStream.write(b"x" * round(LEVEL0_SIZE * ((MAX_RESTART_LEVEL_SIZE + 15) / 100)))

        archiverMock = ArchiverTestUtils.createArchiverMock()
        archiveSpecFilePath = ArchivingTestUtils._makeArchiveSpecFile(BACKUP_ID)

        options = {
            Options.RESTARTING: True,
            Options.RESTART_AFTER_LEVEL: 2,
            Options.MAX_RESTART_LEVEL_SIZE: MAX_RESTART_LEVEL_SIZE
        }

        # call the backup creation for level 0
        ArchivingTestUtils._createIncrementalBackup(archiverMock, options, 0, self.__storageState, archiveSpecFilePath)

        # call the backup creation for level 1
        ArchivingTestUtils._createIncrementalBackup(archiverMock, options, 1, self.__storageState, archiveSpecFilePath)

        os.remove(level0Backup)
        os.remove(level1Backup)

        # call the backup creation for last two levels so it gets restarted
        ArchivingTestUtils._createIncrementalBackup(archiverMock, options, 2, self.__storageState, archiveSpecFilePath)
        ArchivingTestUtils._createIncrementalBackup(archiverMock, options, 3, self.__storageState, archiveSpecFilePath)

        # check that the last call of backupFilesIncrementally() was with backup level 2
        self.assertEqual(2, archiverMock.backupFilesIncrementally.call_args[0][2],
                         "The backup creation on the service was not called with expected backup level.")



    def test_makeBackupMaxRestartLevelSize_Allowed(self):
        """Tests the makeBackup() method for restarting not to a higher level.

        Configures that the backup level shall be restarted after level 2 and that the size of the target level can not
        exceed 60% of level 0 backup size.  Creates a level 0 backup then the level 1 backup with the service mock
        set up so that it creates (backup) file smaller than 60% of the level 0 (backup) file.  Finally, creates two
        more backups so that level is restarted.  Checks that the service method was called to create backup of level 1
        (which means that it was allowed to restart to level 1)."""

        LEVEL0_SIZE = 10
        MAX_RESTART_LEVEL_SIZE = 60
        BACKUP_ID = "test backup"

        # create files which will represent backup files of particular levels
        # >create level 0 backup file of size LEVEL0_SIZE
        level0Backup = os.path.join(ComponentTestUtils.getComponentTestContext().workDir, BACKUP_ID + ".0")
        with open(level0Backup, "wb") as level0BackupStream:
            level0BackupStream.write(b"x" * LEVEL0_SIZE)

        # >create level 1 backup file which size is MAX_RESTART_LEVEL_SIZE - 15 percent of the level 0 size
        level1Backup = os.path.join(ComponentTestUtils.getComponentTestContext().workDir, BACKUP_ID + ".1")
        with open(level1Backup, "wb") as level1BackupStream:
            level1BackupStream.write(b"x" * round(LEVEL0_SIZE * ((MAX_RESTART_LEVEL_SIZE - 15) / 100)))

        archiverMock = ArchiverTestUtils.createArchiverMock()
        archiveSpecFilePath = ArchivingTestUtils._makeArchiveSpecFile(BACKUP_ID)

        options = {
            Options.RESTARTING: True,
            Options.RESTART_AFTER_LEVEL: 2,
            Options.MAX_RESTART_LEVEL_SIZE: MAX_RESTART_LEVEL_SIZE
        }

        # call the backup creation for level 0
        ArchivingTestUtils._createIncrementalBackup(archiverMock, options, 0, self.__storageState, archiveSpecFilePath)

        # call the backup creation for level 1
        ArchivingTestUtils._createIncrementalBackup(archiverMock, options, 1, self.__storageState, archiveSpecFilePath)

        os.remove(level0Backup)
        os.remove(level1Backup)

        archiverMock.backupFilesIncrementally.return_value = self.__irrelevantFilePath

        # call the backup creation for last two levels so it gets restarted
        ArchivingTestUtils._createIncrementalBackup(archiverMock, options, 2, self.__storageState, archiveSpecFilePath)
        ArchivingTestUtils._createIncrementalBackup(archiverMock, options, 3, self.__storageState, archiveSpecFilePath)

        # check that the last call of backupFilesIncrementally() was with backup level 1
        self.assertEqual(1, archiverMock.backupFilesIncrementally.call_args[0][2],
                         "The backup creation on the service was not called with expected backup level.")

    # }}} makeBackup() tests for backup level restarting



    # {{{ helpers for makeBackup() tests for backup level restarting

    def __createRestartableArchives(self, archiverMock, options = None, levels = 1, archiveSpecFile = None):
        if options is None: options = {}

        jointOptions = {
            Options.RESTARTING: True
        }
        jointOptions.update(options)

        ArchivingTestUtils._createIncrementalBackups(archiverMock, jointOptions, levels, self.__storageState,
                                                     archiveSpecFile)

    # }}} helpers for makeBackup() tests for backup level restarting



class TestIArchivingMakeBackupOptionsPriority(unittest.TestCase):
    """Test of :meth:`.IArchiving.makeBackup()` method for priority of configuration options vs. .aa file."""



    @classmethod
    def setUpClass(cls):
        ArchivingTestUtils._setUpClassArchivingComponent()



    @classmethod
    def tearDownClass(cls):
        ArchivingTestUtils._tearDownClassArchivingComponent()



    def setUp(self):
        ArchivingTestUtils._setUpArchivingComponent()



    def tearDown(self):
        ArchivingTestUtils._tearDownArchivingComponent()



    # {{{ makeBackup() tests for options priority

    def test_makeBackupConfigOptionOverride(self):
        """Tests the makeBackup() method for overriding a configuration option by the
        :term:`archive specification file`.

        Overrides :attr:`.Options.ARCHIVER` configured option by a new value in :term:`archive specification file` and
        creates a backup.  Checks that the service was called to create the backup type specified in archive
        specification file was created."""

        AA_SPEC_ARCHIVER = ArchiverTypes.TarGzInternal

        options = {
            Options.USER_CONFIG_DIR: ComponentTestUtils.getComponentTestContext().userConfigDir,
            Options.ARCHIVER: ArchiverTypes.TarBz2Internal
        }

        archiverMock = ArchiverTestUtils.createArchiverMock()

        ArchivingTestUtils._createBackup(archiverMock, options, archiverType = AA_SPEC_ARCHIVER)

        # test that the service was called to create backup type configured in .aa file
        self.assertEqual(ArchivingTestUtils._ARCHIVER_TYPE_TO_BACKUP_TYPE_MAP[AA_SPEC_ARCHIVER],
                         archiverMock.backupFiles.call_args[0][0].backupType)



    # Strictly speaking, this is a test for Configuration component functionality
    def test_makeBackupConfigOptionOverrideForce(self):
        """Tests the makeBackup() method for overriding a ``force-`` config. option by the
        :term:`archive specification file`.

        Overrides :attr:`.Options.FORCE_ARCHIVER` configured option by a new value in :term:`archive specification file`
        and creates a backup.  Checks that the service was called to create the backup type specified in the
        ``force-`` option (i. e. that the ``force-`` option was not overridden)."""

        AA_SPEC_ARCHIVER = ArchiverTypes.TarGzInternal
        FORCED_ARCHIVER = ArchiverTypes.TarBz2Internal

        options = {
            Options.USER_CONFIG_DIR: ComponentTestUtils.getComponentTestContext().userConfigDir,
            Options.FORCE_ARCHIVER: FORCED_ARCHIVER
        }

        archiverMock = ArchiverTestUtils.createArchiverMock()

        ArchivingTestUtils._createBackup(archiverMock, options, AA_SPEC_ARCHIVER)

        # test that the service was called to create forced backup type
        self.assertEqual(ArchivingTestUtils._ARCHIVER_TYPE_TO_BACKUP_TYPE_MAP[FORCED_ARCHIVER],
                         archiverMock.backupFiles.call_args[0][0].backupType)

    # }}} makeBackup() tests for options priority

# }}} makeBackup() tests



# {{{ configured archive info tests

class TestIArchivingConfiguredArchiveInfo(unittest.TestCase):
    "Test of methods for getting info about configured archives."

    __ARCHIVE_NAME = "test archive name"



    @classmethod
    def setUpClass(cls):
        ArchivingTestUtils._setUpClassArchivingComponent()



    @classmethod
    def tearDownClass(cls):
        ArchivingTestUtils._tearDownClassArchivingComponent()



    def setUp(self):
        self.__mockInterfaceAccessor = None

        ArchivingTestUtils._setUpArchivingComponent()
        options = {Options.USER_CONFIG_DIR: ComponentTestUtils.getComponentTestContext().userConfigDir}
        mockAppConfig = ConfigurationTestUtils.createMockAppConfig(options)
        self.__mockInterfaceAccessor = ArchivingTestUtils._setUpMockInterfaceAccessor(mockAppConfig)
        ArchivingComponent(self.__mockInterfaceAccessor)



    def tearDown(self):
        ArchivingTestUtils._tearDownArchivingComponent()



    def test_filterValidSpecFiles(self):
        """Tests the :meth:`IArchiving.filterValidSpecFiles()` method.

        Creates two :term:`archive specification files <archive specification file>`, one with defined ``name``
        variable and the other without it.  It calls tested method with iterable of these two files and compares that
        the returned iterable contains a member that equals to the value of the specifies ``name`` variable and the
        member that equals to the file name of the second file."""

        archiveSpecFilesPaths = (ArchivingTestUtils._makeArchiveSpecFile(self.__ARCHIVE_NAME),
                                 ArchivingTestUtils._makeArchiveSpecFile())

        archiving = self.__mockInterfaceAccessor.getComponentInterface(IArchiving)

        archiveNames = archiving.filterValidSpecFiles(archiveSpecFilesPaths)

        self.assertCountEqual((self.__ARCHIVE_NAME, os.path.basename(archiveSpecFilesPaths[1])), archiveNames)



    def test_getArchiveInfo(self):
        """Tests the :meth:`IArchiving.getArchiveInfo()` method.

        Creates an :term:`archive specification file` with some defined variables.  Also sets up Archiver service mocks
        to return predefined values.  Calls the tested method and checks that :class:`ArchiveInfo` instance is
        created; then checks a few basic properties that they have expected values."""

        PATH = os.curdir
        ARCHIVER = ArchiverTypes.TarXz
        DEST_DIR = '"test dest dir"'
        MAX_BACKUP_LEVEL = 3

        # set up archive specification file and archiver service mocks
        archiveSpecFilePath = ArchivingTestUtils._makeArchiveSpecFile(
            self.__ARCHIVE_NAME, PATH, archiver = ARCHIVER, destDir = DEST_DIR)
        archiverMock = ArchiverTestUtils.createArchiverMock()
        archiverMock.getMaxBackupLevel.return_value = MAX_BACKUP_LEVEL
        archiverServiceCreatorMock = ArchivingTestUtils._setUpArchiverServices(
            archiverMock, supportedFeatures = frozenset({ArchiverFeatures.Incremental}))

        archiving = self.__mockInterfaceAccessor.getComponentInterface(IArchiving)

        with mock.patch("AutoArchive._archiving._core._archiver_manipulator.ArchiverServiceCreator",
                        archiverServiceCreatorMock):
            with mock.patch("AutoArchive._archiving._core._backup_information_provider.ArchiverServiceCreator",
                            archiverServiceCreatorMock):

                # call the tested method
                archiveInfo = archiving.getArchiveInfo(archiveSpecFilePath)

        self.assertIsNotNone(archiveInfo)
        self.assertEqual(self.__ARCHIVE_NAME, archiveInfo.name)
        self.assertEqual(PATH, archiveInfo.path)
        self.assertEqual(ARCHIVER, archiveInfo.archiverType)
        self.assertEqual(DEST_DIR, archiveInfo.destDir)
        self.assertFalse(archiveInfo.incremental)
        self.assertEqual(MAX_BACKUP_LEVEL - 1, archiveInfo.backupLevel)
        self.assertFalse(archiveInfo.restarting)
        self.assertIsNone(archiveInfo.lastRestart)

# }}} configured archive info tests



# {{{ stored archive info tests

class TestIArchivingStoredArchiveInfo(unittest.TestCase):
    "Test of :meth:`.IArchiving.getStoredArchiveInfo()` method."



    @classmethod
    def setUpClass(cls):
        ArchivingTestUtils._setUpClassArchivingComponent()



    @classmethod
    def tearDownClass(cls):
        ArchivingTestUtils._tearDownClassArchivingComponent()



    def setUp(self):
        self.__mockInterfaceAccessor = None
        self.__archiveSpecFilePath = None

        ArchivingTestUtils._setUpArchivingComponent()

        options = {
            Options.USER_CONFIG_DIR: ComponentTestUtils.getComponentTestContext().userConfigDir,
            Options.INCREMENTAL: True
        }
        mockAppConfig = ConfigurationTestUtils.createMockAppConfig(options)
        self.__mockInterfaceAccessor = ArchivingTestUtils._setUpMockInterfaceAccessor(mockAppConfig)
        ArchivingComponent(self.__mockInterfaceAccessor)



    def tearDown(self):
        ArchivingTestUtils._tearDownArchivingComponent()



    def test_getStoredArchiveInfo(self):
        """Tests the :meth:`IArchiving.getStoredArchiveInfo()` method.

        Sets up Archiver service mocks to return predefined values.  Calls the tested method and checks that
        :class:`ArchiveInfo` instance is created; then checks a few basic properties that they have expected values."""

        TEST_STORED_BACKUP = "test stored backup"
        IRRELEVANT_BACKUP_LEVEL = 5

        # set up archiver service mocks
        archiverMock = ArchiverTestUtils.createArchiverMock()
        archiverMock.getMaxBackupLevel.return_value = IRRELEVANT_BACKUP_LEVEL
        archiverMock.getStoredBackupIds.return_value = {TEST_STORED_BACKUP}
        archiverServiceCreatorMock = ArchivingTestUtils._setUpArchiverServices(
            archiverMock, supportedFeatures = frozenset({ArchiverFeatures.Incremental}))

        archiving = self.__mockInterfaceAccessor.getComponentInterface(IArchiving)

        with mock.patch("AutoArchive._archiving._core._archiver_manipulator.ArchiverServiceCreator",
                        archiverServiceCreatorMock):
            with mock.patch("AutoArchive._archiving._core._backup_information_provider.ArchiverServiceCreator",
                            archiverServiceCreatorMock):

                # call the tested method
                archiveInfo = archiving.getStoredArchiveInfo(TEST_STORED_BACKUP)

        self.assertIsNotNone(archiveInfo)
        self.assertEqual(archiveInfo.name, TEST_STORED_BACKUP)
        self.assertTrue(archiveInfo.incremental)

        # path shall be ``None`` in case of stored info (and not ``None`` in case of configured info)
        self.assertIsNone(archiveInfo.path)



    def test_getStoredArchiveNames(self):
        """Tests the :meth:`IArchiving.getStoredArchiveNames()` method.

        Sets up archiver's service method for returning stored backup IDs to a predefined value.  Calls the tested
        method and checks that the same stored archive names as the predefined ones were returned."""

        TEST_STORED_BACKUPS = {"test stored backup 1", "test stored backup 2"}

        # set up archiver service mocks
        archiverMock = ArchiverTestUtils.createArchiverMock()
        archiverMock.getStoredBackupIds.return_value = TEST_STORED_BACKUPS
        archiverServiceCreatorMock = ArchivingTestUtils._setUpArchiverServices(archiverMock)

        archiving = self.__mockInterfaceAccessor.getComponentInterface(IArchiving)

        with mock.patch("AutoArchive._archiving._core._archiver_manipulator.ArchiverServiceCreator",
                        archiverServiceCreatorMock):
            with mock.patch("AutoArchive._archiving._core._backup_information_provider.ArchiverServiceCreator",
                            archiverServiceCreatorMock):

                # call the tested method
                # (enumerate generator into set right away when the mock.patch is active)
                archiveNames = set(archiving.getStoredArchiveNames())

        self.assertCountEqual(TEST_STORED_BACKUPS, archiveNames)



    def test_purgeStoredArchiveData(self):
        """Tests the :meth:`IArchiving.purgeStoredArchiveData()` method.

        Sets up archiver's service method for returning stored backup IDs to a predefined value.  Calls the tested
        method to remove a particular backup.  Checks that the service method was called with an argument equal to
        the backup name that was requested for purge."""

        TEST_STORED_BACKUP_2 = "test stored backup 2"
        TEST_STORED_BACKUPS = ("test stored backup 1", TEST_STORED_BACKUP_2)

        # set up archiver service mocks
        archiverMock = ArchiverTestUtils.createArchiverMock()
        archiverMock.getStoredBackupIds.return_value = TEST_STORED_BACKUPS
        archiverServiceCreatorMock = ArchivingTestUtils._setUpArchiverServices(archiverMock)

        archiving = self.__mockInterfaceAccessor.getComponentInterface(IArchiving)

        with mock.patch("AutoArchive._archiving._core._archiver_manipulator.ArchiverServiceCreator",
                        archiverServiceCreatorMock):
            with mock.patch("AutoArchive._archiving._core._backup_information_provider.ArchiverServiceCreator",
                            archiverServiceCreatorMock):

                # call the tested method
                archiving.purgeStoredArchiveData(TEST_STORED_BACKUP_2)

        archiverMock.purgeStoredBackupData.assert_called_with(TEST_STORED_BACKUP_2)

# }}} stored archive info tests

# }}} CLASSES

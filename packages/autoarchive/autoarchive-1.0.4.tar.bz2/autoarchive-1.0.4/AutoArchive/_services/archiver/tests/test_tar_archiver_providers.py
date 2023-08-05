# test_archiver_providers.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2012 Róbert Čerňanský



""":class:`TestInternalTarArchiverProvidersBackupTypes`, :class:`TestExternalTarArchiverProvidersBackupTypes`,
:class:`TestInternalTarArchiverProvidersContent`, :class:`TestExternalTarArchiverProvidersContent`,
:class:`TestInternalTarBackupRemoval`, :class:`TestExternalTarBackupRemoval`,
:class:`TestExternalTarArchiverProvidersIncremental`."""



__all__ = ["TestInternalTarArchiverProvidersBackupTypes", "TestExternalTarArchiverProvidersBackupTypes",
           "TestInternalTarArchiverProvidersContent", "TestExternalTarArchiverProvidersContent",
           "TestInternalTarBackupRemoval", "TestExternalTarBackupRemoval",
           "TestExternalTarArchiverProvidersIncremental"]



# {{{ INCLUDES

import unittest
from mock import Mock

from abc import *
import os
import shutil
import glob
import time

from .._internal_tar_archiver_provider import *
from .._external_tar_archiver_provider import *

from ...._archiving import *

from ....tests import *
from .archiver_test_utils import *
from .archiver_test_utils import _BackupDefinitionBuilder

# }}} INCLUDES



# {{{ CLASSES

class _TestTarArchiverProvidersBackupTypes(unittest.TestCase):
    """Base class for tests of tar archiver providers for different archive types."""

    # Attention! Tests included in this class and in derived classes has to initialize the self.extractPath_ variable
    # with a path to the extracted backup.



    @classmethod
    def setUpClass(cls):
        ArchiverTestUtils._setUpClassArchivingComponent()



    @classmethod
    def tearDownClass(cls):
        ArchiverTestUtils._tearDownClassArchivingComponent()



    def setUp(self):
        self.archiverProvider_ = None
        self.testFileStructurePath_ = None
        self.extractPath_ = None

        self.archiverProvider_ = self.createTestSubject_()
        self.testFileStructurePath_ = ArchiverTestUtils._makeTestFileStructure()



    def tearDown(self):
        ArchiverTestUtils._removeExtractedBackup(self.extractPath_)
        if os.path.isfile(ArchiverTestUtils._irrelevantValidFilePath):
            os.remove(ArchiverTestUtils._irrelevantValidFilePath)
        ArchiverTestUtils._removeTestFileStructure(self.testFileStructurePath_)



    @abstractmethod
    def createTestSubject_(self):
        """Creates an instance of tested archiver provider."""



    # {{{ supported backup types and features tests

    def test_SupportedBackupTypes(self):
        """Tests the supportedBackupTypes property.

        Asserts that the tested archiver service provider supports at least one backup type."""

        self.assertGreater(len(self.archiverProvider_.supportedBackupTypes), 0)



    def test_getSupportedFeatures(self):
        """Tests the getSupportedFeatures() method.

        Asserts that the tested archiver service provider does not return ``None`` as the iterable of features."""

        self.assertIsNotNone(self.archiverProvider_.getSupportedFeatures())



    def test_getSupportedFeaturesForBackupType(self):
        """Tests the getSupportedFeatures() method for all supported backup types.

        Gets all supported features then asserts that for each supported backup type, supported features for the given
        type is a subset of all supported features."""

        allSupportedFeatures = self.archiverProvider_.getSupportedFeatures()
        for backupType in self.archiverProvider_.supportedBackupTypes:
            self.assertTrue(self.archiverProvider_.getSupportedFeatures(backupType) <= allSupportedFeatures)

    # }}} supported backup types and features tests



    # {{{ backup creation tests for backup types

    def test_BackupCreationOfTypeTar(self):
        """Tests the creation of "tar" backup."""

        self.createAndCheckBackupType_(BackupTypes.Tar, b"ustar\x00", 257)



    def test_BackupCreationOfTypeTarGz(self):
        """Tests the creation of "tar.gz" backup."""

        self.createAndCheckBackupType_(BackupTypes.TarGz, b"\x1f\x8b")



    def test_BackupCreationOfTypeTarBz2(self):
        """Tests the creation of "tar.bz2" backup."""

        self.createAndCheckBackupType_(BackupTypes.TarBz2, b"BZh")



    def createAndCheckBackupType_(self, backupType, magicBytes, magicOffset = 0):
        """Tests the creation of a backup of passed type.

        Creates the backup of specified type and asserts that the corresponding backup file exists and the magic bytes
        matches."""

        backupDefinition = _BackupDefinitionBuilder()\
            .withBackupType(backupType)\
            .withRoot(self.testFileStructurePath_)\
            .withIncludeFiles(os.listdir(self.testFileStructurePath_))\
            .build()
        backupFilePath = self.archiverProvider_.backupFiles(backupDefinition)

        self.assertTrue(os.path.isfile(backupFilePath), "The backup file does not exists.")
        with open(backupFilePath ,"rb") as archiveStream:
            readMagicBytes = \
                archiveStream.read(magicOffset + len(magicBytes))[magicOffset:(magicOffset + len(magicBytes))]
            self.assertEqual(magicBytes, readMagicBytes, str.format("The created backup is not of type \"{}\".",
                                                                    str(backupType)))

    # }}} backup creation tests for backup types



class TestInternalTarArchiverProvidersBackupTypes(_TestTarArchiverProvidersBackupTypes):
    """Tests of internal tar archiver provider for different archive types."""

    def createTestSubject_(self):
        return _InternalTarArchiverProvider(ComponentTestUtils.getComponentTestContext().workDir)



class TestExternalTarArchiverProvidersBackupTypes(_TestTarArchiverProvidersBackupTypes):
    """Tests of external tar archiver provider for different archive types."""

    def createTestSubject_(self):
        return _ExternalTarArchiverProvider(ComponentTestUtils.getComponentTestContext().workDir)



    # {{{ backup creation tests for backup types

    def test_BackupCreationOfTypeTarXz(self):
        """Tests the creation of "tar.xz" backup."""

        self.createAndCheckBackupType_(BackupTypes.TarXz, b"\xFD7zXZ\x00")

    # }}} backup creation tests for backup types



    # {{{ backup creation tests for compression level

    def test_BackupCreationCompressionStrengthTarGz(self):
        """Tests the effect of compression strength for "tar.gz" backup type."""

        self.__testCompressionStrength(BackupTypes.TarGz)



    def test_BackupCreationCompressionStrengthTarBz2(self):
        """Tests the effect of compression strength for "tar.bz2" backup type."""

        # create significantly big test file structure
        ArchiverTestUtils._removeTestFileStructure(self.testFileStructurePath_)
        self.testFileStructurePath_ = ArchiverTestUtils._makeTestFileStructure(200)

        self.__testCompressionStrength(BackupTypes.TarBz2)



    def test_BackupCreationCompressionStrengthTarXz(self):
        """Tests the effect of compression strength for "tar.xz" backup type."""

        self.__testCompressionStrength(BackupTypes.TarXz)



    def __testCompressionStrength(self, backupType):
        """Tests the effect of compression strength for passed archive type.

        Creates a backup with lowest compression strength and then with highest.  Asserts tha the size of the backup
        with highest strength is smaller than the other."""

        backupDefinition = _BackupDefinitionBuilder()\
            .withBackupType(backupType)\
            .withRoot(self.testFileStructurePath_)\
            .withIncludeFiles(os.listdir(self.testFileStructurePath_))\
            .build()

        backupFilePath = self.archiverProvider_.backupFiles(backupDefinition, 0)
        sizeOfStrength0 = os.path.getsize(backupFilePath)
        backupFilePath = self.archiverProvider_.backupFiles(backupDefinition, 9)
        sizeOfStrength9 = os.path.getsize(backupFilePath)

        self.assertLess(sizeOfStrength9, sizeOfStrength0,
                        "The backup file created with stronger compression strength " +
                        "has not smaller size than the one created with weaker strength.")

    # }}} backup creation tests for compression level



class _TestTarArchiverProvidersContent(unittest.TestCase):
    """Base class for tests of tar archiver providers for archive content."""

    # Attention! Tests included in this class and derived classes has to fulfill following requirements:
    # - Create a test file structure and store the path to it to self.testFileStructurePath_ variable.
    # - Initialize the self.extractPath_ variable with a path to the extracted backup.



    @classmethod
    def setUpClass(cls):
        ArchiverTestUtils._setUpClassArchivingComponent()



    @classmethod
    def tearDownClass(cls):
        ArchiverTestUtils._tearDownClassArchivingComponent()



    def setUp(self):
        self.archiverProvider_ = None
        self.testFileStructurePath_ = None
        self.extractPath_ = None

        self.archiverProvider_ = self.createTestSubject_()



    def tearDown(self):
        ArchiverTestUtils._removeExtractedBackup(self.extractPath_)
        if os.path.isfile(ArchiverTestUtils._irrelevantValidFilePath):
            os.remove(ArchiverTestUtils._irrelevantValidFilePath)
        ArchiverTestUtils._removeTestFileStructure(self.testFileStructurePath_)



    @abstractmethod
    def createTestSubject_(self):
        """Creates an instance of tested archiver provider."""



    # {{{ backup creation tests for archive content

    def test_BackupCreationContent(self):
        """Tests the creation of a backup and its content.

        Creates a backup and extracts it.  Asserts that the backup content is identical to the archived file
        structure."""

        self.testFileStructurePath_ = ArchiverTestUtils._makeTestFileStructure()

        backupDefinition = _BackupDefinitionBuilder()\
            .withRoot(self.testFileStructurePath_)\
            .withIncludeFiles(os.listdir(self.testFileStructurePath_))\
            .build()
        backupFilePath = self.archiverProvider_.backupFiles(backupDefinition)

        self.extractPath_ = ArchiverTestUtils._extractBackup(backupFilePath)
        self.assertTrue(ArchiverTestUtils._compareDirs(self.testFileStructurePath_, self.extractPath_))



    def test_BackupCreationContentLinks(self):
        """Tests the creation of a backup and its content with file structure containing symlinks.

        Creates a backup and extracts it.  Asserts that the backup content is identical to the archived file
        structure."""

        self.testFileStructurePath_ = ArchiverTestUtils._makeTestFileStructure(links = True)

        backupDefinition = _BackupDefinitionBuilder()\
            .withRoot(self.testFileStructurePath_)\
            .withIncludeFiles(os.listdir(self.testFileStructurePath_))\
            .build()
        backupFilePath = self.archiverProvider_.backupFiles(backupDefinition)

        self.extractPath_ = ArchiverTestUtils._extractBackup(backupFilePath)
        self.assertTrue(ArchiverTestUtils._compareDirs(self.testFileStructurePath_, self.extractPath_))



    def test_BackupCreationContentExclude(self):
        """Tests the creation of a backup and its content with some file excluded.

        Creates a backup and extracts it.  Asserts that the backup content is identical to the archived file
        structure."""

        EXCLUDE_FILES = frozenset({str.format(ArchiverTestUtils._DIR_NAME, index = 1),
                                   os.path.join(str.format(ArchiverTestUtils._DIR_NAME, index = 0),
                                                str.format(ArchiverTestUtils._FILE_NAME, index = 0))})

        self.testFileStructurePath_ = ArchiverTestUtils._makeTestFileStructure()

        backupDefinition = _BackupDefinitionBuilder()\
            .withRoot(self.testFileStructurePath_)\
            .withIncludeFiles(os.listdir(self.testFileStructurePath_))\
            .withExcludeFiles(EXCLUDE_FILES)\
            .build()
        backupFilePath = self.archiverProvider_.backupFiles(backupDefinition)

        self.extractPath_ = ArchiverTestUtils._extractBackup(backupFilePath)

        # make a set of files that were archived but exclude the content of directories in EXCLUDE_FILES; beware that
        # the algorithm below works only for top-level directories in EXCLUDE_FILES
        originalFiles = set()
        for root, dirs, files in os.walk(self.testFileStructurePath_):
            relativeRoot = os.path.relpath(root, self.testFileStructurePath_)
            if ((os.path.dirname(relativeRoot) and os.path.dirname(relativeRoot) not in EXCLUDE_FILES) or
                not os.path.dirname(relativeRoot)):
                originalFiles.add(relativeRoot)
            if relativeRoot not in EXCLUDE_FILES and \
               ((os.path.dirname(relativeRoot) and os.path.dirname(relativeRoot) not in EXCLUDE_FILES) or
                not os.path.dirname(relativeRoot)):
                originalFiles.update({os.path.join(relativeRoot, f) for f in files})

        # make a set of files that the archive contains
        extractedFiles = set()
        for root, dirs, files in os.walk(self.extractPath_):
            relativeRoot = os.path.relpath(root, self.extractPath_)
            extractedFiles.add(relativeRoot)
            extractedFiles.update({os.path.join(relativeRoot, f) for f in files})

        excluded = originalFiles - extractedFiles
        self.assertEqual(EXCLUDE_FILES, excluded)



    def test_BackupCreationContentSocket(self):
        """Tests the creation of a backup and its content with file structure containing a socket.

        Creates a backup and extracts it.  Asserts that the backup content does not contains the socket."""

        self.testFileStructurePath_ = ArchiverTestUtils._makeTestFileStructure(socket = True)

        backupDefinition = _BackupDefinitionBuilder()\
            .withRoot(self.testFileStructurePath_)\
            .withIncludeFiles(os.listdir(self.testFileStructurePath_))\
            .build()
        backupFilePath = self.archiverProvider_.backupFiles(backupDefinition)

        # check that the backup does not contains the socket
        self.extractPath_ = ArchiverTestUtils._extractBackup(backupFilePath)
        sockets = set(os.listdir(self.testFileStructurePath_)) - set(os.listdir(self.extractPath_))
        self.assertEqual(sockets, {ArchiverTestUtils._SOCKET_NAME})



    def test_PermissionDeniedContent(self):
        """Tests the content of the backup with some unreadable filesystem objects.

        Creates a backup and extracts it.  Asserts that the backup content does not contains filesystem objects which
        were not readable."""

        self.testFileStructurePath_ = ArchiverTestUtils._makeTestFileStructure(denied = True, links = True)

        backupDefinition = _BackupDefinitionBuilder()\
            .withRoot(self.testFileStructurePath_)\
            .withIncludeFiles(os.listdir(self.testFileStructurePath_))\
            .build()
        backupFilePath = self.archiverProvider_.backupFiles(backupDefinition)

        # check that the backup does not contain the unreadable file and directory
        self.extractPath_ = ArchiverTestUtils._extractBackup(backupFilePath)
        denied = set(os.listdir(self.testFileStructurePath_)) - set(os.listdir(self.extractPath_))
        self.assertEqual(denied, {ArchiverTestUtils._DENIED_FILE_NAME, ArchiverTestUtils._DENIED_DIR_NAME})

    # }}} backup creation tests for archive content



    # {{{ backup creation tests for events propagation

    def test_PermissionDeniedPropagation(self):
        """Tests the propagation of permission denied error during backup creation.

        Creates a backup of file structure containing non-readable objects.  Asserts that during creation the
        corresponding event was fired for each unreadable object."""

        self.testFileStructurePath_ = ArchiverTestUtils._makeTestFileStructure(denied = True, links = True)
        onBackupOperationErrorMock = Mock()
        self.archiverProvider_.backupOperationError += onBackupOperationErrorMock

        backupDefinition = _BackupDefinitionBuilder()\
            .withRoot(self.testFileStructurePath_)\
            .withIncludeFiles(os.listdir(self.testFileStructurePath_))\
            .build()
        self.archiverProvider_.backupFiles(backupDefinition)

        self.assertEqual([((BackupSubOperations.Open, BackupOperationErrors.PermissionDenied,
                            ArchiverTestUtils._DENIED_DIR_NAME), {}),
                          ((BackupSubOperations.Open, BackupOperationErrors.PermissionDenied,
                            ArchiverTestUtils._DENIED_FILE_NAME), {})],
            onBackupOperationErrorMock.call_args_list)



    def test_BackupCreationSocketIgnoredPropagation(self):
        """Tests the propagation of socket ignored error during backup creation.

        Creates a backup of file structure containing a socket.  Asserts that during creation the corresponding event
        was fired for the socket."""

        self.testFileStructurePath_ = ArchiverTestUtils._makeTestFileStructure(socket = True)

        onBackupOperationErrorMock = Mock()
        self.archiverProvider_.backupOperationError += onBackupOperationErrorMock

        backupDefinition = _BackupDefinitionBuilder()\
            .withRoot(self.testFileStructurePath_)\
            .withIncludeFiles(os.listdir(self.testFileStructurePath_))\
            .build()
        self.archiverProvider_.backupFiles(backupDefinition)

        onBackupOperationErrorMock.assert_called_once_with(
            BackupSubOperations.Open, BackupOperationErrors.SocketIgnored, ArchiverTestUtils._SOCKET_NAME)



    def test_BackupCreationFileAddPropagation(self):
        """Tests the propagation of adding a filesystem object during backup creation.

        Creates a backup.  Asserts that the corresponding event was fired for each valid filesystem object."""

        self.testFileStructurePath_ = ArchiverTestUtils._makeTestFileStructure(
            socket = True, denied = True, links = True)

        onFileAddMock = Mock()
        self.archiverProvider_.fileAdd += onFileAddMock

        backupDefinition = _BackupDefinitionBuilder()\
            .withRoot(self.testFileStructurePath_)\
            .withIncludeFiles(os.listdir(self.testFileStructurePath_))\
            .build()
        self.archiverProvider_.backupFiles(backupDefinition)

        self.assertEqual(19, onFileAddMock.call_count)

    # }}} backup creation tests for events propagation



class TestInternalTarArchiverProvidersContent(_TestTarArchiverProvidersContent):
    """Tests of internal tar archiver provider for archive content."""

    def createTestSubject_(self):
        return _InternalTarArchiverProvider(ComponentTestUtils.getComponentTestContext().workDir)



class TestExternalTarArchiverProvidersContent(_TestTarArchiverProvidersContent):
    """Tests of external tar archiver provider for archive content."""

    def createTestSubject_(self):
        return _ExternalTarArchiverProvider(ComponentTestUtils.getComponentTestContext().workDir)



class TestInternalTarBackupRemoval(unittest.TestCase):
    """Tests of internal tar archiver provider for backup removal functionality."""

    @classmethod
    def setUpClass(cls):
        ArchiverTestUtils._setUpClassArchivingComponent()



    @classmethod
    def tearDownClass(cls):
        ArchiverTestUtils._tearDownClassArchivingComponent()



    def setUp(self):
        self.__archiverProvider = _InternalTarArchiverProvider(ComponentTestUtils.getComponentTestContext().workDir)



    def test_RemoveBackup(self):
        """Tests the removal of a backup."""

        backupDefinition = _BackupDefinitionBuilder().build()
        backupFilePath = self.__archiverProvider.backupFiles(backupDefinition)

        self.__archiverProvider.removeBackup(backupDefinition)

        self.assertFalse(os.path.isfile(backupFilePath), "The backup file was not removed.")



class TestExternalTarBackupRemoval(unittest.TestCase):
    """Tests of external tar archiver provider for backup removal functionality."""

    __SNAPSHOTS_SUBDIR = "snapshots"



    @classmethod
    def setUpClass(cls):
        ArchiverTestUtils._setUpClassArchivingComponent()



    @classmethod
    def tearDownClass(cls):
        ArchiverTestUtils._tearDownClassArchivingComponent()



    def setUp(self):
        self.__snapshotsDir = None
        self.__archiverProvider = None

        self.__snapshotsDir = os.path.join(
            ComponentTestUtils.getComponentTestContext().workDir, self.__SNAPSHOTS_SUBDIR)
        os.mkdir(self.__snapshotsDir)
        self.__archiverProvider = _ExternalTarArchiverProvider(ComponentTestUtils.getComponentTestContext().workDir)



    def tearDown(self):
        shutil.rmtree(self.__snapshotsDir)



    def test_RemoveBackup(self):
        """Tests the removal of a non-incremental backup."""

        backupDefinition = _BackupDefinitionBuilder().build()
        backupFilePath = self.__archiverProvider.backupFiles(backupDefinition)

        self.__archiverProvider.removeBackup(backupDefinition)

        self.assertFalse(os.path.isfile(backupFilePath), "The backup file was not removed.")



    def test_removeBackupIncrements(self):
        """Tests the removal of backup levels of an incremental backup.

        Creates incremental backups of level 0 and level 1.  Removes the level 1 backup.  Asserts that level 1 backup
        was removed and the level 0 remained."""

        backupDefinition = _BackupDefinitionBuilder().build()

        # create the level 0 and level 1 backups
        backupFilePath0 = self.__archiverProvider.backupFilesIncrementally(backupDefinition)
        backupFilePath1 = self.__archiverProvider.backupFilesIncrementally(backupDefinition, level = 1)

        self.__archiverProvider.removeBackupIncrements(backupDefinition, level = 1)

        self.assertFalse(os.path.exists(backupFilePath1), "The backup file was not removed.")
        self.assertTrue(os.path.exists(backupFilePath0), "The backup file was removed.")



    def test_removeBackupIncrements_SetBackupLevel(self):
        """Tests that obsolete backup levels are being removed.

        Creates incremental backups of level 0 and level 1.  Removes the level 1 backup.  Asserts that the next level
        that would be created is level 1."""

        backupDefinition = _BackupDefinitionBuilder().build()

        # create the level 0 and level 1 backups
        self.__archiverProvider.backupFilesIncrementally(backupDefinition)
        self.__archiverProvider.backupFilesIncrementally(backupDefinition, level = 1)

        self.__archiverProvider.removeBackupIncrements(backupDefinition, level = 1)

        self.assertEqual(1, self.__archiverProvider.getMaxBackupLevel(backupDefinition.backupId))



class TestExternalTarArchiverProvidersIncremental(unittest.TestCase):
    """Tests of external tar archiver provider for incremental backups."""

    __SNAPSHOTS_SUBDIR = "snapshots"



    @classmethod
    def setUpClass(cls):
        ArchiverTestUtils._setUpClassArchivingComponent()



    @classmethod
    def tearDownClass(cls):
        ArchiverTestUtils._tearDownClassArchivingComponent()



    def setUp(self):
        self.__archiverProvider = None
        self.__testFileStructurePath = None
        self.__extractPath = None
        self.__snapshotsDir = None

        self.__snapshotsDir = os.path.join(
            ComponentTestUtils.getComponentTestContext().workDir, self.__SNAPSHOTS_SUBDIR)
        os.mkdir(self.__snapshotsDir)
        self.__archiverProvider = _ExternalTarArchiverProvider(ComponentTestUtils.getComponentTestContext().workDir)



    def tearDown(self):
        if self.__extractPath:
            ArchiverTestUtils._removeExtractedBackup(self.__extractPath)
        for irrelevantFile in glob.glob(ArchiverTestUtils._irrelevantValidFilePath + "*"):
            os.remove(irrelevantFile)
        if self.__testFileStructurePath:
            ArchiverTestUtils._removeTestFileStructure(self.__testFileStructurePath)

        shutil.rmtree(self.__snapshotsDir)



    # {{{ incremental backup creation tests

    def test_backupFilesIncrementally_Level0(self):
        """Tests the creation of an incremental backup of level 0.

        Creates an incremental backup and extracts it.  Asserts that the backup content is identical to the archived
        file structure."""

        self.__testFileStructurePath = ArchiverTestUtils._makeTestFileStructure()

        backupDefinition = _BackupDefinitionBuilder()\
            .withRoot(self.__testFileStructurePath)\
            .withIncludeFiles(os.listdir(self.__testFileStructurePath))\
            .build()
        backupFilePath = self.__archiverProvider.backupFilesIncrementally(backupDefinition)

        self.__extractPath = ArchiverTestUtils._extractBackup(backupFilePath)
        self.assertTrue(ArchiverTestUtils._compareDirs(self.__testFileStructurePath, self.__extractPath))



    def test_backupFilesIncrementally_LinksLevel0(self):
        """Tests the creation of an incremental backup of level 0 with file structure containing symlinks.

        Creates an incremental backup and extracts it.  Asserts that the backup content is identical to the archived
        file structure."""

        self.__testFileStructurePath = ArchiverTestUtils._makeTestFileStructure(links = True)

        backupDefinition = _BackupDefinitionBuilder()\
            .withRoot(self.__testFileStructurePath)\
            .withIncludeFiles(os.listdir(self.__testFileStructurePath))\
            .build()
        backupFilePath = self.__archiverProvider.backupFilesIncrementally(backupDefinition)

        self.__extractPath = ArchiverTestUtils._extractBackup(backupFilePath)
        self.assertTrue(ArchiverTestUtils._compareDirs(self.__testFileStructurePath, self.__extractPath))



    def test_backupFilesIncrementally_Level1(self):
        """Tests the creation of an incremental backup of level 1.

        Creates an incremental backup of level 0, modifies the test file structure and creates level 1 backup.  Extracts
        it and asserts that the backup content is identical to the archived file structure."""

        self.__testFileStructurePath = ArchiverTestUtils._makeTestFileStructure()

        backupDefinition = _BackupDefinitionBuilder()\
            .withRoot(self.__testFileStructurePath)\
            .withIncludeFiles(os.listdir(self.__testFileStructurePath))\
            .build()

        # create the level 0 backup
        backupFilePath0 = self.__archiverProvider.backupFilesIncrementally(backupDefinition)

        # rest a little so that file modifications has significantly different time stamps
        time.sleep(1.2)

        # modify the test file structure
        # TODO: Temporally disable the remove modification because of GNU tar bug.
#        os.remove(os.path.join(self.__testFileStructurePath, str.format(ArchiverTestUtils._DIR_NAME, index = 0),
#                               str.format(ArchiverTestUtils._FILE_NAME, index = 1)))
        with open(os.path.join(self.__testFileStructurePath, str.format(ArchiverTestUtils._DIR_NAME, index = 1),
                               "incremental.t"), "w") as testFile:
            testFile.write("Content of the incremental test file.")
        with open(os.path.join(self.__testFileStructurePath, str.format(ArchiverTestUtils._DIR_NAME, index = 1),
                               str.format(ArchiverTestUtils._FILE_NAME, index = 1)), "a") as testFile:
            testFile.write("Additional content of the file for incremental test.")

        # create the level 1 backup
        backupFilePath1 = self.__archiverProvider.backupFilesIncrementally(backupDefinition, level = 1)

        self.assertLess(os.path.getsize(backupFilePath1), os.path.getsize(backupFilePath0))
        self.__extractPath = ArchiverTestUtils._extractBackup((backupFilePath0, backupFilePath1))
        self.assertTrue(ArchiverTestUtils._compareDirs(self.__testFileStructurePath, self.__extractPath))



    def test_backupFilesIncrementally_SpecifiedLevel(self):
        """Tests the creation of an incremental backup of a specified backup level.

        Creates an incremental backup of level 0, modifies the test file structure and creates level 1 backup.  Modifies
        the test file structure again and creates level 1 backup again.  Extracts first and last increments and asserts
        that the backup content is identical to the archived file structure."""

        self.__testFileStructurePath = ArchiverTestUtils._makeTestFileStructure()

        backupDefinition = _BackupDefinitionBuilder()\
            .withRoot(self.__testFileStructurePath)\
            .withIncludeFiles(os.listdir(self.__testFileStructurePath))\
            .build()

        # create the level 0 backup
        backupFilePath0 = self.__archiverProvider.backupFilesIncrementally(backupDefinition)

        # rest a little so that file modifications has significantly different time stamps
        time.sleep(1.2)

        # modify the test file structure
        with open(os.path.join(self.__testFileStructurePath, str.format(ArchiverTestUtils._DIR_NAME, index = 1),
                               "incremental.t"), "w") as testFile:
            testFile.write("Content of the incremental test file.")

        # create the level 1 backup
        self.__archiverProvider.backupFilesIncrementally(backupDefinition, level = 1)

        time.sleep(1.2)

        # modify the test file structure again
        with open(os.path.join(self.__testFileStructurePath, str.format(ArchiverTestUtils._DIR_NAME, index = 1),
                               "incremental2.t"), "w") as testFile:
            testFile.write("Content of the incremental2 test file.")

        # create the level 1 backup again
        backupFilePath1 = self.__archiverProvider.backupFilesIncrementally(backupDefinition, level = 1)

        self.__extractPath = ArchiverTestUtils._extractBackup((backupFilePath0, backupFilePath1))
        self.assertTrue(ArchiverTestUtils._compareDirs(self.__testFileStructurePath, self.__extractPath))

    # }}} incremental backup creation tests



    # {{{ getMaxBackupLevel() tests

    def test_getMaxBackupLevel(self):
        """Tests the obtaining the maximal backup level."""

        TEST_BACKUP_ID = "test backup ID"

        self.__testFileStructurePath = ArchiverTestUtils._makeTestFileStructure()

        backupDefinition = _BackupDefinitionBuilder()\
            .withBackupId(TEST_BACKUP_ID)\
            .withRoot(self.__testFileStructurePath)\
            .withIncludeFiles(os.listdir(self.__testFileStructurePath))\
            .build()
        self.__archiverProvider.backupFilesIncrementally(backupDefinition)

        maxBackupLevel = self.__archiverProvider.getMaxBackupLevel(TEST_BACKUP_ID)

        self.assertEqual(1, maxBackupLevel)



    def test_getMaxBackupLevel_NoBackupYet(self):
        """Tests the obtaining the maximal backup level when no backup was created yet."""

        maxBackupLevel = self.__archiverProvider.getMaxBackupLevel(ArchiverTestUtils._IRRELEVANT_BACKUP_ID)

        self.assertEqual(0, maxBackupLevel)



    def test_getMaxBackupLevel_NameClash(self):
        """Tests the :meth:`IArchiver.getMaxBackupLevel()` for similar backup IDs.

        Creates two incremental :term:`backups <backup>` so snapshot files are stored for them.  Backup IDs are
        deliberately chosen to be similar (one ID is a substring of the other).  Created number of backup levels of the
        archive with shorter ID will be lower than of the other.  As the shorter name substring matches also the longer
        name, this tests the possibility of incorrect file name matching while determining the backup level by counting
        the snapshot files.  Checks that the reported maximal backup level of the archive with shorter name is
        correct."""

        BACKUP_ID_1 = "test_backup"
        BACKUP_ID_2 = BACKUP_ID_1 + "_2"

        self.__testFileStructurePath = ArchiverTestUtils._makeTestFileStructure()

        # creates the level 0 backup for BACKUP_ID_1
        backupDefinition = _BackupDefinitionBuilder()\
            .withBackupId(BACKUP_ID_1)\
            .withRoot(self.__testFileStructurePath)\
            .withIncludeFiles(os.listdir(self.__testFileStructurePath))\
            .build()
        self.__archiverProvider.backupFilesIncrementally(backupDefinition)

        # creates levels 0 and 1 backups for BACKUP_ID_2
        backupDefinition = _BackupDefinitionBuilder()\
            .withBackupId(BACKUP_ID_2)\
            .withRoot(self.__testFileStructurePath)\
            .withIncludeFiles(os.listdir(self.__testFileStructurePath))\
            .build()
        self.__archiverProvider.backupFilesIncrementally(backupDefinition)
        self.__archiverProvider.backupFilesIncrementally(backupDefinition, level = 1)

        maxBackupLevel = self.__archiverProvider.getMaxBackupLevel(BACKUP_ID_1)

        self.assertEqual(1, maxBackupLevel)

    # }}} getMaxBackupLevel() tests



    # {{{ getStoredBackupIds() tests

    def test_getStoredBackupIds(self):
        """Tests the obtaining backup IDs of all known backups."""

        TEST_BACKUP_IDS = ("test backup 1", "test backup 2", "test backup 3")

        self.__testFileStructurePath = ArchiverTestUtils._makeTestFileStructure()

        backupDefinitionBuilderWithFiles = _BackupDefinitionBuilder()\
            .withRoot(self.__testFileStructurePath)\
            .withIncludeFiles(os.listdir(self.__testFileStructurePath))

        for backupId in TEST_BACKUP_IDS:
            backupDefinition = backupDefinitionBuilderWithFiles\
                .withBackupId(backupId)\
                .build()
            self.__archiverProvider.backupFilesIncrementally(backupDefinition)

        # create also level 1 of one of the backups
        backupDefinition = backupDefinitionBuilderWithFiles\
            .withBackupId(TEST_BACKUP_IDS[1])\
            .build()
        self.__archiverProvider.backupFilesIncrementally(backupDefinition, level = 1)

        storedBackupIds = self.__archiverProvider.getStoredBackupIds()

        self.assertCountEqual(TEST_BACKUP_IDS, storedBackupIds)

    # }}} getStoredBackupIds() tests

# }}} CLASSES

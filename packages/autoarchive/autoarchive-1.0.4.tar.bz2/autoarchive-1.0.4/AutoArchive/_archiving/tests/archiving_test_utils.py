# archiving_test_utils.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2015 Róbert Čerňanský



""":class:`ArchivingTestUtils` class."""



__all__ = ["ArchivingTestUtils"]



# {{{ INCLUDES

import mock

from abc import *
import os
import tempfile
import shutil

from ..._py_additions import *
from ..._services import *
from ..._mainf import *
from ..._configuration import *
from .. import *
from .._core import ArchivingComponent

from ...tests import *
from ..._mainf.tests import MainfTestUtils
from ..._configuration.tests import ConfigurationTestUtils

# }}} INCLUDES



# {{{ CLASSES

class ArchivingTestUtils(metaclass = ABCMeta):
    """Utility methods for Archiving component tests."""

    _ARCHIVER_TYPE_TO_BACKUP_TYPE_MAP = {ArchiverTypes.Tar: BackupTypes.Tar,
                                         ArchiverTypes.TarGz: BackupTypes.TarGz,
                                         ArchiverTypes.TarBz2: BackupTypes.TarBz2,
                                         ArchiverTypes.TarXz: BackupTypes.TarXz,
                                         ArchiverTypes.TarInternal: BackupTypes.Tar,
                                         ArchiverTypes.TarGzInternal: BackupTypes.TarGz,
                                         ArchiverTypes.TarBz2Internal: BackupTypes.TarBz2}

    _IRRELEVANT_SET_OF_FEATURES = frozenset()

    # archive name patter in archive specification file
    __NAME_VARIABLE_PATTERN = "name = "



    @abstractmethod
    def __init__(self):
        pass



    # SMELL: Should go to ConfigurationTestUtils.
    @staticmethod
    def makeArchiveSpecsDirectory():
        """Creates the arch. spec. files directory and stores its path in the :class:`.ComponentTestContext` instance.

        :raise RuntimeError: If the user configuration directory was already created, i. e. the
           :attr:`.ComponentTestContext.userConfigDir` is not ``None``."""

        if ComponentTestUtils.getComponentTestContext().archiveSpecsDir is not None:
            raise RuntimeError("Archive specification files directory already created.")

        ComponentTestUtils.getComponentTestContext().archiveSpecsDir = tempfile.mkdtemp(
            prefix = "archive_specs_test", dir = ComponentTestUtils.getComponentTestContext().workDir)



    # SMELL: Should go to ConfigurationTestUtils.
    @staticmethod
    def removeArchiveSpecsDirectory():
        """Removes the arch. spec. files directory and its path from the :class:`.ComponentTestContext` instance."""

        shutil.rmtree(ComponentTestUtils.getComponentTestContext().archiveSpecsDir)
        ComponentTestUtils.getComponentTestContext().archiveSpecsDir = None



    @staticmethod
    def createMockArchiving(configuredArchiveNames = None, storedArchiveNames = None):
        """Creates mock of the :class:`.IArchiving` interface.

        .. note:: Methods that returns :class:`.ArchiveInfo` populates only its :attr:`.ArchiveInfo.name` property (as
           ``os.path.basename(archiveSpecFilePath)`` stripping its ``.aa`` extension).

        :param configuredArchiveNames: Iterable of archive names that shall be considered as :term:`configured`.  If
            ``None`` then each archive is considered as configured.  This affects methods
            :meth:`.IArchiving.filterValidSpecFiles()` and :meth:`.IArchiving.getArchiveInfo()`.
        :type configuredArchiveNames: ``Iterable<str>``
        :param storedArchiveNames: Iterable of archive names that shall be returned by
            :meth:`.IArchiving.getStoredArchiveNames()`.
        :type storedArchiveNames: ``Iterable<str>``

        :return: Mock of the :class:`.IArchiving`.
        :rtype: :class:`mock.Mock<IArchiving>`"""

        class _ArchiveInfo(ArchiveInfo):
            def __init__(self, name):
                super().__init__(name)



        def filterValidSpecFilesSideEffect(specFiles):
            return (name for name in (getArchiveName(sf) for sf in specFiles) if isConfigured(name))



        def getArchiveInfoSideEffect(specFile):
            archiveName = getArchiveName(specFile)
            return _ArchiveInfo(archiveName) if isConfigured(archiveName) else None



        def getStoredArchiveInfoSideEffect(archiveName):
            return _ArchiveInfo(archiveName)



        def getArchiveName(specFile):
            return os.path.basename(specFile).replace(ConfigConstants.ARCHIVE_SPEC_EXT, "")



        def isConfigured(archiveName):
            return configuredArchiveNames is None or archiveName in configuredArchiveNames



        if storedArchiveNames is None:
            storedArchiveNames = ()

        mockArchiving = mock.Mock(spec_set = IArchiving)
        mockArchiving.filterValidSpecFiles.side_effect = filterValidSpecFilesSideEffect
        mockArchiving.getArchiveInfo.side_effect = getArchiveInfoSideEffect
        mockArchiving.getStoredArchiveInfo.side_effect = getStoredArchiveInfoSideEffect
        mockArchiving.getStoredArchiveNames.return_value = storedArchiveNames

        return mockArchiving



    @classmethod
    def _setUpClassArchivingComponent(cls):
        ComponentTestUtils.setUpClassComponent()



    @classmethod
    def _tearDownClassArchivingComponent(cls):
        ComponentTestUtils.tearDownClassComponent()



    @classmethod
    def _setUpArchivingComponent(cls):
        ConfigurationTestUtils.makeUserConfigDirectory()
        cls.makeArchiveSpecsDirectory()



    @classmethod
    def _tearDownArchivingComponent(cls):
        ServiceCleaner.cleanServices()
        cls.removeArchiveSpecsDirectory()
        ConfigurationTestUtils.removeUserConfigDirectory()
        ComponentTestUtils.checkWorkDirEmptiness()



    @staticmethod
    def _setUpArchiverServices(archiverMock, errorOccur = False, supportedFeatures = _IRRELEVANT_SET_OF_FEATURES):
        """Sets up Archiver service layer with the passed ``archiverMock``.

        Creates ArchiverServiceCreator mock and performs basic set up on it and also on ``archiverMock``.

        :param archiverMock: Archiver service provider mock that shall be returned by ArchiverServiceCreator.
        :type archiverMock: :class:`mock.Mock<IArchiver>`
        :param errorOccur: ``True`` if the backup creation shall emit an error.
        :type errorOccur: ``bool``
        :param supportedFeatures: Set of features that ``archiverMock`` shall support.
        :type supportedFeatures: ``Set<ArchiverFeatures>``

        :return: New ArchiverServiceCreator mock instance.
        :rtype: :class:`mock.Mock<ArchiverServiceCreator>`"""

        IRRELEVANT_BACKUP_SUB_OPERATION = BackupSubOperations.Unknown
        backupFilesOriginalSideEffect = archiverMock.backupFiles.side_effect

        @event
        def backupOperationErrorEventMock(operation, error, filesystemObjectName = None, unknownErrorString = None):
            pass

        def backupFilesSideEffect(backupDefinition, compressionStrength = None):
            backupOperationErrorEventMock(IRRELEVANT_BACKUP_SUB_OPERATION, BackupOperationErrors.UnknownError)
            return backupFilesOriginalSideEffect(backupDefinition, compressionStrength)

        archiverMock.getSupportedFeatures.return_value = supportedFeatures

        archiverMock.backupOperationError = backupOperationErrorEventMock
        if errorOccur:
            archiverMock.backupFiles.side_effect = backupFilesSideEffect

        archiverServiceCreatorMock = mock.Mock(spec_set = ArchiverServiceCreator)
        archiverServiceCreatorMock.getOrCreateArchiverService.return_value = archiverMock
        archiverServiceCreatorMock.getSupportedFeatures.return_value = supportedFeatures

        return archiverServiceCreatorMock



    @staticmethod
    def _setUpMockInterfaceAccessor(mockAppConfig = None, storageState = None, mockInterfaceAccessor = None):
        """Creates and sets up :class:`IInterfaceAccessor` mock.

        :param mockAppConfig: :class:`IAppConfig` instance that shall be registered to :class:`IInterfaceAccessor` mock.
            If not passed, a new :class:`IAppConfig` mock will be created that does not contains any configuration
            variables.
        :type mockAppConfig: :class:`IAppConfig`
        :param storageState: A mutable instance that serves as the storage place for :class:`.IStorage` mock.
        :type storageState: ``dict<str: dict<str: dict<str: object>>>``
        :param: mockInterfaceAccessor: Mock of :class:`.IInterfaceAccessor`.  A new one will be created if not passed.
        :type mockInterfaceAccessor: :class:`mock.Mock<IInterfaceAccessor>`

        :return: Mock of :class:`IInterfaceAccessor`.  If ``mockInterfaceAccessor`` was passed then the same instance is
            returned.
        :rtype: :class:`mock.Mock<IInterfaceAccessor>`"""

        if storageState is None:
            storageState = {}

        if not mockInterfaceAccessor:
            mockInterfaceAccessor = MainfTestUtils.createMockInterfaceAccessor({})

        if not mockAppConfig:
            mockAppConfig = ConfigurationTestUtils.createMockAppConfig()
        mockInterfaceAccessor.registerComponentInterface(IAppConfig, mockAppConfig)

        mockStorage = ConfigurationTestUtils.createMockStorage(storageState)
        mockInterfaceAccessor.registerComponentInterface(IStorage, mockStorage)

        mockComponentUi = mock.Mock(spec_set = IComponentUi)
        mockInterfaceAccessor.registerComponentInterface(IComponentUi, mockComponentUi)

        return mockInterfaceAccessor



    @classmethod
    def _makeArchiveSpecFile(cls, name = None, path = None, includeFiles = "*", excludeFiles = "",
                             archiver = ArchiverTypes.TarGzInternal, destDir = None):
        "Creates an archive specification file."

        workDir = ComponentTestUtils.getComponentTestContext().workDir

        content = str.format("""\
[Content]
{}
path = {}
include-files = {}
exclude-files = {}
[Archive]
archiver = {}
dest-dir = {}
""", cls.__NAME_VARIABLE_PATTERN + name if name else "", path or workDir, includeFiles, excludeFiles,
                             OptionsUtils.archiverTypeToStr(archiver), destDir or workDir)

        archiveSpecFileFd, archiveSpecFilePath = tempfile.mkstemp(
            dir = ComponentTestUtils.getComponentTestContext().archiveSpecsDir)
        with open(archiveSpecFileFd, "w") as archiveSpecFile:
            archiveSpecFile.write(content)
        return archiveSpecFilePath



    @classmethod
    def _createIrrelevantFile(cls):
        """Creates a file and return the path to it.

        :return: Path to the created file.
        :rtype: ``str``."""

        filePath = cls.__irrelevantValidFilePath
        open(filePath, "w").close()
        return filePath



    @classmethod
    def _removeIrrelevantFile(cls):
        """Removes the file created by the :meth:`_createIrrelevantFile()`."""

        os.remove(cls.__irrelevantValidFilePath)



    @classmethod
    def _createBackup(cls, archiverMock, options = None, archiverType = ArchiverTypes.TarGzInternal,
                      errorOccur = False, interfaceAccessorMock = None):
        """Performs non-incremental backup creation with Archiver service replaced by mocks.

        Backup creation will be called with ``archiverMock`` used as the archiver service provider.  An
        :term:`archive specification file` with option ``archiver`` will be created and used for the backup creation.

        :param archiverMock: Archiver service provider mock that shall be used to perform the backup creation.
        :type archiverMock: :class:`mock.Mock<IArchiver>`
        :param options: Configuration options dictionary.  Key is the :class:`Option` and value is its value.
        :type options: ``dict<Option: object>``
        :param archiverType: Type of an archiver that will be configured in :term:`archive specification file` as the
           one that shall be used for the backup creation.
        :type archiverType: :attr:`.ArchiverTypes`
        :param errorOccur: ``True`` if the backup creation shall emit an error.
        :type errorOccur: ``bool``
        :param interfaceAccessorMock: Uninitialized mock of the :class:`.IInterfaceAccessor`.
        :type interfaceAccessorMock: :class:`mock.Mock<IInterfaceAccessor>`"""

        cls.__createBackup(archiverMock, options = options,  errorOccur = errorOccur,
                           archiveSpecFile = (cls._makeArchiveSpecFile(archiver = archiverType)),
                           interfaceAccessorMock = interfaceAccessorMock)



    @classmethod
    def _createIncrementalBackup(cls, archiverMock, options = None, maxBackupLevel = 0, storageState = None,
                                 archiveSpecFile = None, interfaceAccessorMock = None):
        """Performs incremental backup creation with Archiver service replaced by mocks.

        :param archiverMock: Archiver service provider mock that shall be used to perform the backup creation.
        :type archiverMock: :class:`mock.Mock<IArchiver>`
        :param options: Configuration options dictionary.  Key is the :class:`Option` and value is its value.
        :type options: ``dict<Option: object>``
        :param maxBackupLevel: Maximal backup level that can be created.  This value is normally returned by Archiver
           service and will be set to the mock.
        :type maxBackupLevel: ``int``
        :param storageState: A mutable instance that serves as the storage place for :class:`.IStorage` mock.
        :type storageState: ``dict<str: dict<str: dict<str: object>>>``
        :param archiveSpecFile: Path to the `archive specification file`.
        :type archiveSpecFile: ``str``
        :param interfaceAccessorMock: An uninitialized :class:`.IInterfaceAccessor` mock.
        :type interfaceAccessorMock: :class:`mock.Mock<IInterfaceAccessor>`"""

        if options is None: options = {}

        jointOptions = {
            Options.INCREMENTAL: True,
        }
        jointOptions.update(options)

        cls.__createBackup(archiverMock, jointOptions, maxBackupLevel, storageState, archiveSpecFile = archiveSpecFile,
                           interfaceAccessorMock = interfaceAccessorMock)



    @classmethod
    def _createIncrementalBackups(cls, archiverMock, options = None, levels = 1, storageState = None,
                                  archiveSpecFile = None):
        """Performs multiple incremental backup creations with Archiver service replaced by mocks.

        :param archiverMock: Archiver service provider mock that shall be used to perform the backup creation.
        :type archiverMock: :class:`mock.Mock<IArchiver>`
        :param options: Configuration options dictionary.  Key is the :class:`Option` and value is its value.
        :type options: ``dict<Option: object>``
        :param levels: Number of backup levels which shall be created.  If less than 1 is specified, no backup will be
           created.  If it equals 1 then the backup level 0 will be created; if 2 then backup levels 0 and 1 will be
           created; etc.
        :type levels: ``int``
        :param storageState: A mutable instance that serves as the storage place for :class:`.IStorage` mock.
        :type storageState: ``dict<str: dict<str: dict<str: object>>>``
        :param archiveSpecFile: Path to the `archive specification file`.
        :type archiveSpecFile: ``str``"""

        if storageState is None: storageState = {}

        if archiveSpecFile is None:
            archiveSpecFile = cls._makeArchiveSpecFile()

        # create archives
        for level in range(levels):
            cls._createIncrementalBackup(archiverMock, options, level, storageState, archiveSpecFile = archiveSpecFile)



    @classmethod
    def __createBackup(cls, archiverMock, options = None, maxBackupLevel = 0, storageState = None,
                       errorOccur = False, archiveSpecFile = None, interfaceAccessorMock = None):
        if options is None: options = {}

        if storageState is None: storageState = {}

        if archiveSpecFile is None:
            archiveSpecFile = cls._makeArchiveSpecFile()

        # create IAppConfig mock
        jointOptions = {
            Options.USER_CONFIG_DIR: ComponentTestUtils.getComponentTestContext().userConfigDir,
        }
        jointOptions.update(options)
        mockAppConfig = ConfigurationTestUtils.createMockAppConfig(jointOptions)

        # call the backup creation
        archiverMock.getMaxBackupLevel.return_value = maxBackupLevel
        mockInterfaceAccessor = cls._setUpMockInterfaceAccessor(mockAppConfig, storageState, interfaceAccessorMock)
        ArchivingComponent(mockInterfaceAccessor)
        archiverServiceCreatorMock = cls._setUpArchiverServices(
            archiverMock, errorOccur, supportedFeatures = frozenset({ArchiverFeatures.Incremental}))
        archiving = mockInterfaceAccessor.getComponentInterface(IArchiving)
        with mock.patch("AutoArchive._archiving._core._archiver_manipulator.ArchiverServiceCreator",
                        archiverServiceCreatorMock):
            with mock.patch("AutoArchive._archiving._core._backup_information_provider.ArchiverServiceCreator",
                            archiverServiceCreatorMock):
                archiving.makeBackup(archiveSpecFile)



    @staticproperty
    def __irrelevantValidFilePath():
        """Gets a path to a file used if it is irrelevant.

        The returned file does not exists but its directory does.

        :rtype: ``str``."""

        return os.path.join(ComponentTestUtils.irrelevantDirectory, "irrelevant file name")

# }}} CLASSES

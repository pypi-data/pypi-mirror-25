# archiving_test_utils.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2017 Róbert Čerňanský



""":class:`ArchivingTestUtils` class."""



__all__ = ["ArchivingTestUtils"]



# {{{ INCLUDES

from abc import ABCMeta, abstractmethod

import mock

from AutoArchive._infrastructure.py_additions import event, staticproperty
from AutoArchive._infrastructure._application_context import ApplicationContext
from AutoArchive._infrastructure.configuration import Options, OptionsUtils, ArchiverTypes
from AutoArchive._services.external_command_executor import ExternalCommandExecutorServiceIdentification
from AutoArchive._services.external_command_executor._external_command_executor import ExternalCommandExecutor
from AutoArchive._services.archiver import BackupTypes, BackupSubOperations, BackupOperationErrors, ArchiverFeatures, \
    ArchiverServiceProviderIDs, ArchiverServiceIdentification
from AutoArchive._services.archiver._tar_archiver_provider_identification import _TarArchiverProviderIdentification
from AutoArchive._ui.cmdline._cmdline_ui import CmdlineUi
from .._command_executor import _CommandExecutor
from .._archiving import _Archiving
from AutoArchive.tests import ComponentTestUtils
from AutoArchive._infrastructure.service.tests import ServiceTestUtils
from AutoArchive._infrastructure.configuration.tests import ConfigurationTestUtils
from AutoArchive._infrastructure.storage.tests import StorageTestUtils
from AutoArchive._application.archiving.archive_spec.tests import ArchiveSpecTestUtils

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



    @abstractmethod
    def __init__(self):
        pass



    @classmethod
    def _setUpClassArchivingComponent(cls):
        ComponentTestUtils.setUpClassComponent()



    @classmethod
    def _tearDownClassArchivingComponent(cls):
        ComponentTestUtils.tearDownClassComponent()



    @classmethod
    def _setUpArchivingComponent(cls):
        ConfigurationTestUtils.makeUserConfigDirectory()
        ConfigurationTestUtils.makeArchiveSpecsDirectory()



    @classmethod
    def _tearDownArchivingComponent(cls):
        ConfigurationTestUtils.removeArchiveSpecsDirectory()
        ConfigurationTestUtils.removeUserConfigDirectory()
        ComponentTestUtils.checkWorkDirEmptiness()



    @classmethod
    def _setUpServiceAccessorMock(cls, serviceStorage = None, serviceAccessorMock = None):
        if serviceStorage is None:
            serviceStorage = {}

        if serviceAccessorMock is None:
            serviceAccessorMock = ServiceTestUtils.createServiceAccessorMock(serviceStorage)

        cls.__setUpExternalCommandExecutor(serviceAccessorMock)

        return serviceAccessorMock



    @staticmethod
    def _setUpArchiverServices(serviceAccessorMock, archiverMock, errorOccur = False,
                               supportedFeatures = _IRRELEVANT_SET_OF_FEATURES):
        """Sets up Archiver service layer with the passed ``archiverMock``.

        Creates ArchiverServiceCreator mock and performs basic set up on it and also on ``archiverMock``.

        :param archiverMock: Archiver service provider mock that shall be returned by ArchiverServiceCreator.
        :type archiverMock: :class:`mock.Mock<_TarArchiverProviderBase>`
        :param errorOccur: ``True`` if the backup creation shall emit an error.
        :type errorOccur: ``bool``
        :param supportedFeatures: Set of features that ``archiverMock`` shall support.
        :type supportedFeatures: ``Set<ArchiverFeatures>``"""

        IRRELEVANT_BACKUP_SUB_OPERATION = BackupSubOperations.Unknown
        backupFilesOriginalSideEffect = archiverMock.backupFiles.side_effect

        @event
        def backupOperationErrorEventMock(operation, error, filesystemObjectName = None, unknownErrorString = None):
            pass

        def backupFilesSideEffect(backupDefinition, compressionStrength = None, overwriteAtStart = False):
            backupOperationErrorEventMock(IRRELEVANT_BACKUP_SUB_OPERATION, BackupOperationErrors.UnknownError)
            return backupFilesOriginalSideEffect(backupDefinition, compressionStrength, overwriteAtStart)

        archiverMock.getSupportedFeatures.return_value = supportedFeatures

        archiverMock.backupOperationError = backupOperationErrorEventMock
        if errorOccur:
            archiverMock.backupFiles.side_effect = backupFilesSideEffect

        internalArchiverServiceProviderInfoMock = mock.Mock(spec_set = _TarArchiverProviderIdentification)
        internalArchiverServiceProviderInfoMock.getSupportedFeatures.return_value = supportedFeatures
        internalArchiverServiceProviderInfoMock.providerId = ArchiverServiceProviderIDs.TarInternal
        externalArchiverServiceProviderInfoMock = mock.Mock(spec_set = _TarArchiverProviderIdentification)
        externalArchiverServiceProviderInfoMock.getSupportedFeatures.return_value = supportedFeatures
        externalArchiverServiceProviderInfoMock.providerId = ArchiverServiceProviderIDs.TarExternal

        archiverProviderClassMock = mock.Mock()
        archiverProviderClassMock.return_value = archiverMock

        serviceAccessorMock.registerService(ArchiverServiceIdentification, archiverProviderClassMock,
                                            internalArchiverServiceProviderInfoMock)
        serviceAccessorMock.registerService(ArchiverServiceIdentification, archiverProviderClassMock,
                                            externalArchiverServiceProviderInfoMock)



    # SMELL: Move to Infrastructure?
    @staticmethod
    def _setUpApplicationContextMock(applicationContextMock = None, configurationMock = None, storage = None,
                                     storageState = None):
        """Creates and sets up :class:`.ApplicationContext` mock.

        :param: applicationContextMock: Mock of :class:`.ApplicationContext`.  A new one will be created if not passed.
        :type applicationContextMock: :class:`mock.Mock<ApplicationContext>`
        :param configurationMock: :class:`ConfigurationBase` instance that shall be passed to
           :class:`ApplicationContext` mock.  If not passed, a new mock will be created that does not contains any
           configuration variables.
        :type configurationMock: :class:`ConfigurationBase`
        :param storage: Application configuration.
        :type storage: :class:`.FileStorage`
        :param storageState: A mutable instance that serves as the storage place for :class:`.IStorage` mock.
        :type storageState: ``dict<str: dict<str: dict<str: object>>>``

        :return: Mock of :class:`.ApplicationContext`.  If ``mockInterfaceAccessor`` was passed then the same instance is
            returned.
        :rtype: :class:`mock.Mock<ApplicationContext>`"""

        if storageState is None:
            storageState = {}

        if applicationContextMock is None:
            applicationContextMock = mock.Mock(spec_set = ApplicationContext)

        applicationContextMock.configuration = ConfigurationTestUtils.createConfigurationMock() if \
            configurationMock is None else configurationMock
        applicationContextMock.storage = StorageTestUtils.createMockStorage(
            storageState) if storage is None else storage

        return applicationContextMock



    @classmethod
    def _createBackup(cls, archiverMock, options = None, archiverType = ArchiverTypes.TarGzInternal,
                      errorOccur = False, componentUiMock = None, serviceAccessorMock = None):
        """Performs non-incremental backup creation with Archiver service replaced by mocks.

        Backup creation will be called with ``archiverMock`` used as the archiver service provider.  An
        :term:`archive specification file` with option ``archiver`` will be created and used for the backup creation.

        :param archiverMock: Archiver service provider mock that shall be used to perform the backup creation.
        :type archiverMock: :class:`mock.Mock<_TarArchiverProviderBase>`
        :param options: Configuration options dictionary.  Key is the :class:`Option` and value is its value.
        :type options: ``dict<Option: object>``
        :param archiverType: Type of an archiver that will be configured in :term:`archive specification file` as the
           one that shall be used for the backup creation.
        :type archiverType: :attr:`.ArchiverTypes`
        :param errorOccur: ``True`` if the backup creation shall emit an error.
        :type errorOccur: ``bool``"""

        cls.__createBackup(archiverMock, options = options,  errorOccur = errorOccur,
                           archiveSpecFile = (ArchiveSpecTestUtils.makeArchiveSpecFile(archiver = archiverType)),
                           componentUiMock = componentUiMock, serviceAccessorMock = serviceAccessorMock)



    @classmethod
    def _createIncrementalBackup(cls, archiverMock, options = None, maxBackupLevel = 0, storageState = None,
                                 archiveSpecFile = None, componentUiMock = None):
        """Performs incremental backup creation with Archiver service replaced by mocks.

        :param archiverMock: Archiver service provider mock that shall be used to perform the backup creation.
        :type archiverMock: :class:`mock.Mock<_TarArchiverProviderBase>`
        :param options: Configuration options dictionary.  Key is the :class:`Option` and value is its value.
        :type options: ``dict<Option: object>``
        :param maxBackupLevel: Maximal backup level that can be created.  This value is normally returned by Archiver
           service and will be set to the mock.
        :type maxBackupLevel: ``int``
        :param storageState: A mutable instance that serves as the storage place for :class:`.IStorage` mock.
        :type storageState: ``dict<str: dict<str: dict<str: object>>>``
        :param archiveSpecFile: Path to the `archive specification file`.
        :type archiveSpecFile: ``str``"""

        if options is None: options = {}

        jointOptions = {
            Options.INCREMENTAL: True,
        }
        jointOptions.update(options)

        cls.__createBackup(archiverMock, jointOptions, maxBackupLevel, storageState, archiveSpecFile = archiveSpecFile,
                           componentUiMock = componentUiMock)



    @classmethod
    def _createIncrementalBackups(cls, archiverMock, options = None, levels = 1, storageState = None,
                                  archiveSpecFile = None):
        """Performs multiple incremental backup creations with Archiver service replaced by mocks.

        :param archiverMock: Archiver service provider mock that shall be used to perform the backup creation.
        :type archiverMock: :class:`mock.Mock<_TarArchiverProviderBase>`
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
            archiveSpecFile = ArchiveSpecTestUtils.makeArchiveSpecFile()

        # create archives
        for level in range(levels):
            cls._createIncrementalBackup(archiverMock, options, level, storageState, archiveSpecFile = archiveSpecFile)



    @classmethod
    def __createBackup(cls, archiverMock, options = None, maxBackupLevel = 0, storageState = None,
                       errorOccur = False, archiveSpecFile = None, componentUiMock = None, serviceAccessorMock = None):
        if options is None: options = {}

        if storageState is None: storageState = {}

        if archiveSpecFile is None:
            archiveSpecFile = ArchiveSpecTestUtils.makeArchiveSpecFile()

        # create configuration mock
        jointOptions = {
            Options.USER_CONFIG_DIR: ComponentTestUtils.getComponentTestContext().userConfigDir,
            Options.NUMBER_OF_OLD_BACKUPS: 3
        }
        jointOptions.update(options)
        configurationMock = ConfigurationTestUtils.createConfigurationMock(jointOptions)

        # create UI mock
        if componentUiMock is None:
            componentUiMock = mock.Mock(spec_set = CmdlineUi)

        # create component
        archiverMock.getMaxBackupLevel.return_value = maxBackupLevel
        applicationContextMock = cls._setUpApplicationContextMock(
            configurationMock = configurationMock, storageState = storageState)
        serviceAccessorMock = cls._setUpServiceAccessorMock(None, serviceAccessorMock)
        externalCommandExecutorMock = serviceAccessorMock.getOrCreateService(
            ExternalCommandExecutorServiceIdentification, None)
        cls._setUpArchiverServices(serviceAccessorMock, archiverMock, errorOccur,
                                   supportedFeatures = frozenset({ArchiverFeatures.Incremental}))
        commandExecutor = _CommandExecutor(configurationMock, externalCommandExecutorMock, componentUiMock)
        archiving = _Archiving(componentUiMock, applicationContextMock, serviceAccessorMock, commandExecutor)

        # call the backup creation
        archiving.makeBackup(archiveSpecFile)



    @staticmethod
    def __setUpExternalCommandExecutor(serviceAccessorMock):
        @event
        def commandMessageEventMock(command, message, isError):
            pass

        externalCommandExecutorMock = mock.Mock(spec_set = ExternalCommandExecutor)
        externalCommandExecutorMock.commandMessage = commandMessageEventMock

        externalCommandExecutorClassMock = mock.Mock()
        externalCommandExecutorClassMock.return_value = externalCommandExecutorMock
        serviceAccessorMock.registerService(ExternalCommandExecutorServiceIdentification,
                                            externalCommandExecutorClassMock)

# }}} CLASSES

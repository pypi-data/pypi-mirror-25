# archiving_component.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2012 Róbert Čerňanský



""":class:`ArchivingComponent` class."""



__all__ = ["ArchivingComponent"]



# {{{ INCLUDES

from ..._utils import *
from ..._mainf import *
from ..._configuration import *
from .. import *
from ._archiving_constants import *
from ._backup_information_provider import *
from ._archiver_manipulator import *
from ._archive_spec import *

# }}} INCLUDES



# {{{ CLASSES

class ArchivingComponent(IComponent, IArchiving):
    """Provides an interface for working with archives.

    During construction it registers itself as :class:`.IArchiving` component interface to ``interfaceAccessor``.

    Several methods of this class requires an :term:`archive specification file` as the input parameter (usually
    named ``specFile``).  This file should contain all information required to create the :term:`backup`.  Its format is
    defined by the standard :mod:`configparser` module.  It has to contain section ``[Content]`` and may contain
    section ``[Archive]``.  The ``[Content]`` section requires following options to be present: ``path``,
    ``include-files`` and ``exclude-files``.  Optionally, ``name`` can be present.  Options in the archive
    specification file has higher priority than those in the configuration."""



    def __init__(self, interfaceAccessor):
        self.__interfaceAccessor = interfaceAccessor

        # stores already created _ArchiveSpec instances; key is path to the archive specification file and the value
        # is the instance
        self.__archiveSpecs = {}

        self.__appConfig = interfaceAccessor.getComponentInterface(IAppConfig)
        self.__storage = interfaceAccessor.getComponentInterface(IStorage)

        self.__interfaceAccessor.registerComponentInterface(IArchiving, self)



    def run(self):
        "See: :meth:`.IComponent.run()`."

        return True



    # {{{ IArchiving implementation

    def makeBackup(self, specFile):
        """Creates the :term:`backup` based on ``specFile``.

        The result can be a file with a full backup or an incremental backup of some particular level.  This depends on
        the :term:`archive specification file` (``specFile``), the configuration (:class:`.IAppConfig`), previous
        operations with the ``specFile`` and the time.  Some of the properties of :class:`.ArchiveInfo` returned by the
        method :meth:`getArchiveInfo()` can be used to determine what the result will be.  The path and name of the
        created file will be assembled as follows:
        “<Options.DEST_DIR>/<archive_name>[.<backup_level>].<archiver_specific_extension>”.

        Method uses :class:`.IComponentUi` interface to report errors, warnings et al. to the user.

        .. warning:: This method utilizes the :term:`user configuration directory` so the option \
           :attr:`.Options.USER_CONFIG_DIR` has to point to an *existing* directory.

        See also: :meth:`.IArchiving.makeBackup()`."""

        archiveSpec = self.__getOrTryCreateArchiveSpec(specFile)
        if not archiveSpec:
            return

        try:
            archiverManipulator = _ArchiverManipulator(_BackupInformationProvider(
                archiveSpec, self.__interfaceAccessor), self.__interfaceAccessor)
            backupFilePath = archiverManipulator.createBackup()
            archiverManipulator.saveBackupLevelInfo(backupFilePath)
        except OSError as ex:
            componentUi = self.__interfaceAccessor.getComponentInterface(IComponentUi)
            componentUi.showError(str.format("Unable to create the backup: ", ex.args[0]))
        except RuntimeError as ex:
            componentUi = self.__interfaceAccessor.getComponentInterface(IComponentUi)
            componentUi.showError(str.format("Unable to create the backup: {}", ex))



    def filterValidSpecFiles(self, specFiles):
        "See: :meth:`.IArchiving.filterValidSpecFiles()`."

        def getOrTryCreateArchiveSpecSilently(specFile):
            try:
                return self.__getOrCreateArchiveSpec(specFile, True)
            except (IOError, LookupError, SyntaxError, KeyError, ValueError):
                return None



        archiveSpecs = (getOrTryCreateArchiveSpecSilently(archiveSpec)
                        for archiveSpec in specFiles)
        return (archiveSpec[_ArchiveSpecOptions.NAME]
                for archiveSpec in archiveSpecs
                if archiveSpec is not None)



    def getArchiveInfo(self, specFile):
        """See: :meth:`.IArchiving.getArchiveInfo()`

        .. warning:: This method utilizes the :term:`user configuration directory` so the option \
           :attr:`.Options.USER_CONFIG_DIR` has to point to an *existing* directory."""

        archiveSpec = self.__getOrTryCreateArchiveSpec(specFile)
        if not archiveSpec:
            return None

        storagePortion = self.__storage.createStoragePortion(realm = archiveSpec[_ArchiveSpecOptions.NAME])

        archiverManipulator = None
        try:
            backupInformationProvider = _BackupInformationProvider(archiveSpec, self.__interfaceAccessor)
            archiverManipulator = _ArchiverManipulator(backupInformationProvider, self.__interfaceAccessor)
        except OSError as ex:
            componentUi = self.__interfaceAccessor.getComponentInterface(IComponentUi)
            componentUi.showError(str.format("Unable to get some of the archive information: {}", ex.args[0]))
        except RuntimeError as ex:
            componentUi = self.__interfaceAccessor.getComponentInterface(IComponentUi)
            componentUi.showError(str.format("Unable to get archive information: {}", ex))
            return None

        # create and populate ArchiveInfo instance
        archiveInfo = self.__ArchiveInfo(archiveSpec[_ArchiveSpecOptions.NAME]) if archiverManipulator \
            else self.getStoredArchiveInfo(archiveSpec[_ArchiveSpecOptions.NAME])

        archiveInfo._path = archiveSpec[_ArchiveSpecOptions.PATH]
        archiveInfo._archiverType = archiveSpec[Options.ARCHIVER]
        archiveInfo._destDir = archiveSpec[Options.DEST_DIR]

        if archiverManipulator and archiverManipulator.isOptionSupported(Options.INCREMENTAL):
            archiveInfo._incremental = archiveSpec[Options.INCREMENTAL]

            archiveInfo._backupLevel = backupInformationProvider.currentBackupLevel

            archiveInfo._restarting = archiveSpec[Options.RESTARTING]

            archiveInfo._restartAfterLevel = archiveSpec[Options.RESTART_AFTER_LEVEL]

            if backupInformationProvider.nextBackupLevel == 0:
                if backupInformationProvider.restartReason is BackupLevelRestartReasons.RestartCountLimitReached or \
                   backupInformationProvider.restartReason is BackupLevelRestartReasons.LastFullRestartAgeLimitReached:
                    archiveInfo._nextBackupLevel = 0
                else:
                    archiveInfo._nextBackupLevel = None
            else:
                archiveInfo._nextBackupLevel = backupInformationProvider.nextBackupLevel
            archiveInfo._restartReason = backupInformationProvider.restartReason

            archiveInfo._restartLevel = backupInformationProvider.restartLevel

            if storagePortion.hasVariable(_RestartStorageVariables.RESTART_COUNT):
                archiveInfo._restartCount = int(storagePortion.getValue(
                    _RestartStorageVariables.RESTART_COUNT))

            archiveInfo._fullRestartAfterCount = archiveSpec[Options.FULL_RESTART_AFTER_COUNT]

            archiveInfo._lastRestart = backupInformationProvider.getLastRestartDate()

            archiveInfo._restartAfterAge = archiveSpec[Options.RESTART_AFTER_AGE]

            archiveInfo._lastFullRestart = backupInformationProvider.getLastFullRestartDate()

            archiveInfo._fullRestartAfterAge = archiveSpec[Options.FULL_RESTART_AFTER_AGE]

        return archiveInfo



    def getStoredArchiveInfo(self, archiveName):
        """See: :meth:`.IArchiving.getStoredArchiveInfo()`.

        .. warning:: This method utilizes the :term:`user configuration directory` so the option \
           :attr:`.Options.USER_CONFIG_DIR` has to point to an *existing* directory."""

        if archiveName not in self.getStoredArchiveNames():
            return None

        archiveInfo = self.__ArchiveInfo(archiveName)
        storagePortion = self.__storage.createStoragePortion(realm = archiveName)

        archiveInfo._archiverType = self.__appConfig[Options.ARCHIVER]
        archiveInfo._destDir = self.__appConfig[Options.DEST_DIR]

        try:
            archiveInfo._backupLevel = _BackupInformationProvider.getBackupLevelForBackup(
                archiveName, self.__appConfig[Options.USER_CONFIG_DIR])
        except OSError as ex:
            componentUi = self.__interfaceAccessor.getComponentInterface(IComponentUi)
            componentUi.showError(str.format("Unable to determine the backup level: {}", ex.args[0]))
        except RuntimeError as ex:
            componentUi = self.__interfaceAccessor.getComponentInterface(IComponentUi)
            componentUi.showError(str.format("Unable to determine the backup level: {}", ex))

        archiveInfo._incremental = \
            self.__appConfig[Options.INCREMENTAL] if archiveInfo.backupLevel is not None else None

        if archiveInfo.incremental is not None:
            archiveInfo._restartAfterLevel = self.__appConfig[Options.RESTART_AFTER_LEVEL]

            if storagePortion.hasVariable(_RestartStorageVariables.RESTART_COUNT):
                archiveInfo._restartCount = int(
                    storagePortion.getValue(_RestartStorageVariables.RESTART_COUNT))

            archiveInfo._fullRestartAfterCount = self.__appConfig[Options.FULL_RESTART_AFTER_COUNT]

            archiveInfo._lastRestart = _BackupInformationProvider.getRestartDate(
                _RestartStorageVariables.LAST_RESTART, storagePortion)

            archiveInfo._lastFullRestart = _BackupInformationProvider.getRestartDate(
                _RestartStorageVariables.LAST_FULL_RESTART, storagePortion)

        return archiveInfo



    def getStoredArchiveNames(self):
        """See: :meth:`.IArchiving.getStoredArchiveNames()`.

        .. warning:: This method utilizes the :term:`user configuration directory` so the option \
           :attr:`.Options.USER_CONFIG_DIR` has to point to an *existing* directory."""

        archiveNames = ()
        try:
            archiveNames = _BackupInformationProvider.getStoredArchiveNames(self.__appConfig[Options.USER_CONFIG_DIR],
                                                                            self.__storage)
        except RuntimeError as ex:
            componentUi = self.__interfaceAccessor.getComponentInterface(IComponentUi)
            componentUi.showError(str.format("Unable to get list of stored archive names: {}", ex))

        return archiveNames



    def purgeStoredArchiveData(self, archiveName):
        """See: :meth:`.IArchiving.purgeStoredArchiveData()`.

        .. warning:: This method utilizes the :term:`user configuration directory` so the option \
           :attr:`.Options.USER_CONFIG_DIR` has to point to an **existing** directory."""

        try:
            if not _ArchiverManipulator.tryPurgeStoredArchiveData(
                archiveName, self.__appConfig[Options.USER_CONFIG_DIR], self.__storage):

                raise KeyError(str.format("There is no data stored for an archive named \"{}\".", archiveName))
        except RuntimeError as ex:
            raise OSError(ex)

    # }}} IArchiving implementation



    def __getOrTryCreateArchiveSpec(self, specFile):
        componentUi = self.__interfaceAccessor.getComponentInterface(IComponentUi)
        try:
            return self.__getOrCreateArchiveSpec(specFile)
        except IOError:
            componentUi.showError(str.format("Unable to open archive specification file \"{}\".", specFile))
        except (LookupError, SyntaxError, KeyError, ValueError) as ex:
            componentUi.showError(ex)

        return None



    def __getOrCreateArchiveSpec(self, specFile, silently = False):
        if specFile in self.__archiveSpecs.keys():
            return self.__archiveSpecs[specFile]

        componentUi = self.__interfaceAccessor.getComponentInterface(IComponentUi)
        archiveSpec = _ArchiveSpec(specFile, self.__appConfig, componentUi if not silently else None)
        self.__archiveSpecs[specFile] = archiveSpec
        return archiveSpec



    class __ArchiveInfo(ArchiveInfo):
        def __init__(self, name):
            super().__init__(name)

# }}} CLASSES

# _archiving.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2017 Róbert Čerňanský



""":class:`_Archiving` class."""



__all__ = ["_Archiving"]



# {{{ INCLUDES

import os

from AutoArchive._infrastructure.configuration import Options
from AutoArchive._application.archiving.archive_spec import ArchiveSpec, ConfigConstants, ArchiveSpecInfo, \
    ArchiveSpecOptions
from ._archive_info import _ArchiveInfo, _BackupLevelRestartReasons
from ._archiver_manipulator import ArchiverManipulator
from ._archiving_constants import _RestartStorageVariables
from ._backup_information_provider import _BackupInformationProvider
from ._command_executor import _CommandExecutor

# }}} INCLUDES



# {{{ CLASSES

class _Archiving:
    """Provides means for working with archives.

    Several methods of this class requires an :term:`archive specification file` as the input parameter (usually
    named ``specFile``).  This file should contain all information required to create the :term:`backup`.  Its format is
    defined by the standard :mod:`configparser` module.  It has to contain section ``[Content]`` and may contain
    section ``[Archive]``.  The ``[Content]`` section requires following options to be present: ``path``,
    ``include-files`` and ``exclude-files``.  Optionally, ``name`` can be present.  Options in the archive
    specification file has higher priority than those in the configuration.

    :param componentUi: Access to user interface.
    :type componentUi: :class:`.CmdlineUi`
    :param applicationContext: Application context.
    :type applicationContext: :class:`.ApplicationContext`
    :param serviceAccessor: Access to services.
    :type serviceAccessor: :class:`.IServiceAccessor`
    :param commandExecutor: For executing commands before and after backup creation.
    :type commandExecutor: :class:`_CommandExecutor`"""

    def __init__(self, componentUi, applicationContext, serviceAccessor, commandExecutor):
        self.__componentUi = componentUi
        self.__serviceAccessor = serviceAccessor
        self.__commandExecutor = commandExecutor

        self.__configuration = applicationContext.configuration
        self.__storage = applicationContext.storage

        # stores already created ArchiveSpec instances; key is path to the archive specification file and the value
        # is the instance
        self.__archiveSpecs = {}



    def makeBackup(self, specFile):
        """Creates the :term:`backup` based on ``specFile``.

        The result can be a file with a full backup or an incremental backup of some particular level.  This depends on
        the :term:`archive specification file` (``specFile``), the configuration (:class:`.IConfiguration`), previous
        operations with the ``specFile`` and the time.  Some of the properties of :class:`._ArchiveInfo` returned by the
        method :meth:`getArchiveInfo()` can be used to determine what the result will be.  The path and name of the
        created file will be assembled as follows:
        “<Options.DEST_DIR>/<archive_name>[.<backup_level>].<archiver_specific_extension>”.

        Method uses :class:`.CmdlineUi`-like interface to report errors, warnings et al. to the user.

        .. warning:: This method utilizes the :term:`user configuration directory` so the option \
           :attr:`.Options.USER_CONFIG_DIR` has to point to an *existing* directory.

        :param specFile: Path to the :term:`archive specification file`.
        :type specFile: ``str``

        :raise ValueError: If the desired archiver type is not supported."""

        archiveSpec = self.__getOrTryCreateArchiveSpec(specFile)
        if not archiveSpec:
            return

        try:
            self.__commandExecutor.executeBeforeCommand(archiveSpec)
        except OSError as ex:
            self.__componentUi.showError(ex.args[0])
            return

        try:
            archiverManipulator = ArchiverManipulator(
                _BackupInformationProvider(archiveSpec, self.__componentUi, self.__storage, self.__serviceAccessor),
                self.__componentUi, self.__storage, self.__serviceAccessor)
            backupFilePath = archiverManipulator.createBackup()
            archiverManipulator.saveBackupLevelInfo(backupFilePath)
        except OSError as ex:
            self.__componentUi.showError(str.format("Unable to create the backup: {}", ex.args[0]))
        except RuntimeError as ex:
            self.__componentUi.showError(str.format("Unable to create the backup: {}", ex))

        try:
            self.__commandExecutor.executeAfterCommand(archiveSpec)
        except OSError as ex:
            self.__componentUi.showError(ex.args[0])



    def getArchiveSpecs(self):
        """Iterable of all known archive specification files.

        :return: Iterable of archive specification files information.
        :rtype: ``Iterable<ArchiveSpecInfo>``

        :raise RuntimeError: If list of archive specification can not be obtained."""

        archiveSpecsDir = self.__configuration[Options.ARCHIVE_SPECS_DIR]
        if os.path.isdir(archiveSpecsDir):
            specFiles = filter(lambda fname: os.path.splitext(fname)[1] == ConfigConstants.ARCHIVE_SPEC_EXT,
                               os.listdir(archiveSpecsDir))
            for specFile in specFiles:
                yield ArchiveSpecInfo(os.path.splitext(specFile)[0], os.path.join(archiveSpecsDir, specFile))
        else:
            raise RuntimeError(str.format("Archive specifications directory \"{}\" does not exists.", archiveSpecsDir))



    def filterValidSpecFiles(self, specFiles):
        """Returns names of :term:`configured archives <configured archive>` from valid only
        :term:`archive specification files <archive specification file>` passed in ``specFiles``.

        :param specFiles: Paths to archive specification files that shall be validated and from which the names
          shall be retrieved.
        :type specFiles: ``Iterable<str>``

        :return: Iterable of names of validly configured archives.
        :rtype: ``Iterable<str>``"""

        def getOrTryCreateArchiveSpecSilently(specFile):
            try:
                return self.__getOrCreateArchiveSpec(specFile, True)
            except (IOError, LookupError, SyntaxError, KeyError, ValueError):
                return None



        archiveSpecs = (getOrTryCreateArchiveSpecSilently(archiveSpec)
                        for archiveSpec in specFiles)
        return (archiveSpec[ArchiveSpecOptions.NAME]
                for archiveSpec in archiveSpecs
                if archiveSpec is not None)



    def getArchiveInfo(self, specFile):
        """Returns information about archive represented by the ``specFile`` parameter.

        .. warning:: This method utilizes the :term:`user configuration directory` so the option \
           :attr:`.Options.USER_CONFIG_DIR` has to point to an *existing* directory.

        :param specFile: Path to the :term:`archive specification file`.
        :type specFile: ``str``

        :return: Information about an archive or ``None``.
        :rtype: :class:`_ArchiveInfo`"""

        archiveSpec = self.__getOrTryCreateArchiveSpec(specFile)
        if not archiveSpec:
            return None

        storagePortion = self.__storage.createStoragePortion(realm = archiveSpec[ArchiveSpecOptions.NAME])

        archiverManipulator = None
        try:
            backupInformationProvider = _BackupInformationProvider(
                archiveSpec, self.__componentUi, self.__storage, self.__serviceAccessor)
            archiverManipulator = ArchiverManipulator(
                backupInformationProvider, self.__componentUi, self.__storage, self.__serviceAccessor)
        except OSError as ex:
            self.__componentUi.showError(str.format("Unable to get some of the archive information: {}", ex.args[0]))
        except RuntimeError as ex:
            self.__componentUi.showError(str.format("Unable to get archive information: {}", ex))
            return None

        # create and populate _ArchiveInfo instance
        archiveInfo = self.__ArchiveInfo(archiveSpec[ArchiveSpecOptions.NAME]) if archiverManipulator \
            else self.getStoredArchiveInfo(archiveSpec[ArchiveSpecOptions.NAME])

        archiveInfo._path = archiveSpec[ArchiveSpecOptions.PATH]
        archiveInfo._archiverType = archiveSpec[Options.ARCHIVER]
        archiveInfo._destDir = archiveSpec[Options.DEST_DIR]

        if archiverManipulator and archiverManipulator.isOptionSupported(Options.INCREMENTAL):
            archiveInfo._incremental = archiveSpec[Options.INCREMENTAL]

            archiveInfo._backupLevel = backupInformationProvider.currentBackupLevel

            archiveInfo._restarting = archiveSpec[Options.RESTARTING]

            archiveInfo._restartAfterLevel = archiveSpec[Options.RESTART_AFTER_LEVEL]

            if backupInformationProvider.nextBackupLevel == 0:
                if backupInformationProvider.restartReason is _BackupLevelRestartReasons.RestartCountLimitReached or \
                   backupInformationProvider.restartReason is _BackupLevelRestartReasons.LastFullRestartAgeLimitReached:
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
        """Returns information about an archive from stored data.

        Unlike in the :meth:`getArchiveInfo` method the information is not read from the
        :term:`archive specification file` but from other stored data about the archive created by the component in
        previous runs.  Such data can be fetched for example from application storage (:class:`.IStorage`) or other
        sources specific to the archiver.  It is expected that the large portion of data will be missing in the
        returned information.

        .. warning:: This method utilizes the :term:`user configuration directory` so the option \
           :attr:`.Options.USER_CONFIG_DIR` has to point to an *existing* directory.

        See also: :meth:`getStoredArchiveNames()`

        :param archiveName: Name of the archive which information shall be returned.
        :type archiveName: ``str``

        :return: Information about an archive or ``None`` if no data for the archive was found.
        :rtype: :class:`_ArchiveInfo`"""

        if archiveName not in self.getStoredArchiveNames():
            return None

        archiveInfo = self.__ArchiveInfo(archiveName)
        storagePortion = self.__storage.createStoragePortion(realm = archiveName)

        archiveInfo._archiverType = self.__configuration[Options.ARCHIVER]
        archiveInfo._destDir = self.__configuration[Options.DEST_DIR]

        try:
            archiveInfo._backupLevel = _BackupInformationProvider.getBackupLevelForBackup(
                archiveName, self.__configuration[Options.USER_CONFIG_DIR], self.__serviceAccessor)
        except OSError as ex:
            self.__componentUi.showError(str.format("Unable to determine the backup level: {}", ex.args[0]))
        except RuntimeError as ex:
            self.__componentUi.showError(str.format("Unable to determine the backup level: {}", ex))

        archiveInfo._incremental = \
            self.__configuration[Options.INCREMENTAL] if archiveInfo.backupLevel is not None else None

        if archiveInfo.incremental is not None:
            archiveInfo._restartAfterLevel = self.__configuration[Options.RESTART_AFTER_LEVEL]

            if storagePortion.hasVariable(_RestartStorageVariables.RESTART_COUNT):
                archiveInfo._restartCount = int(
                    storagePortion.getValue(_RestartStorageVariables.RESTART_COUNT))

            archiveInfo._fullRestartAfterCount = self.__configuration[Options.FULL_RESTART_AFTER_COUNT]

            archiveInfo._lastRestart = _BackupInformationProvider.getRestartDate(
                _RestartStorageVariables.LAST_RESTART, storagePortion)

            archiveInfo._lastFullRestart = _BackupInformationProvider.getRestartDate(
                _RestartStorageVariables.LAST_FULL_RESTART, storagePortion)

        return archiveInfo



    def getStoredArchiveNames(self):
        """Returns iterable of archive names which has some data stored in a persistent storage.

        .. warning:: This method utilizes the :term:`user configuration directory` so the option \
           :attr:`.Options.USER_CONFIG_DIR` has to point to an *existing* directory.

        See also: :meth:`getStoredArchiveInfo()`

        :return: Iterable of archive names.
        :rtype: ``Iterable<str>``"""

        archiveNames = ()
        try:
            archiveNames = _BackupInformationProvider.getStoredArchiveNames(
                self.__configuration[Options.USER_CONFIG_DIR], self.__storage, self.__serviceAccessor)
        except RuntimeError as ex:
            self.__componentUi.showError(str.format("Unable to get list of stored archive names: {}", ex))

        return archiveNames



    def purgeStoredArchiveData(self, archiveName):
        """Deletes all data stored for the archive named ``archiveName``.

        .. warning:: This method utilizes the :term:`user configuration directory` so the option \
           :attr:`.Options.USER_CONFIG_DIR` has to point to an **existing** directory.

        See also: :meth:`getStoredArchiveInfo()`

        :param archiveName: Name of the archive which data shall be purged.
        :type archiveName: ``str``

        :raise KeyError: If ``archiveName`` does not have any stored data to purge.
        :raise OSError: If an error occurred during the operation of removing data from a physical storage."""

        try:
            if not ArchiverManipulator.tryPurgeStoredArchiveData(
                archiveName, self.__configuration[Options.USER_CONFIG_DIR], self.__storage, self.__serviceAccessor):

                raise KeyError(str.format("There is no data stored for an archive named \"{}\".", archiveName))
        except RuntimeError as ex:
            raise OSError(ex)



    def __getOrTryCreateArchiveSpec(self, specFile):
        try:
            return self.__getOrCreateArchiveSpec(specFile)
        except OSError as ex:
            self.__componentUi.showError(str.format("Unable to open archive specification file \"{}\".", ex.filename))
        except (LookupError, SyntaxError, KeyError, ValueError) as ex:
            self.__componentUi.showError(ex)

        return None



    def __getOrCreateArchiveSpec(self, specFile, silently = False):
        if specFile in self.__archiveSpecs.keys():
            return self.__archiveSpecs[specFile]

        archiveSpec = ArchiveSpec(specFile, self.__configuration, self.__componentUi if not silently else None)
        self.__archiveSpecs[specFile] = archiveSpec
        return archiveSpec



    class __ArchiveInfo(_ArchiveInfo):
        def __init__(self, name):
            super().__init__(name)

# }}} CLASSES

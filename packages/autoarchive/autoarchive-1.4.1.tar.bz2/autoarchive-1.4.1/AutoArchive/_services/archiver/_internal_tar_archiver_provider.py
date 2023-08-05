# _internal_tar_archiver_provider.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2016 Róbert Čerňanský



""":class:`_InternalTarArchiverProvider` class."""



__all__ = ["_InternalTarArchiverProvider"]



# {{{ INCLUDES

import os
import stat
import shutil
import itertools
import errno
import tarfile

from AutoArchive._infrastructure.py_additions import staticproperty
from . import BackupSubOperations, BackupOperationErrors
from ._tar_archiver_provider_base import _TarArchiverProviderBase, BackupTypes

# }}} INCLUDES



# {{{ CLASSES

class _InternalTarArchiverProvider(_TarArchiverProviderBase):
    """Internal archiver service provider.

    See also: :class:`._TarArchiverProviderBase`."""

    # backup type to tarfile compress token map
    __BACKUP_TYPE_TO_COMPRESS_TOKEN = {BackupTypes.Tar: "",
                                       BackupTypes.TarGz: "gz",
                                       BackupTypes.TarBz2: "bz2"}



    # {{{ _TarArchiverProviderBase overrides

    def __init__(self, workDir):
        super().__init__(workDir)

        self.__someFilesChanged = None



    @staticproperty
    def supportedBackupTypes():
        "See :attr:`._TarArchiverProviderBase.supportedBackupTypes`"

        return frozenset({BackupTypes.Tar,
                          BackupTypes.TarGz,
                          BackupTypes.TarBz2})



    def backupFiles(self, backupDefinition, compressionStrength = None, overwriteAtStart = False):
        "See: :meth:`._TarArchiverProviderBase.backupFiles()`."

        super().backupFiles(backupDefinition, compressionStrength, overwriteAtStart)

        backupFilePath = self.getBackupFilePath_(backupDefinition.backupId, backupDefinition.backupType,
                                                 backupDefinition.destination)
        workingBackupFilePath = backupFilePath if overwriteAtStart else self.getWorkingPath_(backupFilePath)

        self.__someFilesChanged = False

        openModeCompressionToken = self.__BACKUP_TYPE_TO_COMPRESS_TOKEN[backupDefinition.backupType]
        tarFile = tarfile.open(workingBackupFilePath, "w:" + openModeCompressionToken, format = tarfile.PAX_FORMAT)

        try:
            cwdSave = os.getcwd()
            os.chdir(backupDefinition.root)
            for name in self.__getFileNames(backupDefinition.includeFiles, backupDefinition.excludeFiles):
                try:
                    statInfo = os.lstat(name)
                except OSError as ex:
                    self.__handleIoOrOsError(BackupSubOperations.Stat, ex)
                    continue
                try:
                    if stat.S_ISREG(statInfo[stat.ST_MODE]):
                        self.__addRegularFile(tarFile, name, statInfo)
                    else:
                        self.__addSpecialFile(tarFile, name, statInfo)
                except (IOError, OSError) as ex:
                    self.__handleIoOrOsError(BackupSubOperations.Open, ex)
            os.chdir(cwdSave)
        except OSError as ex:
            self.__handleIoOrOsError(BackupSubOperations.Open, ex)

        tarFile.close()

        if self.__someFilesChanged:
            self.backupOperationError(BackupSubOperations.Finish, BackupOperationErrors.SomeFilesChanged)
        if not overwriteAtStart:
            shutil.move(workingBackupFilePath, backupFilePath)

        return backupFilePath



    def backupFilesIncrementally(self, backupDefinition, compressionStrength = None, level = None,
                                 overwriteAtStart = False):
        "See: :meth:`._TarArchiverProviderBase.backupFilesIncrementally()`."

        raise NotImplementedError("Not supported.")



    @classmethod
    def getSupportedFeatures(cls, backupType = None):
        "See: :meth:`._TarArchiverProviderBase.getSupportedFeatures()`."

        if backupType is not None:
            cls.raiseIfUnsupportedBackupType_(backupType)
        return _TarArchiverProviderBase.getSupportedFeatures()

    # }}} _TarArchiverProviderBase overrides



    def __addRegularFile(self, tarFile, name, statInfo):
        """Adds a regular file to the :term:`backup`.

        Method is called for each regular file that shall be added to the backup.

        See also: :meth:`__addSpecialFile()`.

        :param tarFile: Tar file where the ``name`` shall be added.
        :type tarFile: :class:`TarFile`
        :param name: Path to a regular file that shall be added to the backup.  It should be relative to archive's
           root directory.
        :type name: ``str``
        :param statInfo: Stat information of the file ``name`` as returned by :meth:`os.lstat()`.
        :type statInfo: ``stat_result``

        :raise IOError: If there was an error while opening the file."""

        tarInfo = tarFile.gettarinfo(name)

        with open(name, "rb") as fileObj:
            self.fileAdd(name)
            tarFile.addfile(tarInfo, fileObj)

            statInfoAfter = os.lstat(name)
            if statInfo[stat.ST_SIZE] != statInfoAfter[stat.ST_SIZE] or \
                statInfo[stat.ST_MTIME] != statInfoAfter[stat.ST_MTIME] or \
                statInfo[stat.ST_MODE] != statInfoAfter[stat.ST_MODE] or \
                statInfo[stat.ST_UID] != statInfoAfter[stat.ST_UID] or \
                statInfo[stat.ST_GID] != statInfoAfter[stat.ST_GID]:

                self.backupOperationError(BackupSubOperations.Read, BackupOperationErrors.FileChanged, name)
                self.__someFilesChanged = True



    def __addSpecialFile(self, tarFile, name, statInfo):
        """Adds a special file to the :term:`backup`.

        Method is called for each special file, such as directory, named pipe, device file, link et al. that shall be
        added to the backup.

        See also: :meth:`addRegularFile_()`.

        :param tarFile: Tar file where the ``name`` shall be added.
        :type tarFile: :class:`TarFile`
        :param name: Path to a special file that shall be added to the backup.  It should be relative to archive's
           root directory.
        :type name: ``str``
        :param statInfo: Stat information of the file ``name`` as returned by :meth:`os.lstat()`.
        :type statInfo: ``stat_result``"""

        tarInfo = tarFile.gettarinfo(name)
        if tarInfo is not None:
            self.fileAdd(name)
            tarFile.addfile(tarInfo)
        else:
            if stat.S_ISSOCK(statInfo[stat.ST_MODE]):
                self.backupOperationError(BackupSubOperations.Open, BackupOperationErrors.SocketIgnored, name)
            else:
                self.backupOperationError(BackupSubOperations.Open, BackupOperationErrors.UnknownTypeIgnored, name)



    def __getFileNames(self, includeFiles, excludeFiles):

        def getFileNamesUnfiltered(fileNames):
            for fileName in fileNames:

                if os.path.isdir(fileName) and not os.path.islink(fileName):

                    # variables to track if includeName and directories list returned by os.walk() were visited in the
                    # os.walk() for loop; if not, assume permission denied
                    includeNameVisited = False
                    listedDirs = set()
                    visitedDirs = set()

                    for root, dirs, files in os.walk(fileName):
                        includeNameVisited = True
                        listedDirs.update({os.path.join(root, d)
                                           for d in dirs
                                           if not os.path.islink(os.path.join(root, d))})
                        visitedDirs.add(root)

                        yield root

                        # yield files and links to directories within root (we yield links to directories as they
                        # were files because we do not follow them)
                        for name in itertools.chain(files, (d for d in dirs if os.path.islink(os.path.join(root, d)))):
                            yield os.path.join(root, name)

                    if not includeNameVisited:
                        showDirOpenError(fileName)
                    for notVisitedDir in listedDirs - visitedDirs:
                        showDirOpenError(notVisitedDir)

                else:
                    yield fileName



        def showDirOpenError(dirName):
            if dirName not in excludeFiles:
                self.backupOperationError(BackupSubOperations.Open, BackupOperationErrors.PermissionDenied, dirName)



        def parentDirs(path, _result = None, _lastDirName = None):
            """Returns a set of parent directories of ``path``.

            For example for "dir/foo/bar" it returns {"dir/foo", "dir"}."""

            if _result is None:
                _result = set()

            dirName = os.path.dirname(path)
            if dirName and dirName != _lastDirName:
                _result.add(dirName)
                parentDirs(dirName, _result, dirName)
            return _result



        def filterFileNames(names, excludeNames):
            return (name for name in names if (name not in excludeNames and parentDirs(name).isdisjoint(excludeNames)))



        return filterFileNames(getFileNamesUnfiltered(includeFiles), excludeFiles)



    def __handleIoOrOsError(self, operation, errorException):
        if errorException.errno == errno.EACCES:
            self.backupOperationError(operation, BackupOperationErrors.PermissionDenied, errorException.filename)
        elif errorException.errno == errno.ENOSPC:
            raise RuntimeError("No space left on device.")
        else:
            self.backupOperationError(operation, BackupOperationErrors.UnknownOsError, errorException.filename,
                                      errorException.strerror)

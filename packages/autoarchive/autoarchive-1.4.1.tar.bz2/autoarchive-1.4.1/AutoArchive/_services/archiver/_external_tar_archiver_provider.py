# _external_tar_archiver_provider.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2016 Róbert Čerňanský



""":class:`_ExternalTarArchiverProvider` class."""



__all__ = ["_ExternalTarArchiverProvider"]



# {{{ INCLUDES

import os
import glob
import shutil
import select
import itertools
import subprocess
import re
import errno
import tempfile

from AutoArchive._infrastructure.utils import Utils
from AutoArchive._infrastructure.py_additions import staticproperty
from . import BackupTypes, BackupSubOperations, ArchiverFeatures, BackupOperationErrors, MIN_COMPRESSION_STRENGTH, \
    MAX_COMPRESSION_STRENGTH
from ._tar_archiver_provider_base import _TarArchiverProviderBase, _BACKUP_TYPES_TO_EXTENSIONS

# }}} INCLUDES



# {{{ CLASSES

class _ExternalTarArchiverProvider(_TarArchiverProviderBase):
    """External archiver service provider.

    See also: :class:`._TarArchiverProviderBase`.

    :raise OSError: If creation of the snapshot directory failed."""

    # name of the archiver binary
    __ARCHIVER_BINARY = "tar"

    # directories where tar is being looked up if it was not found in PATH
    __ARCHIVER_LOCATIONS_FALLBACKS = ("/bin", "/usr/bin", "/usr/local/bin")

    # backup type to GNU tar compress option map
    __BACKUP_TYPE_TO_COMPRESS_OPTION = {BackupTypes.Tar: "",
                                        BackupTypes.TarGz: "--gzip",
                                        BackupTypes.TarBz2: "--bzip2",
                                        BackupTypes.TarXz: "--xz"}



    # {{{ _TarArchiverProviderBase overrides

    def __init__(self, workDir):
        super().__init__(workDir)

        # stores the error state during the backup operation
        self.__errorOccurred = None

        # path to the tar binary
        self.__archiver = self.__locateTar()

        self.__ExternalTarIncrementalUtility.makeSnapshotsDir(workDir)



    @staticproperty
    def supportedBackupTypes():
        "See :attr:`._TarArchiverProviderBase.supportedBackupTypes`"

        return frozenset({BackupTypes.Tar,
                          BackupTypes.TarGz,
                          BackupTypes.TarBz2,
                          BackupTypes.TarXz})



    def backupFiles(self, backupDefinition, compressionStrength = None, overwriteAtStart = False):
        "See: :meth:`._TarArchiverProviderBase.backupFiles()`."

        super().backupFiles(backupDefinition, compressionStrength, overwriteAtStart)

        self.__raiseIfBadCompressionStrength(compressionStrength)

        backupFilePath = self.getBackupFilePath_(backupDefinition.backupId, backupDefinition.backupType,
                                                 backupDefinition.destination)
        workingBackupFilePath = backupFilePath if overwriteAtStart else self.getWorkingPath_(backupFilePath)

        sysEnvironment = os.environ.copy()
        arguments = self.__arguments(backupDefinition.backupType, workingBackupFilePath, backupDefinition.root,
                                     backupDefinition.includeFiles, backupDefinition.excludeFiles, compressionStrength,
                                     sysEnvironment)
        sysEnvironment.update(arguments[1])
        tarProcess = self.__executeTar(arguments[0], sysEnvironment)
        self.__processTarOutput(tarProcess)
        if not overwriteAtStart:
            shutil.move(workingBackupFilePath, backupFilePath)

        return backupFilePath



    def backupFilesIncrementally(self, backupDefinition, compressionStrength = None, level = None,
                                 overwriteAtStart = False):
        "See: :meth:`._TarArchiverProviderBase.backupFilesIncrementally()`."

        super().backupFilesIncrementally(backupDefinition, compressionStrength, level, overwriteAtStart)

        self.__raiseIfBadCompressionStrength(compressionStrength)

        externalTarIncrementalUtility = self.__ExternalTarIncrementalUtility(backupDefinition.backupId, self.workDir_)

        maxBackupLevel = externalTarIncrementalUtility.getMaxBackupLevel()
        if level is None:
            level = maxBackupLevel

        if level < 0 or level > maxBackupLevel:
            raise ValueError(str.format(
                "'level' must be from interval 0 <= level <= maxBackupLevel ({}). The passed value was {}.",
                maxBackupLevel, level))

        workingSnapshotFilePath = externalTarIncrementalUtility.createWorkingSnapshotFile(level)

        backupFilePath = self.getBackupFilePath_(backupDefinition.backupId, backupDefinition.backupType,
                                                 backupDefinition.destination, level)
        workingBackupFilePath = backupFilePath if overwriteAtStart else self.getWorkingPath_(backupFilePath)

        sysEnvironment = os.environ.copy()
        arguments = self.__arguments(backupDefinition.backupType, workingBackupFilePath, backupDefinition.root,
                                     backupDefinition.includeFiles, backupDefinition.excludeFiles, compressionStrength,
                                     sysEnvironment, workingSnapshotFilePath)
        sysEnvironment.update(arguments[1])

        try:
            tarProcess = self.__executeTar(arguments[0], sysEnvironment)
            self.__processTarOutput(tarProcess)
            if not overwriteAtStart:
                shutil.move(workingBackupFilePath, backupFilePath)
            externalTarIncrementalUtility.manageSnapshotFiles(level, workingSnapshotFilePath)
        finally:
            if os.path.exists(workingSnapshotFilePath):
                os.remove(workingSnapshotFilePath)

        return backupFilePath



    def removeBackupIncrements(self, backupDefinition, level = None, keepingId = None):
        "See: :meth:`._TarArchiverProviderBase.removeBackupIncrements()`."

        externalTarIncrementalUtility = self.__ExternalTarIncrementalUtility(backupDefinition.backupId, self.workDir_)

        self.raiseIfUnsupportedBackupType_(backupDefinition.backupType)

        if level is not None:
            if level < 0:
                raise ValueError(str.format("'level' must be > 0. The passed value was {}.", level))
        else:
            level = self.getMaxBackupLevel(backupDefinition.backupId)

        removeLevel = level
        backupExists = True
        while backupExists:
            backupFilePath = self.getBackupFilePath_(
                backupDefinition.backupId, backupDefinition.backupType, backupDefinition.destination, removeLevel,
                keepingId)
            backupExists = os.path.exists(backupFilePath)
            if backupExists:
                os.remove(backupFilePath)
                externalTarIncrementalUtility.tryRemoveSnapshotFile(removeLevel, keepingId)
            removeLevel += 1

        if self.getMaxBackupLevel(backupDefinition.backupId) > level and keepingId is None:

            # ouch! some rogue snapshots still exists; deal with them slowly and painfully
            externalTarIncrementalUtility.removeSnapshotFiles(level)



    @classmethod
    def getSupportedFeatures(cls, backupType = None):
        "See: :meth:`._TarArchiverProviderBase.getSupportedFeatures()`."

        if backupType is not None:
            cls.raiseIfUnsupportedBackupType_(backupType)

        if backupType == BackupTypes.Tar:
            supportedFeatures = frozenset((ArchiverFeatures.Incremental,))
        else:
            supportedFeatures = frozenset({ArchiverFeatures.Incremental,
                                           ArchiverFeatures.CompressionStrength})
        return supportedFeatures



    def getMaxBackupLevel(self, backupId):
        "See: :meth:`._TarArchiverProviderBase.getMaxBackupLevel()`."

        return self.__ExternalTarIncrementalUtility(backupId, self.workDir_).getMaxBackupLevel()



    @Utils.uniq
    def getStoredBackupIds(self):
        "See: :meth:`._TarArchiverProviderBase.getStoredBackupIds()`."

        snapshots = self.__ExternalTarIncrementalUtility.getSnapshotsForBackup(
            self.__ExternalTarIncrementalUtility.getSnapshotsDir(self.workDir_))
        return (os.path.splitext(os.path.splitext(os.path.basename(snapshot))[0])[0] for snapshot in snapshots)



    def purgeStoredBackupData(self, backupId):
        "See: :meth:`._TarArchiverProviderBase.purgeStoredBackupData()`."

        snapshotsDir = self.__ExternalTarIncrementalUtility.getSnapshotsDir(self.workDir_)
        snapshots = self.__ExternalTarIncrementalUtility.getSnapshotsForBackup(snapshotsDir, backupId)
        for snapshot in snapshots:
            os.remove(os.path.join(snapshotsDir, snapshot))



    def doesAnyBackupLevelExist(self, backupDefinition, fromLevel = 0, keepingId = None):
        "See: :meth:`._TarArchiverProviderBase.doesAnyBackupLevelExist()`."

        keepToken = "." + keepingId if keepingId else ""

        # SMELL: Backup path is similarly assembled in super().getBackupFilePath_.
        level0Glob = os.path.join(backupDefinition.destination,
                                  backupDefinition.backupId + keepToken + "." +
                                  _BACKUP_TYPES_TO_EXTENSIONS[backupDefinition.backupType])
        levelGreaterThan0Glob = os.path.join(backupDefinition.destination,
                                             backupDefinition.backupId + ".*" + keepToken + "." +
                                             _BACKUP_TYPES_TO_EXTENSIONS[backupDefinition.backupType])
        backups = itertools.chain(glob.iglob(os.path.join(level0Glob)),
                                  glob.iglob(os.path.join(levelGreaterThan0Glob)))
        backups = itertools.dropwhile(
            lambda bac:
            self.__ExternalTarIncrementalUtility.getLevelFromFileName(
                os.path.basename(bac), keepingId is not None) < fromLevel, backups)

        return bool(list(itertools.islice(backups, 1)))

    # }}} _TarArchiverProviderBase overrides



    def __executeTar(self, arguments, environment):
        environment["LC_MESSAGES"] = "C"
        if "LC_ALL" in environment:
            del environment["LC_ALL"]
        try:
            tarProcess = subprocess.Popen([self.__archiver] + arguments, stdout = subprocess.PIPE,
                                          stderr = subprocess.PIPE, env = environment, universal_newlines = True)
        except OSError as ex:
            raise OSError(str.format("Error while executing external archiving program: {}.", self.__archiver),
                          self.__archiver, ex)

        return tarProcess



    def __processTarOutput(self, archiverProcess):
        self.__errorOccurred = False
        self.backupOperationError += self.__onBackupOperationError

        try:

            # capture program's standard output and standard error and use CmdlineUi-like interface to print captured
            # messages; note that the order of messages written to stdout vs. messages written to stderr might not be
            # preserved
            while True:
                readyStreams = select.select((archiverProcess.stdout, archiverProcess.stderr), (), ())[0]
                streamActive = False
                for readyStream in readyStreams:
                    line = readyStream.readline()
                    if line:
                        streamActive = True
                        self.__propagateArchiverMessage(line[:-1], readyStream is not archiverProcess.stdout)
                if archiverProcess.poll() is not None and not streamActive:
                    break
        finally:
            self.backupOperationError -= self.__onBackupOperationError

        if archiverProcess.returncode:
            self.__handleArchiverExitCode(archiverProcess.returncode)



    def __arguments(self, backupType, backupFilePath, root, includeFiles, excludeFiles, compressionStrength,
                    sysEnvironment, snapshotPath = None):
        "Assembles and returns arguments to the tar binary."

        compressOption = self.__BACKUP_TYPE_TO_COMPRESS_OPTION[backupType]

        # operation has to be first one
        archiverOptions = ["--create", "--format=posix", "--verbose"]

        # insert options required for this archiver
        if compressOption:
            archiverOptions.append(compressOption)

        if snapshotPath is not None:
            archiverOptions.append("--listed-incremental=" + snapshotPath)

        # add options required for this archiver type
        archiverOptions += ["--file=" + backupFilePath,
                            "--directory=" + root]

        # add converted include and exclude files
        archiverOptions += self.__convertIncludesAndExcludes(includeFiles, excludeFiles)

        # create environment
        environment = self.__convertCompressionStrength(backupType, compressionStrength, sysEnvironment)

        return archiverOptions, environment



    def __propagateArchiverMessage(self, message, sentToStderr = False):
        """Propagates archiver message an event.

        Parses the passed ``message``, evaluates it and fires :meth:`._TarArchiverProviderBase.backupOperationError`
        event if it is an (non-fatal) error message or :meth:`._TarArchiverProviderBase.fileAdd` otherwise."""

        if sentToStderr:

            # messages that will be ignored
            if not message or re.search("(: Exiting with failure status due to previous errors)|" +
                         "(: (.*): Directory is new)", message):
                return

            match = re.search(": (.*): cannot stat: (.*)", message, re.IGNORECASE)
            if match:
                if match.groups()[1].find(os.strerror(errno.EACCES)) != -1:
                    self.backupOperationError(BackupSubOperations.Stat, BackupOperationErrors.PermissionDenied,
                                              match.groups()[0])
                else:
                    self.backupOperationError(BackupSubOperations.Stat, BackupOperationErrors.UnknownOsError,
                                              match.groups()[0], match.groups()[1])
                return
            match = re.search(": (.*): cannot open: (.*)", message, re.IGNORECASE)
            if match:
                if match.groups()[1].find(os.strerror(errno.EACCES)) != -1:
                    self.backupOperationError(BackupSubOperations.Open, BackupOperationErrors.PermissionDenied,
                                              match.groups()[0])
                else:
                    self.backupOperationError(BackupSubOperations.Open, BackupOperationErrors.UnknownOsError,
                                              match.groups()[0], match.groups()[1])
                return
            match = re.search(": (.*): socket ignored", message, re.IGNORECASE)
            if match:
                self.backupOperationError(BackupSubOperations.Open, BackupOperationErrors.SocketIgnored,
                                          match.groups()[0])
                return
            match = re.search(": (.*): file changed as we read it", message, re.IGNORECASE)
            if match:
                self.backupOperationError(BackupSubOperations.Read, BackupOperationErrors.FileChanged,
                                          match.groups()[0])
                return
            match = re.search(": (.*): directory has been renamed", message, re.IGNORECASE)
            if match:
                self.backupOperationError(BackupSubOperations.Read, BackupOperationErrors.DirectoryRenamed,
                                          match.groups()[0])
                return
            match = re.search(": No space left on device", message, re.IGNORECASE)
            if match:
                raise RuntimeError("No space left on device.")
            match = re.search("(unrecognized option.*)|(Try.+--help.+for more information.*)", message, re.IGNORECASE)
            if match:
                raise RuntimeError(str.format("Incompatible external archiver binary: {} ({}).",
                                              self.__archiver, match.group(0)))
            match = re.search(": Error is not recoverable: exiting now", message, re.IGNORECASE)
            if match:
                raise RuntimeError("External archiver aborted.")
            match = re.search(": (.*): (.+)", message, re.IGNORECASE)
            if match:
                self.backupOperationError(BackupSubOperations.UnknownFileOperation,
                                          BackupOperationErrors.UnknownError, match.groups()[0], match.groups()[1])
                return

            self.backupOperationError(BackupSubOperations.Unknown, BackupOperationErrors.UnknownError,
                                      unknownErrorString = message)

        else:
            self.fileAdd(message)



    def __handleArchiverExitCode(self, exitCode):
        if exitCode == 1:
            self.backupOperationError(BackupSubOperations.Finish, BackupOperationErrors.SomeFilesChanged)
        else:
            if not self.__errorOccurred:
                raise RuntimeError(str.format("Unexpected failure of the archiver program; exit code: {}", exitCode))



    @staticmethod
    def __convertIncludesAndExcludes(includeFiles, excludeFiles):
        """Converts list of files and list of excluded files to the form suitable for the archiver program.

        :return: List of arguments for the archiver."""

        archiverOptions = []

        if excludeFiles:
            archiverOptions.append("--anchored")
        for exclude in excludeFiles:
            archiverOptions.append("--exclude=" + exclude)

        archiverOptions += includeFiles

        return archiverOptions



    @staticmethod
    def __convertCompressionStrength(backupType, compressionStrength, sysEnvironment):
        """Converts compression strength to an environment variable.

        :return: Dictionary representing environment with the required environment variable."""

        environment = {}

        if compressionStrength is not None:
            if backupType == BackupTypes.TarGz:
                envName = "GZIP"
                if compressionStrength < 1:
                    compressionStrength = 1
            elif backupType == BackupTypes.TarBz2:
                envName = "BZIP2"
                if compressionStrength < 1:
                    compressionStrength = 1
            else:
                envName = "XZ_OPT"

            sysEnvValue = sysEnvironment[envName] + " " if envName in sysEnvironment else ""
            environment[envName] = sysEnvValue + "-" + str(compressionStrength)

        return environment



    def __onBackupOperationError(self, operation, error, filesystemObjectName = None, unknownErrorString = None):
        self.__errorOccurred = self.__errorOccurred or \
                               (operation != BackupSubOperations.Finish and
                                (error == BackupOperationErrors.PermissionDenied or
                                 error == BackupOperationErrors.UnknownOsError or
                                 error == BackupOperationErrors.UnknownError))



    @staticmethod
    def __raiseIfBadCompressionStrength(compressionStrength):
        if compressionStrength is not None and \
           (compressionStrength < MIN_COMPRESSION_STRENGTH or compressionStrength > MAX_COMPRESSION_STRENGTH):
            raise ValueError(str.format("Compression strength value {} is out of defined interval",
                                        compressionStrength))



    @classmethod
    def __locateTar(cls):

        def getTarPath(directories):
            resultPath = None

            for directory in directories:
                testTarPath = os.path.join(directory, cls.__ARCHIVER_BINARY)
                if os.path.exists(testTarPath) and os.access(testTarPath, os.R_OK | os.X_OK):
                    resultPath = testTarPath
                    break

            return resultPath



        # first try to find tar in PATH
        tarPath = getTarPath(os.get_exec_path())

        # then try fallback locations
        if tarPath is None:
            tarPath = getTarPath(cls.__ARCHIVER_LOCATIONS_FALLBACKS)

        if tarPath is None:
            raise OSError(str.format("Unable to locate the archiver binary: {}.", cls.__ARCHIVER_BINARY))

        return tarPath



    class __ExternalTarIncrementalUtility:
        """Utility class for GNU tar incremental backup operations."""

        # subdirectory for snapshots
        __SNAPSHOTS_SUBDIR = "snapshots"

        # suffix for snapshot files used in incremental backups
        __SNAPSHOT_SUFFIX = ".snar"



        def __init__(self, backupId, workDir):
            self.__backupId = backupId
            self.__workDir = workDir

            self.__snapshotsDir = self.getSnapshotsDir(self.__workDir)



        def getMaxBackupLevel(self):
            """Returns maximal backup level that is possible to create.

            :raise OSError: If a system error occurred."""

            currentBackupLevel = self.__getBackupLevel()
            return currentBackupLevel + 1 if currentBackupLevel is not None else 0



        def getSnapshotFileName(self, level, keepingId = None):
            "Returns full path to snapshot file for a certain backup level."

            keepingToken = "." + keepingId if keepingId else ""
            return os.path.join(self.__snapshotsDir,
                                self.__backupId + self.__getLevelSuffix(level) + keepingToken + self.__SNAPSHOT_SUFFIX)



        def getSnapshots(self):
            "Returns sequence of snapshot file names for current backup."

            return self.getSnapshotsForBackup(self.__snapshotsDir, self.__backupId)



        @classmethod
        def getSnapshotsForBackup(cls, snapshotsDir, backupId = ""):
            """Returns sequence of snapshot file names for the archive named ``backupId`` or all of them.

            :param snapshotsDir: Directory where the snapshot files are stored.  Can be obtained with
               :meth:`getSnapshotsDir` method.
            :type snapshotsDir: ``str``
            :param backupId: Name of the archive for which the snapshot file names shall be returned.  If not specified
               all snapshot files will be returned.
            :type backupId: ``str``

            :return: Sequence of snapshot file names.
            :rtype: ``Sequence<str>``

            :raise OSError: If ``snapshotsDir`` does not exists or is not accessible.  The exception contains two
               parameters: the error message and the name of the directory."""

            if not os.path.isdir(snapshotsDir):
                raise OSError("Snapshots directory does not exists.", snapshotsDir)
            if not os.access(snapshotsDir, os.R_OK | os.X_OK):
                raise OSError("Snapshots directory is not accessible for reading or listing", snapshotsDir)

            if backupId == "":
                backupId = "*"
            snapshots = itertools.chain(
                glob.iglob(os.path.join(snapshotsDir, backupId + cls.__SNAPSHOT_SUFFIX)),
                glob.iglob(os.path.join(snapshotsDir, backupId + ".*" + cls.__SNAPSHOT_SUFFIX)))

            return tuple(os.path.basename(snapshot) for snapshot in snapshots)



        @classmethod
        def getSnapshotsDir(cls, workDir):
            return os.path.join(workDir, cls.__SNAPSHOTS_SUBDIR)



        def manageSnapshotFiles(self, level, latestLevelSnapshotFilePath):
            """Moves snapshot file to its proper location and name in order to preserve it and removes redundant ones.

            :raise OSError: If a system error occurred."""

            self.removeSnapshotFiles(level + 1)

            shutil.move(latestLevelSnapshotFilePath, self.getSnapshotFileName(level))

            # change the file permissions according to umask
            umask = os.umask(0)
            os.umask(umask)
            os.chmod(self.getSnapshotFileName(level), 0o666 & ~umask)



        def removeSnapshotFiles(self, level):
            """Remove snapshot files for levels higher or equal to ``level``."""

            for snapshot in self.getSnapshots():
                if self.getLevelFromFileName(snapshot) >= level:
                    os.remove(os.path.join(self.__snapshotsDir, snapshot))



        # SMELL: Currently a snapshot file with a keeping ID other than None will never exists.  Snapshots are not kept.
        def tryRemoveSnapshotFile(self, level, keepingId = None):
            """Removes snapshot file for given backup level if it exists.

            :param level: Backup level for which the snapshot file shall be removed.
            :type level: ``int``
            :param keepingId: If not ``None`` a kept snapshot with this ID will be removed.
            :type keepingId: ``str``

            :return: ``True`` if the snapshot file was removed; ``False`` if the file does not exists.

            :raise OSError: If a system error occurred."""

            snapshotFileName = self.getSnapshotFileName(level, keepingId)
            if os.path.exists(snapshotFileName):
                try:
                    os.remove(snapshotFileName)
                except OSError as ex:
                    if ex.errno != errno.ENOENT:
                        raise
                    return False

                return True

            return False



        def createWorkingSnapshotFile(self, level):
            """Copies snapshot file for ``level`` to a temporary file."""

            tempFileDescriptor, tempFilePath = tempfile.mkstemp(".snar", "autoarchive")

            # copy the snapshot file for previous level to a temporary one which will be used to create the new
            # increment; after that it will be moved to the proper location and name according to processed archive and
            # level; this way backup files for each created level will be preserved and thus it will be possible to
            # create also lower level backups (otherwise it would be only possible to create level N+1 backup (where N
            # is the latest/current level) or level 0 (go from the beginning))
            if level > 0:
                with open(self.getSnapshotFileName(level - 1), "rb") as srcSnapshotFile:
                    with open(tempFileDescriptor, "wb") as tempFile:
                        shutil.copyfileobj(srcSnapshotFile, tempFile)
            else:

                # we do not need a previous snapshot file if the backup level is 0
                os.remove(tempFilePath)

            return tempFilePath



        @classmethod
        def makeSnapshotsDir(cls, workDir):
            """Creates the snapshots directory.

            :raise OSError: If creation of the directory was not successful."""

            snapshotsDir = cls.getSnapshotsDir(workDir)
            if not os.path.exists(snapshotsDir):
                try:
                    os.mkdir(snapshotsDir)
                except OSError as ex:
                    if ex.errno != errno.EEXIST:
                        raise



        @staticmethod
        def getLevelFromFileName(fileName, keptBackup = False):
            """Extracts backup level number from the file name.

            :param fileName: Name of the file used to get the backup level from.  It should be in the form:
              '<archive_name>[.<level>].<suffix>'.
            :type fileName: ``str``

            :return: The :term:`backup level` retrieved from the file name.
            :rtype: ``int``"""

            root, levelToken = os.path.splitext(os.path.splitext(fileName)[0])
            if keptBackup:
                root, levelToken = os.path.splitext(root)
            try:
                level = int(levelToken[1:])
            except ValueError:
                levelToken = os.path.splitext(root)[1]
                try:
                    level = int(levelToken[1:])
                except ValueError:
                    level = 0

            return level



        def __getBackupLevel(self):
            level = None
            snapshotFiles = self.getSnapshots()

            if len(snapshotFiles) > 0:
                level = max((self.getLevelFromFileName(snapshotFile)
                             for snapshotFile in snapshotFiles))

            return level



        @staticmethod
        def __getLevelSuffix(level):
            """Returns file name suffix according to the backup level.

            :param level: Backup level for which the suffix shall be returned.
            :type level: ``int``

            :return: File name suffix for backup level in the form '.<level>'.
            :rtype: ``str``"""

            return "." + str(level) if level > 0 else ""

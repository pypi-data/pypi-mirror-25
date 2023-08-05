# archiver_test_utils.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2017 Róbert Čerňanský



""":class:`ArchiverTestUtils` class."""



__all__ = ["ArchiverTestUtils"]



# {{{ INCLUDES

from mock import Mock

from abc import ABCMeta, abstractmethod
import os
import stat
import tempfile
import shutil
import collections
import tarfile
import subprocess

from .. import BackupDefinition, BackupTypes
from AutoArchive.tests import ComponentTestUtils
from .._tar_archiver_provider_base import _TarArchiverProviderBase

# }}} INCLUDES



# {{{ CLASSES

class ArchiverTestUtils(metaclass = ABCMeta):
    """Utility methods for Archiving component tests."""

    #: Name of the file created in the testing file structure; {number} is replaced with a file index (e. g. 1).
    _FILE_NAME = "test_file_{index}.t"

    #: Directory name created in the testing file structure; {number} is replaced with a directory index (e. g. 1).
    _DIR_NAME = "test_dir_{index}"

    #: Name of the socked created in the testing file structure.
    _SOCKET_NAME = "test_sock.t"

    #: Name of the file without read permissions created in the testing file structure.
    _DENIED_FILE_NAME = "test_denied.t"

    #: Name of the directory without read permissions created in the testing file structure.
    _DENIED_DIR_NAME = "test_denied"

    _IRRELEVANT_BACKUP_ID = "irrelevant backup ID"

    __TAR_PATH = "/bin/tar"



    @abstractmethod
    def __init__(self):
        pass



    @staticmethod
    def createArchiverMock():
        """Creates a mock of :class:`_TarArchiverProviderBase`.

        :return: Mock of the :class:`_TarArchiverProviderBase`.
        :rtype: :class:`mock.Mock<_TarArchiverProviderBase>`"""

        def backupFilesSideEffect(backupDefinition, compressionStrength = None, level = None, overwriteAtStart = False):
            levelToken = "." + str(level) if level is not None else ""
            return os.path.join(backupDefinition.destination, backupDefinition.backupId + levelToken)

        archiverMock = Mock(spec_set = _TarArchiverProviderBase)
        archiverMock.backupFiles.side_effect = backupFilesSideEffect
        archiverMock.backupFilesIncrementally.side_effect = backupFilesSideEffect
        return archiverMock



    @classmethod
    def _setUpClassArchiverComponent(cls):
        ComponentTestUtils.setUpClassComponent()



    @classmethod
    def _tearDownClassArchiverComponent(cls):
        ComponentTestUtils.tearDownClassComponent()



    @classmethod
    def _makeTestFileStructure(cls, filesCount = 2, dirsCount = 2, depth = 1, socket = False, denied = False,
                               links = False):
        """Creates a directory and file structure for testing purposes.

        See also: :meth:`_removeTestFileStructure()`."""

        def getFileNames(root):
            return (os.path.join(root, str.format(cls._FILE_NAME, index = nr))
                    for nr in range(filesCount))



        def getDirNames(root):
            return (os.path.join(root, str.format(cls._DIR_NAME, index = nr))
                    for nr in range(dirsCount))



        def createDirStructure(root, level = 0):
            for fileName in getFileNames(root):
                with open(fileName, "w") as testFile:
                    testFile.write(str.format("Content of the test file \"{}\".", fileName))

            for dirName in getDirNames(root):
                os.mkdir(dirName)
                level += 1
                if level <= depth:
                    createDirStructure(dirName, level)
                level -= 1



        root = tempfile.mkdtemp(prefix = "test_structure", dir = ComponentTestUtils.getComponentTestContext().workDir)

        createDirStructure(root)

        if links:
            firstTestDir = str.format(cls._DIR_NAME, index = 0)

            # create directory links - one in toplevel directory so it is selected among included files and the other
            # within a directory so it is nested
            if dirsCount > 0:
                os.symlink(firstTestDir, os.path.join(root, "included_dir_link"))
                os.symlink(os.path.join(os.pardir, firstTestDir), os.path.join(root, firstTestDir, "nested_dir_link"))

            # create file links similarly to directory links above
            if filesCount > 0:
                firstTestFile = str.format(cls._FILE_NAME, index = 0)
                os.symlink(firstTestFile, os.path.join(root, "included_file_link"))
                if dirsCount > 0:
                    os.symlink(firstTestFile, os.path.join(root, firstTestDir, "nested_file_link"))

            # create broken links
            os.symlink("non existing source", os.path.join(root, "broken_included_link"))
            if dirsCount > 0:
                os.symlink("non existing source", os.path.join(root, firstTestDir, "broken_nested_link"))

        os.mkfifo(os.path.join(root, "test_fifo.t"))

        if socket:
            os.mknod(os.path.join(root, cls._SOCKET_NAME), stat.S_IRUSR | stat.S_IWUSR | stat.S_IFSOCK)

        if denied:
            with open(os.path.join(root, cls._DENIED_FILE_NAME), "w") as deniedFile:
                deniedFile.write(str.format("Content of the denied test file."))
                os.fchmod(deniedFile.fileno(), stat.S_IWRITE)
            os.mkdir(os.path.join(root, cls._DENIED_DIR_NAME))
            os.chmod(os.path.join(root, cls._DENIED_DIR_NAME), stat.S_IWRITE | stat.S_IEXEC)

        return root



    @classmethod
    def _removeTestFileStructure(cls, root):
        """Removes the test file structure created by :meth:`_makeTestFileStructure()`.

        :param root: Path to the test file structure.
        :type root: ``str``"""

        deniedDirName = os.path.join(root, cls._DENIED_DIR_NAME)
        if os.path.isdir(deniedDirName):
            os.rmdir(deniedDirName)

        ComponentTestUtils.clearDir(root)
        os.rmdir(root)



    @classmethod
    def _extractBackup(cls, backupFilePaths):
        """Extracts non-incremental or incremental backup.

        :param backupFilePaths: Path to the backup file or files.  In case of incremental backup, list should
        be provided otherwise a single path only.
        :type backupFilePaths: ``str`` or ``Iterable<str>``

        :return: Path to the extracted backup.
        :rtype: ``str``"""

        extractPath = tempfile.mkdtemp(prefix = "extracted", dir = ComponentTestUtils.getComponentTestContext().workDir)

        if isinstance(backupFilePaths, str):
            tarFile = tarfile.open(backupFilePaths, "r")
            tarFile.extractall(extractPath)
        else:
            for backupFilePath in backupFilePaths:
                subprocess.call([cls.__TAR_PATH, "-xf", backupFilePath, "--listed-incremental=/dev/null", "-C",
                                 extractPath])
        return extractPath



    @classmethod
    def _removeExtractedBackup(cls, extractPath):
        """Deletes extracted files from a backup.

        :param extractPath: A path to the extracted backup.
        :type extractPath: ``str``"""

        if extractPath and os.path.isdir(extractPath):
            shutil.rmtree(extractPath)



    @classmethod
    def _compareDirs(cls, orig, other):
        """Compares content of ``orig`` and ``other`` directories.

        Compares the stat info and the content of files and directories.  Content of any two directories is compared
        only if their stat infos are equal.  Content of any two files is compared only if their containing directories
        are equal and the stat infos of those two files are equal.

        :param orig: Path to the "orig" directory which will be compared with the "other"
        :param other: Path to the "other" directory.

        :return: ``True`` if content of ``orig`` and ``other`` are equal.
        :rtype: ``bool``"""

        for root, dirs, files in os.walk(other):
            origRoot = os.path.join(orig, os.path.relpath(root, other))

            # >compare stat info of the directory.
            if not cls.__isFsObjectsStatInfoEqual(root, origRoot):
                return False

            # >compare the content of directories
            if collections.Counter(dirs + files) != collections.Counter(os.listdir(origRoot)):
                return False

            # >compare files
            filesEqual = True
            for fileName in files:

                # >>compare the stat info of files
                extractedFilePath = os.path.join(root, fileName)
                origFilePath = os.path.join(origRoot, fileName)
                if not cls.__isFsObjectsStatInfoEqual(extractedFilePath, origFilePath):
                    filesEqual = False
                    break

                # >>compare the content of files
                if os.path.isfile(extractedFilePath):
                    with open(extractedFilePath, "rb") as extractedFile:
                        extractedData = extractedFile.read()
                    with open(origFilePath, "rb") as origFile:
                        origData = origFile.read()
                    if extractedData != origData:
                        filesEqual = False
                        break

            if not filesEqual:
                return False

        return True



    @staticmethod
    def __isFsObjectsStatInfoEqual(fsObject1, fsObject2):
        statInfo1 = os.lstat(fsObject1)
        statInfo2 = os.lstat(fsObject2)
        return statInfo1[stat.ST_SIZE] == statInfo2[stat.ST_SIZE] or \
               statInfo1[stat.ST_MTIME] == statInfo2[stat.ST_MTIME] or \
               statInfo1[stat.ST_ATIME] == statInfo2[stat.ST_ATIME] or \
               statInfo1[stat.ST_CTIME] == statInfo2[stat.ST_CTIME] or \
               statInfo1[stat.ST_MODE] == statInfo2[stat.ST_MODE] or \
               statInfo1[stat.ST_UID] == statInfo2[stat.ST_UID] or \
               statInfo1[stat.ST_GID] == statInfo2[stat.ST_GID]



class _BackupDefinitionBuilder:
    """:class:`BackupDefinition` factory."""

    # default type of the archive supported by an archiver provider used if it is irrelevant.
    __IRRELEVANT_SUPPORTED_BACKUP_TYPE = BackupTypes.Tar



    def __init__(self):
        self.__backupId = ArchiverTestUtils._IRRELEVANT_BACKUP_ID
        self.__backupType = self.__IRRELEVANT_SUPPORTED_BACKUP_TYPE
        self.__destination = ComponentTestUtils.irrelevantDirectory
        self.__root = ComponentTestUtils.irrelevantDirectory
        self.__includeFiles = frozenset({"*"})
        self.__excludeFiles = frozenset()



    def build(self):
        """Creates initialized instance of :class:`BackupDefinition`."""

        backupDefinition = BackupDefinition()
        backupDefinition.backupId = self.__backupId
        backupDefinition.backupType = self.__backupType
        backupDefinition.destination = self.__destination
        backupDefinition.root = self.__root
        backupDefinition.includeFiles = self.__includeFiles
        backupDefinition.excludeFiles = self.__excludeFiles
        return backupDefinition



    def withBackupId(self, backupId):
        self.__backupId = backupId
        return self



    def withBackupType(self, backupType):
        self.__backupType = backupType
        return self



    def withDestination(self, destination):
        self.__destination = destination
        return self



    def withRoot(self, root):
        self.__root = root
        return self



    def withIncludeFiles(self, includeFiles):
        self.__includeFiles = includeFiles
        return self



    def withExcludeFiles(self, excludeFiles):
        self.__excludeFiles = excludeFiles
        return self

# }}} CLASSES

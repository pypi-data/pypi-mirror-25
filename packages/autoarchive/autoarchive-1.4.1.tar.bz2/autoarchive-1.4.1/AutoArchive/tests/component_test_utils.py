# component_test_utils.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2017 Róbert Čerňanský



""":class:`ComponentTestUtils` and :class:`ComponentTestContext` classes."""



__all__ = ["ComponentTestUtils", "ComponentTestContext"]



# {{{ INCLUDES

from abc import *
import os
import shutil
import tempfile

from .._infrastructure.py_additions import *


# }}} INCLUDES



# {{{ CLASSES

class ComponentTestUtils(metaclass = ABCMeta):
    """Utility methods for component tests."""

    __componentTestContext = None



    @abstractmethod
    def __init__(self):
        pass



    @staticproperty
    def irrelevantDirectory():
        """Gets a path to some existing directory.

        :rtype: ``str``."""

        return ComponentTestUtils.getComponentTestContext().workDir



    @staticproperty
    def irrelevantValidFilePath():
        """Gets a path to a file used if it is irrelevant.

        The returned file does not exists but its directory does.

        :rtype: ``str``."""

        return os.path.join(ComponentTestUtils.irrelevantDirectory, "irrelevant file name")



    @classmethod
    def getComponentTestContext(cls):
        """Gets the :class:`ComponentTestContext` instance.

        :return: :class:`ComponentTestContext` instance.
        :rtype: :class:`ComponentTestContext`

        :raise RuntimeError: If the class was not initialized by :meth:`setUpClassComponent()` call."""

        if not cls.__componentTestContext:
            raise RuntimeError("Not initialized!")

        return cls.__componentTestContext



    @classmethod
    def setUpClassComponent(cls):
        """Performs basic set up for component tests.

        Instantiates :class:`ComponentTestContext` and creates *working directory*.  Initializes
        the :attr:`ComponentTestContext.workDir` property.

        :raise RuntimeError: If the class is already initialized."""

        if cls.__componentTestContext:
            raise RuntimeError("Already initialized!")

        cls.__componentTestContext = ComponentTestContext()
        cls.__componentTestContext.workDir = tempfile.mkdtemp(prefix = "autoarchive")



    @classmethod
    def tearDownClassComponent(cls):
        """Performs final clean up.

        Removes the *work directory*.

        :raise RuntimeError: If the class is not initialized."""

        if not cls.__componentTestContext:
            raise RuntimeError("Not initialized!")

        shutil.rmtree(cls.__componentTestContext.workDir)
        cls.__componentTestContext.workDir = None
        cls.__componentTestContext = None



    @classmethod
    def createIrrelevantFile(cls):
        """Creates a file and return the path to it.

        :return: Path to the created file.
        :rtype: ``str``."""

        filePath = cls.irrelevantValidFilePath
        open(filePath, "w").close()
        return filePath



    @classmethod
    def removeIrrelevantFile(cls):
        """Removes the file created by the :meth:`createIrrelevantFile()`."""

        os.remove(cls.irrelevantValidFilePath)



    @classmethod
    def checkWorkDirEmptiness(cls):
        """Raises an exception if the *working directory* is not empty.

        :raise RuntimeError: If *working directory* is not empty."""

        if os.listdir(cls.__componentTestContext.workDir):
            raise RuntimeError("Working directory is not empty.")



    @classmethod
    def clearDir(cls, root):
        """Removes everything from the passed directory path.

        :param root: Path to the directory which content shall be deleted.
        :type root: ``str``"""

        for filesystemObject in os.listdir(root):
            filesystemObjectPath = os.path.join(root, filesystemObject)
            if os.path.isdir(filesystemObjectPath) and not os.path.islink(filesystemObjectPath):
                shutil.rmtree(filesystemObjectPath)
            else:
                os.remove(filesystemObjectPath)



class ComponentTestContext:
    """Stores various objects used by component tests.

    The instance is typically populated by tests themselves as needed.

    .. note:: Each property in this class can return ``None``."""

    def __init__(self):
        self.__workDir = None
        self.__archiveSpecsDir = None
        self.__userConfigDir = None



    @property
    def workDir(self):
        """Path to the root of the *working directory* for tests.

        Every file or directory created by tests should be created within this directory.

        :rtype: ``str``"""

        return self.__workDir

    @workDir.setter
    def workDir(self, value):
        self.__workDir = value



    @property
    def archiveSpecsDir(self):
        """Path to the archive specifications directory.

        :rtype: ``str``"""

        return self.__archiveSpecsDir

    @archiveSpecsDir.setter
    def archiveSpecsDir(self, value):
        self.__archiveSpecsDir = value



    @property
    def userConfigDir(self):
        """Path to the user configuration directory.

        :rtype: ``str``"""

        return self.__userConfigDir

    @userConfigDir.setter
    def userConfigDir(self, value):
        self.__userConfigDir = value

# }}} CLASSES

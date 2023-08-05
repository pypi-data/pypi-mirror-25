# configuration_test_utils.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2012 Róbert Čerňanský



""":class:`ConfigurationTestUtils` class."""



__all__ = ["ConfigurationTestUtils"]



# {{{ INCLUDES

from mock import Mock, MagicMock

from abc import *
import os
import shutil
import tempfile
import glob
from optparse import OptionParser

from ..._app_environment import *
from ..._mainf import *
from .. import *
from .._core import ConfigurationComponent

from ...tests import *
from ..._mainf.tests import MainfTestUtils

# }}} INCLUDES



# {{{ CLASSES

class ConfigurationTestUtils(metaclass = ABCMeta):
    """Utility methods for Configuration component tests."""

    # Name of the default storage realm used if the realm is not specified.
    __DEFAULT_REALM = "TestDefaultRealm"

    # Name of the default storage section used if the section is not specified.
    DEFAULT_SECTION = "TestDefaultSection"

    # Subdirectory where the storage place its files.
    __STORAGE_SUBDIR = "storage"

    # Mock of the IInterfaceAccessor.
    _mockInterfaceAccessor = None



    @abstractmethod
    def __init__(self):
        pass



    @staticmethod
    def createMockAppConfig(options = None, archiveSpecs = None):
        """Creates a mock of :class:`IAppConfig` and initializes it with passed arguments.

        :param options: Dictionary of option: value with which the mock will be initialized.
        :type options: ``dict<Option, object>``
        :param archiveSpecs: Iterable of archive specification files that shall be returned by getArchiveSpecs().
        :type archiveSpecs: ``Iterable<ArchiveSpecInfo>``

        :return: Mock of the :class:`IAppConfig`.
        :rtype: :class:`mock.Mock<IAppConfig>`"""

        def getItemSideEffect(option):
            try:
                return options[option]
            except KeyError:
                return None



        if options is None:
            options = {}

        mockAppConfig = MagicMock(spec_set = IAppConfig)
        mockAppConfig.__getitem__.side_effect = getItemSideEffect
        mockAppConfig.getRawValue.side_effect = getItemSideEffect
        if archiveSpecs:
            mockAppConfig.getArchiveSpecs.return_value = archiveSpecs

        return mockAppConfig



    @classmethod
    def createMockStorage(cls, storageState):
        """Creates mock of the :class:`IStorage` interface.

        Mock is a functional implementation of :class:`IStorage` which means that values saved to the storage can be
        read back.  Other interface methods works as expected as well.  Error cases may behave differently than defined
        by the interface.

        .. note:: Mock provides only transient storage, i. e. stored values exists as long as ``storageState`` exists;
           they are not persistent (saved to disk or so) as proper implementation of :class:`IStorage` should
           provide.

        :param storageState: A mutable instance where the mock stores its state (values of variables in sections and
           realms).  The type is ``dict<str: dict<str: dict<str: object>>>`` where the key (of the most outer
           dictionary) is realm name, and the value is dictionary with the key representing the section name
           and the value of variable name and value dictionary.
        :type storageState: ``dict<str: dict<str: dict<str: object>>>``

        :return: Mock of the :class:`IStorage`.
        :rtype: :class:`mock.Mock<IStorage>`"""

        def getValueSideEffect(variable, section = None, realm = None):
            return mockStorage._storage[realm or cls.__DEFAULT_REALM][section or cls.DEFAULT_SECTION][variable]



        def saveValueSideEffect(variable, value, section = None, realm = None):
            realm = realm or cls.__DEFAULT_REALM
            section = section or cls__.DEFAULT_SECTION
            if realm not in mockStorage._storage:
                mockStorage._storage[realm] = {}
            if section not in mockStorage._storage[realm]:
                mockStorage._storage[realm][section] = {}
            mockStorage._storage[realm][section][variable] = str(value)



        def hasVariableSideEffect(variable, section = None, realm = None):
            try:
                return variable in mockStorage._storage[realm or cls.__DEFAULT_REALM][section or cls.DEFAULT_SECTION]
            except KeyError:
                return False



        def tryRemoveVariableSideEffect(variable, section = None, realm = None):
            if variable in mockStorage._storage[realm or cls.__DEFAULT_REALM][section or cls.DEFAULT_SECTION]:
                del mockStorage._storage[realm or cls.__DEFAULT_REALM][section or cls.DEFAULT_SECTION][variable]
                return True

            return False



        def getRealmsSideEffect():
            return mockStorage._storage.keys()



        def removeRealmSideEffect(realm):
            del mockStorage._storage[realm]



        def createStoragePortionSideEffect(section = None, realm = None):
            return cls.__createMockStoragePortion(mockStorage, section or cls.DEFAULT_SECTION,
                                                  realm or cls.__DEFAULT_REALM)



        mockStorage = Mock(spec = IStorage)

        # initialize the internal attribute that will serve as the storage
        mockStorage._storage = storageState

        mockStorage.getValue.side_effect = getValueSideEffect
        mockStorage.saveValue.side_effect = saveValueSideEffect
        mockStorage.hasVariable.side_effect = hasVariableSideEffect
        mockStorage.tryRemoveVariable.side_effect = tryRemoveVariableSideEffect
        mockStorage.getRealms.side_effect = getRealmsSideEffect
        mockStorage.removeRealm.side_effect = removeRealmSideEffect
        mockStorage.createStoragePortion.side_effect = createStoragePortionSideEffect

        return mockStorage



    @staticmethod
    def __createMockStoragePortion(storage, defaultSection, realm):
        "Creates mock of the :class:`IStoragePortion` interface."

        def getValueSideEffect(variable, section = None):
            return storage.getValue(variable, section or mockStoragePortion.section, mockStoragePortion.realm)



        def saveValueSideEffect(variable, value, section = None):
            storage.saveValue(variable, value, section or mockStoragePortion.section, mockStoragePortion.realm)



        def hasVariableSideEffect(variable, section = None):
            return storage.hasVariable(variable, section or mockStoragePortion.section, mockStoragePortion.realm)



        def tryRemoveVariableSideEffect(variable, section = None):
            return storage.tryRemoveVariable(variable, section or mockStoragePortion.section, mockStoragePortion.realm)



        mockStoragePortion = Mock(spec_set = IStoragePortion)

        mockStoragePortion.realm = realm
        mockStoragePortion.section = defaultSection
        mockStoragePortion.getValue.side_effect = getValueSideEffect
        mockStoragePortion.saveValue.side_effect = saveValueSideEffect
        mockStoragePortion.hasVariable.side_effect = hasVariableSideEffect
        mockStoragePortion.tryRemoveVariable.side_effect = tryRemoveVariableSideEffect

        return mockStoragePortion



    @staticmethod
    def makeUserConfigDirectory():
        """Creates the user configuration directory and stores its path in the :class:`.ComponentTestContext` instance.

        :raise RuntimeError: If the user configuration directory was already created, i. e. the
           :attr:`.ComponentTestContext.userConfigDir` is not ``None``."""

        if ComponentTestUtils.getComponentTestContext().userConfigDir is not None:
            raise RuntimeError("User configuration directory already created.")

        ComponentTestUtils.getComponentTestContext().userConfigDir = tempfile.mkdtemp(
            prefix = "user_config", dir = ComponentTestUtils.getComponentTestContext().workDir)



    @staticmethod
    def removeUserConfigDirectory():
        """Removes the user configuration directory and its path from the :class:`.ComponentTestContext` instance."""

        shutil.rmtree(ComponentTestUtils.getComponentTestContext().userConfigDir)
        ComponentTestUtils.getComponentTestContext().userConfigDir = None



    @classmethod
    def _setUpClassConfigurationComponent(cls):
        ComponentTestUtils.setUpClassComponent()

        # although it is not necessary to create the directory since the class will create it we just reusing
        # the utility method here
        ConfigurationTestUtils.makeUserConfigDirectory()

        os.mkdir(os.path.join(ComponentTestUtils.getComponentTestContext().userConfigDir, cls.__STORAGE_SUBDIR))
        from ..._archiving.tests import ArchivingTestUtils

        # although it is not necessary to create the directory since the class will create it we just reusing
        # the utility method here
        ArchivingTestUtils.makeArchiveSpecsDirectory()



    @classmethod
    def _tearDownClassConfigurationComponent(cls):
        from ..._archiving.tests import ArchivingTestUtils
        ArchivingTestUtils.removeArchiveSpecsDirectory()
        os.rmdir(os.path.join(ComponentTestUtils.getComponentTestContext().userConfigDir, cls.__STORAGE_SUBDIR))
        ConfigurationTestUtils.removeUserConfigDirectory()

        ComponentTestUtils.tearDownClassComponent()



    @classmethod
    def _setUpConfigurationComponent(cls, options = None, userConfigFile = None):
        cls._mockInterfaceAccessor = MainfTestUtils.createMockInterfaceAccessor({})

        # create and set up the IMainfContext mock
        mockMainfContext = Mock(spec_set = IMainfContext)

        parser = OptionParser()
        parser.add_option(cls._makeCmdlineOption(Options.USER_CONFIG_DIR))
        cmdline = [cls._makeCmdlineOption(Options.USER_CONFIG_DIR) + "=" +
                   ComponentTestUtils.getComponentTestContext().userConfigDir]
        if userConfigFile:
            parser.add_option(cls._makeCmdlineOption(Options.USER_CONFIG_FILE))
            cmdline.append(cls._makeCmdlineOption(Options.USER_CONFIG_FILE) + "=" + userConfigFile)
        parser.add_option(cls._makeCmdlineOption(Options.ARCHIVE_SPECS_DIR))
        cmdline.append(cls._makeCmdlineOption(Options.ARCHIVE_SPECS_DIR) + "=" +
                       ComponentTestUtils.getComponentTestContext().archiveSpecsDir)
        options = parser.parse_args(cmdline, options)[0]

        mockMainfContext.appEnvironment = _AppEnvironment("test_aa", options, [])

        cls._mockInterfaceAccessor.registerComponentInterface(IMainfContext, mockMainfContext)

        ConfigurationComponent(cls._mockInterfaceAccessor)



    @classmethod
    def _tearDownConfigurationComponent(cls):
        cls._mockInterfaceAccessor = None



    @staticmethod
    def _makeCmdlineOption(option):
        return "--" + str(option)

    

    @classmethod
    def _removeStorageDirContent(cls):
        for realmFile in glob.iglob(os.path.join(
            ComponentTestUtils.getComponentTestContext().userConfigDir, cls.__STORAGE_SUBDIR, "*.realm")):
            os.remove(realmFile)

# }}} CLASSES

# configuration_test_utils.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2014 Róbert Čerňanský



""":class:`StorageTestUtils` class."""


__all__ = ["StorageTestUtils"]



# {{{ INCLUDES

from abc import ABCMeta, abstractmethod
import os
import glob

from mock import Mock

from AutoArchive._infrastructure.configuration import Options
from .._file_storage import FileStorage
from .._storage_portion import _StoragePortion
from AutoArchive.tests import ComponentTestUtils
from AutoArchive._infrastructure.configuration.tests import ConfigurationTestUtils

# }}} INCLUDES



# {{{ CLASSES

class StorageTestUtils(metaclass = ABCMeta):
    """Utility methods for Configuration component tests."""

    # Name of the default storage realm used if the realm is not specified.
    __DEFAULT_REALM = "TestDefaultRealm"

    # Name of the default storage section used if the section is not specified.
    DEFAULT_SECTION = "TestDefaultSection"

    # Subdirectory where the storage place its files.
    __STORAGE_SUBDIR = "storage"

    # Mock of the ApplicationContext.
    _applicationContextMock = None



    @abstractmethod
    def __init__(self):
        pass



    @classmethod
    def createMockStorage(cls, storageState):
        """Creates mock of the :class:`FileStorage` class.

        Mock is a functional implementation of the interface of :class:`FileStorage` which means that values saved to
        the storage can be read back.  Other interface methods works as expected as well.  Error cases may behave
        differently than defined by the interface.

        .. note:: Mock provides only transient storage, i. e. stored values exists as long as ``storageState`` exists;
           they are not persistent (saved to disk or so) as proper implementation should provide.

        :param storageState: A mutable instance where the mock stores its state (values of variables in sections and
           realms).  The type is ``dict<str: dict<str: dict<str: object>>>`` where the key (of the most outer
           dictionary) is realm name, and the value is dictionary with the key representing the section name
           and the value of variable name and value dictionary.
        :type storageState: ``dict<str: dict<str: dict<str: object>>>``

        :return: Mock of the :class:`FileStorage`.
        :rtype: :class:`mock.Mock<FileStorage>`"""

        def getValueSideEffect(variable, section = None, realm = None):
            return mockStorage._storage[realm or cls.__DEFAULT_REALM][section or cls.DEFAULT_SECTION][variable]



        def saveValueSideEffect(variable, value, section = None, realm = None):
            realm = realm or cls.__DEFAULT_REALM
            section = section or cls.DEFAULT_SECTION
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



        mockStorage = Mock(spec = FileStorage)

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



        mockStoragePortion = Mock(spec_set = _StoragePortion)

        mockStoragePortion.realm = realm
        mockStoragePortion.section = defaultSection
        mockStoragePortion.getValue.side_effect = getValueSideEffect
        mockStoragePortion.saveValue.side_effect = saveValueSideEffect
        mockStoragePortion.hasVariable.side_effect = hasVariableSideEffect
        mockStoragePortion.tryRemoveVariable.side_effect = tryRemoveVariableSideEffect

        return mockStoragePortion



    @classmethod
    def _setUpClassStorageComponent(cls):
        ComponentTestUtils.setUpClassComponent()

        ConfigurationTestUtils.makeUserConfigDirectory()
        os.mkdir(os.path.join(ComponentTestUtils.getComponentTestContext().userConfigDir, cls.__STORAGE_SUBDIR))



    @classmethod
    def _tearDownClassStorageComponent(cls):
        os.rmdir(os.path.join(ComponentTestUtils.getComponentTestContext().userConfigDir, cls.__STORAGE_SUBDIR))
        ConfigurationTestUtils.removeUserConfigDirectory()

        ComponentTestUtils.tearDownClassComponent()



    @classmethod
    def _setUpStorageComponent(cls):
        options = {Options.USER_CONFIG_DIR: ComponentTestUtils.getComponentTestContext().userConfigDir}
        configurationMock = ConfigurationTestUtils.createConfigurationMock(options)

        storage = FileStorage(configurationMock)

        from AutoArchive._application.archiving.tests import ArchivingTestUtils
        cls._applicationContextMock = ArchivingTestUtils._setUpApplicationContextMock(
            configurationMock = configurationMock, storage = storage)



    @classmethod
    def _tearDownStorageComponent(cls):
        cls._applicationContextMock = None



    @classmethod
    def _removeStorageDirContent(cls):
        for realmFile in glob.iglob(os.path.join(
            ComponentTestUtils.getComponentTestContext().userConfigDir, cls.__STORAGE_SUBDIR, "*.realm")):
            os.remove(realmFile)

# }}} CLASSES

# test_storage_portion.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2014 Róbert Čerňanský



""":class:`TestStoragePortion` class."""



__all__ = ["TestStoragePortion"]



# {{{ INCLUDES

import unittest
import mock

from .storage_test_utils import StorageTestUtils

# }}} INCLUDES



# {{{ CLASSES

class TestStoragePortion(unittest.TestCase):
    "Test of :class:`._StoragePortion`."

    @classmethod
    def setUpClass(cls):
        StorageTestUtils._setUpClassStorageComponent()



    @classmethod
    def tearDownClass(cls):
        StorageTestUtils._tearDownClassStorageComponent()



    def setUp(self):
        self.__storagePortion = None

        StorageTestUtils._setUpStorageComponent()
        self.__storagePortion = StorageTestUtils._applicationContextMock.storage.createStoragePortion()



    def tearDown(self):
        StorageTestUtils._removeStorageDirContent()
        StorageTestUtils._tearDownStorageComponent()



    # {{{ getValue() tests

    def test_getValueEmpty(self):
        """Tests the getValue() method with the empty storage.

        Tries to retrieve a value from an emtpy storage portion."""

        with self.assertRaises(KeyError):
            self.__storagePortion.getValue("TEST_VARIABLE")

    # }}} getValue() tests



    # {{{ saveValue() tests

    def test_saveValueDefaults(self):
        """Tests the saveValue() method with default section and realm.

        Saves an object to the storage with section unspecified, thus using default one.  Then it ensures
        that the retrieved value from the storage is the string representation of saved object."""

        variable = "TEST_VARIABLE"

        self.__storagePortion.saveValue(variable, mock.sentinel.testValue)
        self.assertEqual(self.__storagePortion.getValue(variable), str(mock.sentinel.testValue))



    def test_saveValueNoDefaults(self):
        """Tests the saveValue() method with a specified section and realm.

        Saves an object to the storage with section and realm specified.  Then it ensures that retrieved value from
        the same section and realm is the string representation of saved object."""

        variable = "TEST_VARIABLE"
        section = "TEST_SECTION"

        self.__storagePortion.saveValue(variable, mock.sentinel.testValue, section)
        self.assertEqual(self.__storagePortion.getValue(variable, section), str(mock.sentinel.testValue))

    # }}} saveValue() tests



    # {{{ hasVariable() tests

    def test_hasVariableEmpty(self):
        """Tests the hasVariable() method with the empty storage.

        Checks whether the method returns ``False`` for a variable."""

        self.assertFalse(self.__storagePortion.hasVariable("TEST_VARIABLE"))



    def test_hasVariableDefaults(self):
        """Tests the hasVariable() method with default section.

        Saves an object to the storage with section unspecified, thus using default one.  Then it checks
        whether ``True`` is returned when asked about the existence of the variable to which the object was saved."""

        variable = "TEST_VARIABLE"

        self.__storagePortion.saveValue(variable, None)
        self.assertTrue(self.__storagePortion.hasVariable(variable))

    # }}} hasVariable() tests



    # {{{ tryRemoveVariable() tests

    def test_tryRemoveVariableNonExistingSection(self):
        """Tests the tryRemoveVariable() method with section that does not exists.

        Saves an object to a variable.  Then it tries to remove the variable but in another, non-existing section."""

        variable = "TEST_VARIABLE"

        self.__storagePortion.saveValue(variable, None)
        with self.assertRaises(KeyError):
            self.__storagePortion.tryRemoveVariable(variable, "TEST_SECTION")



    def test_tryRemoveVariableExisting(self):
        """Tests the tryRemoveVariable() method with variable that do exists.

        Saves an object to a variable and then it tries to remove the same variable.  Checks whether ``True`` was
        returned and that the variable does not exists anymore."""

        variable = "TEST_VARIABLE"

        self.__storagePortion.saveValue(variable, None)
        self.assertTrue(self.__storagePortion.tryRemoveVariable(variable))
        self.assertFalse(self.__storagePortion.hasVariable(variable))



    def test_tryRemoveVariableNonExisting(self):
        """Tests the tryRemoveVariable() method with variable that do exists.

        Saves an object to a variable to some section and another object to another variable and section.  Then it
        tries to remove the first same variable but in second section section.  Checks whether ``False`` was
        returned."""

        variable1 = "TEST_VARIABLE1"
        variable2 = "TEST_VARIABLE2"

        self.__storagePortion.saveValue(variable1, None, "TEST_SECTION")
        self.__storagePortion.saveValue(variable2, None)
        self.assertFalse(self.__storagePortion.tryRemoveVariable(variable1))

    # }}} tryRemoveVariable() tests

# }}} CLASSES

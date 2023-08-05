# test_file_storage.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2014 Róbert Čerňanský



""":class:`TestFileStorage` class."""



__all__ = ["TestFileStorage"]



# {{{ INCLUDES

import unittest
import mock

from .storage_test_utils import StorageTestUtils

# }}} INCLUDES



# {{{ CLASSES

class TestFileStorage(unittest.TestCase):
    "Test of :class:`.IStorage` provided interface."

    @classmethod
    def setUpClass(cls):
        StorageTestUtils._setUpClassStorageComponent()



    @classmethod
    def tearDownClass(cls):
        StorageTestUtils._tearDownClassStorageComponent()



    def setUp(self):
        self.__storage = None

        StorageTestUtils._setUpStorageComponent()
        self.__storage = StorageTestUtils._applicationContextMock.storage



    def tearDown(self):
        StorageTestUtils._removeStorageDirContent()
        StorageTestUtils._tearDownStorageComponent()



    # {{{ getValue() tests

    def test_getValueEmpty(self):
        """Tests the getValue() method with the empty storage.

        Tries to retrieve a value from an emtpy storage."""

        with self.assertRaises(KeyError):
            self.__storage.getValue("TEST_VARIABLE")

    # }}} getValue() tests



    # {{{ saveValue() tests

    def test_saveValueDefaults(self):
        """Tests the saveValue() method with default section and realm.

        Saves an object to the storage with section and realm unspecified, thus using default ones.  Then it ensures
        that the retrieved value from the storage is the string representation of saved object."""

        variable = "TEST_VARIABLE"

        self.__storage.saveValue(variable, mock.sentinel.testValue)
        self.assertEqual(self.__storage.getValue(variable), str(mock.sentinel.testValue))



    def test_saveValueNoDefaults(self):
        """Tests the saveValue() method with a specified section and realm.

        Saves an object to the storage with section and realm specified.  Then it ensures that the retrieved value from
        the same section and realm is the string representation of saved object."""

        variable = "TEST_VARIABLE"
        section = "TEST_SECTION"
        realm = "TEST_REALM"

        self.__storage.saveValue(variable, mock.sentinel.testValue, section, realm)
        self.assertEqual(self.__storage.getValue(variable, section, realm), str(mock.sentinel.testValue))

    # }}} saveValue() tests



    # {{{ hasVariable() tests

    def test_hasVariableEmpty(self):
        """Tests the hasVariable() method with the empty storage.

        Checks whether the method returns ``False`` for a variable."""

        self.assertFalse(self.__storage.hasVariable("TEST_VARIABLE"))



    def test_hasVariableDefaults(self):
        """Tests the hasVariable() method with default section and realm.

        Saves an object to the storage with section and realm unspecified, thus using default ones.  Then it checks
        whether ``True`` is returned when asked about the existence of the variable to which the object was saved."""

        variable = "TEST_VARIABLE"

        self.__storage.saveValue(variable, None)
        self.assertTrue(self.__storage.hasVariable(variable))



    def test_hasVariableDefaultSection(self):
        """Tests the hasVariable() method with unspecified section.

        Saves an object to the storage with section unspecified.  Then it checks whether ``True`` is returned when
        asked about the existence of the variable to which the object was saved."""

        variable = "TEST_VARIABLE"
        realm = "TEST_REALM"

        self.__storage.saveValue(variable, mock.sentinel.testValue, realm = realm)
        self.assertTrue(self.__storage.hasVariable(variable, realm = realm))

    # }}} hasVariable() tests



    # {{{ tryRemoveVariable() tests

    def test_tryRemoveVariableNonExistingSection(self):
        """Tests the tryRemoveVariable() method with section that does not exists.

        Saves an object to a variable.  Then it tries to remove the variable but in another, non-existing section."""

        variable = "TEST_VARIABLE"

        self.__storage.saveValue(variable, None)
        with self.assertRaises(KeyError):
            self.__storage.tryRemoveVariable(variable, "TEST_SECTION")



    def test_tryRemoveVariableNonExistingRealm(self):
        """Tests the tryRemoveVariable() method with realm that does not exists.

        Saves an object to a variable.  Then it tries to remove the variable but in another, non-existing realm."""

        variable = "TEST_VARIABLE"

        self.__storage.saveValue(variable, None)
        with self.assertRaises(KeyError):
            self.__storage.tryRemoveVariable(variable, realm = "TEST_REALM")



    def test_tryRemoveVariableExisting(self):
        """Tests the tryRemoveVariable() method with variable that do exists.

        Saves an object to a variable and then it tries to remove the same variable.  Checks whether ``True`` was
        returned and that the variable does not exists anymore."""

        variable = "TEST_VARIABLE"

        self.__storage.saveValue(variable, None)
        self.assertTrue(self.__storage.tryRemoveVariable(variable))
        self.assertFalse(self.__storage.hasVariable(variable))



    def test_tryRemoveVariableNonExisting(self):
        """Tests the tryRemoveVariable() method with variable that do exists.

        Saves an object to a variable to some section and another object to another variable and section.  Then it
        tries to remove the first same variable but in second section section.  Checks whether ``False`` was
        returned."""

        variable1 = "TEST_VARIABLE1"
        variable2 = "TEST_VARIABLE2"

        self.__storage.saveValue(variable1, None, "TEST_SECTION")
        self.__storage.saveValue(variable2, None)
        self.assertFalse(self.__storage.tryRemoveVariable(variable1))

    # }}} tryRemoveVariable() tests



    # {{{ getRealms() tests

    def test_getRealmsEmpty(self):
        """Tests the getRealms() method with the empty storage.

        Retrieve realms from an emtpy storage and checks whether the returned Iterable is empty."""

        self.assertCountEqual(self.__storage.getRealms(), ())



    def test_getRealmsNonEmpty(self):
        """Tests the getRealms() method with the non-empty empty storage.

        Saves some variables into different realms.  Retrieve realms and checks whether the returned Iterable has same
        elements as the list of realms to which variables were saved to."""

        variable1 = "TEST_VARIABLE1"
        variable2 = "TEST_VARIABLE2"
        realm1 = "TEST_REALM1"
        realm2 = "TEST_REALM2"

        self.__storage.saveValue(variable1, None, realm = realm1)
        self.__storage.saveValue(variable2, None, realm = realm2)

        self.assertCountEqual(self.__storage.getRealms(), (realm1, realm2))

    # }}} getRealms() tests



    # {{{ removeRealm() tests

    def test_removeRealmEmpty(self):
        """Tests the removeRealm() method with the empty storage.

        Tries to remove a realm from the empty storage."""

        with self.assertRaises(KeyError):
            self.__storage.removeRealm("TEST_REALM")



    def test_removeRealm(self):
        """Tests the removeRealm() method.

        Saves a variable to a realm then removes that realm and checks whether it does not exists anymore."""

        variable = "TEST_VARIABLE"
        realm = "TEST_REALM"

        self.__storage.saveValue(variable, None, realm = realm)

        self.__storage.removeRealm(realm)
        self.assertNotIn(realm, self.__storage.getRealms())

    # }}} removeRealm() tests



    # {{{ createStoragePortion() tests

    def test_createStoragePortionDefault(self):
        """Tests the createStoragePortion() method with default section and realm.

        Creates storage portion with default section and realm."""

        self.assertIsNotNone(self.__storage.createStoragePortion())



    def test_createStoragePortion(self):
        """Tests the createStoragePortion() method.

        Creates storage portion defined section and realm."""

        section = "TEST_SECTION"
        realm = "TEST_REALM"

        storagePortion = self.__storage.createStoragePortion(section, realm)
        self.assertEqual(storagePortion.section, section)
        self.assertEqual(storagePortion.realm, realm)

    # }}} createStoragePortion() tests

# }}} CLASSES

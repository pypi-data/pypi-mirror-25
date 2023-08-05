# test_iinterface_accessor.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2011 Róbert Čerňanský



""":class:`TestIInterfaceAccessor` class."""



__all__ = ["TestIInterfaceAccessor"]



# {{{ INCLUDES

import unittest

from .. import *
from .mainf_test_utils import *

# }}} INCLUDES



# {{{ CLASSES

class TestIInterfaceAccessor(unittest.TestCase):
    "Test of :class:`.IInterfaceAccessor` provided interface."

    def setUp(self):
        self.__interfaceAccessor = None
        self.__componentInterfaceStub = None

        MainfTestUtils._setUpMainfComponent()
        self.__interfaceAccessor = MainfTestUtils._interfaceAccessor
        self.__componentInterfaceStub = self._ComponentInterfaceStub()



    def tearDown(self):
        MainfTestUtils._tearDownMainfComponent()



    def test_registerComponentInterface(self):
        """Test the registerComponentInterface method.

        Registers :class:`_ComponentInterfaceStub` to a :class:`.IInterfaceAccessor`-type instance then retrieves an
        object of the same type and checks whether it is the same instance as it was registered."""

        self.__interfaceAccessor.registerComponentInterface(self._ComponentInterfaceStub, self.__componentInterfaceStub)
        self.assertIs(self.__interfaceAccessor.getComponentInterface(
            self._ComponentInterfaceStub), self.__componentInterfaceStub)



    def test_unregisterComponentInterface(self):
        """Test the unregisterComponentInterface method.

        Registers and unregisters a type to a :class:`.IInterfaceAccessor`-type instance.  Tries to retrieve an object
        of the same type and checks whether :exc:`KeyError` was raised."""

        self.__interfaceAccessor.registerComponentInterface(self._ComponentInterfaceStub, self.__componentInterfaceStub)
        self.assertIs(self.__interfaceAccessor.getComponentInterface(
            self._ComponentInterfaceStub), self.__componentInterfaceStub)
        self.__interfaceAccessor.unregisterComponentInterface(self._ComponentInterfaceStub)
        with self.assertRaises(KeyError):
            self.__interfaceAccessor.getComponentInterface(self._ComponentInterfaceStub)



    class _ComponentInterfaceStub(IComponentInterface):
        "Stub implementation of IComponentInterface."

        def __init__(self):
            pass

# }}} CLASSES

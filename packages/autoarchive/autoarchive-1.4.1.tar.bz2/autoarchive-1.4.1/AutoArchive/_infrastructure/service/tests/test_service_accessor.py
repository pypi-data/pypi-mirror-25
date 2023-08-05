# test_service_accessor.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2014 Róbert Čerňanský



""":class:`TestServiceAccessor` class."""



__all__ = ["TestServiceAccessor"]



# {{{ INCLUDES

import unittest

from AutoArchive._infrastructure.py_additions import staticproperty
from .. import IServiceIdentification
from .._service_accessor import ServiceAccessor

# }}} INCLUDES



# {{{ CLASSES

class TestServiceAccessor(unittest.TestCase):
    "Test of :class:`ServiceAccessor` class."

    def setUp(self):
        self.__serviceAccessor = ServiceAccessor()



    def test_registerService(self):
        """Test service registration.

        Registers a service stub then retrieves it and checks that the returned service is instance of registered
        class."""

        providerIdentificationStub = _ProviderIdentificationStub()
        self.__serviceAccessor.registerService(_ServiceIdentificationStub, _ServiceStub1, providerIdentificationStub)

        service = self.__serviceAccessor.getOrCreateService(_ServiceIdentificationStub, providerIdentificationStub)

        self.assertIsInstance(service, _ServiceStub1, "Returned service provider instance is not of correct type.")



    def test_unregisterService(self):
        """Test service unregistration.

        Registers a service stub then unregisters it.  Operation should not throw an exception.  Then it registers
        the same service again.  If the unregistration was correct it should not throw an exception either."""

        providerIdentificationStub = _ProviderIdentificationStub()
        self.__serviceAccessor.registerService(_ServiceIdentificationStub, _ServiceStub1, providerIdentificationStub)

        self.__serviceAccessor.unregisterService(_ServiceIdentificationStub)
        self.__serviceAccessor.registerService(_ServiceIdentificationStub, _ServiceStub1, providerIdentificationStub)



    def test_getOrCreateServiceMultipleProviders(self):
        """Test getting a service when multiple providers are registered.

        Registers two service stubs then retrieves one specific and checks that the returned service is the correct
        one."""

        testProviderIdentificationStubs = (_ProviderIdentificationStub(), _ProviderIdentificationStub())
        self.__serviceAccessor.registerService(_ServiceIdentificationStub, _ServiceStub1,
                                               testProviderIdentificationStubs[0])
        self.__serviceAccessor.registerService(_ServiceIdentificationStub, _ServiceStub2,
                                               testProviderIdentificationStubs[1])

        service = self.__serviceAccessor.getOrCreateService(_ServiceIdentificationStub,
                                                            testProviderIdentificationStubs[1])

        self.assertIsInstance(service, _ServiceStub2, "Returned service provider instance is not of correct type.")



    def test_getProvidersIdentifications(self):
        testProviderIdentificationStubs = (_ProviderIdentificationStub(), _ProviderIdentificationStub())
        self.__serviceAccessor.registerService(_ServiceIdentificationStub, _ServiceStub1,
                                               testProviderIdentificationStubs[0])
        self.__serviceAccessor.registerService(_ServiceIdentificationStub, _ServiceStub2,
                                               testProviderIdentificationStubs[1])

        providerIdentifications = tuple(self.__serviceAccessor.getProvidersIdentifications(_ServiceIdentificationStub))

        self.assertSequenceEqual(testProviderIdentificationStubs, providerIdentifications,
                                 "Returned provider identifications does not match the registered ones.")



class _ServiceStubBase:
    def anyServiceMethod(self):
        pass


class _ServiceStub1(_ServiceStubBase):
    pass



class _ServiceStub2(_ServiceStubBase):
    pass



class _ProviderIdentificationStub:
    def someProviderIdentificationMethod(self):
        pass



class _ServiceIdentificationStub(IServiceIdentification):

    @staticproperty
    def interface():
        return _ServiceStubBase



    @staticproperty
    def providerIdentificationInterface():
        return _ProviderIdentificationStub

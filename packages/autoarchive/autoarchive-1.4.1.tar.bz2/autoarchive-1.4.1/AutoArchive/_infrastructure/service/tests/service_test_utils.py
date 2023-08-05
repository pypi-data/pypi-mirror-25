# service_test_utils.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2015 Róbert Čerňanský



""":class:`ServiceTestUtils` class."""



__all__ = ["ServiceTestUtils"]



# {{{ INCLUDES

from abc import ABCMeta, abstractmethod
from mock import Mock
from .._service_accessor import ServiceAccessor

# }}} INCLUDES



# {{{ CLASSES

class ServiceTestUtils(metaclass = ABCMeta):
    """Utility methods for service framework tests."""

    @abstractmethod
    def __init__(self):
        pass



    @staticmethod
    def createServiceAccessorMock(serviceStorage):
        """Creates mock of the :class:`.IServiceAccessor` interface.

        :param serviceStorage: Object to store registered services.
        :type serviceStorage: ``Dictionary``"""

        def getOrCreateServiceSideEffect(serviceIdentification, providerIdentification, *args):
            providers = serviceStorage[serviceIdentification]
            return [p[0](*args) for p in providers if p[1] == providerIdentification][0]



        def getProvidersIdentificationsSideEffect(serviceIdentification):
            return [provider[1] for provider in serviceStorage[serviceIdentification]]



        def registerServiceSideEffect(serviceIdentification, providerClass, providerIdentification = None):
            if serviceIdentification not in serviceStorage:
                serviceStorage[serviceIdentification] = []
            serviceStorage[serviceIdentification].append((providerClass, providerIdentification))



        serviceStorageMock = Mock(spec_set = ServiceAccessor)
        serviceStorageMock.getOrCreateService.side_effect = getOrCreateServiceSideEffect
        serviceStorageMock.getProvidersIdentifications.side_effect = getProvidersIdentificationsSideEffect
        serviceStorageMock.registerService.side_effect = registerServiceSideEffect

        return serviceStorageMock

# }}} CLASSES

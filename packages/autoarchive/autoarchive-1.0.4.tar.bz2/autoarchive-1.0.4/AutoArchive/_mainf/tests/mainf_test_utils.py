# mainf_test_utils.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2012 Róbert Čerňanský



""":class:`MainfTestUtils` class."""



__all__ = ["MainfTestUtils"]



# {{{ INCLUDES

from mock import Mock

from abc import *
from .. import *

# }}} INCLUDES



# {{{ CLASSES

class MainfTestUtils(metaclass = ABCMeta):
    """Utility methods for Mainf component tests."""

    _interfaceAccessor = None



    @abstractmethod
    def __init__(self):
        pass



    @staticmethod
    def createMockInterfaceAccessor(interfacesStorage):
        """Creates mock of the :class:`.IInterfaceAccessor` interface.

        :param interfacesStorage: The mock will use this object to store its internal data (which are in fact the
            registered interface types and their instances).
        :type interfacesStorage: ``dict<type: object>``

        :return: :class:`.IInterfaceAccessor` mock.
        :rtype: :class:`mock.Mock<IInterfaceAccessor>`"""

        def getComponentInterfaceSideEffect(interfaceType):
            return interfacesStorage[interfaceType]



        def registerComponentInterfaceSideEffect(interfaceType, instance):
            interfacesStorage[interfaceType] = instance



        def unregisterComponentInterfaceSideEffect(interfaceType):
            del interfacesStorage[interfaceType]



        mockInterfaceAccessor = Mock(spec_set = IInterfaceAccessor)
        mockInterfaceAccessor.getComponentInterface.side_effect = getComponentInterfaceSideEffect
        mockInterfaceAccessor.registerComponentInterface.side_effect = registerComponentInterfaceSideEffect
        mockInterfaceAccessor.unregisterComponentInterface.side_effect = unregisterComponentInterfaceSideEffect

        return mockInterfaceAccessor



    @classmethod
    def _setUpMainfComponent(cls, appEnvironment = None):
        from .._core.mainf_engine import MainfEngine
        mainfEngine = MainfEngine()

        # MainfEngine instantiates cls.__ComponentStub providing it with IInterfaceAccessor instance
        mainfEngine.addComponent(cls.__ComponentStub)

        mainfEngine.start(appEnvironment)



    @classmethod
    def _tearDownMainfComponent(cls):
        cls._interfaceAccessor = None



    class __ComponentStub(IComponent):
        """Stub implementation of class:`.IComponent`."""

        def __init__(self, interfaceAccessor):
            MainfTestUtils._interfaceAccessor = interfaceAccessor



        def run(self):
            return True

# }}} CLASSES

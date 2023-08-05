# _interface_accessor.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2011 Róbert Čerňanský



""":class:`_InterfaceAccessor` class."""



__all__ = ["_InterfaceAccessor"]



# {{{ INCLUDES

from .. import *

# }}} INCLUDES



# {{{ CLASSES

class _InterfaceAccessor(IInterfaceAccessor):
    ":class:`.IInterfaceAccessor` implementation."

    def __init__(self):

        # holds component interfaces in dictionary of type dict<type{IComponentInterface}: IComponentInterface>
        self.__interfaces = {}



    def getComponentInterface(self, interfaceType):
        "See: :meth:`.IInterfaceAccessor.getComponentInterface()`."

        self.__checkInterfaceType(interfaceType)
        return self.__interfaces[interfaceType]



    def registerComponentInterface(self, interfaceType, instance):
        "See: :meth:`.IInterfaceAccessor.registerComponentInterface()`."

        self.__checkInterfaceType(interfaceType)
        if not isinstance(instance, IComponentInterface):
            raise TypeError("interfaceType")

        if interfaceType in self.__interfaces:
            raise KeyError(str.format("Interface {} already registered.", interfaceType))

        self.__interfaces[interfaceType] = instance



    def unregisterComponentInterface(self, interfaceType):
        "See: :meth:`.IInterfaceAccessor.unregisterComponentInterface()`."

        self.__checkInterfaceType(interfaceType)
        del self.__interfaces[interfaceType]



    @staticmethod
    def __checkInterfaceType(interfaceType):
        if not issubclass(interfaceType, IComponentInterface):
            raise TypeError("interfaceType")

# }}} CLASSES

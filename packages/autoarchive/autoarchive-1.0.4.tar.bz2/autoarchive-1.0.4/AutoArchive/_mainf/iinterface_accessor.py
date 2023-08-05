# iinterface_accessor.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2011 Róbert Čerňanský



""":class:`IInterfaceAccessor and :class:`IComponentInterface` interfaces."""



__all__ = ["IInterfaceAccessor", "IComponentInterface"]



# {{{ INCLUDES

from abc import *

# }}} INCLUDES



# {{{ CLASSES

class IInterfaceAccessor(metaclass = ABCMeta):
    """Provides access to components public interfaces.

    A :term:`component` can make available its provided interfaces to other components by registering them via this
    interface.  Registered classes has to implement :class:`.IComponentInterface`.

    See also the description of _mainf package (:mod:`._mainf`)."""

    @abstractmethod
    def getComponentInterface(self, interfaceType):
        """Provides access to registered :term:`component` interfaces.

        See also: :meth:`registerComponentInterface`.

        :param interfaceType: Type of the desired interface.
        :type interfaceType: ``type{``:class:`.IComponentInterface`\ ``}``
        :return: Instance of ``interfaceType``.
        :rtype: ``interfaceType``

        :raise TypeError: If ``interfaceType`` does not implement :class:`.IComponentInterface`.
        :raise KeyError: If ``interfaceType`` is not registered."""



    @abstractmethod
    def registerComponentInterface(self, interfaceType, instance):
        """Registers a component public interface.

        Makes an interface available to other components by registering it.

        See also: :meth:`unregisterComponentInterface`,
        :meth:`getComponentInterface`.

        :param interfaceType: Type of registering instance.
        :type interfaceType: ``type{``:class:`.IComponentInterface`\ ``}``
        :param instance: An instance of a class implementing the ``interfaceType``.
        :type instance: :class:``.IComponentInterface``

        :raise TypeError: If ``interfaceType`` or ``instance`` does not implement :class:`.IComponentInterface`.
        :raise KeyError: If ``interfaceType`` is already registered."""



    @abstractmethod
    def unregisterComponentInterface(self, interfaceType):
        """Unregister a component interface.

        See also: :meth:`registerComponentInterface`,
        :meth:`getComponentInterface`

        :param interfaceType: Type of the instance that should be unregistered.
        :type interfaceType: ``type{``:class:`.IComponentInterface`\ ``}``

        :raise TypeError: If ``interfaceType`` does not implement :class:`.IComponentInterface`.
        :raise KeyError: If ``interfaceType`` is not registered."""



class IComponentInterface(metaclass = ABCMeta):
    """Tagging interface for components provided interfaces.

    See also: :class:`IInterfaceAccessor`."""

    @abstractmethod
    def __init__(self):
        pass

# }}} CLASSES

# icomponent.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2011 Róbert Čerňanský



""":class:`IComponent` interface."""



__all__ = ["IComponent"]



# {{{ INCLUDES

from abc import *

# }}} INCLUDES



# {{{ CLASSES

class IComponent(metaclass = ABCMeta):
    """Interface for components of :term:`Mainf` framework.

    Each :term:`component` of :term:`Mainf` framework has to implement this interface.  Components are managed by
    :class:`.MainfEngine` and can expose their interfaces via :class:`.IInterfaceAccessor`.

    During construction the :term:`component` can get and access other's components interfaces via
    ``interfaceAccessor``.  Using the same object it can register its own public interfaces as well.

    See also the description of _mainf package (:mod:`._mainf`).

    :param interfaceAccessor: Can be used to get/register public interfaces.
    :type interfaceAccessor: :class:`.IInterfaceAccessor`"""

    @abstractmethod
    def __init__(self, interfaceAccessor):
        pass



    @abstractmethod
    def run(self):
        """Runs the :term:`component`.

        Executes the work that the component is meant to do.

        :return: ``True``, if execution was successful.
        :rtype: ``bool``"""

# }}} CLASSES

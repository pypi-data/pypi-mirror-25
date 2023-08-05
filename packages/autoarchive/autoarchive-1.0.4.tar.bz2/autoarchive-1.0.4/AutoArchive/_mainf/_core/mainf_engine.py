# mainf_engine.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2011 Róbert Čerňanský



""":class:`MainfEngine` class."""



__all__ = ["MainfEngine"]



# {{{ INCLUDES

from ..._utils import *
from .. import *
from ._interface_accessor import *
from ._mainf_context import *

# }}} INCLUDES



# {{{ CLASSES

class MainfEngine:
    """Manages components and starts the program.

    Contains all components managed by the :term:`Mainf` framework.  Typically, components are added after
    instantiation of this class.  Usage of the class should be followed by calling its :meth:`start()` method which
    creates, initializes and runs components.

    See also the description of _mainf package (:mod:`._mainf`)."""

    def __init__(self):

        # list of managed IComponent classes
        self.__componentTypes = []



    def start(self, appEnvironment = None):
        """Starts the program.

        Creates and initializes components.  This method is typically called by a class or function exposed to the
        startup script.

        See also: :mod:`._mainf`, :class:`MainfEngine`.

        :param appEnvironment: An arbitrary object.  It will be available to components.
        :type appEnvironment: ``object``

        :return: Exit code of the program.
        :rtype: ``int``"""

        mainfContext = _MainfContext(appEnvironment)
        interfaceAccessor = _InterfaceAccessor()
        interfaceAccessor.registerComponentInterface(IMainfContext, mainfContext)

        try:
            components = self.__createComponents(interfaceAccessor)
            result = 0 if self.__runComponents(components) else 1
        except KeyboardInterrupt:
            print("\nAborted by user.")
            result = 1
        except Exception as ex:
            import traceback
            if _Constants.DEBUG:
                print(traceback.print_exc())
            else:
                _Utils.printError(str.format("Exception occurred: {}.", traceback.format_exception_only(type(ex), ex)))
            result = 1

        return result



    def addComponent(self, componentType):
        """Add a component to be managed by :term:`Mainf` framework.

        :param componentType: A component class that will be added.
        :type componentType: ``type{``:class:`.IComponent`\ ``}``

        :raise TypeError: If ``componentType`` does not implement :class:`.IComponent`."""

        if not issubclass(componentType, IComponent):
            raise TypeError("componentType")

        self.__componentTypes.append(componentType)



    def __createComponents(self, interfaceAccessor):
        components = []

        for componentClass in self.__componentTypes:
            components.append(componentClass(interfaceAccessor))

        return components



    def __runComponents(self, components):
        result = True
        for component in components:
            result = component.run() and result
        return result

# }}} CLASSES

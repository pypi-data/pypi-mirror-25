# iservice_component.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2014 Róbert Čerňanský



""":class:`IServiceComponent` interface."""



__all__ = ["IServiceComponent"]



# {{{ INCLUDES

from abc import *

# }}} INCLUDES



# {{{ CLASSES

class IServiceComponent(metaclass = ABCMeta):
    """Interface for service components.

    :param serviceAccessor: Can be used to get/register services.
    :type serviceAccessor: :class:`.IServiceAccessor`
    :param applicationContext: Application context.
    :type applicationContext: :class:`.ApplicationContext`"""



    @abstractmethod
    def __init__(self, applicationContext, serviceAccessor):
        pass



    @abstractmethod
    def destroyServices(self):
        """Destroys all services owned by this component."""

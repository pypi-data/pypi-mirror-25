# iservice.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2014 Róbert Čerňanský



""":class:`IService` interface."""



__all__ = ["IService"]



# {{{ INCLUDES

from abc import *

# }}} INCLUDES



# {{{ CLASSES

class IService(metaclass = ABCMeta):
    """Interface for component's services.

    See also: :class:`.ServiceAccessor`."""

    @abstractmethod
    def __init__(self):
        pass

# }}} CLASSES

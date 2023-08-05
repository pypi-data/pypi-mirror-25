# service_cleaner.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2012 Róbert Čerňanský



""":class:`ServiceCleaner` class."""



__all__ = ["ServiceCleaner"]



# {{{ INCLUDES

from abc import *
from .archiver import *

# }}} INCLUDES



# {{{ CONSTANTS

_SERVICE_CREATORS = frozenset({ArchiverServiceCreator})

# }}} CONSTANTS



# {{{ CLASSES

class ServiceCleaner(metaclass = ABCMeta):
    """Performs clean actions on services."""

    @abstractmethod
    def __init__(self):
        pass



    @staticmethod
    def cleanServices():
        """Puts services to the state before their creation.

        Existing instances of all services will be forgotten.  Subsequent request to get or create a service will
        result in creation of a new instance."""

        for serviceCreator in _SERVICE_CREATORS:
            serviceCreator.destroyServices()

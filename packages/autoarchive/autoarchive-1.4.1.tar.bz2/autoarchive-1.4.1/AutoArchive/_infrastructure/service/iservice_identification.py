# iservice_identification.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2014 Róbert Čerňanský



""":class:`IServiceIdentification` interface."""



__all__ = ["IServiceIdentification"]



# {{{ INCLUDES

from abc import *

# }}} INCLUDES



# {{{ CLASSES

class IServiceIdentification(metaclass = ABCMeta):
    """Identifies a service.

    .. Note:: Implementations should be static classes."""



    @abstractproperty
    def interface():
        """Gets interface type of the service.

        :rtype: ``type{``object``\ ``}``"""



    @abstractproperty
    def providerIdentificationInterface():
        """Gets interface type for accessing information about providers of this service.

        :rtype: ``type{``object``\ ``}``"""

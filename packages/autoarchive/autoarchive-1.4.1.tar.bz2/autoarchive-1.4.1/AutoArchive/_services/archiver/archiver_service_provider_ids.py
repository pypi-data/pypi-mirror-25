# archiver_service_provider_ids.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2014 Róbert Čerňanský



""":data:`ArchiverServiceProviderIDs` enum."""



__all__ = ["ArchiverServiceProviderIDs"]



# {{{ INCLUDES

from AutoArchive._infrastructure.py_additions import Enum

# }}} INCLUDES



# {{{ CONSTANTS

#: Implementations of the archiver service.
ArchiverServiceProviderIDs = Enum(

    #: Archiver service implementation using the python internal tar libraries.
    "TarInternal",

    #: Archiver service implementation using GNU tar binary.
    "TarExternal")

# }}} CONSTANTS

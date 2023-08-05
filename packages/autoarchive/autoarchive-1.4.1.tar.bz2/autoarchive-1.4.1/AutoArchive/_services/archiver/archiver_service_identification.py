# archiver_service_identification.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2014 Róbert Čerňanský



""":class:`ArchiverServiceIdentification` interface."""



__all__ = ["ArchiverServiceIdentification"]



# {{{ INCLUDES

from AutoArchive._infrastructure.py_additions import staticproperty
from AutoArchive._infrastructure.service import IServiceIdentification
from ._tar_archiver_provider_base import _TarArchiverProviderBase
from ._tar_archiver_provider_identification import _TarArchiverProviderIdentification

# }}} INCLUDES



# {{{ CLASSES

class ArchiverServiceIdentification(IServiceIdentification):
    """Identifies the Archiver service.

    Parameters required by the service upon creation:

       ``workDir``: Path to a writable directory.  The service will use it as persistent storage (type ``str``)."""

    @staticproperty
    def interface():
        """Gets interface type of the Archiver service.

        :rtype: ``type{``_TarArchiverProviderBase``\ ``}``"""

        return _TarArchiverProviderBase



    @staticproperty
    def providerIdentificationInterface():
        """Gets interface type for accessing information about providers of Archiver service.  Can be ``None``.

        :rtype: ``type{``_TarArchiverProviderIdentification``\ ``}``"""

        return _TarArchiverProviderIdentification

# }}} CLASSES

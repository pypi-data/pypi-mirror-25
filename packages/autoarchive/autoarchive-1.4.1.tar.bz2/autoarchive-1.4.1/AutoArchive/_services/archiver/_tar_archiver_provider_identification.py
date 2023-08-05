# _tar_archiver_provider_identification.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2014 Róbert Čerňanský



""":class:`_TarArchiverProviderIdentification`."""



__all__ = ["_TarArchiverProviderIdentification"]



# {{{ INCLUDES

from .archiver_service_provider_ids import ArchiverServiceProviderIDs
from ._internal_tar_archiver_provider import _InternalTarArchiverProvider
from ._external_tar_archiver_provider import _ExternalTarArchiverProvider

# }}} INCLUDES



# {{{ CLASSES

class _TarArchiverProviderIdentification:
    """Provides information about services defined in ``ArchiverServiceProviderIDs``.

    :param serviceProviderId: Identifier of the service that this instance shall provide information for.
    :type serviceProviderId: ``ArchiverServiceProviderIDs``."""

    __PROVIDER_TO_CLASS_MAP = {ArchiverServiceProviderIDs.TarInternal: _InternalTarArchiverProvider,
                               ArchiverServiceProviderIDs.TarExternal: _ExternalTarArchiverProvider}



    def __init__(self, serviceProviderId):
        self.__serviceProviderId = serviceProviderId



    @property
    def providerId(self):
        "See: :meth:`.IArchiverProviderIdentification.providerId`."

        return self.__serviceProviderId



    def getSupportedBackupTypes(self):
        "See: :meth:`.IArchiverProviderIdentification.getSupportedBackupTypes()`."

        return self.__PROVIDER_TO_CLASS_MAP[self.__serviceProviderId].supportedBackupTypes



    def getSupportedFeatures(self, backupType = None):
        "See: :meth:`.IArchiverProviderIdentification.getSupportedFeatures()`."

        return self.__PROVIDER_TO_CLASS_MAP[self.__serviceProviderId].getSupportedFeatures(backupType)

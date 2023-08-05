# archiver_service_component.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2014 Róbert Čerňanský



""":class:`ArchiverServiceComponent`."""



__all__ = ["ArchiverServiceComponent"]



# {{{ INCLUDES

from AutoArchive._infrastructure.service import IServiceComponent
from . import ArchiverServiceProviderIDs, ArchiverServiceIdentification
from ._internal_tar_archiver_provider import _InternalTarArchiverProvider
from ._external_tar_archiver_provider import _ExternalTarArchiverProvider
from ._tar_archiver_provider_identification import _TarArchiverProviderIdentification

# }}} INCLUDES



# {{{ CLASSES

class ArchiverServiceComponent(IServiceComponent):
    """Service component for archiver services.

    Registers service identified by :class:`.ArchiverServiceIdentification` with two providers of
    :class:`._TarArchiverProviderIdentification`-like interface."""

    def __init__(self, applicationContext, serviceAccessor):
        self.__serviceAccessor = serviceAccessor

        serviceAccessor.registerService(ArchiverServiceIdentification, _InternalTarArchiverProvider,
                                        _TarArchiverProviderIdentification(ArchiverServiceProviderIDs.TarInternal))
        serviceAccessor.registerService(ArchiverServiceIdentification, _ExternalTarArchiverProvider,
                                        _TarArchiverProviderIdentification(ArchiverServiceProviderIDs.TarExternal))



    def destroyServices(self):
        "See: :meth:`IServiceComponent.destroyServices()`"

        self.__serviceAccessor.unregisterService(ArchiverServiceIdentification)

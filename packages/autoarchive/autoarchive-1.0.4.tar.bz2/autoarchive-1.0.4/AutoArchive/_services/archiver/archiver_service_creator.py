# archiver_service_creator.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2012 Róbert Čerňanský



""":data:`ArchiverServiceProviders` enum and :class:`ArchiverServiceCreator` class."""



__all__ = ["ArchiverServiceProviders", "ArchiverServiceCreator"]



# {{{ INCLUDES

from abc import *

from ..._py_additions import *

from ._internal_tar_archiver_provider import *
from ._external_tar_archiver_provider import *

# }}} INCLUDES



# {{{ CONSTANTS

#: Implementations of the archiver service.
ArchiverServiceProviders = Enum(

    #: Archiver service implementation using the python internal tar libraries.
    "TarInternal",

    #: Archiver service implementation using GNU tar binary.
    "TarExternal")

# }}} CONSTANTS



# {{{ CLASSES

class ArchiverServiceCreator(metaclass = ABCMeta):
    """Creator of archiver service instances."""

    __PROVIDER_TO_CLASS_MAP = {ArchiverServiceProviders.TarInternal: _InternalTarArchiverProvider,
                               ArchiverServiceProviders.TarExternal: _ExternalTarArchiverProvider}

    __serviceInstances = {}



    @abstractmethod
    def __init__(self):
        pass



    @classmethod
    def getOrCreateArchiverService(cls, archiverServiceProvider, workDir):
        """Gets existing or creates the new archiver service instance.

        See also: :meth:`destroyServices()`.

        :param archiverServiceProvider: The requested service provider.
        :type archiverServiceProvider: :data:`ArchiverServiceProviders`
        :param workDir: Path to a directory which can be used to persistently store data.
        :type workDir: ``str``

        :return: Instance of an archiver service.
        :rtype: :class:`.IArchiver`

        :raise RuntimeError: If creation of the service provider failed."""

        providerClass = cls.__PROVIDER_TO_CLASS_MAP[archiverServiceProvider]
        if providerClass not in cls.__serviceInstances:
            try:
                cls.__serviceInstances[providerClass] = providerClass(workDir)
            except OSError as ex:
                raise RuntimeError(str.format("System error occurred while creating the archiver service: {}", ex))
        return cls.__serviceInstances[providerClass]



    @classmethod
    def getSupportedBackupTypes(cls, archiverServiceProvider):
        """Returns a set of backup types supported by the given archiver service provider.

        :param archiverServiceProvider: Service provider for which the backup types shall be returned.
        :type archiverServiceProvider: :data:`ArchiverServiceProviders`

        :return: Set of supported backup types.
        :rtype: ``set<BackupTypes>``"""

        return cls.__PROVIDER_TO_CLASS_MAP[archiverServiceProvider].supportedBackupTypes



    @classmethod
    def getSupportedFeatures(cls, archiverServiceProvider, backupType = None):
        """Returns a set of features supported by the given archiver service provider.

        :param archiverServiceProvider: Service provider for which the backup types shall be returned.
        :type archiverServiceProvider: :data:`ArchiverServiceProviders`
        :param backupType: The backup type for which the features shall be returned or ``None`` if all supported
           features shall be returned.
        :type backupType: :data:`BackupTypes`

        :return: Set of supported features.
        :rtype: ``set<ArchiverFeatures>``

        :raise ValueError: If the given ``backupType`` is not supported by the ``archiverServiceProvider``"""

        return cls.__PROVIDER_TO_CLASS_MAP[archiverServiceProvider].getSupportedFeatures(backupType)



    @classmethod
    def destroyServices(cls):
        """Removes all existing archiver service instances.

        Existing instances of all services will be forgotten.  Subsequent request to
        :meth:`getOrCreateArchiverService()` will result in creation of a new instance."""

        cls.__serviceInstances.clear()

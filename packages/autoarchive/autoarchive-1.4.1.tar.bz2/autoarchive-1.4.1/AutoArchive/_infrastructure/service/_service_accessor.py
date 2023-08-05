# _service_accessor.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2014 Róbert Čerňanský



""":class:`ServiceAccessor`."""



# {{{ CLASSES

# SMELL: Application layer can register.  Factor the registration out to a separate class?.
class ServiceAccessor:
    """Access to services.

    A service can be made available by registering via this interface.  Registered classes has to implement
    :class:`.IService`."""

    def __init__(self):

        # key is :class:`IServiceIdentification`, value is list of tuples (service provider class,
        # service provider identification)
        self.__services = {}

        # key is service provider class, value is its instance
        self.__serviceInstances = {}



    def getOrCreateService(self, serviceIdentification, providerIdentification, *args):
        """Provides access to registered services interfaces.

        See also: :meth:`registerInterface`.

        :param serviceIdentification: Identification of the service that shall be created.
        :type serviceIdentification: :class:`.IServiceIdentification`
        :param providerIdentification: Corresponding service provider identification object.  It should be one of the
          instances returned by :meth:`getProvidersIdentifications`.  For services with a single provider
          (implementation) it can be ``None``.
        :type providerIdentification: ``serviceIdentification.providerIdentificationInterface``
        :param args: Service specific arguments.
        :return: Instance of a service provider of the particular service.
        :rtype:  ``serviceIdentification.interface``

        :raise KeyError: If ``serviceIdentification`` is not registered."""

        providers = self.__findProviders(serviceIdentification)
        if len(self.__filterProvidersByIdentification(providers, providerIdentification)) == 0:
            raise KeyError(
                str.format("Service {} is not registered with service provider {}.", serviceIdentification,
                           providerIdentification))

        providerClass = self.__findProviderClass(providers, providerIdentification)

        if providerClass in self.__serviceInstances:
            serviceInstance = self.__serviceInstances[providerClass]
        else:
            serviceInstance = providerClass(*args)
            self.__serviceInstances[providerClass] = serviceInstance

        return serviceInstance



    def getProvidersIdentifications(self, serviceIdentification):
        """Returns providers identifications for the given service.

        :param serviceIdentification: Identification of the service.
        :type serviceIdentification: :class:`.IServiceIdentification`
        :return: Service providers.
        :rtype: ``iterable<serviceIdentification.providerIdentificationInterface>``

        :raise KeyError: If ``serviceIdentification`` is not registered."""

        return (p[1] for p in self.__findProviders(serviceIdentification))



    def registerService(self, serviceIdentification, providerClass, providerIdentification = None):
        """Registers a service.

        See also: :meth:`unregisterService`, :meth:`getOrCreateService`.

        :param serviceIdentification: Identification of the service that shall be registered.
        :type serviceIdentification: :class:`.IServiceIdentification`
        :param providerClass: Provider of the service.
        :type providerClass: ``type{`` ``serviceIdentification.interface``, :class:`IService`\ ``}``
        :param providerIdentification: Corresponding service provider identification object.
        :type providerIdentification: ``serviceIdentification.providerIdentificationInterface``

        :raise TypeError: If ``providerClass`` does not implement ``serviceIdentification.interface``.  If
          ``providerIdentification`` does not implement ``serviceIdentification.providerIdentificationInterface``.
        :raise KeyError: If ``serviceIdentification`` is already registered with ``providerClass`` or
          ``providerIdentification``."""

        if not issubclass(providerClass, serviceIdentification.interface):
            raise TypeError("providerClass")
        if providerIdentification is not None and not isinstance(
                providerIdentification, serviceIdentification.providerIdentificationInterface):
            raise TypeError("serviceProviderInfo")

        providers = self.__tryFindProviders(serviceIdentification)
        if providers is None:
            providers = []
            self.__services[serviceIdentification] = providers

        if len(self.__filterProvidersByIdentification(providers, providerIdentification)) > 0:
            raise KeyError(
                str.format("Service {} is already registered with service provider info {}.", serviceIdentification,
                           providerIdentification))
        if len(self.__filterProvidersByClass(providers, providerClass)) > 0:
            raise KeyError(
                str.format("Service {} is already registered with service provider class {}.", serviceIdentification,
                           providerClass))

        self.__services[serviceIdentification].append((providerClass, providerIdentification))



    def unregisterService(self, serviceIdentification):
        """Unregisters a service with all its providers.

        All serviceType instances all destroyed first.

        See also: :meth:`registerService`, :meth:`getOrCreateService`.

        :param serviceIdentification: Identification of the service that shall be registered.
        :type serviceIdentification: :class:`.IServiceIdentification`

        :raise KeyError: If ``serviceIdentification`` is not registered."""

        self.__destroyServiceInstances(serviceIdentification)
        del self.__services[self.__findService(serviceIdentification)]



    def __destroyServiceInstances(self, serviceIdentification):
        "Destroys service instances if any."

        providers = self.__findProviders(serviceIdentification)
        for provider in providers:
            if provider[0] in self.__serviceInstances:
                del self.__serviceInstances[provider[0]]



    def __findProviders(self, serviceIdentification):
        return self.__services[self.__findService(serviceIdentification)]



    def __tryFindProviders(self, serviceIdentification):
        if serviceIdentification not in self.__services:
            return None
        return self.__services[serviceIdentification]



    def __findService(self, serviceIdentification):
        if serviceIdentification not in self.__services:
            raise KeyError(str.format("Service {} is not registered", serviceIdentification))
        return serviceIdentification



    @classmethod
    def __findProviderClass(cls, providers, providerIdentification):
        provider = cls.__filterProvidersByIdentification(providers, providerIdentification)[0]
        return provider[0]



    @staticmethod
    def __filterProvidersByIdentification(providers, providerIdentification):
        return [p for p in providers if p[1] == providerIdentification]



    @staticmethod
    def __filterProvidersByClass(providers, providerClass):
        return [p for p in providers if p[0] == providerClass]

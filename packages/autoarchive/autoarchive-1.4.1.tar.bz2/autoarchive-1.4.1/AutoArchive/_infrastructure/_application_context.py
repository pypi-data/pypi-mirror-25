# _application_context.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2014 Róbert Čerňanský



""":class:`ApplicationContext` class."""



__all__ = ["ApplicationContext"]



# {{{ CLASSES

class ApplicationContext:
    """Provides access to a various program-related objects.

    :param appEnvironment: Object that will be made available via :attr:`appEnvironment` property.
    :type appEnvironment: ``object``
    :param configuration: Application configuration.
    :type configuration: :class:`.IConfiguration`
    :param storage: Application storage.
    :type storage: :class:`.FileStorage`"""



    def __init__(self, appEnvironment, configuration, storage):
        self.__appEnvironment = appEnvironment
        self.__configuration = configuration
        self.__storage = storage



    @property
    def appEnvironment(self):
        """Gets the application environment object.

        :rtype: ``object``"""

        return self.__appEnvironment



    @property
    def configuration(self):
        """Gets access to application configuration.

        :rtype: :class:`.ConfigurationBase`

        .. warning:: Can be ``None``"""

        return self.__configuration



    @property
    def storage(self):
        """Gets access to application persistent storage.

        :rtype: :class:`.FileStorage`

        .. warning:: Can be ``None``"""

        return self.__storage

# }}} CLASSES

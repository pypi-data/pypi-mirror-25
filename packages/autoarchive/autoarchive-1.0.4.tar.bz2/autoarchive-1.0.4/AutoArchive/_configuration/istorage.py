# istorage.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2011 Róbert Čerňanský



""":class:`IStorage` interface."""



__all__ = ["IStorage"]



# {{{ INCLUDES

from abc import *
from .._mainf import *

# }}} INCLUDES



# {{{ CLASSES

class IStorage(IComponentInterface):
    """Provides access to a persistent storage.

    Stored content shall not be lost between program runs."""

    @abstractmethod
    def getValue(self, variable, section = None, realm = None):
        """Returns a cached value from the persistent storage.

        :param variable: The name of the variable which value shall be read.
        :type variable: ``str``
        :param section: Name of a section within a realm.
        :type section: ``str``
        :param realm: Name of a separate storage entity (typically represented by a file).
        :type realm: ``str``

        :return: Value of the passed ``variable``.
        :rtype: ``str``

        :raise KeyError: If ``variable``, ``section`` or ``realm`` does not
           exists."""



    @abstractmethod
    def saveValue(self, variable, value, section = None, realm = None):
        """Saves a value to the persistent storage.

        A value passed as ``value`` parameter will be saved to the persistent storage under the name passed as
        ``variable`` argument.

        .. note:: A string representation of the value is saved (str(value)).

        :param variable: The name under which the value will be saved.
        :type variable: ``str``
        :param value: The value that shall be saved.
        :type value: ``object``
        :param section: Name of a section within a realm.
        :type section: ``str``
        :param realm: Name of a separate storage entity (typically represented by a file).
        :type realm: ``str``"""



    @abstractmethod
    def hasVariable(self, variable, section = None, realm = None):
        """Returns ``True`` if the storage contains ``variable``.

        :param variable: Name of the variable which presence shall be determined.
        :type variable: ``str``
        :param section: Name of a section within a realm.
        :type section: ``str``
        :param realm: Name of a separate storage entity (typically represented by a file).
        :type realm: ``str``

        :return: ``True`` if ``variable`` is present in the storage.
        :rtype: ``bool``"""



    @abstractmethod
    def tryRemoveVariable(self, variable, section = None, realm = None):
        """Removes variable from the persistent storage.

        If variable existed to be removed, returns ``True``; otherwise return ``False``.

        :param variable: The name of the variable which value shall be removed.
        :type variable: ``str``
        :param section: Name of a section within a realm.
        :type section: ``str``
        :param realm: Name of a separate storage entity (typically represented by a file).
        :type realm: ``str``

        :return: ``True`` if variable existed; ``False`` otherwise.
        :rtype: ``bool``

        :raise KeyError: If ``section`` or ``realm`` does not exists."""



    @abstractmethod
    def getRealms(self):
        """Returns all realms that exists in the storage.

        :return: Iterable of realm names.
        :rtype: ``Iterable<str>``"""



    @abstractmethod
    def removeRealm(self, realm):
        """Deletes the ``realm`` including all information that contains from the persistent storage.

        :param realm: Name of a separate storage entity (typically represented by a file).
        :type realm: ``str``

        :raise KeyError: If ``realm`` does not exists.
        :raise OSError: If an error occurred during the operation of removing data from a physical storage."""



    @abstractmethod
    def createStoragePortion(self, section = None, realm = None):
        """Returns IStoragePortion instance set to ``section`` and ``realm``.

        .. note:: If ``section`` or ``realm`` does not exists the implementation should not create either of them right
           away but rather on first value save.

        :param section: Name of a section within a realm.
        :type section: ``str``
        :param realm: Name of a separate storage entity (typically represented by a file).
        :type realm: ``str``

        :return: :class:`.IStoragePortion` instance
        :rtype: :class:`.IStoragePortion`"""

# }}} CLASSES

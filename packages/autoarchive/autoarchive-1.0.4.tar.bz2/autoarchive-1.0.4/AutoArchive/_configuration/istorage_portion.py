# istorage_portion.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2011 Róbert Čerňanský



""":class:`IStoragePortion` interface."""



__all__ = ["IStoragePortion"]



# {{{ INCLUDES

from abc import *

# }}} INCLUDES



# {{{ CLASSES

class IStoragePortion(metaclass = ABCMeta):
    """Provides access to a part of the persistent storage.

    Portion of the :class:`.IStorage` that can be accessed is defined by :attr:`realm` and :attr:`section`.  While the
    :attr:`section` can be changed dynamically, :attr:`realm` can not be changed for entire lifetime of the
    :class:`IStoragePortion`-type object."""

    @abstractproperty
    def realm(self):
        """Gets the realm in which this :class:`IStoragePortion` instance operates.

        :rtype: ``str``"""



    @abstractproperty
    def section(self):
        """Gets or sets the section in which this :class:`IStoragePortion` instance operates by default.

        :rtype: ``str``"""



    @abstractmethod
    def getValue(self, variable, section = None):
        """Returns a cached value from the persistent storage.

        :param variable: The name of the variable which value shall be read.
        :type option: ``str``
        :param section: Name of a section within :attr:`realm`.
        :type section: ``str``

        :return: Value of the passed ``variable``.
        :rtype: ``str``

        :raise KeyError: If ``variable`` or ``section`` does not exists."""



    @abstractmethod
    def saveValue(self, variable, value, section = None):
        """Saves a value to the persistent storage.

        A value passed as ``value`` parameter will be saved to a persistent storage under the name passed as
        ``variable`` argument.

        .. note:: A string representation of the value is saved (str(value)).

        :param variable: The name under which the value will be saved.
        :type variable: ``str``
        :param value: The value that shall be saved.
        :type value: ``object``
        :param section: Name of a section within :attr:`realm`.
        :type section: ``str``"""



    @abstractmethod
    def hasVariable(self, variable, section = None):
        """Returns ``true`` if the storage contains ``variable``.

        :param variable: Name of the variable which presence shall be determined.
        :type variable: ``str``
        :param section: Name of a section within a realm.
        :type section: ``str``

        :return: ``true`` if ``variable`` is present in the storage.
        :rtype: ``bool``"""



    @abstractmethod
    def tryRemoveVariable(self, variable, section = None):
        """Removes variable from the persistent storage.

        If variable existed to be removed, returns ``True``; otherwise return ``False``.

        :param variable: The name of the variable which value shall be removed.
        :type option: ``str``
        :param section: Name of a section within :attr:`realm`.
        :type section: ``str``

        :return: ``True`` if variable existed; ``False`` otherwise.
        :rtype: ``bool``

        :raise KeyError: If ``section`` does not exists."""

# }}} CLASSES

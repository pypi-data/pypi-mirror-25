# _storage_portion.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2014 Róbert Čerňanský



""":class:`_StoragePortion` class."""



__all__ = ["_StoragePortion"]



# {{{ CLASSES

class _StoragePortion:
    """Provides access to a part of the persistent storage.

    Portion of a storage (which can be any :class:`.FileStorage`-like class) that can be accessed is defined by
    :attr:`realm` and :attr:`section`.  While the :attr:`section` can be changed dynamically, :attr:`realm` can not
    be changed for entire lifetime of the :class:`_StoragePortion`-type object.

    See also: :class:`.FileStorage`.

    :param storage: Storage which portion shall this instance provide access to.
    :type storage: :class:`.FileStorage`
    :param section: Section that shall be accessed by default.
    :type section: ``str``
    :param realm: Realm that this portion shall provide access to.
    :type realm: ``str``"""

    def __init__(self, storage, section, realm):
        self.__storage = storage
        self.__section = section
        self.__realm = realm



    @property
    def realm(self):
        """Gets the realm in which this :class:`IStoragePortion` instance operates.

        :rtype: ``str``"""

        return self.__realm



    @property
    def section(self):
        """Gets or sets the section in which this :class:`IStoragePortion` instance operates by default.

        :rtype: ``str``"""

        return self.__section

    @section.setter
    def section(self, value):
        "Setter for :attr:`section`."

        self.__section = value



    def getValue(self, variable, section = None):
        """Returns a cached value from the persistent storage.

        :param variable: The name of the variable which value shall be read.
        :type variable: ``str``
        :param section: Name of a section within :attr:`realm`.
        :type section: ``str``

        :return: Value of the passed ``variable``.
        :rtype: ``str``

        :raise KeyError: If ``variable`` or ``section`` does not exists."""

        section = section or self.section
        return self.__storage.getValue(variable, section, self.realm)



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

        section = section or self.section
        self.__storage.saveValue(variable, value, section, self.realm)



    def hasVariable(self, variable, section = None):
        """Returns ``true`` if the storage contains ``variable``.

        :param variable: Name of the variable which presence shall be determined.
        :type variable: ``str``
        :param section: Name of a section within a realm.
        :type section: ``str``

        :return: ``true`` if ``variable`` is present in the storage.
        :rtype: ``bool``"""

        section = section or self.section
        return self.__storage.hasVariable(variable, section, self.realm)



    def tryRemoveVariable(self, variable, section = None):
        """Removes variable from the persistent storage.

        If variable existed to be removed, returns ``True``; otherwise return ``False``.

        :param variable: The name of the variable which value shall be removed.
        :type variable: ``str``
        :param section: Name of a section within :attr:`realm`.
        :type section: ``str``

        :return: ``True`` if variable existed; ``False`` otherwise.
        :rtype: ``bool``

        :raise KeyError: If ``section`` does not exists."""

        section = section or self.section
        return self.__storage.tryRemoveVariable(variable, section, self.realm)

# }}} CLASSES

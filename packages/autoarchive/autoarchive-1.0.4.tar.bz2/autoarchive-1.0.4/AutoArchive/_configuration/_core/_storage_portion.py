# _storage_portion.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2011 Róbert Čerňanský



""":class:`_StoragePortion` class."""



__all__ = ["_StoragePortion"]



# {{{ INCLUDES

from .. import *

# }}} INCLUDES



# {{{ CLASSES

class _StoragePortion(IStoragePortion):
    """Portion of the application's persistent storage.

    See also: :class:`.FileStorage`.

    :param storage: :class:`.IStorage` which portion shall this instance provide access to.
    :type storage: :class:`.IStorage`
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
        "See: :attr:`.IStoragePortion.realm`."

        return self.__realm



    @property
    def section(self):
        "See: :attr:`.IStoragePortion.section`."

        return self.__section

    @section.setter
    def section(self, value):
        "See: :attr:`.IStoragePortion.section`."

        self.__section = value



    def getValue(self, variable, section = None):
        "See: :meth:`.IStoragePortion.getValue()`."

        section = section or self.section
        return self.__storage.getValue(variable, section, self.realm)



    def saveValue(self, variable, value, section = None):
        "See: :meth:`.IStoragePortion.saveValue()`."

        section = section or self.section
        self.__storage.saveValue(variable, value, section, self.realm)



    def hasVariable(self, variable, section = None):
        "See: :meth:`.IStoragePortion.hasVariable()`."

        section = section or self.section
        return self.__storage.hasVariable(variable, section, self.realm)



    def tryRemoveVariable(self, variable, section = None):
        "See: :meth:`.IStoragePortion.tryRemoveVariable()`."

        section = section or self.section
        return self.__storage.tryRemoveVariable(variable, section, self.realm)

# }}} CLASSES

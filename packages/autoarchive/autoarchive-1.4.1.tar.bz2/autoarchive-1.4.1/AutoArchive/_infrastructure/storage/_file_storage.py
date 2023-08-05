# _file_storage.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2014 Róbert Čerňanský



""":class:`FileStorage` class."""



__all__ = ["FileStorage"]



# {{{ INCLUDES

import os.path
import glob
import configparser

from AutoArchive._infrastructure.utils import Utils
from AutoArchive._infrastructure.configuration import Options
from ._storage_portion import _StoragePortion

# }}} INCLUDES



# {{{ CLASSES

class FileStorage:
    """Application's persistent storage.

    Provides access to application's persistent storage.  Any arbitrary variables can be saved to it.  Data are stored
    in text files.

    This storage implementation utilizes local filesystem, specifically a subdirectory of
    :term:`user configuration directory` named ``storage``.  Data are stored in text files.  The directory is
    automatically created if it does not exists.  Storage content is read upon construction and cached into memory.
    This class does not provide any means to re-read the storage content from disk.

    .. note:: This class can be instantiated only once.

    :param configuration: Application configuration.
    :type configuration: :class:`.IConfiguration`"""

    __STORAGE_SUBDIR = "storage"
    __REALM_SUFFIX = "realm"
    __DEFAULT_SECTION = "AutoArchive"
    __DEFAULT_REALM = "default"

    # ``True`` if an instance of this class was already created.
    __instantiated = False



    def __init__(self, configuration):
        if self.__instantiated:
            raise RuntimeError("Instance already created.")
        self.__instantiated = True

        # dictionary of realm name as the key and ConfigParser instance as the value
        self.__storage = {}

        self.__storageDir = os.path.join(configuration[Options.USER_CONFIG_DIR], self.__STORAGE_SUBDIR)

        if not os.path.exists(self.__storageDir):
            if not configuration[Options.QUIET]:
                Utils.printWarning(str.format("Storage directory does not exists. Creating \"{}\".",
                                               self.__storageDir))
            os.makedirs(self.__storageDir)

        for storageFile in glob.iglob(self.__storageDir + os.path.sep + "*." + self.__REALM_SUFFIX):
            storage = configparser.RawConfigParser()
            storage.read(storageFile)
            self.__storage[os.path.splitext(os.path.basename(storageFile))[0]] = storage



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

        section = section or self.__DEFAULT_SECTION
        realm = realm or self.__DEFAULT_REALM

        try:
            return self.__storage[realm].get(section, variable)
        except Exception as ex:
            self.__handleStorageOperationException(ex, variable, section, realm)



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

        section = section or self.__DEFAULT_SECTION
        realm = realm or self.__DEFAULT_REALM

        if realm not in self.__storage.keys():
            self.__storage[realm] = configparser.RawConfigParser()
        storage = self.__storage[realm]

        if not storage.has_section(section):
            storage.add_section(section)

        storage.set(section, variable, str(value))
        with open(self.__getStorageFile(realm), "w") as sf:
            storage.write(sf)



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

        section = section or self.__DEFAULT_SECTION
        realm = realm or self.__DEFAULT_REALM

        if realm not in self.__storage.keys():
            return False
        if not self.__storage[realm].has_section:
            return False
        return self.__storage[realm].has_option(section, variable)



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

        section = section or self.__DEFAULT_SECTION
        realm = realm or self.__DEFAULT_REALM

        try:
            return self.__storage[realm].remove_option(section, variable)
        except Exception as ex:
            self.__handleStorageOperationException(ex, variable, section, realm)



    def getRealms(self):
        """Returns all realms that exists in the storage.

        :return: Iterable of realm names.
        :rtype: ``Iterable<str>``"""

        return self.__storage.keys()



    def removeRealm(self, realm):
        """Deletes the ``realm`` including all information that contains from the persistent storage.

        :param realm: Name of a separate storage entity (typically represented by a file).
        :type realm: ``str``

        :raise KeyError: If ``realm`` does not exists.
        :raise OSError: If an error occurred during the operation of removing data from a physical storage."""

        del self.__storage[realm]
        os.remove(self.__getStorageFile(realm))



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

        section = section or self.__DEFAULT_SECTION
        realm = realm or self.__DEFAULT_REALM
        return _StoragePortion(self, section, realm)



    # {{{ helpers

    @staticmethod
    def __handleStorageOperationException(exception, variable, section, realm):
        try:
            raise exception
        except configparser.NoOptionError:
            raise KeyError(str.format(
                    "No such variable '{}' in storage realm '{}' and section '{}'.", variable, realm, section))
        except KeyError:
            raise KeyError(str.format("No such realm in the storage: {}.", realm))
        except configparser.NoSectionError:
            raise KeyError(str.format("No such section '{}' in storage realm '{}'.", section, realm))



    def __getStorageFile(self, realm):
        return os.path.join(self.__storageDir, realm + "." + self.__REALM_SUFFIX)

    # }}} helpers

# }}} CLASSES

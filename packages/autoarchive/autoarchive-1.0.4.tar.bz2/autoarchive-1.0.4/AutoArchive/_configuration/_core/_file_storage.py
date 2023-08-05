# _file_storage.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2011 Róbert Čerňanský



""":class:`_FileStorage` class."""



__all__ = ["_FileStorage"]



# {{{ INCLUDES

import os.path
import glob
import configparser

from ..._utils import *
from .. import *
from ._storage_portion import *

# }}} INCLUDES



# {{{ CLASSES

class _FileStorage(IStorage):
    """Application's persistent storage.

    Provides access to application's persistent storage.  Any arbitrary variables can be saved to it.  Data are stored
    in text files.

    Storage content is read upon construction and cached into memory.  This class does not provide any means to re-read
    the storage content from disk.

    :param userConfigDir: Path to the user configuration directory.
    :type userConfigDir: ``str``"""

    __STORAGE_SUBDIR = "storage"
    __REALM_SUFFIX = "realm"
    __DEFAULT_SECTION = "AutoArchive"
    __DEFAULT_REALM = "default"



    def __init__(self, userConfigDir, quiet):

        # dictionary of realm name as the key and ConfigParser instance as the value
        self.__storage = {}

        self.__storageDir = os.path.join(userConfigDir, self.__STORAGE_SUBDIR)

        if not os.path.exists(self.__storageDir):
            if not quiet:
                _Utils.printWarning(str.format("Storage directory does not exists. Creating \"{}\".",
                                               self.__storageDir))
            os.makedirs(self.__storageDir)

        for storageFile in glob.iglob(self.__storageDir + os.path.sep + "*." + self.__REALM_SUFFIX):
            storage = configparser.RawConfigParser()
            storage.read(storageFile)
            self.__storage[os.path.splitext(os.path.basename(storageFile))[0]] = storage



    # {{{ IStorage implementation

    def getValue(self, variable, section = None, realm = None):
        "See: :meth:`.IStorage.getValue()`."

        section = section or self.__DEFAULT_SECTION
        realm = realm or self.__DEFAULT_REALM

        try:
            return self.__storage[realm].get(section, variable)
        except Exception as ex:
            self.__handleStorageOperationException(ex, variable, section, realm)



    def saveValue(self, variable, value, section = None, realm = None):
        "See: :meth:`.IStorage.saveValue()`."

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
        "See: :meth:`.IStorage.hasVariable()`."

        section = section or self.__DEFAULT_SECTION
        realm = realm or self.__DEFAULT_REALM

        if realm not in self.__storage.keys():
            return False
        if not self.__storage[realm].has_section:
            return False
        return self.__storage[realm].has_option(section, variable)



    def tryRemoveVariable(self, variable, section = None, realm = None):
        "See: :meth:`.IStorage.tryRemoveVariable()`."

        section = section or self.__DEFAULT_SECTION
        realm = realm or self.__DEFAULT_REALM

        try:
            return self.__storage[realm].remove_option(section, variable)
        except Exception as ex:
            self.__handleStorageOperationException(ex, variable, section, realm)



    def getRealms(self):
        "See: :meth:`.IStorage.getRealms()`."

        return self.__storage.keys()



    def removeRealm(self, realm):
        "See: :meth:`.IStorage.removeRealm()`."

        del self.__storage[realm]
        os.remove(self.__getStorageFile(realm))



    def createStoragePortion(self, section = None, realm = None):
        "See: :meth:`.IStorage.createStoragePortion()`."

        section = section or self.__DEFAULT_SECTION
        realm = realm or self.__DEFAULT_REALM
        return _StoragePortion(self, section, realm)

    # }}} IStorage implementation



    # {{{ helpers

    def __handleStorageOperationException(self, exception, variable, section, realm):
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

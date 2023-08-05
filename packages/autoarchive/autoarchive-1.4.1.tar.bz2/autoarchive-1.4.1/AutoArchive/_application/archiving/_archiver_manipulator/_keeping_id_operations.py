# _keeping_id_operations.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2014 Róbert Čerňanský



""":class:`_KeepingIdOperations` class."""



__all__ = ["_KeepingIdOperations"]



# {{{ INCLUDES

from AutoArchive._infrastructure.py_additions import *

# }}} INCLUDES



# {{{ CLASSES

class _KeepingIdOperations:
    __BASE = 26
    __NUMERALS = [chr(nmr) for nmr in range(ord("a"), ord("z") + 1)]
    __MAX_KEEPING_ID = "zz"



    @classproperty
    def maxKeepingIdAsInt(cls):
        return cls.keepingIdToInt(cls.__MAX_KEEPING_ID)



    @classmethod
    def getNextKeepingId(cls, keepingId = None):
        if keepingId is None:
            return cls.intToKeepingId(0)
        else:
            return cls.intToKeepingId(cls.keepingIdToInt(keepingId) + 1)



    @classmethod
    def keepingIdToInt(cls, keepingId):
        return int(ord(keepingId[0]) - ord("a")) * cls.__BASE + int(ord(keepingId[1]) - ord("a"))



    @classmethod
    def intToKeepingId(cls, number):
        firstDigit = cls.__NUMERALS[number // cls.__BASE]
        secondDigit = cls.__NUMERALS[number % cls.__BASE]
        return firstDigit + secondDigit

# _utils.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2011 Róbert Čerňanský



""":class:`Utils` and :class:`Constants` classes."""



__all__ = ["Utils", "Constants"]



# {{{ INCLUDES

import sys
import os
from abc import *
from functools import wraps

# }}} INCLUDES



# {{{ CLASSES

class Utils(metaclass = ABCMeta):
    "Various utility methods."

    @abstractmethod
    def __init__(self):
        pass



    @classmethod
    def printWarning(cls, msg, appName = None):
        "Prints ``msg`` as a warning to standard error."

        cls.__printToStdErr("Warning", msg, appName)



    @classmethod
    def printError(cls, msg, appName = None):
        "Prints ``msg`` as an error to standard error."

        cls.__printToStdErr("Error", msg, appName)



    @classmethod
    def fatalExit(cls, msg, appName = None):
        "Prints ``msg`` to standard error and exits with exit code 2."

        cls.__printToStdErr("Fatal Error", msg, appName)
        sys.exit(2)



    @staticmethod
    def uniq(decorated):
        "Decorator that filters out duplicate elements from an iterable returned by decorated function."

        @wraps(decorated)
        def wrapper(*args, **kwargs):
            seen = set()
            for item in decorated(*args, **kwargs):
                if item not in seen:
                    seen.add(item)
                    yield item

        return wrapper



    @staticmethod
    def __printToStdErr(attentionString, msg, appName = None):
        if appName is None:
            appName = sys.argv[0]
        sys.stderr.write(str.format("{}: {}! {}\n", appName, attentionString, msg))



class Constants(metaclass = ABCMeta):
    "Defines various “global” constants."

    #: Debugging support.
    DEBUG = os.environ.get("AADEBUG")



    @abstractmethod
    def __init__(self):
        pass

# }}} CLASSES

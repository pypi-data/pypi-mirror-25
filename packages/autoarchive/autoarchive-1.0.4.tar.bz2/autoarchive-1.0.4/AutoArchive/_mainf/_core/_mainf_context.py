# _mainf_context.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2011 Róbert Čerňanský



""":class:`_MainfContext` class."""



__all__ = ["_MainfContext"]



# {{{ INCLUDES

from .. import *

# }}} INCLUDES



# {{{ CLASSES

class _MainfContext(IMainfContext):
    """:class:`.IMainfContext` implementation.

    :param appEnvironment: Object that will be made available via :attr:`appEnvironment` property.
    :type appEnvironment: ``object``"""



    def __init__(self, appEnvironment):
        self.__appEnvironment = appEnvironment



    @property
    def appEnvironment(self):
        "See: :attr:`.IMainfContext.appEnvironment`"

        return self.__appEnvironment

# }}} CLASSES

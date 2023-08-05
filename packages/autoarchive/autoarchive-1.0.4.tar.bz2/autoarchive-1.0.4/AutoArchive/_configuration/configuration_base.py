# _configuration.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2012 Róbert Čerňanský



""":class:`ConfigurationBase` class."""



__all__ = ["ConfigurationBase"]



# {{{ INCLUDES

from abc import *
from . import *

# }}} INCLUDES



# {{{ CLASSES

class ConfigurationBase(IConfiguration):
    "See :class:`.IConfiguration`"

    @abstractmethod
    def __init__(self):

        #: Stores options and their values.  Key is of :class:`.Option` type and value is `object`.
        self.options_ = {}



    def __getitem__(self, option):
        "See: :meth:`.IConfiguration.__getitem__()`."

        optionForceForm = OptionsUtils.tryGetForceForm(option)
        if optionForceForm is not None:
            forceValue = self.getRawValue(optionForceForm)
            if forceValue is not None:
                return forceValue

        optionNegationForm = OptionsUtils.tryGetNegationForm(option)
        if optionNegationForm is not None:
            negationValue = self.getRawValue(optionNegationForm)
            if negationValue:
                return False

        # bool-type options can not return None
        if option._optType is bool:
            return self.getRawValue(option) or False

        return self.getRawValue(option)



    def getRawValue(self, option):
        "See: :meth:`.IConfiguration.getRawValue()`."

        return self.options_[option]

# }}} CLASSES

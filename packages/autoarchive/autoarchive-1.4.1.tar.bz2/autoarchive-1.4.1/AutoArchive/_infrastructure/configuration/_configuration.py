# _configuration.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2014 Róbert Čerňanský



""":class:`_Configuration` class."""



__all__ = ["_Configuration"]



# {{{ INCLUDES

from . import ConfigurationBase, OptionsUtils

# }}} INCLUDES



# {{{ CLASSES

class _Configuration(ConfigurationBase):
    """Application's configuration.

    Provides access to application's configuration.  All configuration options that can be accessed via this class are
    defined as static attributes of :class:`.Options`.

    After construction, all options are added and initialized to ``None``.  It is expected that concrete values will be
    added using the :meth:`_addOrReplaceOption()` method."""

    def __init__(self):
        super().__init__()

        self.__populateWithNones()



    def _addOrReplaceOption(self, optionName, value):
        """Adds an *option* and its *value* replacing the *value* if already exists.

        String representation of the *value* is expected.  It will be converted to a proper type defined by the
        *option*.

        :param optionName: Option that will be added or replaced.
        :type optionName: ``str``
        :param value: Value of passed *option* with name ``optionName``.
        :type value: ``str``

        :raise KeyError: If *option* with name ``optionName`` does not exists.
        :raise ValueError: If *option's* *value* is not correct."""

        option = OptionsUtils.getOption(optionName)
        self.options_[option] = OptionsUtils.strToOptionType(option, value)



    def __populateWithNones(self):
        for option in OptionsUtils.getAllOptions():
            self.options_[option] = None

# }}} CLASSES

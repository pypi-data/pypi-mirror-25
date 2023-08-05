# iconfiguration.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2012 Róbert Čerňanský



""":class:`IConfiguration` interface."""



__all__ = ["IConfiguration"]



# {{{ INCLUDES

from abc import *

# }}} INCLUDES



# {{{ CLASSES

class IConfiguration(metaclass = ABCMeta):
    "Provides access to configuration options."

    @abstractmethod
    def __getitem__(self, option):
        """Gets consolidated value of a configuration option.

        Method takes into account values of other option forms such as :term:`negation form <negation option form>` and
        :term:`force form <force option form>`.  For example if the raw value of the option FOO is 10 and raw value of
        FORCE_FOO is 5 then value 5 will be returned.

        The precedence order of option forms is following: force form > negation form > normal form; with force form
        as the highest and normal form as the lowest priority form.

        For options of type ``bool`` value ``None`` is never returned; it is converted to ``False``.

        :param option:  The option in the *normal form* for which the value should be returned.
        :type option: :class:`.Option`

        :return: The merged value of the passed ``option`` (can be ``None``).
        :rtype: ``object``

        :raise KeyError: If ``option`` does not exists."""



    @abstractmethod
    def getRawValue(self, option):
        """Gets the raw value of a configuration option or ``None``.

        Unlike the :meth:`__getitem__()` this method returns the real raw value of the ``option``.

        :param option: The option for which the value should be returned.
        :type option: :class:`.Option`

        :return: The raw value of the passed ``option`` (can be ``None``).
        :rtype: ``object``

        :raise KeyError: If ``option`` does not exists."""

# }}} CLASSES

# archive_spec_options.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2017 Róbert Čerňanský



""":class:`ArchiveSpecOptions` class."""



__all__ = ["ArchiveSpecOptions"]



from abc import *
from AutoArchive._infrastructure.configuration import Option, SpecialOptionTypes



class ArchiveSpecOptions(metaclass = ABCMeta):
    """Constants for options used specifically in the :term:`archive specification file`.

    These constants should be used to access options in :class:`.ArchiveSpec`.

    .. note:: It is not allowed to change values of these constants."""

    #: Archive name (``str``).  Guaranteed to be defined.
    NAME = Option("name", str)

    #: Path to the base directory for :data:`INCLUDE_FILES`, :data:`EXCLUDE_FILES` (:data:`.SpecialOptionTypes.PATH`).
    #: Guaranteed to be defined.
    PATH = Option("path", SpecialOptionTypes.PATH)

    #: Files and directories that will be included in the :term:`backup` (``frozenset<str>``).
    #: Note that frozenset<str> is not supported by :meth:`.OptionsUtils.strToOptionType()`; it is not used while
    #: populating this option.  Guaranteed to be defined.
    INCLUDE_FILES = Option("include-files", str)

    #: Files and directories that will be excluded from the :term:`backup` (``frozenset<str>``).
    #: Note that frozenset<str> is not supported by :meth:`.OptionsUtils.strToOptionType()`; it is not used while
    #: populating this option.  Guaranteed to be defined.
    EXCLUDE_FILES = Option("exclude-files", str)



    @abstractmethod
    def __init__(self):
        pass


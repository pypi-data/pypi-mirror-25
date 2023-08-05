# options.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2012 Róbert Čerňanský



""":class:`Options`, :class:`OptionsUtils` static classes and :class:`Option` class."""



__all__ = ["Options", "OptionsUtils", "Option", "SpecialOptionTypes"]



# {{{ INCLUDES

from abc import *
import os.path

from .._archiving import *

# }}} INCLUDES



# {{{ CLASSES

class Option:
    """Represents a configuration option.

    :param name: Option name.
    :type name: ``str``
    :param optType: Type of the option.
    :type optType: ``type`` or ``str``"""

    def __init__(self, name, optType):
        self.__name = name
        self.__optType = optType



    def __str__(self):
        return self.__name



    def __repr__(self):
        return str.format("<Option {} of type {}>", self.__name, self._optType)



    @property
    def _optType(self):
        """Gets the option type.

        :rtype: ``type`` or ``str``"""

        return self.__optType



# all option type constants defined in this class has to have uppercase names; there can not be any other constants
# defined that has uppercase names and are type of str, besides those representing option types
class SpecialOptionTypes(metaclass = ABCMeta):
    """Constants for special option types.

    Normally, options are of some standard type, such as ``int``, ``str``, etc.  Some of them however, requires special
    handling for which the special option types are defined in this class.

    .. note:: It is not allowed to change values of these constants."""

    # {{{ special option types constants

    #: A filesystem path.
    PATH = "path"

    # }}} special option types constants



    @abstractmethod
    def __init__(self):
        pass



# all option constants defined in this class has to have uppercase names; there can not be any other constants defined
# that has uppercase names and are type of Option, besides those representing options
class Options(metaclass = ABCMeta):
    """Constants for configuration options.

    These constants should be used to access options in the :class:`.IConfiguration` implementation provided by the
    :term:`Configuration` :term:`component`.

    .. note:: It is not allowed to change values of these constants."""

    # {{{ option constants

    # {{{ archiving related options

    #: Archiver type.  Guaranteed to be defined.
    ARCHIVER = Option("archiver", ArchiverTypes)

    #: Compression strength level.
    COMPRESSION_LEVEL = Option("compression-level", int)

    #: Directory where the backup will be created.  Guaranteed to be defined.
    DEST_DIR = Option("dest-dir", SpecialOptionTypes.PATH)

    # }}} archiving related options

    # {{{ incremental archiving related options

    #: Incremental backup.
    INCREMENTAL = Option("incremental", bool)

    #: Backup level used in incremental archiving.
    LEVEL = Option("level", int)

    #: Turns on backup level restarting.
    RESTARTING = Option("restarting", bool)

    #: Maximal backup level.  If reached, it will be restarted back to a lower level (which is typically level 1 but it
    #: depends on :attr:`MAX_RESTART_LEVEL_SIZE`).  Guaranteed to be defined.
    RESTART_AFTER_LEVEL = Option("restart-after-level", int)

    #: Number of days after which the backup level is restarted.  Similarly to :attr:`RESTART_AFTER_LEVEL` it will be
    #: restarted to level 1 or higher.
    RESTART_AFTER_AGE = Option("restart-after-age", int)

    #: Number of backup level restarts after which the level is restarted to 0.
    FULL_RESTART_AFTER_COUNT = Option("full-restart-after-count", int)

    #: Number of days after which the backup level is restarted to 0.
    FULL_RESTART_AFTER_AGE = Option("full-restart-after-age", int)

    #: Maximal percentage size of a :term:`backup` (of level > 0) to which level is allowed restart to.  The size is
    #: percentage of size of the level 0 backup file.  If a backup of particular level has its size bigger than
    #: defined percentage, restart to that level will not be allowed.
    MAX_RESTART_LEVEL_SIZE = Option("max-restart-level-size", int)

    #: Turns on removing backups of levels that are no longer valid due to the backup level restart.  All backups of
    #: the backup level higher than the one currently being created will be removed.
    REMOVE_OBSOLETE_BACKUPS = Option("remove-obsolete-backups", bool)

    # }}} incremental archiving related options

    # {{{ general options

    #: Turns on verbose output.
    VERBOSE = Option("verbose", int)

    #: Turns on quiet output.  Only errors will be shown.  If QUIET is turned on at the same level as VERBOSE
    #: (e. g. both are specified on the command line) then QUIET has higher priority than VERBOSE.
    QUIET = Option("quiet", bool)

    #: Operate on all configured archive specification files.
    ALL = Option("all", bool)

    #: Directory where :term:`archive specification files <archive specification file>` will be searched.
    #: Guaranteed to be defined.
    ARCHIVE_SPECS_DIR = Option("archive-specs-dir", SpecialOptionTypes.PATH)

    #: User configuration file.  Guaranteed to be defined.
    USER_CONFIG_FILE = Option("user-config-file", SpecialOptionTypes.PATH)

    #: User configuration directory.  Guaranteed to be defined.
    USER_CONFIG_DIR = Option("user-config-dir", SpecialOptionTypes.PATH)

    # }}} general options

    # {{{ force options

    #: Force archiver type regardless to what is specified in the :term:`archive specification file`.
    FORCE_ARCHIVER = Option("force-archiver", ArchiverTypes)

    #: Force incremental backup regardless to what is specified in the :term:`archive specification file`.
    FORCE_INCREMENTAL = Option("force-incremental", bool)

    #: Force the backup level restarting regardless to what is specified in the :term:`archive specification file`.
    FORCE_RESTARTING = Option("force-restarting", bool)

    #: Force compression level regardless to what is specified in the :term:`archive specification file`.
    FORCE_COMPRESSION_LEVEL = Option("force-compression-level", int)

    #: Force the directory where the backup will be created.
    FORCE_DEST_DIR = Option("force-dest-dir", SpecialOptionTypes.PATH)

    # }}} force options

    # {{{ negation options

    #: Disable incremental backup.
    NO_INCREMENTAL = Option("no-incremental", bool)

    #: Turns off backup level restarting.
    NO_RESTARTING = Option("no-restarting", bool)

    #: Do not operate on all configured archive specification files.
    NO_ALL = Option("no-all", bool)

    # }}} negation options

    # }}} option constants



    @abstractmethod
    def __init__(self):
        pass



class OptionsUtils(metaclass = ABCMeta):
    "Various utility methods working with :class:`Options`."

    __ARCHIVER_OPTION_ENUM_MAP = {"tar": ArchiverTypes.Tar,
                                  "targz": ArchiverTypes.TarGz,
                                  "tarbz2": ArchiverTypes.TarBz2,
                                  "tarxz": ArchiverTypes.TarXz,
                                  "tar_internal": ArchiverTypes.TarInternal,
                                  "targz_internal": ArchiverTypes.TarGzInternal,
                                  "tarbz2_internal": ArchiverTypes.TarBz2Internal}

    __NEGATION_PREFIX = "no-"
    __FORCE_PREFIX = "force-"



    @abstractmethod
    def __init__(self):
        pass



    @staticmethod
    def getAllOptions():
        """Iterator over all known options.

        :return: All options defined in :class:`Options`.
        :rtype: ``Iterator<Option>``"""

        for member in Options.__dict__:
            if member.isupper and isinstance(Options.__dict__[member], Option):
                yield Options.__dict__[member]



    @staticmethod
    def getAllSpecialOptionTypes():
        """Iterator over all known special option types.

        :return: All option types defined in :class:`SpecialOptionTypes`.
        :rtype: ``Iterator<str>``"""

        for member in SpecialOptionTypes.__dict__:
            if member.isupper and isinstance(
                SpecialOptionTypes.__dict__[member], str):

                yield SpecialOptionTypes.__dict__[member]



    @classmethod
    def getOption(cls, optionName):
        """Return option with given name.

        :param optionName: Name of the option that shall be returned.
        :type optionName: ``str``

        :return: First option from :meth:`getAllOptions()` which name is ``optionName``.
        :rtype: :class:`Option`

        :raise KeyError: If option with name ``optionName`` does not exist."""

        try:
            return next(filter(lambda opt: str(opt) == optionName, cls.getAllOptions()))
        except StopIteration:
            raise KeyError(str.format("Unknown option with name: {}", optionName))



    @classmethod
    def isExistingOption(cls, optionName):
        """Check whether an option with name ``optionName`` does exists in :class:`OptionsUtils`.

        :param optionName: Name of the option which existence shall be checked.
        :type optionName: ``str``

        :return: ``True`` if option with name ``optionName`` exists; ``False`` otherwise.
        :rtype: ``bool``"""

        try:
            cls.getOption(optionName)
            return True
        except KeyError:
            return False



    @classmethod
    def tryGetNegationForm(cls, option):
        """Returns :term:`negation form <negation option form>` for ``option`` or ``None``.

        :param option: An option in the :term:`normal form <normal option form>` for which the negation form for shall
          be returned.
        :type option: :class:`Option`

        :return: Negation form of the passed ``option`` or ``None`` if it does not have a negation form.
        :rtype: :class:`Option`"""

        negationFormName = cls.__NEGATION_PREFIX + str(option)
        if cls.isExistingOption(negationFormName):
            return cls.getOption(negationFormName)
        return None



    @classmethod
    def tryGetForceForm(cls, option):
        """Returns :term:`force form <force option form>` for ``option`` or ``None``.

        :param option: An option in the :term:`normal form <normal option form>` for which the force form for shall be
          returned.
        :type option: :class:`Option`

        :return: Force form of the passed ``option`` or ``None`` if it does not have a force form.
        :rtype: :class:`Option`"""

        forceFormName = cls.__FORCE_PREFIX + str(option)
        if cls.isExistingOption(forceFormName):
            return cls.getOption(forceFormName)
        return None



    @classmethod
    def strToOptionType(cls, option, optionValue):
        """Converts string option value to its proper, defined type.

        :param option: Option which value shall be converted.
        :type option: :class:`Option`
        :param optionValue: Value to be converted.
        :type optionValue: ``str``

        :return: Converted ``optionValue``.
        :rtype: ``object``

        :raise ValueError: If ``optionValue`` can not be converted to ``option``\ 's type.
        :raise RuntimeError: If ``option``\ 's type is not supported."""

        result = None

        if optionValue is None:
            result = optionValue

        elif optionValue == "" and not issubclass(option._optType, str):
            result = None

        elif isinstance(option._optType, type):

            if issubclass(option._optType, str):
                result = optionValue

            elif issubclass(option._optType, bool):
                if optionValue.strip().lower() in ("false", "0", "no"):
                    result = False
                else:
                    result = bool(optionValue)

            elif issubclass(option._optType, int):
                result = int(optionValue)

            elif issubclass(option._optType, float):
                result = float(optionValue)

        elif option._optType in cls.getAllSpecialOptionTypes():

            if option._optType == SpecialOptionTypes.PATH:
                result = os.path.expanduser(optionValue)

        else:

            if option._optType is ArchiverTypes:
                result = cls.__strToArchiverType(optionValue)

            else:
                raise(RuntimeError("Unknown option type."))

        return result



    @classmethod
    def archiverTypeToStr(cls, archiverType):
        """Converts :data:`.ArchiverTypes` to string representation.

        Value of the ``archiverType`` parameter is converted to a string representation that is accepted by the
        :meth:`strToOptionType()` method.

        :param archiverType: Archiver type that shall be converted.
        :type archiverType: :data:`.ArchiverTypes`

        :return: String form of passed ``archiverType``.
        :rtype: ``str``

        :raise ValueError: If ``archiverType`` is not known."""

        try:
            return next(filter(
                    lambda key: cls.__ARCHIVER_OPTION_ENUM_MAP[key] ==
                    archiverType, cls.__ARCHIVER_OPTION_ENUM_MAP.keys()))
        except StopIteration:
            raise ValueError("Unknown archiver type: {}.", archiverType)



    @classmethod
    def __strToArchiverType(cls, archiverStr):
        "Converts string to :data:`.ArchiverTypes`."

        if archiverStr in cls.__ARCHIVER_OPTION_ENUM_MAP:
            return cls.__ARCHIVER_OPTION_ENUM_MAP[archiverStr]
        else:
            raise ValueError(str.format("Unknown archiver type: \"{}\".", archiverStr))

# }}} CLASSES

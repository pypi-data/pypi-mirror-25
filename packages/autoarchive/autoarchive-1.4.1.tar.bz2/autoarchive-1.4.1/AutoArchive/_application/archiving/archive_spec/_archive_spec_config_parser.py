# _archive_spec_config_parser.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2017 Róbert Čerňanský



""":class:`_ArchiveSpecConfigParser` class."""



__all__ = ["_ArchiveSpecConfigParser"]



# {{{ INCLUDES

import os
import re
import configparser
from AutoArchive._infrastructure.py_additions import Flag, maxRecursion
from . import ConfigConstants
from ._sections import _Sections

# }}} INCLUDES



# {{{ CLASSES

class _ArchiveSpecConfigParser(configparser.ConfigParser):
    """:class:`configparser.ConfigParser` with specifics regards to :term:`archive specification file` reading.

    Supports external references, empty values and adapted exception handling.

    :param forbiddenOptions: Options which are not allowed in :attr:`._Sections.ARCHIVE` and :attr:`._Sections.CONTENT`
    :type forbiddenOptions: collections.abc.Set[str]
    :param str archiveSpecsDir: Directory where to look for external archive specification files without path"""

    def __init__(self, forbiddenOptions, archiveSpecsDir):
        super().__init__(allow_no_value = True)

        self.__forbiddenOptions = forbiddenOptions
        self.__archiveSpecsDir = archiveSpecsDir

        # directory of the file which was read by this instance
        self.__specDir = None

        self.__inGetCallFlag = Flag()



    def get(self, section, *args, **kwargs):
        """Gets value and resolve external references.

        :param str section: Section the value shall be read from.
        :param args: See :meth:`configparser.ConfigParser.get`.
        :param kwargs: See :meth:`configparser.ConfigParser.get`.

        :raise RuntimeError: If directory where the configuration file is located is not known.  :meth:`read_file` has
            to be called first.
        :raise ValueError: If an external reference can not be resolved."""

        if self.__inGetCallFlag.isSet():
            return super().get(section, *args, **kwargs)

        with self.__inGetCallFlag:
            if self.__specDir is None:
                raise RuntimeError("Directory of configuration file not set.")

            return self.__resolveExternalReferences(super().get(section, *args, **kwargs), section)



    def read_file(self, file, source = None):
        """Read configuration file with sanity checking and error handling.

        :param file: The file handle that shall be read.
        :param str source: Path to the file that passed handle represents.

        :raise ValueError: If name of the source file can not be determined.  If an empty option is present.
        :raise KeyError: If an invalid (unsupported) *section* or *option* is found in the :term:`archive specification
            file`.
        :raise SyntaxError: If the file can not be parsed."""

        try:
            source = source or file.name
            if not source:
                raise ValueError
        except (AttributeError, ValueError):
            raise ValueError("None or empty source file name.")

        self.__specDir = os.path.dirname(source)

        try:
            super().read_file(file, source)
        except (configparser.InterpolationError,
                configparser.MissingSectionHeaderError,
                configparser.ParsingError) as ex:
            raise SyntaxError(ex)
        except UnicodeDecodeError as ex:
            raise SyntaxError(str.format("Unable to parse file \"{}\" [{}].", source, ex))

        # check the specification file for sanity

        supportedSections = {_Sections.EXTERNAL, _Sections.ARCHIVE, _Sections.CONTENT}
        if len(supportedSections.union(self.sections())) > len(supportedSections):
            raise KeyError(str.format(
                "One or more invalid sections found in the archive specification file \"{}\".", source))

        for section in self.sections():
            if not self.__forbiddenOptions.isdisjoint(self.options(section)):
                raise KeyError(str.format(
                    "One or more invalid options found in the archive specification file \"{}\".", source))

        for section in (_Sections.ARCHIVE, _Sections.CONTENT):
            if section not in self.sections():
                continue
            for option, value in self.items(section, raw = True):
                if value is None:
                    raise ValueError(str.format("Option without a value found: \"[{}] {}\".", section, option))



    def optionxform(self, optionStr):
        """Override that does not modify option name.

        :param str optionStr: The option name.
        :return: Unmodified option name.
        :rtype: str"""

        return optionStr



    # referring through more than 40 levels is considered excessive and it is most likely a circular dependency
    @maxRecursion(40)
    def __resolveExternalReferences(self, value, section):
        if not self.has_section(_Sections.EXTERNAL):
            return value

        options = self[_Sections.EXTERNAL]
        externals = dict(
            (o, os.path.normpath(os.path.join(self.__archiveSpecsDir, o + ConfigConstants.ARCHIVE_SPEC_EXT)))
            if options[o] is None
            else (o, os.path.normpath(os.path.join(self.__specDir, options[o])))
            for o in options)

        for reference in (self._ExternalReference(m.group())
                          for m in re.finditer(r"([\"']?)@\([a-zA-Z0-9-_.]+?\)\1", value)):
            if reference.name not in externals:
                raise ValueError(
                    str.format("Unknown external reference \"{}\" in option \"{}\".", reference.name, reference.option))

            externalConfigParser = _ArchiveSpecConfigParser(self.__forbiddenOptions, self.__archiveSpecsDir)
            try:
                externalConfigParser.read_file(open(externals[reference.name]))
            except (ValueError, KeyError, SyntaxError) as ex:
                raise ValueError(str.format(
                    "Error while reading referenced file: \"{}\".  Error: {}", externals[reference.name], ex))

            if reference.option not in externalConfigParser[section]:
                raise ValueError(str.format("Referenced option not found: \"{}\".", reference.option))

            value = value.replace(reference.referenceStr, externalConfigParser.get(section, reference.option))

        return value



    class _ExternalReference:
        """Represents reference to an external configuration file."""

        def __init__(self, referenceStr):
            self.__referenceStr = referenceStr



        @property
        def name(self):
            return self.__referenceStr.lstrip("\"'").split(".")[0][2:]



        @property
        def option(self):
            return self.__referenceStr.rstrip("\"'").split(".")[1][:-1]



        @property
        def referenceStr(self):
            return self.__referenceStr

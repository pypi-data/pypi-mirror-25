# archive_spec.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2017 Róbert Čerňanský



""":class:`ArchiveSpec` class."""



__all__ = ["ArchiveSpec"]



# {{{ INCLUDES

import os
import re
import glob
import configparser
import itertools

from AutoArchive._infrastructure.configuration import ConfigurationBase, Options, OptionsUtils
from . import ArchiveSpecOptions
from ._sections import _Sections
from ._archive_spec_config_parser import _ArchiveSpecConfigParser

# }}} INCLUDES



# {{{ CLASSES

class ArchiveSpec(ConfigurationBase):
    """The :term:`archive` specification.

    Contains all information needed to create the :term:`backup` such as the name, list of files which shall be
    included into the backup, list of files to exclude, etc.  These values can be configured in the
    :term:`archive specification file` (``specFile``) or in the general configuration such as command line or
    configuration files.  Options that can be read from this class are defined as static attributes of
    :class:`.ArchiveSpecOptions` and :class:`.Options`.  If an option is not defined in the
    archive specification file it is read from ``configuration``.

    The instance is fully populated during construction.

    :param specFile: :term:`Archive specification file` name (the “.aa file”).
    :type specFile: ``str``
    :param configuration: The application's configuration.
    :type configuration: :class:`.ConfigurationBase`
    :param componentUi: The application's :term:`UI` interface.  If ``None`` then messages about non-accessible
       files or other errors during processing of **included** and **excluded** file lists will not be shown.
    :type componentUi: :class:`.CmdlineUi`

    :raise OSError: If ``specFile`` can not be opened.
    :raise LookupError: If a *section* or an *option* is missing in ``specFile``.
    :raise SyntaxError: If ``specFile`` can not be parsed.
    :raise KeyError: If an invalid (unsupported) *section* or *option* is found in the :term:`archive specification
       file`.
    :raise ValueError: If option's *value* is not correct."""

    # configuration options that are also supported in the arch. spec. file
    __CONFIG_OPTIONS = frozenset({Options.ARCHIVER,
                                  Options.COMPRESSION_LEVEL,
                                  Options.DEST_DIR,
                                  Options.INCREMENTAL,
                                  Options.RESTARTING,
                                  Options.RESTART_AFTER_LEVEL,
                                  Options.RESTART_AFTER_AGE,
                                  Options.FULL_RESTART_AFTER_COUNT,
                                  Options.FULL_RESTART_AFTER_AGE,
                                  Options.MAX_RESTART_LEVEL_SIZE,
                                  Options.REMOVE_OBSOLETE_BACKUPS,
                                  Options.KEEP_OLD_BACKUPS,
                                  Options.NUMBER_OF_OLD_BACKUPS,
                                  Options.COMMAND_BEFORE_BACKUP,
                                  Options.COMMAND_AFTER_BACKUP,
                                  Options.OVERWRITE_AT_START})



    def __init__(self, specFile, configuration, componentUi = None):
        super().__init__()

        # {{{ attributes

        self.__configuration = configuration
        self.__componentUi = componentUi

        self.__spec = _ArchiveSpecConfigParser(
            forbiddenOptions = {str(opt) for opt in set(OptionsUtils.getAllOptions()) - self.__CONFIG_OPTIONS},
            archiveSpecsDir = configuration[Options.ARCHIVE_SPECS_DIR])

        # }}} attributes

        # read the archive specification file (the .aa file)
        self.__spec.read_file(open(specFile))

        # populate the instance
        self.__addRequiredSpecFileOptions(specFile)
        self.__addOptionalSpecFileOptions(specFile)
        self.__addOptionalConfigurationOptions()



    # {{{ ConfigurationBase overrides

    def getRawValue(self, option):
        "See: :meth:`.ConfigurationBase.getRawValue()`."

        if option in self.options_:
            return super().getRawValue(option)
        else:
            return self.__configuration.getRawValue(option)

    # }}} ConfigurationBase overrides



    # {{{ helpers

    # {{{ options adding

    def __addRequiredSpecFileOptions(self, specFile):
        "Add non-optional options (specific to archive spec. file)."

        try:

            # add path and check its existence
            self.__addOptionFromSpec(_Sections.CONTENT, ArchiveSpecOptions.PATH)

            path = self[ArchiveSpecOptions.PATH]
            if not os.path.exists(path):
                raise ValueError(str.format(
                    "Cannot access directory \"{}\" configured in the \"{}\" option; it does not exists.",
                    path, ArchiveSpecOptions.PATH))

            if not os.path.isdir(path):
                raise ValueError(str.format(
                    "Cannot access directory \"{}\" configured in the \"{}\" option; it is not a directory.",
                    path, ArchiveSpecOptions.PATH))

            self.options_[ArchiveSpecOptions.INCLUDE_FILES] = \
                self.__readFilesLists(str(ArchiveSpecOptions.INCLUDE_FILES))
            self.options_[ArchiveSpecOptions.EXCLUDE_FILES] = \
                self.__readFilesLists(str(ArchiveSpecOptions.EXCLUDE_FILES))

        except configparser.NoSectionError as ex:
            raise LookupError(str.format(
                "Missing section \"{}\" in specification file \"{}\".", ex.section, specFile))
        except configparser.NoOptionError as ex:
            raise LookupError(str.format(
                "Missing option \"{}\" in section \"{}\" of specification file \"{}\".",
                ex.option, ex.section, specFile))



    def __addOptionalSpecFileOptions(self, specFile):
        "Add optional options specific to archive spec. file."

        self.__addOptionFromSpec(
            _Sections.CONTENT, ArchiveSpecOptions.NAME, os.path.splitext(os.path.basename(specFile))[0])



    def __addOptionalConfigurationOptions(self):
        "Add optional options that can be present also in configuration."

        if self.__spec.has_section(_Sections.ARCHIVE):
            for option in self.__CONFIG_OPTIONS:
                self.__tryAddOptionFromSpec(_Sections.ARCHIVE, option)



    # {{{ options adding sub-helpers

    def __addOrReplaceOption(self, option, value):
        try:
            self.options_[option] = OptionsUtils.strToOptionType(option, value)
        except ValueError:
            raise ValueError(str.format(
                "Wrong value \"{}\" of the option \"{}\" in the archive specification file.", value, option))



    def __addOptionFromSpec(self, section, option, default = None):
        self.__addOrReplaceOption(option, self.__spec.get(section, str(option), fallback = default))



    def __tryAddOptionFromSpec(self, section, option):
        if self.__spec.has_option(section, str(option)):
            self.__addOrReplaceOption(option, self.__spec.get(section, str(option)))



    # {{{ file lists processing

    def __readFilesLists(self, listKind):
        "Read configured include or exclude files or directories."

        # extract filenames from specFile and store them into list
        files = re.findall(r'(?:".+?")|(?:\S+)', self.__spec.get(_Sections.CONTENT, listKind))

        # previous regexp leaves quotes in filenames so they must be removed
        files = self.__clearQuotes(files)

        # remove parent directory path elements and absolute path token ("/"); for paths like "../../foo/bar" it
        # returns "foo/bar" and for absolute paths like "/bar/baz" it returns "bar/baz";
        # for each path in files it splits it by "/" and uses dropwhile() function to filter-out
        # first "/" (empty pathElement) and ".." (pathElement == os.pardir); then joins the result back to the path
        # representation
        files = (os.path.join(*(itertools.dropwhile(lambda pathElement: not pathElement or pathElement == os.pardir,
                                                    os.path.normpath(path).split(os.sep)))) for path in files)

        return self.__expandWilds(files)



    def __expandWilds(self, files):
        "Expand wildcards in list of files."

        cwdSave = os.getcwd()
        try:
            os.chdir(os.path.expanduser(self.__spec.get(_Sections.CONTENT, str(ArchiveSpecOptions.PATH))))
        except OSError as ex:
            if self.__componentUi:
                self.__componentUi.showError(ex)
            return frozenset()

        expandedFiles = set()
        for fileName in files:
            expanded = glob.glob(fileName)
            if expanded:
                expandedFiles.update(expanded)
            else:
                if self.__componentUi:
                    self.__componentUi.showWarning(
                        str.format("Cannot access \"{}\". No such file or directory.", fileName))

        os.chdir(cwdSave)
        return frozenset(expandedFiles)



    @staticmethod
    def __clearQuotes(files):
        "Remove quotes from file names."

        for fileName in files:
            match = re.search('(?<=").+(?=")', fileName)
            if match is not None:
                yield match.group(0)
            else:
                yield fileName

    # }}} file lists processing

    # }}} options adding sub-helpers

    # }}} options adding

    # }}} helpers

# }}} CLASSES

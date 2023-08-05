# starter.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2012 Róbert Čerňanský



"""Initializes :term:`Mainf` framework and passes the control to it."""



__all__ = ["Starter"]



# {{{ INCLUDES

from abc import *
import os.path
import sys
from optparse import OptionParser, OptionGroup

from ._py_additions import *
from ._meta import *
from ._mainf import *
from ._services import *
from ._app_environment import *

from ._configuration import *
from ._archiving import ArchiverTypes
from ._ui import *

# deliberately violating the access rules and importing IComponent-s from internal packages
from ._configuration._core import ConfigurationComponent
from ._archiving._core import ArchivingComponent
from ._ui._cmdline._core import CmdlineUiComponent

# }}} INCLUDES



# {{{ CONSTANTS

#: Tuple of component classes (which has to derive from :class:`.IComponent`) in dependency order
_COMPONENTS = (ConfigurationComponent, ArchivingComponent, CmdlineUiComponent)

# }}} CONSTANTS



# {{{ CLASSES

class Starter(metaclass = ABCMeta):
    "Fires up the show."

    @abstractmethod
    def __init__(self):
        pass



    @classmethod
    def start(cls):
        "Initializes :term:`Mainf` and starts the program."

        mainfEngine = createMainfEngine()

        for componentType in _COMPONENTS:
            mainfEngine.addComponent(componentType)

        optparseValues, arguments = cls.__parseArguments()
        appEnvironment = _AppEnvironment(os.path.basename(sys.argv[0]), optparseValues, arguments)

        result = mainfEngine.start(appEnvironment)
        ServiceCleaner.cleanServices()
        return result



    @classmethod
    def __parseArguments(cls):
        "Parses command line arguments."

        # define usage and version strings
        usage = "Usage: %prog [options] [command] [AA_SPEC]..."
        description = _Meta.DESCRIPTION
        version = """\
%prog version {version}

{copyright}

{license}
    """.format(version = _Meta.VERSION, copyright = _Meta.COPYRIGHT,
               license = _Meta.LICENSE)
        epilog = str.format("""\
AA_SPEC is the archive specification file argument.  It determines the archive specification file that shall be
processed.  If AA_SPEC contains the ".aa" extension then it is taken as the path to an archive specification
file.  Otherwise, if specified without the extension, the corresponding .aa file is searched in the archive
specifications directory (see option --{}).""", Options.ARCHIVE_SPECS_DIR)

        # create parser and add the options
        parser = OptionParser(usage = usage, version = version, description = description, epilog = epilog,
                              add_help_option = False)

        # {{{ commands

        commandsGroup = OptionGroup(parser, "Commands",
                                    "Commands for program's operations.  The default operation is the backup " +
                                    "creation if no command is specified.")

        commandsGroup.add_option(cls.__makeCmdlineOption(CmdlineCommands.LIST), action = "store_true",
                                 help = "Show all configured or orphaned archives.")

        commandsGroup.add_option(cls.__makeCmdlineOption(CmdlineCommands.PURGE), action = "store_true",
                                 help = "Purge stored data for an orphaned archive.")

        parser.remove_option("--version")
        commandsGroup.add_option("--version", action = "version", help = "Show program's version number and exit.")

        commandsGroup.add_option("-h", "--help", action = "help", help = "Show this help message and exit.")

        parser.add_option_group(commandsGroup)

        # }}} commands

        # {{{ archiving related options

        archivingGroup = OptionGroup(parser, "Archiving options")

        archiverChoices = [OptionsUtils.archiverTypeToStr(arch)
                           for arch in ArchiverTypes]
        archivingGroup.add_option("-a", cls.__makeCmdlineOption(Options.ARCHIVER), choices = archiverChoices,
                                  help = str.format("Specify archiver type.  Supported types are: {choices} " +
                                                    "(default: targz).",  choices = archiverChoices))

        compressionLevelChoices = [str(level)
                                   for level in range(1, 10)]
        archivingGroup.add_option("-c", cls.__makeCmdlineOption(Options.COMPRESSION_LEVEL),
                                  choices = compressionLevelChoices,
                                  metavar = "NUM",
                                  help = "Compression strength level.  If not specified, default behaviour of " +
                                         "underlying compression program will be used.")

        archivingGroup.add_option("-d", cls.__makeCmdlineOption(Options.DEST_DIR),
                                  metavar = "DIR_PATH",
                                  help = "Directory where the backup will be created (default: <current directory>).")

        parser.add_option_group(archivingGroup)

        # }}} archiving related options

        # {{{ incremental archiving related options

        incrementalGroup = OptionGroup(parser, "Incremental archiving options")

        incrementalGroup.add_option("-i", cls.__makeCmdlineOption(Options.INCREMENTAL),
                                    action = "store_true",
                                    help = "Perform incremental backup.")

        incrementalGroup.add_option("-l", cls.__makeCmdlineOption(Options.LEVEL),
                                    type = "int",
                                    help = "Specify the backup level which should be created.  All information about " +
                                           "higher levels---if any exists---will be erased.  If not present, the " +
                                           "next level in a row will be created.")

        incrementalGroup.add_option(cls.__makeCmdlineOption(Options.RESTARTING),
                                    action = "store_true",
                                    help = "Turns on backup level restarting.  See other '*restart-*' options to " +
                                           "configure the restarting behaviour.")

        incrementalGroup.add_option(cls.__makeCmdlineOption(Options.RESTART_AFTER_LEVEL),
                                    type = "int",
                                    metavar = "LEVEL",
                                    help = str.format("Maximal backup level.  If reached, it will be restarted back " +
                                                      "to a lower level (which is typically level 1 but it depends " +
                                                      "on '--{}') (default: 10).", Options.MAX_RESTART_LEVEL_SIZE))

        incrementalGroup.add_option(cls.__makeCmdlineOption(Options.RESTART_AFTER_AGE),
                                    type = "int",
                                    metavar = "DAYS",
                                    help = str.format("Number of days after which the backup level is restarted.  " +
                                                      "Similarly to '--{}' it will be restarted to level 1 or higher.",
                                                      Options.RESTART_AFTER_LEVEL))

        incrementalGroup.add_option(cls.__makeCmdlineOption(Options.FULL_RESTART_AFTER_COUNT),
                                    type = "int",
                                    metavar = "COUNT",
                                    help = "Number of backup level restarts after which the level is restarted to 0.")

        incrementalGroup.add_option(cls.__makeCmdlineOption(Options.FULL_RESTART_AFTER_AGE),
                                    type = "int",
                                    metavar = "DAYS",
                                    help = "Number of days after which the backup level is restarted to 0.")

        incrementalGroup.add_option(cls.__makeCmdlineOption(Options.MAX_RESTART_LEVEL_SIZE),
                                    type = "int",
                                    metavar = "PERCENTAGE",
                                    help = "Maximal percentage size of a backup (of level > 0) to which level is " +
                                           "allowed restart to.  The size is percentage of size of the level 0 " +
                                           "backup file.  If a backup of particular level has its size bigger " +
                                           "than defined percentage, restart to that level will not be allowed.")

        incrementalGroup.add_option(cls.__makeCmdlineOption(Options.REMOVE_OBSOLETE_BACKUPS),
                                    action = "store_true",
                                    help = "Turns on removing backups of levels that are no longer valid due to the " +
                                           "backup level restart.  All backups of the backup level higher than the " +
                                           "one currently being created will be removed.")

        parser.add_option_group(incrementalGroup)

        # }}} incremental archiving related options

        # {{{ general options

        generalGroup = OptionGroup(parser, "General options")

        generalGroup.add_option("-v", cls.__makeCmdlineOption(Options.VERBOSE),
                                action = "count",
                                help = "Turns on verbose output.")

        generalGroup.add_option("-q", cls.__makeCmdlineOption(Options.QUIET),
                                action = "store_true",
                                help = str.format("Turns on quiet output.  Only errors will be shown.  If --{quiet} " +
                                                  "is turned on at the same level as --{verbose} (e. g. both are " +
                                                  "specified on the command line) then --{quiet} has higher priority " +
                                                  "than --{verbose}.", quiet = Options.QUIET,
                                                  verbose = Options.VERBOSE))

        generalGroup.add_option(cls.__makeCmdlineOption(Options.ALL), action = "store_true",
                                help = str.format("Operate on all configured archives. See also --{}.",
                                                  Options.ARCHIVE_SPECS_DIR))

        generalGroup.add_option(cls.__makeCmdlineOption(Options.ARCHIVE_SPECS_DIR),
                                metavar = "DIR_PATH",
                                help = "Directory where archive specification files will be searched for (default: " +
                                       "~/.config/aa/archive_specs).")

        generalGroup.add_option(cls.__makeCmdlineOption(Options.USER_CONFIG_FILE),
                                metavar = "FILE_PATH",
                                help = "Alternate user configuration file (default: ~/.config/aa/aa.conf).")

        generalGroup.add_option(cls.__makeCmdlineOption(Options.USER_CONFIG_DIR),
                                metavar = "DIR_PATH",
                                help = "Alternate user configuration directory (default: ~/.config/aa).")

        parser.add_option_group(generalGroup)

        # }}} general options

        # {{{ force options

        forceGroup = OptionGroup(parser, "Force options", "Options to override standard options defined in " +
                                                          "archive specification files.")

        forceGroup.add_option(cls.__makeCmdlineOption(Options.FORCE_ARCHIVER),
                              choices = archiverChoices,
                              metavar = "ARCHIVER",
                              help = str.format(
                                  "Force archiver type.  Supported types are: {choices}.", choices = archiverChoices))

        forceGroup.add_option(cls.__makeCmdlineOption(Options.FORCE_INCREMENTAL),
                              action = "store_true",
                              help = "Force incremental backup.")

        forceGroup.add_option(cls.__makeCmdlineOption(Options.FORCE_RESTARTING),
                              action = "store_true",
                              help = "Force backup level restarting.")

        forceGroup.add_option(cls.__makeCmdlineOption(Options.FORCE_COMPRESSION_LEVEL),
                              choices = compressionLevelChoices,
                              metavar = "NUM",
                              help = "Force compression strength level.")

        forceGroup.add_option(cls.__makeCmdlineOption(Options.FORCE_DEST_DIR),
                              metavar = "DIR_PATH",
                              help = "Force the directory where the backup will be created.")

        parser.add_option_group(forceGroup)

        # }}} force options

        # {{{ negation options

        negationGroup = OptionGroup(parser, "Negation options", "Negative variants of standard boolean options.")

        negationGroup.add_option(cls.__makeCmdlineOption(Options.NO_INCREMENTAL),
                                 action = "store_true",
                                 help = "Disable incremental backup.")

        negationGroup.add_option(cls.__makeCmdlineOption(Options.NO_RESTARTING),
                                 action = "store_true",
                                 help = "Disable backup level restarting.")

        negationGroup.add_option(cls.__makeCmdlineOption(Options.NO_ALL), action = "store_true",
                                 help = "Do not operate on all configured archive specification files.")

        parser.add_option_group(negationGroup)

        # }}} negation options

        return parser.parse_args()



    @staticmethod
    def __makeCmdlineOption(option):
        return "--" + str(option)

# }}} CLASSES

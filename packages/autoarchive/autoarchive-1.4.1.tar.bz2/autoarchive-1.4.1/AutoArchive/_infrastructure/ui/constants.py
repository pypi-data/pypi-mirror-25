# constants.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2014 Róbert Čerňanský



""":data:`UiMessageKinds` and :data:`VerbosityLevels` enums."""



__all__ = ["UiMessageKinds", "VerbosityLevels"]



# {{{ INCLUDES

from AutoArchive._infrastructure.py_additions import Enum

# }}} INCLUDES



# {{{ CONSTANTS

#: Kinds of user messages.
UiMessageKinds = Enum(
    "Verbose",
    "Notification",
    "Info",
    "Warning",
    "Error")



#: Verbosity levels.
VerbosityLevels = Enum(
    "Quiet",
    "Normal",
    "Verbose")

# }}} CONSTANTS

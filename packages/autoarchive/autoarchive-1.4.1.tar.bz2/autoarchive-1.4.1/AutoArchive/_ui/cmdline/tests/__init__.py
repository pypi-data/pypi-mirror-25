# __init__.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2011 Róbert Čerňanský



"""Component tests for :term:`Cmdline UI`."""



from .test_cmdline_ui import *
from .test_user_action_executor import *



__all__ = test_cmdline_ui.__all__ + test_user_action_executor.__all__

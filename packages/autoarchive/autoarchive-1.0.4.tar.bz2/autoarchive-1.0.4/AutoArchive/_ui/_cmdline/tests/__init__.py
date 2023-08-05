# __init__.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2011 Róbert Čerňanský



"""Component tests for :term:`Cmdline UI`."""



from .test_icomponent_ui import *
from .test_icomponent import *



__all__ = test_icomponent_ui.__all__ + test_icomponent.__all__

# __init__.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2011 Róbert Čerňanský



"""Component tests for :term:`Archiving`."""



from .archiving_test_utils import *
from .test_iarchiving import *



__all__ = archiving_test_utils.__all__ + test_iarchiving.__all__

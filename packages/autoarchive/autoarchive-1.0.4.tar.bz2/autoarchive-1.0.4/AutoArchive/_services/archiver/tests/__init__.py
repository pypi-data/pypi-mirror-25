# __init__.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2012 Róbert Čerňanský



"""Component tests for :term:`Archiver <Archiver Service Component>`."""



from .archiver_test_utils import *
from .test_tar_archiver_providers import *



__all__ = archiver_test_utils.__all__ + test_tar_archiver_providers.__all__

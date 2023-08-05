# __init__.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2017 Róbert Čerňanský



"""Component tests for :term:`ArchiveSpec`."""



from .archive_spec_test_utils import *
from .test_archive_spec import *



__all__ = archive_spec_test_utils.__all__ + test_archive_spec.__all__

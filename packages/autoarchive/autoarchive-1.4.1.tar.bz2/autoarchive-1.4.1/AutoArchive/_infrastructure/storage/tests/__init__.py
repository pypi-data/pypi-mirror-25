# __init__.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2014 Róbert Čerňanský



"""Component tests for :term:`Storage`."""



from .storage_test_utils import *
from .test_file_storage import *
from .test_storage_portion import *



__all__ = storage_test_utils.__all__ + test_file_storage.__all__ + test_storage_portion.__all__

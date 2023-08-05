# __init__.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2014 Róbert Čerňanský



"""Component tests for :term:`Configuration`."""



from .configuration_test_utils import *
from .test_configuration import *



__all__ = configuration_test_utils.__all__ + test_configuration.__all__

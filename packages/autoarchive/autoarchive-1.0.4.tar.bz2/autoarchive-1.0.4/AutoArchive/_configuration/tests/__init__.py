# __init__.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2011 Róbert Čerňanský



"""Component tests for :term:`Configuration`."""



from .configuration_test_utils import *
from .test_iapp_config import *
from .test_istorage import *
from .test_istorage_portion import *



__all__ = configuration_test_utils.__all__ + test_iapp_config.__all__ + test_istorage.__all__ + \
          test_istorage_portion.__all__

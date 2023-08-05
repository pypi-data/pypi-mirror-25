# __init__.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2014 Róbert Čerňanský



"""Component tests for service framework."""



from .service_test_utils import *
from .test_service_accessor import *



__all__ = service_test_utils.__all__ + test_service_accessor.__all__

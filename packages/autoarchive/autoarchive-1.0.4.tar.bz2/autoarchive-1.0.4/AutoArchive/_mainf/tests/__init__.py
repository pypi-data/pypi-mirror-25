# __init__.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2011 Róbert Čerňanský



"""Component tests for :term:`Mainf`."""



from .mainf_test_utils import *
from .test_imainf_context import *
from .test_iinterface_accessor import *



__all__ = mainf_test_utils.__all__ + test_imainf_context.__all__ + test_iinterface_accessor.__all__

# __init__.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2011 Róbert Čerňanský



"""Utilities for component tests.

Tests are using standard :mod:`unittest` module; they can be ran by the means provided by it or by using the
:mod:`run_tests` module."""



from .component_test_utils import *
from .run_tests import *



__all__ = component_test_utils.__all__ + run_tests.__all__

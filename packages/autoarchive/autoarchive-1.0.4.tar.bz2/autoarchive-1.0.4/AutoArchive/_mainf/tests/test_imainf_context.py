# test_imainf_context.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2011 Róbert Čerňanský



""":class:`TestIMainfContext` class."""



__all__ = ["TestIMainfContext"]



# {{{ INCLUDES

import unittest

from .. import *
from .mainf_test_utils import *

# }}} INCLUDES



# {{{ CLASSES

class TestIMainfContext(unittest.TestCase):
    "Test of :class:`.IMainfContext` provided interface."

    __TEST_APP_ENVIRONMENT = "app_environment"



    def setUp(self):
        MainfTestUtils._setUpMainfComponent(self.__TEST_APP_ENVIRONMENT)



    def tearDown(self):
        MainfTestUtils._tearDownMainfComponent()



    def test_appEnvironment(self):
        """Test the appEnvironment property.

        Mainf is set-up with self.__TEST_APP_ENVIRONMENT as the application environment object.  Checks that the object
        returned by :attr:`.IMainfContext.appEnvironment` property is the same which was used for the initialization."""

        mainfContext = MainfTestUtils._interfaceAccessor.getComponentInterface(IMainfContext)
        self.assertIs(mainfContext.appEnvironment , self.__TEST_APP_ENVIRONMENT)

# }}} CLASSES

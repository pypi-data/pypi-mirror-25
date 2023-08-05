# run_tests.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2011 Róbert Čerňanský



"""Runs all tests.

.. note:: This module has to be called from ``AutoArchive`` as the current directory."""



__all__ = ["runTests"]



# {{{ INCLUDES

import unittest

# }}} INCLUDES



# {{{ FUNCTIONS

def runTests():
    """Runs all tests and shows results on the standard output.

    .. note:: Has to be called from ``AutoArchive`` as the current directory."""

    allTests = unittest.TestLoader().discover("AutoArchive", "tests", "..")
    unittest.TextTestRunner(verbosity = 2).run(allTests)

# }}} FUNCTIONS



# {{{ MAIN PROGRAM

if __name__ == "__main__":
    runTests()

# }}} MAIN PROGRAM

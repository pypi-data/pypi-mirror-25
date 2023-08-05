# test_multi_field_line.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2014 Róbert Čerňanský



""":class:`TestMultiFieldLine` class."""



__all__ = ["TestMultiFieldLine"]



# {{{ INCLUDES

import unittest
from .. import DisplayField, FieldStretchiness, MultiFieldLine

# }}} INCLUDES



# {{{ CLASSES

class TestMultiFieldLine(unittest.TestCase):
    "Test of :class:`.MultiFieldLine`."

    def setUp(self):
        self.__referenceLineWidth = 1000
        self.__fields = (DisplayField("irrelevant string", 0.2, FieldStretchiness.Normal),
                         DisplayField("irrelevant string", 0.1, FieldStretchiness.Low),
                         DisplayField("irrelevant string", 0.4, FieldStretchiness.Low),
                         DisplayField("irrelevant string", 0.1, FieldStretchiness.Medium),
                         DisplayField("irrelevant string", 0.2, FieldStretchiness.Normal))



    def test_computeFieldWidthsReference(self):
        """Tests field widths for total physical line width same as reference line width.

        Sets up fields with various relative sizes and stretchiness.  Calls computation of physical widths with the
        same physical line width as reference one.  Checks that computed widths directly corresponds to relative
        ones."""

        multiFieldLine = MultiFieldLine(self.__fields, self.__referenceLineWidth)

        widths = multiFieldLine.computeFieldWidths(self.__referenceLineWidth)

        for idx in range(5):
            expectedWidth = self.__fields[idx].widthWeight * self.__referenceLineWidth
            self.assertAlmostEqual(expectedWidth, widths[idx],
                                   msg = str.format("Calculated width ({}) is different than expected ({}).",
                                                    widths[idx], expectedWidth))



    def test_computeFieldWidthsHalfShrink(self):
        """Tests field widths for total physical line width half of the reference line width.

        Sets up fields with various relative sizes and stretchiness.  Calls computation of physical widths with the
        physical line width half of the reference one.  Checks that computed widths directly corresponds to shrinked
        size and stretchiness."""

        multiFieldLine = MultiFieldLine(self.__fields, self.__referenceLineWidth)

        widths = multiFieldLine.computeFieldWidths(self.__referenceLineWidth // 2)

        self.assertAlmostEqual(5, widths[0], msg = str.format(
            "Normal stretchiness field computed width ({}) is too different from expected ({})", widths[0], 5),
                               delta = 1)
        self.assertAlmostEqual(self.__fields[1].widthWeight * self.__referenceLineWidth, widths[1], msg = str.format(
            "Low stretchiness field computed width ({}) is too different from reference width.", widths[1]), delta = 30)
        self.assertAlmostEqual(self.__fields[2].widthWeight * self.__referenceLineWidth, widths[2], msg = str.format(
            "Low stretchiness field computed width ({}) is too different from reference width.", widths[2]), delta = 30)
        self.assertAlmostEqual(15, widths[3], msg = str.format(
            "Medium stretchiness field computed width ({}) is too different from expected ({})", widths[3], 15),
                               delta = 1)
        self.assertEqual(widths[0], widths[4], msg = str.format(
            "Width of last field is different from the first field of the same parameters."))

# }}} CLASSES

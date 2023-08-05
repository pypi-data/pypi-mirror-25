# multi_field_line.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2014 Róbert Čerňanský



""":class:`MultiFieldLine` class, :data:`FieldStretchiness` enum and :class:`DisplayField` namedtuple."""



__all__ = ["MultiFieldLine", "FieldStretchiness", "DisplayField"]



# {{{ INCLUDES

from collections import namedtuple
from AutoArchive._infrastructure.py_additions import Enum

# }}} INCLUDES



# {{{ CONSTANTS

#: Display field stretchiness.
FieldStretchiness = Enum(
    "Normal",
    "Medium",
    "Low"
)

# }}} CONSTANTS



# {{{ CLASSES

class MultiFieldLine:
    """A line of text that consists of multiple fields.

    :param fields: Parts that together assembles the line.
    :type fields: ``Sequence<DisplayField>``
    :param referenceLineWidth: Total physical width of the line used as a reference for computing physical widths
       based on relative widths of fields and re-computing them to a different total size in :meth:`computeFieldWidths`.
    :type referenceLineWidth: ``int``"""

    __MAX_STRETCHINESS_CONSTANT = 1000



    def __init__(self, fields, referenceLineWidth = 1000):
        self.__fields = fields
        self.__referenceLineWidth = referenceLineWidth



    @property
    def fields(self):
        """Gets fields that this line consists of.

        :rtype: ``Sequence<DisplayField>``"""

        return self.__fields



    # SMELL: This should return a structure of text and width.  Full DisplayField is not necessary.  Then the fields
    # property can be removed.
    def computeFieldWidths(self, physicalLineWidth):
        """Computes physical width for each field.

        Widths are computed based on relative widths and stretchiness so that total line width is no bigger than
        passes ``physicalLineWidth``.

        :param physicalLineWidth: Actual total line width (in the same units as ``referenceLineWidth``.
        :type physicalLineWidth: ``int``
        :return: Sequence of physical widths in the same order as :attr:`fields`.
        :rtype: ``list<int>``"""

        referenceToPhysical = physicalLineWidth / self.__referenceLineWidth
        # we are abusing DisplayField here by storing physical (reference) width in widthWeight
        referenceFields = [DisplayField(f.text, f.widthWeight * self.__referenceLineWidth, f.stretchiness) for f in
                          self.__fields]

        lowStretchedFields = [f for f in referenceFields if f.stretchiness == FieldStretchiness.Low]
        lowStretchedPhysicalWidths = [f.widthWeight * self.__applyStretchiness(referenceToPhysical, f.stretchiness) for
                                      f in lowStretchedFields]

        referenceToPhysicalNoLow = (physicalLineWidth - sum(lowStretchedPhysicalWidths)) / \
                                   (self.__referenceLineWidth - sum((f.widthWeight for f in lowStretchedFields)))
        mediumStretchedFields = [f for f in referenceFields if f.stretchiness == FieldStretchiness.Medium]
        mediumStretchedPhysicalWidths = [
            f.widthWeight * self.__applyStretchiness(referenceToPhysicalNoLow, f.stretchiness) for f in
            mediumStretchedFields]

        referenceToPhysicalNoLowMedium = (physicalLineWidth -
            (sum(lowStretchedPhysicalWidths) + sum(mediumStretchedPhysicalWidths))) / (self.__referenceLineWidth -
            (sum((f.widthWeight for f in lowStretchedFields)) + sum((f.widthWeight for f in mediumStretchedFields))))
        normalStretchedFields = [f for f in referenceFields if f.stretchiness == FieldStretchiness.Normal]
        normalStretchedPhysicalWidths = [
            f.widthWeight * self.__applyStretchiness(referenceToPhysicalNoLowMedium, f.stretchiness) for f in
            normalStretchedFields]

        # assemble list of widths in order that corresponds to self.__fields
        widths = []
        lowIdx = 0
        mediumIdx = 0
        normalIdx = 0
        for field in self.__fields:
            if field.stretchiness == FieldStretchiness.Low:
                widths.append(round(lowStretchedPhysicalWidths[lowIdx]))
                lowIdx += 1
            elif field.stretchiness == FieldStretchiness.Medium:
                widths.append(round(mediumStretchedPhysicalWidths[mediumIdx]))
                mediumIdx += 1
            elif field.stretchiness == FieldStretchiness.Normal:
                widths.append(round(normalStretchedPhysicalWidths[normalIdx]))
                normalIdx += 1

        return widths



    def __applyStretchiness(self, coefficient, stretchiness):
        stretchinessConstant = self.__quantifyStretchiness(stretchiness)
        return (1 - coefficient) * (stretchinessConstant / self.__MAX_STRETCHINESS_CONSTANT) + coefficient



    @staticmethod
    def __quantifyStretchiness(stretchiness):
        if stretchiness == FieldStretchiness.Normal:
            return 0
        if  stretchiness == FieldStretchiness.Medium:
            return 100
        if stretchiness == FieldStretchiness.Low:
            return 900



DisplayField = namedtuple("DisplayField", "text widthWeight stretchiness")
"""One part of a multi-field line.

:param text: Text that shall be displayed in the field.
:type text: ``str``
:param widthWeight: Number from 0 to 1 which represents relative width of the field.  0 means zero width and 1 means
   maximal width.
:type widthWeight: ``float``
:param stretchiness: Determines how much the field change its size when the actual total line width changes.
:type stretchiness: :data:`FieldStretchiness`"""

# }}} CLASSES

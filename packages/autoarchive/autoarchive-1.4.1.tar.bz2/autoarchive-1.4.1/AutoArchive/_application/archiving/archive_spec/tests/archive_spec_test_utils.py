# archive_spec_test_utils.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2017 Róbert Čerňanský



""":class:`ArchiveSpecTestUtils` class."""



__all__ = ["ArchiveSpecTestUtils"]



# {{{ INCLUDES

import os
import tempfile
from abc import ABCMeta, abstractmethod

from AutoArchive._infrastructure.configuration import OptionsUtils, ArchiverTypes
from AutoArchive._infrastructure.configuration.tests import ConfigurationTestUtils
from AutoArchive.tests import ComponentTestUtils
from .. import ConfigConstants
from .._sections import _Sections

# }}} INCLUDES



# {{{ CLASSES

class ArchiveSpecTestUtils(metaclass = ABCMeta):
    """Utility methods for :term:`ArchiveSpec` component tests."""

    __EXTERNAL_SECTION_PATTERN = str.format("[{}]", _Sections.EXTERNAL)

    # archive name patter in archive specification file
    __NAME_VARIABLE_PATTERN = "name = "



    @abstractmethod
    def __init__(self):
        pass



    @classmethod
    def _setUpClassArchiveSpecComponent(cls):
        ComponentTestUtils.setUpClassComponent()



    @classmethod
    def _tearDownClassArchiveSpecComponent(cls):
        ComponentTestUtils.tearDownClassComponent()



    @classmethod
    def _setUpArchiveSpecComponent(cls):
        ConfigurationTestUtils.makeUserConfigDirectory()
        ConfigurationTestUtils.makeArchiveSpecsDirectory()



    @classmethod
    def _tearDownArchiveSpecComponent(cls):
        ConfigurationTestUtils.removeArchiveSpecsDirectory()
        ConfigurationTestUtils.removeUserConfigDirectory()
        ComponentTestUtils.checkWorkDirEmptiness()



    @classmethod
    def makeArchiveSpecFile(cls, *, filePath = None, externals = (), name = None, path = None, includeFiles = "*",
                            excludeFiles = "", archiver = ArchiverTypes.TarGzInternal, destDir = None):
        "Creates an archive specification file."

        workDir = ComponentTestUtils.getComponentTestContext().workDir

        content = str.format("""\
{externalSectionDeclaration}
{externalSectionContent}
[Content]
{nameLine}
path = {path}
include-files = {includeFiles}
exclude-files = {excludeFiles}
[Archive]
archiver = {archiver}
dest-dir = {destDir}
""",
            externalSectionDeclaration = cls.__EXTERNAL_SECTION_PATTERN if externals else "",
            externalSectionContent = str.join(os.linesep, externals),
            nameLine = cls.__NAME_VARIABLE_PATTERN + name if name else "",
            path = path or workDir,
            includeFiles = includeFiles,
            excludeFiles = excludeFiles,
            archiver = OptionsUtils.archiverTypeToStr(archiver),
            destDir = destDir or workDir)

        archiveSpecFilePath = filePath if filePath else tempfile.mkstemp(suffix = ConfigConstants.ARCHIVE_SPEC_EXT,
            dir = ComponentTestUtils.getComponentTestContext().archiveSpecsDir)[1]
        with open(archiveSpecFilePath, "w") as archiveSpecFile:
            archiveSpecFile.write(content)
        return archiveSpecFilePath

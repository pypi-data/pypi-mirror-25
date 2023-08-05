# test_archive_spec.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2017 Róbert Čerňanský



""":class:`TestArchiveSpec`."""



__all__ = ["TestArchiveSpec"]



# {{{ INCLUDES

import unittest
import os
import tempfile

from AutoArchive._infrastructure.configuration import Options, ArchiverTypes
from .. import ArchiveSpec, ArchiveSpecOptions, ConfigConstants
from AutoArchive.tests import ComponentTestUtils
from AutoArchive._infrastructure.configuration.tests import ConfigurationTestUtils
from .archive_spec_test_utils import ArchiveSpecTestUtils

# }}} INCLUDES



# {{{ CLASSES

class TestArchiveSpec(unittest.TestCase):
    "Test of :class:`.ArchiveSpec`."

    @classmethod
    def setUpClass(cls):
        ArchiveSpecTestUtils._setUpClassArchiveSpecComponent()



    @classmethod
    def tearDownClass(cls):
        ArchiveSpecTestUtils._tearDownClassArchiveSpecComponent()



    def setUp(self):
        ArchiveSpecTestUtils._setUpArchiveSpecComponent()
        self.__irrelevantConfigurationMock = ConfigurationTestUtils.createConfigurationMock()



    def tearDown(self):
        ArchiveSpecTestUtils._tearDownArchiveSpecComponent()



    def test_constructorSimpleValuesRead(self):
        """Tests basic value reading from :term:`archive specification file`.

        Creates :term:`archive specification file` with simple values and passes it to the tested class.  Verify that
        values that has been put to the file can be read from the tested class."""

        TEST_NAME = "Test Name"
        TEST_PATH = ComponentTestUtils.getComponentTestContext().workDir
        TEST_ARCHIVER = ArchiverTypes.TarGzInternal
        TEST_DEST_DIR = "Test Dest Dir"

        archiveSpec = ArchiveSpec(
            ArchiveSpecTestUtils.makeArchiveSpecFile(name = TEST_NAME, path = TEST_PATH, archiver = TEST_ARCHIVER,
                destDir = TEST_DEST_DIR),
            self.__irrelevantConfigurationMock)

        self.assertEqual(TEST_NAME, archiveSpec[ArchiveSpecOptions.NAME])
        self.assertEqual(TEST_PATH, archiveSpec[ArchiveSpecOptions.PATH])
        self.assertEqual(TEST_ARCHIVER, archiveSpec[Options.ARCHIVER])
        self.assertEqual(TEST_DEST_DIR, archiveSpec[Options.DEST_DIR])



    def test_constructorFileValuesRead(self):
        """Tests file list value reading from :term:`archive specification file`.

        Creates :term:`archive specification file` with file list values and passes it to the tested class.  Verify
        that file list values that has been put to the file as string can be read from the tested class as
        a collection."""

        TEST_INCLUDE_FILES = {"Test Include File 1", "Test Include File 2"}
        TEST_EXCLUDE_FILES = {"Test Exclude File 1", "Test Exclude File 2"}

        for fileName in TEST_INCLUDE_FILES.union(TEST_EXCLUDE_FILES):
            filePath = os.path.join(ComponentTestUtils.getComponentTestContext().workDir, fileName)
            open(filePath, "w").close()

        archiveSpec = ArchiveSpec(
            ArchiveSpecTestUtils.makeArchiveSpecFile(
                includeFiles = str.join(" ", ('"' + s + '"' for s in TEST_INCLUDE_FILES)),
                excludeFiles = str.join(" ", ('"' + s + '"' for s in TEST_EXCLUDE_FILES))),
            self.__irrelevantConfigurationMock)

        for fileName in TEST_INCLUDE_FILES.union(TEST_EXCLUDE_FILES):
            filePath = os.path.join(ComponentTestUtils.getComponentTestContext().workDir, fileName)
            os.remove(filePath)

        self.assertSetEqual(TEST_INCLUDE_FILES, archiveSpec[ArchiveSpecOptions.INCLUDE_FILES])
        self.assertSetEqual(TEST_EXCLUDE_FILES, archiveSpec[ArchiveSpecOptions.EXCLUDE_FILES])



    def test_constructorMissingArchiveSection(self):
        """Tests that [Archive] section is can be missing.

        Creates :term:`archive specification file` without [Archive] section.  Verify that tested class can be
        instantiated with this file passed as parameter."""

        content = str.format("""\
        [Content]
        path = {path}
        include-files =
        exclude-files =
        """, path = ComponentTestUtils.getComponentTestContext().workDir)
        archiveSpecFilePath = tempfile.mkstemp(suffix = ConfigConstants.ARCHIVE_SPEC_EXT,
            dir = ComponentTestUtils.getComponentTestContext().archiveSpecsDir)[1]
        with open(archiveSpecFilePath, "w") as archiveSpecFile:
            archiveSpecFile.write(content)

        exception = None
        try:
            ArchiveSpec(archiveSpecFilePath, self.__irrelevantConfigurationMock)
        except Exception as ex:
            exception = ex
        finally:
            self.assertIsNone(exception)



    def test_constructorEmptyOption(self):
        """Tests that empty options are not allowed in .aa file."""

        content = str.format("""\
        [Content]
        path = {path}
        include-files =
        exclude-files
        [Archive]
        """, path = ComponentTestUtils.getComponentTestContext().workDir)
        archiveSpecFilePath = tempfile.mkstemp(suffix = ConfigConstants.ARCHIVE_SPEC_EXT,
            dir = ComponentTestUtils.getComponentTestContext().archiveSpecsDir)[1]
        with open(archiveSpecFilePath, "w") as archiveSpecFile:
            archiveSpecFile.write(content)

        with self.assertRaisesRegex(ValueError, "Option without a value found.+Content.+exclude-files"):
            ArchiveSpec(archiveSpecFilePath, self.__irrelevantConfigurationMock)



    def test_constructorExternalReferencesOneLevel(self):
        """Tests that value references from an external file are resolved.

        Creates a :term:`archive specification file` with a defined option and its value.  Then creates another
        one that has a reference to the option defined in the first file.  Passes the second file to the tested class
        and verifies that the value has been dereferenced."""

        TEST_DEST_DIR_EXTERNAL = "Test Dest Dir External"

        externalName = self.__externalName(ArchiveSpecTestUtils.makeArchiveSpecFile(destDir = TEST_DEST_DIR_EXTERNAL))

        archiveSpec = ArchiveSpec(
            ArchiveSpecTestUtils.makeArchiveSpecFile(externals = (externalName,),
                destDir = str.format("@({}.dest-dir)", externalName)),
            ConfigurationTestUtils.createConfigurationMock(
                {Options.ARCHIVE_SPECS_DIR: ComponentTestUtils.getComponentTestContext().archiveSpecsDir}))

        self.assertEqual(TEST_DEST_DIR_EXTERNAL, archiveSpec[Options.DEST_DIR])



    def test_constructorExternalReferencesTwoLevels(self):
        """Tests that value references from an external file which has reference to another one are resolved.

        Creates a :term:`archive specification file` with a defined option and its value and another file with a
        reference to that value.  Then creates third file that has a reference to the option defined in the second file.
        Passes the third file to the tested class and verifies that the value has been dereferenced."""

        TEST_PATH_EXTERNAL_1 = ComponentTestUtils.getComponentTestContext().workDir

        external1Name = self.__externalName(ArchiveSpecTestUtils.makeArchiveSpecFile(path = TEST_PATH_EXTERNAL_1))
        external2Name = self.__externalName(ArchiveSpecTestUtils.makeArchiveSpecFile(
            externals = (external1Name,),
            path = str.format("@({}.path)", external1Name)))

        archiveSpec = ArchiveSpec(
            ArchiveSpecTestUtils.makeArchiveSpecFile(
                externals = (external2Name,),
                path = str.format("@({}.path)", external2Name)),
            ConfigurationTestUtils.createConfigurationMock(
                {Options.ARCHIVE_SPECS_DIR: ComponentTestUtils.getComponentTestContext().archiveSpecsDir}))

        self.assertEqual(TEST_PATH_EXTERNAL_1, archiveSpec[ArchiveSpecOptions.PATH])



    def test_constructorExternalReferencesOneLevelWithAbsolutePath(self):
        """Tests that value references from an external file specified by path are resolved.

        Creates a :term:`archive specification file` with a defined option and its value.  Then creates another
        one that has a reference to the option defined in the first file; the reference is defined with full path to
        the referenced file.  Passes the second file to the tested class and verifies that the value has been
        dereferenced."""

        TEST_DEST_DIR_EXTERNAL = "Test Dest Dir External"

        EXTERNAL_ID = "testExternal"

        with tempfile.TemporaryDirectory(dir = ComponentTestUtils.getComponentTestContext().workDir) as customDirectory:
            archiveSpec = ArchiveSpec(
                ArchiveSpecTestUtils.makeArchiveSpecFile(
                    externals = (str.format("{} = {}",
                        EXTERNAL_ID,
                        ArchiveSpecTestUtils.makeArchiveSpecFile(
                            filePath = tempfile.mkstemp(
                                suffix = ConfigConstants.ARCHIVE_SPEC_EXT,
                                dir = customDirectory)[1],
                            destDir = TEST_DEST_DIR_EXTERNAL)),),
                    destDir = str.format("@({}.dest-dir)", EXTERNAL_ID)),
                self.__irrelevantConfigurationMock)

        self.assertEqual(TEST_DEST_DIR_EXTERNAL, archiveSpec[Options.DEST_DIR])



    def test_constructorExternalReferencesTwoLevelsWithAbsolutePathAndNonPath(self):
        """Tests that file plain-referenced in a custom location file is searched in
        :term:`archive specification directory`.

        Creates a file in archive specification directory and another file in a custom location which refers to the
        first one without specifying the path.  Then creates third file which refers to the second one, passes it
        to the tested class and verifies that a value has been dereferenced."""

        TEST_DEST_DIR_EXTERNAL_1 = "Test Dest Dir External 1"

        external1Name = self.__externalName(
            ArchiveSpecTestUtils.makeArchiveSpecFile(destDir = TEST_DEST_DIR_EXTERNAL_1))
        EXTERNAL_2_ID = "testExternal"

        with tempfile.TemporaryDirectory(dir = ComponentTestUtils.getComponentTestContext().workDir) as customDirectory:
            archiveSpec = ArchiveSpec(
                ArchiveSpecTestUtils.makeArchiveSpecFile(
                    externals = (str.format("{} = {}",
                        EXTERNAL_2_ID,
                        ArchiveSpecTestUtils.makeArchiveSpecFile(
                            filePath = tempfile.mkstemp(
                                suffix = ConfigConstants.ARCHIVE_SPEC_EXT,
                                dir = customDirectory)[1],
                            externals = (external1Name,),
                            destDir = str.format("@({}.dest-dir)", external1Name))),),
                    destDir = str.format("@({}.dest-dir)", EXTERNAL_2_ID)),
                ConfigurationTestUtils.createConfigurationMock(
                    {Options.ARCHIVE_SPECS_DIR: ComponentTestUtils.getComponentTestContext().archiveSpecsDir}))

        self.assertEqual(TEST_DEST_DIR_EXTERNAL_1, archiveSpec[Options.DEST_DIR])



    def test_constructorExternalReferencesOneLevelWithAbsoluteAndRelativePaths(self):
        """Tests that file relatively referenced by a custom location file is searched relatively to the custom location.

        Creates a file in a custom location and another one in a subdirectory which refers to the first one by relative
        path.  Then passes the second one to the tested class and verifies that a value has been dereferenced."""

        TEST_DEST_DIR_EXTERNAL = "Test Dest Dir External"

        EXTERNAL_ID = "testExternal"

        with tempfile.TemporaryDirectory(dir = ComponentTestUtils.getComponentTestContext().workDir) as customDirectory:
            with tempfile.TemporaryDirectory(dir = customDirectory) as customDirectorySubDir:
                archiveSpec = ArchiveSpec(
                    ArchiveSpecTestUtils.makeArchiveSpecFile(
                        filePath = tempfile.mkstemp(
                            suffix = ConfigConstants.ARCHIVE_SPEC_EXT,
                            dir = customDirectorySubDir)[1],
                        externals = (str.format("{} = {}",
                            EXTERNAL_ID,
                            ArchiveSpecTestUtils.makeArchiveSpecFile(
                                filePath = tempfile.mkstemp(
                                    suffix = ConfigConstants.ARCHIVE_SPEC_EXT,
                                    dir = customDirectory)[1],
                                destDir = TEST_DEST_DIR_EXTERNAL)),),
                        destDir = str.format("@({}.dest-dir)", EXTERNAL_ID)),
                    ConfigurationTestUtils.createConfigurationMock(
                        {Options.ARCHIVE_SPECS_DIR: ComponentTestUtils.getComponentTestContext().archiveSpecsDir}))

        self.assertEqual(TEST_DEST_DIR_EXTERNAL, archiveSpec[Options.DEST_DIR])



    def test_constructorExternalsReferencesCircularForDifferentOptions(self):
        """Tests circular references in different options are possible.

        Creates two :term:`archive specification files <archive specification file>` each has an option which references
        a different option in the other file.  Passes the first file to the tested class and verifies that the value
        has been dereferenced.  Same for the second file."""

        TEST_DEST_DIR = "Test Dest Dir External"
        TEST_PATH = ComponentTestUtils.getComponentTestContext().workDir

        configurationMock = ConfigurationTestUtils.createConfigurationMock(
            {Options.ARCHIVE_SPECS_DIR: ComponentTestUtils.getComponentTestContext().archiveSpecsDir})

        specFile2 = tempfile.mkstemp(suffix = ConfigConstants.ARCHIVE_SPEC_EXT,
            dir = ComponentTestUtils.getComponentTestContext().archiveSpecsDir)[1]

        external2Name = self.__externalName(specFile2)
        specFile1 = ArchiveSpecTestUtils.makeArchiveSpecFile(externals = (external2Name,),
            path = str.format("@({}.path)", external2Name), destDir = TEST_DEST_DIR)

        external1Name = self.__externalName(specFile1)
        specFile2 = ArchiveSpecTestUtils.makeArchiveSpecFile(filePath = specFile2, externals = (external1Name,),
            path = TEST_PATH, destDir = str.format("@({}.dest-dir)", external1Name))

        archiveSpec1 = ArchiveSpec(specFile1, configurationMock)
        archiveSpec2 = ArchiveSpec(specFile2, configurationMock)

        self.assertEqual(TEST_DEST_DIR, archiveSpec2[Options.DEST_DIR])
        self.assertEqual(TEST_PATH, archiveSpec1[ArchiveSpecOptions.PATH])



    def test_constructorExternalReferencesFileLists(self):
        """Tests that file list references from an external file are resolved.

        Creates a :term:`archive specification file` with a defined 'file list' option and its value.  Then creates
        another one that has a reference to the option defined in the first file.  Passes the second file to the tested
        class and verifies that the value has been dereferenced."""

        TEST_INCLUDE_FILES = {"Test Include File 1"}
        TEST_EXCLUDE_FILES = {"Test Exclude File 1", "Test Exclude File 2"}
        TEST_INCLUDE_FILES_EXTERNAL = {"Test External Include File 1", "Test External Include File 2"}

        for fileName in TEST_INCLUDE_FILES.union(TEST_EXCLUDE_FILES).union(TEST_INCLUDE_FILES_EXTERNAL):
            filePath = os.path.join(ComponentTestUtils.getComponentTestContext().workDir, fileName)
            open(filePath, "w").close()

        externalName = self.__externalName(ArchiveSpecTestUtils.makeArchiveSpecFile(
            includeFiles = str.join(" ", ('"' + s + '"' for s in TEST_INCLUDE_FILES_EXTERNAL))))

        archiveSpec = ArchiveSpec(
            ArchiveSpecTestUtils.makeArchiveSpecFile(
                externals = (externalName,),
                includeFiles = str.join(" ", ('"' + s + '"' for s in TEST_INCLUDE_FILES.union(
                    {str.format("@({}.include-files)", externalName)}))),
                excludeFiles = str.join(" ", ('"' + s + '"' for s in TEST_EXCLUDE_FILES))),
            ConfigurationTestUtils.createConfigurationMock(
                {Options.ARCHIVE_SPECS_DIR: ComponentTestUtils.getComponentTestContext().archiveSpecsDir}))

        for fileName in TEST_INCLUDE_FILES.union(TEST_EXCLUDE_FILES).union(TEST_INCLUDE_FILES_EXTERNAL):
            filePath = os.path.join(ComponentTestUtils.getComponentTestContext().workDir, fileName)
            os.remove(filePath)

        self.assertSetEqual(TEST_INCLUDE_FILES.union(TEST_INCLUDE_FILES_EXTERNAL),
            archiveSpec[ArchiveSpecOptions.INCLUDE_FILES])
        self.assertSetEqual(TEST_EXCLUDE_FILES, archiveSpec[ArchiveSpecOptions.EXCLUDE_FILES])



    def test_constructorExternalReferencesNotExistingOption(self):
        """Tests that exception is thrown when an not existing option is referenced.

        Creates a :term:`archive specification file`. Then creates another one that has a reference to a non existing
        option from the first file.  Passes the second file to the tested class and verifies that exception has been
        thrown."""

        externalName = self.__externalName(ArchiveSpecTestUtils.makeArchiveSpecFile())

        with self.assertRaisesRegex(ValueError, "Referenced option not found"):
            ArchiveSpec(
                ArchiveSpecTestUtils.makeArchiveSpecFile(externals = (externalName,),
                    destDir = str.format("@({}.not-existing-option)", externalName)),
                ConfigurationTestUtils.createConfigurationMock(
                    {Options.ARCHIVE_SPECS_DIR: ComponentTestUtils.getComponentTestContext().archiveSpecsDir}))



    def test_constructorExternalReferencesUnknownReference(self):
        """Tests that exception is thrown when an undeclared reference is used.

        Creates a :term:`archive specification file` with a defined option and its value.  Then creates another one
        that has a reference to the option defined in the first file but without declaring the referenced file.  Passes
        the second file to the tested class and verifies that exception has been thrown."""

        externalName = self.__externalName(ArchiveSpecTestUtils.makeArchiveSpecFile(destDir = "Any Dest Dir"))

        with self.assertRaisesRegex(ValueError, "Unknown external reference"):
            ArchiveSpec(
                ArchiveSpecTestUtils.makeArchiveSpecFile(externals = ("other-external",),
                    destDir = str.format("@({}.dest-dir)", externalName)),
                ConfigurationTestUtils.createConfigurationMock(
                    {Options.ARCHIVE_SPECS_DIR: ComponentTestUtils.getComponentTestContext().archiveSpecsDir}))



    def test_constructorExternalReferencesNotExistingFile(self):
        """Tests that exception is thrown when referenced file does not exists.

        Creates a :term:`archive specification file` that has a reference to an option from not existing file.  Passes
        it to the tested class and verifies that exception has been thrown."""

        NOT_EXISTING_SPEC_FILE_NAME = "not-existing-external"

        with self.assertRaisesRegex(OSError, NOT_EXISTING_SPEC_FILE_NAME):
            ArchiveSpec(
                ArchiveSpecTestUtils.makeArchiveSpecFile(externals = (NOT_EXISTING_SPEC_FILE_NAME,),
                    destDir = str.format("@({}.irrelevant-option)", NOT_EXISTING_SPEC_FILE_NAME)),
                ConfigurationTestUtils.createConfigurationMock(
                    {Options.ARCHIVE_SPECS_DIR: ComponentTestUtils.getComponentTestContext().archiveSpecsDir}))



    @staticmethod
    def __externalName(filePath):
        return os.path.basename(filePath).replace(ConfigConstants.ARCHIVE_SPEC_EXT, "")

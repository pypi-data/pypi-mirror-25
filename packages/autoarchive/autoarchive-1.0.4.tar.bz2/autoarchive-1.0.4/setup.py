#!/usr/bin/env python

# setup.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2015 Róbert Čerňanský



"""The setup script for AutoArchive."""



# {{{ INCLUDES

import sys, os, os.path, glob
from distutils.core import setup
from distutils.command.install_data import install_data
from distutils import log

sys.path.insert(0, "src")
from AutoArchive._meta import *

# }}} INCLUDES



# {{{ CLASSES

class PreserveLinksInstallData(install_data):
    """Subclass of the standard install_data command class which preserves symbolic links while copying a file."""
    
    def copy_file(self, src, dst, preserve_mode = 1, preserve_times = 1, link = None, level = 1):
        """Copy a file with preservation of symbolic links in mind.

        If ``src`` is symlink pointing to a relative destination, ``dst`` will be created as a symlink pointing to
        the same destination.  If ``dst`` is directory, symlink with the same name as ``src`` will be created in
        ``dst``.  If ``src`` if not symlink then base :meth:`copy_file()` method will be called."""

        copied = False

        # skip copying to destinations that are outside of prefix and are not writable; assuming that in such cases
        # the installation is provided in a python virtual environment where copying to system-wide absolute paths
        # is not desirable (installation programs should do this so perhaps this workaround will be removed once)
        # (the program will function correctly because the only file installed outside the prefix is the system-wide
        # configuration file /etc/aa/aa.conf which is ignored when not existing)
        if os.path.normpath(os.path.commonprefix([sys.prefix, dst])) != os.path.normpath(sys.prefix):
            if not os.access(dst, os.W_OK):
                log.warn("skipping (destination is not writable)! %s -> %s", src, dst)
                return dst, copied

        # if src is relative symbolic link, create dst as symlink pointing to the same destination
        if os.path.islink(src):
            linkDestination = os.readlink(src)
            if not os.path.isabs(linkDestination):
                
                if os.path.isdir(dst):
                    dstFile = os.path.join(dst, os.path.basename(src))
                else:
                    dstFile = dst

                log.info("copying symlink %s -> %s", src, dst)
                if not self.dry_run:
                    os.symlink(linkDestination, dstFile)
                copied = True

        # call base copy_file() method if symlink was not created
        if not copied:
            (dstFile, copied) = super().copy_file(src, dst, preserve_mode = preserve_mode,
                                                  preserve_times = preserve_times, link = link, level = level)

        return dstFile, copied

# }}} CLASSES



# {{{ FUNCTIONS

def findDataFiles(destDir, srcDir):
    """Returns content of ``srcDir`` in a format required by ``data_files``."""

    dataFiles = []
    srcDirName = os.path.dirname(srcDir)
    for root, dirs, files in os.walk(srcDir):
        if files:
            dataFiles.append(
                (os.path.join(destDir, os.path.relpath(root, srcDirName)),
                 list(map(lambda f: os.path.join(root, f), files))))
    return dataFiles

# }}} FUNCTIONS



# {{{ MAIN PROGRAM

docDir = os.path.join("share/doc", _Meta.PACKAGE_NAME + "-" + _Meta.VERSION)

dataFiles = [
    ("/etc/aa", ["data/configuration/aa.conf"]),
    ("share/man/man1", ["doc/user/man/aa.1", "doc/user/man/autoarchive.1"]),
    ("share/man/man5", ["doc/user/man/aa.conf.5",
                        "doc/user/man/aa_arch_spec.5"]),
    (docDir, ["README", "README.sk", "NEWS", "COPYING"]),
    (os.path.join(docDir, "examples"), glob.glob("doc/user/examples/*")),
    ("bin", ["bin/autoarchive"])
    ]

dataFiles.extend(findDataFiles(docDir, "doc/user/html"))

setup(
    name = _Meta.PACKAGE_NAME,
    version = _Meta.VERSION,
    description = _Meta.DESCRIPTION,
    long_description = """\
**AutoArchive** is a simple utility to help create backups more easily.  The
idea of the program is that all essential information for creating a single
backup---such as list of directories that should be archived, the archive name,
etc.---is stored in a single file -- the `archive specification file`.  It can
use ‘tar’ for creating archives, it has a command line interface and supports
incremental backups.""",
    author = "Róbert Čerňanský",
    author_email = "openhs@users.sourceforge.net",
    url = "http://autoarchive.sourceforge.net",
    license = "GNU GPLv3",
    keywords = "backup archive compression",
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: POSIX",
        "Topic :: System :: Archiving :: Backup",
        "Topic :: System :: Archiving :: Compression",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities"
    ],

    packages = ["AutoArchive",
                "AutoArchive._services", "AutoArchive._services.archiver",
                "AutoArchive._archiving", "AutoArchive._archiving._core",
                "AutoArchive._configuration",
                "AutoArchive._configuration._core",
                "AutoArchive._mainf", "AutoArchive._mainf._core",
                "AutoArchive._ui",
                "AutoArchive._ui._cmdline", "AutoArchive._ui._cmdline._core"],
    scripts = ["bin/aa"],
    data_files = dataFiles,

    cmdclass = {"install_data": PreserveLinksInstallData}
    )

# }}} MAIN PROGRAM

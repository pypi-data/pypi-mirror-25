.. config_file.rst
.. 
.. Project: AutoArchive
.. License: GNU GPLv3
.. 
.. Copyright (C) 2003 - 2017 Róbert Čerňanský



.. User documentation - configuration file description



.. _config_file:

Configuration File
==================

.. begin_format

There are two configuration files for AutoArchive -- *system-* and *user-*.  *System configuration file's* location is:
"/etc/aa/aa.conf".  *User configuration file's* location is by default: "~/.config/aa/aa.conf".  Options in the *user
file* have higher priority.  Note that some options can only be specified in the *system file* (see the list of the
options below).

Structure is similar to the `archive specification file` -- options are divided into sections.  A section begins with
the section name enclosed in square brackets.  Sections contains variables which represents the options.

Variables are written in the ``option-name = value`` form, one variable per line.  Boolean values are written as
``yes`` and ``no``.  For path values, tilde (``~``) is expanded to the user's home.  Form ``option-name =`` can be
used to specify a variable with undefined value.

Lines beginning with ``#`` or ``;`` are ignored and may be used for comments.

Two sections are valid: ``[General]`` and ``[Archive]``.  Both are optional although a configuration file without any
section at all is considered invalid.



Section ``[General]``
---------------------

Contains configuration options for the program itself, which do not alter the backup creation.

**Options valid in the [General] section:**

  - verbose

  - quiet

  - archive-specs-dir

  - user-config-file

    This option can not be specified in the *user configuration file*.

  - user-config-dir

    This option can not be specified in the *user configuration file*.

See |usage_ref| for their description.



Section ``[Archive]``
---------------------

This section contains configuration options which are specific to the backup creation.

**Options valid in the [Archive] section:**

  - archiver

  - compression-level

  - dest-dir

  - overwrite-at-start


  - incremental

  - restarting

  - restart-after-level

  - restart-after-age

  - full-restart-after-count

  - full-restart-after-age

  - max-restart-level-size

  - remove-obsolete-backups


  - keep-old-backups

  - number-of-old-backups


  - command-before-all-backups

  - command-after-all-backups

  - command-before-backup

  - command-after-backup


  - force-archiver

  - force-incremental

  - force-restarting

  - force-compression-level

  - force-dest-dir

  - force-overwrite-at-start

See |usage_ref| for their description.

.. end_format



.. |usage_ref| replace:: :ref:`usage`

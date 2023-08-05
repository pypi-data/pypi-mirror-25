.. description.rst
.. 
.. Project: AutoArchive
.. License: GNU GPLv3
.. 
.. Copyright (C) 2003 - 2012 Róbert Čerňanský



.. User documentation - program description



===================
Program Description
===================

.. begin_description

**AutoArchive** is a simple utility to help create backups more easily.  The idea of the program is that all essential
information for creating a single backup---such as list of directories that should be archived, the archive name,
etc.---is stored in a single file -- the `archive specification file`.  It can use |tar_ref| for creating archives, it
has a command line interface and supports incremental backups.

Archive specification files, also called ".aa files" are normally stored in a predefined location from where they are
processed by the ``aa`` command which results to creating of a corresponding `backup` for each.

Command ``autoarchive`` is alias for ``aa``; these commands are equivalent.

.. end_description



.. _usage:

Usage
=====

.. begin_synopsis

| **aa** [*options*] [*command*] [*AA_SPEC*]...
| **autoarchive** [*options*] [*command*] [*AA_SPEC*]...

.. end_synopsis

.. begin_usage

Most of the options can be specified also in *configuration files* and in the `archive specification file` (by using
the long option form and leaving out leading dashes) -- see |configs_reference_text| for complete list of options that
can be specified there.  Command line options has higher priority than options in configuration files but lower
priority than the ones in the archive specification file.  ``--force-*`` options are available for the purpose of
overriding some of the options specified in the `.aa file`.

Boolean options can also have a negation form defined.  It has the "no-" prefix before the option name.  For example:
``--incremental`` vs. ``--no-incremental``.  The negation form has always higher priority than the normal form.

.. end_usage

**List of command line options**

.. begin_options
..

   **Commands:**

   Commands for program's operations.  The default operation is the `backup` creation if no command is specified.

   --list
      Show all `configured <configured archive>` or `orphaned archives <orphaned archive>`.
   --purge
      Purge stored data for an orphaned archive.
   --version
      Show program's version number and exit.

   -h, --help
      Show this help message and exit.

   **Archiving options:**

   -a ARCHIVER, --archiver=ARCHIVER
      Specify archiver type.  Supported types are: 'tar', 'targz', 'tarbz2', 'tarxz', 'tar_internal',
      'targz_internal', 'tarbz2_internal' (default: targz).

   -c NUM, --compression-level=NUM
      Compression strength level.  If not specified, default behaviour of underlying compression program will be used.

   -d DIR_PATH, --dest-dir=DIR_PATH
      Directory where the `backup` will be created (default: <current directory>).

   **Incremental archiving options:**

   -i, --incremental
      Perform incremental backup.

   -l LEVEL, --level=LEVEL
      Specify backup level which should be created.  All information about higher levels---if any exists---will be
      erased.  If not present, the next level in a row will be created.
   --restarting
      Turns on backup level restarting.  See other ``*restart-*`` options to configure the restarting behaviour.

   --restart-after-level=LEVEL
      Maximal backup level.  If reached, it will be restarted back to a lower level (which is typically level 1 but it
      depends on ``--max-restart-level-size``) (default: 10).
   --restart-after-age=DAYS
      Number of days after which the backup level is restarted.  Similarly to ``--restart-after-level`` it will be
      restarted to level 1 or higher.

   --full-restart-after-count=COUNT
      Number of backup level restarts after which the level is restarted to 0.
   --full-restart-after-age=DAYS
      Number of days after which the backup level is restarted to 0.
   --max-restart-level-size=PERCENTAGE
      Maximal percentage size of a `backup` (of level > 0) to which level is allowed restart to.  The size is
      percentage of size of the level 0 backup file.  If a backup of particular level has its size bigger than
      defined percentage, restart to that level will not be allowed.
   --remove-obsolete-backups
      Turns on removing backups of levels that are no longer valid due to the backup level restart.  All backups of
      the backup level higher than the one currently being created will be removed.

   **General options:**

   -v, --verbose
      Turns on verbose output.
   -q, --quiet
      Turns on quiet output.  Only errors will be shown.  If ``--quiet`` is turned on at the same level as
      ``--verbose`` (e. g. both are specified on the command line) then ``--quiet`` has higher priority than
      ``--verbose``.
   --all
      Operate on all `configured archives <configured archive>`. See also ``--archive-specs-dir``.

   --archive-specs-dir=DIR_PATH
      Directory where `archive specification files <archive specification file>` will be searched for (default:
      ~/.config/aa/archive_specs).
   --user-config-file=FILE_PATH
      Alternate user configuration file (default: ~/.config/aa/aa.conf).
   --user-config-dir=DIR_PATH
      Alternate user configuration directory (default: ~/.config/aa).

   **Force options:**

   Options to override standard options defined in archive specification files.

   --force-archiver=ARCHIVER
      Force archiver type.  Supported types are: 'tar', 'targz', 'tarbz2', 'tarxz', 'tar_internal',
      'targz_internal', 'tarbz2_internal'.
   --force-incremental
      Force incremental backup.
   --force-restarting
      Force backup level restarting.
   --force-compression-level=NUM
      Force compression strength level.
   --force-dest-dir=DIR_PATH
      Force the directory where the backup will be created.

   **Negation options:**

   Negative variants of standard boolean options.

   --no-incremental
      Disable incremental backup.
   --no-restarting
      Disable backup level restarting.
   --no-all
      Do not operate on all `configured archives <configured archive>`.

.. end_options

.. begin_aa_spec

*AA_SPEC* is the *archive specification file argument*.  It determines the `archive specification file` that shall be
processed.  None, single or multiple *AA_SPEC* arguments are allowed.  If option ``--all`` or command ``--list`` is
specified then no *AA_SPEC* argument is required.  Otherwise at least single *AA_SPEC* argument is required.  If it
contains the ".aa" extension then it is taken as the path to an archive specification file.  Otherwise, if specified
without the extension, the corresponding `.aa file` is searched in the `archive specifications directory`.

.. end_aa_spec



Exit Codes
==========

.. begin_exit_codes

AutoArchive can return following exit codes:

   - 0: The operation finished successfully.

   - 1: The operation finished with minor (warnings) or major (errors) issues.

.. end_exit_codes



Files
=====

.. begin_files

*~/.config/aa/aa.conf*
   User configuration file.  See |config_file_ref| for its description.

*~/.config/aa/archive_specs/*
   Default directory that contains `archive specification files <archive specification file>`.  See |arch_spec_ref| for
   description of the `.aa file` format.

*~/.config/aa/snapshots/\*.snar*
   Files that stores information about incremental backup.  They are created by |gnu_tar_ref| archiver.

*~/.config/aa/storage/\*.realm*
   Application internal persistent storage.  It stores various data needed to be preserved between program runs.  For
   example: last backup level restart, number of backup level restart, etc.

*/etc/aa/aa.conf*
   System configuration file.  See |config_file_ref| for its description.

.. end_files



.. |configs_reference_text| replace:: |config_file_ref| and |arch_spec_ref|

.. |tar_ref| replace:: :command:`tar`

.. |gnu_tar_ref| replace:: **GNU tar**

.. |config_file_ref| replace:: :ref:`config_file`

.. |arch_spec_ref| replace:: :ref:`arch_spec`

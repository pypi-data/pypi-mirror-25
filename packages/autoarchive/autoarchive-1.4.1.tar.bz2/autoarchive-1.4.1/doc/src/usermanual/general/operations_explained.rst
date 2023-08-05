.. operations_explained.rst
.. 
.. Project: AutoArchive
.. License: GNU GPLv3
.. 
.. Copyright (C) 2003 - 2014 Róbert Čerňanský



.. User documentation - program operations description



====================
Operations Explained
====================

AutoArchive can execute several commands.  Besides the `backup` creation---its main function---it can show list of
`configured <configured archive>` and `orphaned archives <orphaned archive>` displaying various information about them,
or perform a cleaning action that wipes the orphaned archive data.  The operation is chosen by specifying the
corresponding command as a program's argument.  For list of all commands see the :ref:`usage` section.



Configuring the Archive
=======================

One of the actions that is actually not handled by the AutoArchive is the configuration of the `archive`.  In order to
be able to create a `backup` AutoArchive has to be provided by an `archive specification file`.  It needs to be created
manually and placed to `archive specifications directory` or path to it passed as the program's argument.  Archive
specification file is a plain text file with simple structure which is described in the :ref:`config_file` section.
Sample files are distributed with the program and an example is provided also in the
:ref:`configuring_the_archive_example` section.



Backup Creation
===============

Main AutoArchive's function is the `backup` creation.  It is the default operation so no command needs to be specified
in order to create one.  Name or path to an `archive specification file` is required unless ``--all`` option is given.
By default non-incremental *tar.gz* backup is created in the current directory.  This can be changed with options on
the command line, configuration files or the archive specification file itself.  A simple example of the backup
creation is shown in the :ref:`backup_creation_example` section.  See also :ref:`usage`, :ref:`config_file` and
:ref:`arch_spec` sections for all possible configuration options.


Incremental Backup Creation
---------------------------

Passing ``-i`` option on the commandline or specifying corresponding configuration option in a configuration file
causes creation of incremental backups.  In this case a single full backup is created upon first execution.  Subsequent
executions will create diff backups with increasing `backup level`.  To restore a backup the full backup plus all
`increments <increment>` (or all increment up to the desired restoration point) are required.  Options for manual or
automatic restarting to a particular lower level are available.  When restarting is applied option
``--remove-obsolete-backups`` can be specified to remove backups that becomes obsolete due to the restart.


Keeping old backups
-------------------

In order to reduce risk of losing a valuable older backup AutoArchive can keep backups which are going to be
removed or overwritten during a new backup creation.  This feature makes possible to have desired number of older
backups always available with or without using the incremental archiving.  To enable it use ``-k`` option and to
specify desired number of kept backups use the ``--number-of-old-backups=NUM`` option.  The option
``--remove-obsolete-backups`` can be used to automatically remove `kept backups <kept backup>` which may become
obsolete due to lowering the ``--number-of-old-backups=NUM`` value.

Each kept backup (or series of kept backup `increments <increment>` in case of incremental archiving) has its own
`keeping ID`.  The most recent kept backup gets keeping ID 'aa', second most recent gets 'ab' and so on up to
maximal value 'zz' (which is by default further limited by ``--number-of-old-backups=NUM``\ ).  When a new backup is
going to be kept back all existing kept backup are shifted so that they get higher keeping ID.  Backups with
keeping ID 'aa' will get 'ab', those with 'ab' gets 'ac' and so on.  When number of kept backups would exceed value
of the ``--number-of-old-backups=NUM`` option the last kept backup (with highest keeping ID) is removed.

Refer to :ref:`backup_keeping_example` section for an example.



.. _listing_archives:

Listing Archives
================

In order to list all archives and show information about them the ``--list`` command is provided.  By default it shows
all `archives <archive>` that are known to AutoArchive and `orphaned archives <orphaned archive>`.  Note that “archive”
here means the “archive configuration”, which is represented by the `archive specification file`, not the result of the
`backup` creation (the \*.tar.gz file).  If one or more names or paths to archive specification files are passed as
arguments it lists only those.

The output has two forms: normal and verbose.


.. _normal_output:

Normal output
-------------

The structure of the normal ``--list`` output is following::

   <Name> <Root> <Destination directory> <Current backup level/next/max.>

An `archive` per line is listed.


Verbose output
--------------

If ``--verbose`` option is specified alongside with ``--list`` the verbose form is printed.  It shows following
information::

   Name: 
   Root: 
   Archiver type: 
   Destination directory: 
   Current backup level/next/max.: 
   Target backup level for non-full restart: 
   Upcoming restart reason: 
   Restart count/max.: 
   Days since last restart/max.: 
   Days since last full restart/max.: 

**The meaning of the particular fields is:**

Name
   `Archive` name as determined from `archive specification file` name or the ``name`` option.

Root
   Archive's root path as configured with ``path`` option.

Archiver type
   Type of the archiver as configured with the ``archiver`` option.

Destination directory
   Directory where the `backup` will be created as configured with the ``dest-dir`` option.

Current backup level/next/max.
   Corresponds to "Current backup level/Next backup level/Maximal backup level". Current backup level is the backup
   level that was created in last backup creation.  Next backup level is the backup level that will be created in next
   backup creation (if restarting is enabled it will not be always the next level in a row).  Maximal backup level is
   the value configured with the ``restart-after-level`` option.

Target backup level for non-full restart
   Backup level to which will be restarted to in case of non-full backup level restart (for example if
   ``restart-after-level`` value is reached.  It is typically 1 but can be higher due to ``max-restart-level-size``
   option.

Upcoming restart reason
   Show the reason of following backup level restart.

Restart count/max.
   Number of non-full backup level restarts and maximal number of restarts as configured with the
   ``full-restart-after-count`` option.

Days since last restart/max.
   Number of days since last non-full backup level restart occurred and maximal number of days without a restart as
   configured with the ``restart-after-age`` option.

Days since last full restart/max.
   Number of days since last full backup level restart occurred and maximal number of days without a full restart as
   configured with the ``full-restart-after-age`` option.


Value format
------------

If the value is enclosed in square brackets ([]) it means that it is not relevant to the current `archive`
configuration.  For example if an archive was previously configured as incremental and some incremental `backups
<backup>` were already created, and its configuration was changed to non-incremental later, then the actual backup
levels are shown but they are enclosed in square brackets.  **In case of** `orphaned archives <orphaned archive>`
**the** *name* **is enclosed in square brackets.**

If the value is not applicable or not available a dash (-) is printed instead.

Sometimes a question mark (?) is printed instead of the value which means that the value could not be determined while
it is expected to be available.  This happens mostly for orphaned archives where only a limited
number of information is available.



Cleaning Orphaned Information
=============================

`Orphaned archives <orphaned archive>` shown in the ``--list`` output with their names enclosed in square brackets does
not have a corresponding `archive specification file`.  It is just leftover information saved in a previous backup
creation operation (it is not the `backup` itself).  This information can be removed with the ``--purge`` command.  It
may be provided with the orphaned archive name in order to remove information about that particular `archive` or with
the ``--all`` option in order to remove information about all orphaned archives.

Note that the ``--purge`` command does not remove created backups.



Restoration of the Backup
=========================

AutoArchive does not handle backup restoration by itself.  `Backups <backup>` can be restored by using standard
|gnu_tar_ref| archiver or any other tar-compatible archiver.  Please see the |gnu_tar_ref| documentation for more
information or the :ref:`backup_restoration_example` section for examples on restoring backups.



.. |gnu_tar_ref| replace:: **GNU tar**

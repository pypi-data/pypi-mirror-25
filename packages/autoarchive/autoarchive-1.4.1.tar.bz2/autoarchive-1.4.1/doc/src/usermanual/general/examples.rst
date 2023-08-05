.. examples.rst
.. 
.. Project: AutoArchive
.. License: GNU GPLv3
.. 
.. Copyright (C) 2003 - 2017 Róbert Čerňanský



.. User documentation - examples



========
Examples
========

.. begin_examples

Let's make a `backup` of configuration files of all users except the user "foo".  Let's assume that our system has
unix-like style of home directories (directory "/home" contains directories of all users; configuration files begins
with dot).  Name of this backup will be "user-configs".

.. end_examples



.. _configuring_the_archive_example:

Configuring the Archive Example
===============================

.. begin_examples_configuring

First, we need to create the file "user-configs.aa" under the "~/.config/aa/archive_specs/" directory - this is the
`archive specification file`.  The file doesn't need to have the same name as the `backup`.  If it does however, the
option ``name`` can be left out (in this example we specified it anyway, even it is not needed).

In the ``path`` variable we specify the archive root which is the **the base directory which content we want to
backup**.

Variables ``include-files`` and ``exclude-files`` contains list of files and directories that we want to be included or
excluded respectively.  In this example we specify ``*/.*`` pattern because we want to include home directories of all
users (such as /home/**bob**, /home/**joe**, etc.), what the first ``*`` is for.  And from within those user home
directories we want to include everything that begins with ``.`` (for example /home/bob/**.bashrc**), what the ``.*``
pattern is for.  Paths specified in these variables are relative to ``path``.

Although, yet we do not want to include *all* user home directories as we specified in ``include-files``.  Those
directories that should not be included we put in ``exclude-files`` ("foo" in this example, which makes /home/foo
excluded).  If we would not want to exclude any file then the corresponding variable would be specified as
``exclude-files =``.

Content of the "user-configs.aa" file:

.. code-block:: ini

   # ------ begin of user-configs.aa ------
   # AutoArchive's archive specification file for users configuration files
   [Content]
   name = user-configs
   path = /home
   include-files = */.*
   exclude-files = foo

   [Archive]
   dest-dir = /mnt/backup
   # ------ end of user-configs.aa ------

.. end_examples_configuring



.. _backup_creation_example:

Backup Creation Example
=======================

.. begin_examples_backup_creation

Once we configured the `archive` we can create the `backup` easily with command::

   aa user-configs

and in the "/mnt/backup" directory the file "user-configs.tar.gz" will be created.

Given the "user-configs.aa" example file above, the command::

   aa -i user-configs

will create **level 0** incremental backup -- "user-configs.tar.gz" which is essentially the same as a
non-incremental backup.  Another execution of the same command will create **level 1** backup named
"user-configs.1.tar.gz" which contains only a differences from level 0.  Each subsequent call will create a **next
level** which will contain only a differences from previous.

In order to restart to level 0 again, thus create a **fresh full backup**, the following command can be used::

  aa -i -l 0 user-configs

Note that you **should remove** all previously created "user-configs" backups with `level` higher than 0
because they are no longer valid in regards to the newly created level 0 backup.  You may pass
``--remove-obsolete-backups`` option to the command above and they will be removed automatically.

.. end_examples_backup_creation



.. _backup_keeping_example:

Backup Keeping
--------------

.. begin_examples_backup_keeping

We assume that all previously created backups were removed in order to demonstrate the backup keeping.

First we create a standard backup::

   aa user-configs

This creates "user-configs.tar.gz" backup.  Some days later let's say, we want to create the same backup again.
However we do not want to overwrite the original one.  The option ``-k`` can be used to keep the original backup::

   aa -k user-configs

This will rename the original backup to "user-configs.\ **aa**\ .tar.gz" and create the new one "user-configs.tar.gz".
If we create the same backup for the third time (still using the ``-k``) option, "user-configs.aa.tar.gz" will be
removed, "user-configs.tar.gz" will be renamed to "user-configs.aa.tar.gz" and the new "user-configs.tar.gz" will be
created.  So AutoArchive by default keeps single old backup when ``-k`` options is specified.  To keep more, e.g. four
backups we would specify ``--number-of-old-backups=4`` alongside with ``-k``\ .

Incremental backups can be kept as well.  Again, we assume that all previously created backups were removed.  Let's
create a few levels of incremental "user-configs" archive::

   aa -i -l 0 user-configs
   aa -i user-configs
   aa -i user-configs
   aa -i user-configs

This will create following files::

   user-configs.tar.gz
   user-configs.1.tar.gz
   user-configs.2.tar.gz
   user-configs.3.tar.gz

Then we (manually) restart to level 2 while asking to keep old backups::

   aa -i -l 2 -k user-configs

After this command following files will be present::

   user-configs.tar.gz
   user-configs.1.tar.gz
   user-configs.2.tar.gz
   user-configs.2.aa.tar.gz
   user-configs.3.aa.tar.gz

Let's explain what happened.  The original file "user-configs.2.tar.gz" was going to be overwritten therefore it was
renamed to "user-configs.2.aa.tar.gz".  As all backup levels higher than the renamed one depends on it they have to be
renamed as well.  In this example "user-configs.3.tar.gz" depends on "user-configs.2.tar.gz" therefore it was renamed
to "user-configs.3.aa.tar.gz".  Finally the new `increment` "user-configs.2.tar.gz" was created.

.. end_examples_backup_keeping



Listing Archives Example
========================

Our "user-configs" `archive` can be listed by following command::

   aa --list

Which results to the following output::

   user-configs /home                    /mnt/backups               [0]/[1]/[10]

If we pass ``--verbose`` option then it shows::

   Name: user-configs
   Root: /home
   Archiver type: targz
   Destination directory: /mnt/backups
   Current backup level/next/max.: [0]/[1]/[10]
   Target backup level for non-full restart: [1]
   Upcoming restart reason: [No restart scheduled for the next backup.]
   Restart count/max.: [-]/[-]
   Days since last restart/max.: [-]/[-]
   Days since last full restart/max.: [-]/[-]

The archive *Name* is "user-configs" as configured with the ``name`` variable in the
:ref:`configuring_the_archive_example` section.  *Root* corresponds to the value configured with the ``path`` variable.
*Archiver type* is "targz" which is the default.  *Destination directory* "/mnt/backup" is configured with ``dest-dir``
variable.  *Current backup level/next/max.* shows [0]/[1]/[10] because in the section :ref:`backup_creation_example` we
have created an incremental backup of level 0, so current level is 0.  Next level is 1 (restarting is not enabled).
Both the current and the next levels are enclosed in square brackets because incremental archiving is not enabled (it
was enabled only temporarily with the ``-i`` option).  Finally, the maximal backup level is 10 as it is the default.
It is also shown in square brackets because restarting is not enabled; this also applies for all following values.
Since no ``max-restart-level-size`` is specified the *Target backup level for non-full restart* is and always be 1.
Obviously, no restart is scheduled as the *Upcoming restart reason* value is showing.  Since no restart ever occurred
and no value is specified for the rest of restarting options the values *Restart count/max.*, *Days since last
restart/max.* and *Days since last full restart/max.* shows only dashes.



Cleaning Orphaned Information Example
=====================================

If we remove the "user-configs.aa" `archive specification file` then the ``--list`` will still be showing the `archive`
with its name enclosed in square brackets (it becomes the `orphaned archive`)::

   [user-configs] ?                    .                            [0]/[?]/[10]

This is because some information is still stored in the AutoArchive's configuration directory.  It is the snapshot file
created by :command:`tar` when incremental `backup` was created.  There may be more information left behind if
restarting would be enabled.  All of this orphaned information can be deleted with the ``--purge`` command::

   aa --purge user-configs

or::

   aa --purge --all

which would remove all orphaned archives.



.. _backup_restoration_example:

Backup Restoration Example
==========================

Restoring Non-Incremental Backup
--------------------------------

Let's say we have created simple (non-incremental) backup as in the :ref:`backup_creation_example`.  Thus we have
a file called "user-configs.tar.gz" in the "/mnt/backup" directory.  As the AutoArchive does not handle restoration we
will use standard **GNU tar** archiver.

To restore the backup to its original destination and thus **replace all existing files with the ones from the
backup** we can use following command::

   tar -xf /mnt/backup/user-configs.tar.gz -C /home

The value of the ``-C`` option (/home) is the same as the value of ``path`` variable in the "user-configs.aa".  The
``-C`` option can be left out if the destination is the *current working directory* (in other words you did "cd /home"
earlier).

Of course the backup can be restored to any arbitrary location by replacing "/home" with some other path in the command
above.  This may be more safe and convenient as it does not replaces original files.  The extracted backup files can be
reviewed and copied to the original destination afterwards.  You may also use a graphical file manager or an archive
manager to browse content of the backup interactively.


Restoring Incremental Backup
----------------------------

Suppose we have several increments of the "user-configs" archive in the /mnt/backup directory.  The content of the
directory is following::

   $ ls -1 /mnt/backup
   -rw-r--r-- 1 root root  10M Apr 20 17:07 user-configs.tar.gz
   -rw-r--r-- 1 root root   1M May 11 12:21 user-configs.1.tar.gz
   -rw-r--r-- 1 root root 1.5M Jun 26 16:43 user-configs.2.tar.gz

Which means we have backup level 0, 1 and 2.  To restore entire backup to the latest possible date (in this case
Jun 26) we have to restore all backup levels.  Similarly to the previous example the following series of commands will
restore the backup to the original location **replacing** the original files there::

   tar -xf /mnt/backup/user-configs.tar.gz -G -C /home
   tar -xf /mnt/backup/user-configs.1.tar.gz -G -C /home
   tar -xf /mnt/backup/user-configs.2.tar.gz -G -C /home

As in the previous example the "-C /home" can be left out (backup will be restored to the current directory) or "/home"
replaced with some other path (backup will be restored to that path).



.. _referring_to_external_archive_specification_example:

Referring To External Archive Specification Example
===================================================

.. begin_examples_referring_to_external_archive_specification

In this example we want to configure `archive` for "/data" directory `backups <backup>`.  There will be two locations
where backups are stored.  One is a large capacity NAS mounted at "/mnt/nas", the other is a smaller external disk
mounted at "/mnt/backup_disk".

Below is content of two `archive specification files <archive specification file>` for this use case.  The first one
configures archive "data-nas" for NAS storage destination.  Second file configures archive "data-disk" for
external disk location.  It is taking all values except ``dest-dir`` from the "data-nas.aa" file via external
references.  Additionally it excludes "videos" directory so that backup will fit to disk.

.. code-block:: ini

   # ------ begin of data-nas.aa ------
   [Content]
   path = /
   include-files = data-nas
   exclude-files =

   [Archive]
   dest-dir = /mnt/nas
   # ------ end of data-nas.aa ------

.. code-block:: ini

   # ------ begin of data-disk.aa ------
   [External]
   data-nas

   [Content]
   path = @(data-nas.path)
   include-files = @(data-nas.include-files)
   exclude-files = @(data-nas.exclude-files) videos

   [Archive]
   dest-dir = /mnt/backup_disk
   # ------ end of data-disk.aa ------



Specifying path to the external file
------------------------------------

Would the "data-nas.aa" file in previous example be in a different directory than `archive specifications directory` its
path had to be specified:

.. code-block:: ini

   # ------ begin of data-disk.aa ------
   [External]
   data-nas = /path/to/data-nas.aa

   [Content]
   # ...
   # ------ end of data-disk.aa ------

.. end_examples_referring_to_external_archive_specification

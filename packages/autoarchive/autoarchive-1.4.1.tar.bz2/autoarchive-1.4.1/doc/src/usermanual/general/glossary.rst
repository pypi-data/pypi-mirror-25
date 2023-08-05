.. arch_spec.rst
.. 
.. Project: AutoArchive
.. License: GNU GPLv3
.. 
.. Copyright (C) 2003 - 2014 Róbert Čerňanský



.. User documentation - glossary



.. _glossary:

Glossary
========

.. glossary::

   .aa file
      A synonym for `archive specification file`.

   archive
      The primary entity that AutoArchive operates with.  It has a name and holds the configuration used to create the
      corresponding `backup`.  `Archive` is represented by the `archive specification file`.

   archive specification file
      The configuration of an `archive`.  It contains all information needed for creation of a single backup, such as:
      archive name, archive root directory, list of directories and files which should be **included** and
      **excluded**, etc.  It can also contain some of the configuration options.  The file has extension ‘.aa’ and is
      sometimes referred as “.aa file”.  For more information see :ref:`arch_spec`.

   archive specifications directory
      Directory where `archive specification files <archive specification file>` are stored.  It can be configured via
      the ``archive-specs-dir`` option.

   backup
      Result of the backup creation operation.  For example a \*.tar.gz file.

   backup level
      For incremental `archives <archive>` it represents an iteration of a particular `backup`.  It start from 0 which
      always represents the full backup.  Values 1 and greater represents diff backups to previous `level`.  The
      physical representation of a backup level is `increment`.

   configured archive
      See `archive`.

   increment
      A `backup` that has a particular `backup level`.  For example a \*.2.tar.gz file is increment of backup level 2.
      It applies to incremental `archives <archive>`.

   keeping ID
      The identification of `kept backups <kept backup>`.  It can have values from a following set: 'aa', 'ab', ...,
      'zy', 'zz' where 'aa' is ID of the most recent kept backup.

   kept backup
      A `backup` that normally should have been already removed or overwritten but was preserved under a different
      name.  The new name consists of the original name and its `keeping ID`, for example \*.aa.tar.gz is a
      `kept backup` with keeping ID 'aa'.

   level
      See `backup level`.

   orphaned archive
      `Archive` that has no `archive specification file` but has some data stored (snapshot files, information about
      last backup level restart etc.).

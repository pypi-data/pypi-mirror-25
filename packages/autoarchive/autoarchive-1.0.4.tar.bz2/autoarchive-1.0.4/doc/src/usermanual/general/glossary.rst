.. arch_spec.rst
.. 
.. Project: AutoArchive
.. License: GNU GPLv3
.. 
.. Copyright (C) 2003 - 2011 Róbert Čerňanský



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

   configured archive
      See `archive`.

   orphaned archive
      `Archive` that has no `archive specification file` but has some data stored (snapshot files, information about
      last backup level restart etc.).

.. glossary.rst
.. 
.. Project: AutoArchive
.. License: GNU GPLv3
.. 
.. Copyright (C) 2003 - 2017 Róbert Čerňanský



.. Glossary section



.. _glossary:



********
Glossary
********

.. glossary::

   Archiver Service Component
      :term:`Service component <Service Components>` that provides the backup functionality.

   ArchiveSpec
      The :term:`component` that provides ability to read archive specification from a file.

   Archiving
      The :term:`component` that provides core functions of :term:`AutoArchive` application (i. e. working with
      :term:`archives <archive>` and :term:`backups <backup>`).

   archive
      The primary entity that AutoArchive operates with.  It has a name and holds the configuration used to create the
      corresponding :term:`backup`.  :term:`Archive` is represented by the :term:`archive specification file`.

   archive specification file
      The configuration of an :term:`archive`.  It contains all information needed for creation of a single archive,
      such as: archive name, archive root directory, list of directories and files which should be **included** and
      **excluded**, etc.  It can also contain some of the configuration options.  The file has extension ‘.aa’ and is
      sometimes referred as “.aa file”.  For more information see the user documentation.

   archive specifications directory
      Directory where :term:`archive specification files <archive specification file>` are stored.  It can be
      configured via the ``archive-specs-dir`` option.

   archiver
      External program or a class that creates an :term:`archive` from given set of files.

   AutoArchive
      The application which is being documented here.

   backup
      Result of the backup creation operation.  For example a \*.tar.gz file.

   backup level
      The order of an :term:`archive` in incremental backup, where backup level 0 means full backup, backup level 1 is
      an archive that contains only differences from level 0, and so on.

   Cmdline UI
      The :term:`component` that provides textual user interface.

   component
      Application part.

   Configuration
      The :term:`component` that provides configuration options.

   configured archive
      An :term:`archive` that has a valid :term:`archive specification file` recognized by the application.

   force option form
      An option with "force-" prefix.  See also :term:`normal option form`.

   negation option form
      An option with "no-" prefix.  See also :term:`normal option form`.

   normal option form
      A standard option wihout any prefix of a special meaning.  See also :term:`force option form` and
      :term:`negation option form`.

   orphaned archive
      An :term:`archive` which is not :term:`configured <configured archive>` (anymore) but the application still has
      some information stored about it (is a :term:`stored archive`).

   selected archive
      A :term:`configured archive` which is passed to the application for processing either by configuration or as
      an argument (which can be the name of the archive or path to the :term:`archive specification file`.

   Service Components
      Service application level.  Contains all services used in the application.

   Storage
      A :term:`component` that provides persistent storage.

   stored archive
      An :term:`archive` for which the application has stored some information.

   system configuration file
      System-wide configuration file.  It has syntax similar to other configuration files but its options have lower
      priority.  See also :term:`user configuration file`.

   UI
      User interface.

   user configuration directory
      A per-user directory where the application looks for :term:`user configuration file` and stores some internal
      data.  It is also default path for a subdirectory containing :term:`archive specification files <archive
      specification file>`.

   user configuration file
      A per-user configuration file.  See also :term:`system configuration file`.

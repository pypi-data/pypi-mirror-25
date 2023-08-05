.. arch_spec.rst
.. 
.. Project: AutoArchive
.. License: GNU GPLv3
.. 
.. Copyright (C) 2003 - 2017 Róbert Čerňanský



.. User documentation - archive specification file description



.. _arch_spec:

Archive Specification File
==========================

.. begin_description

`Archive specification file` contains all information needed for creation of a single archive.

.. end_description

.. begin_format

Options in the `.aa file` are divided into sections.  A section begins with the section name enclosed in square
brackets.  It contains variables which represents the options.

Variables are written in the ``option-name = value`` form, one variable per line.  Boolean values are written as
``yes`` and ``no``.  For path values, tilde (``~``) is expanded to the user's home.  Form ``option-name =`` can be
used to specify a variable with undefined value.

Values of ``include-files`` and ``exclude-files`` options that contains spaces has to be enclosed in double quotes
(``""``).  They may contain standard shell wildcards.

When specifying the value it is possible to refer to other variables from the same file using the form
``%(variable-name)s`` or variables from an external file using the form ``@(external-name.variable-name)`` where
``external-name`` is reference which has to be defined in ``[External]`` section.

Lines beginning with ``#`` or ``;`` are ignored and may be used for comments.

Three sections are valid: ``[External``, ``[Archive]`` (optional) and ``[Content]``.



Section ``[External]``
----------------------

This section contains definition of external references.  Each reference is put on a single line.  They can be
specified by two forms: as a single variable or as a ``variable = path`` pair.

If **single variable** is specified it refers to `archive specification file` of the same name as the variable but
without the '.aa' extension.  The file is searched in the `archive specifications directory`.

The **variable = path** form allows to refer a file from an arbitrary location by specifying its absolute or relative
path.  Paths are relative to the directory of the original file.  In both cases variable name is used in the reference.
See |external_reference_example| for the example of the `.aa file` with external references.



Section ``[Archive]``
---------------------

This section can contain configuration options which are, when specified, overriding the ones specified in
configuration files and command line.

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


  - command-before-backup

  - command-after-backup

See |usage_ref| for their description.



Section ``[Content]``
---------------------

This section contains options specific to an archive.  All options except ``name`` are required.

**Options valid in the [Content] section:**

  - name

    Archive name.  Created `backup` will be named according value of this variable plus appropriate extension.  It is
    optional; default value is the name of the `.aa file` without the extension.

  - path

    Path to archive root.  All paths and file names specified in the same archive specification file will be relative
    to this path.  It will be also the root of the created archive.

  - include-files

    List of space separated file or directory names to backup.  Paths here are relative to the path specified in
    ``path`` variable above.  Starting forward slash (``/``) from absolute paths as well as parent directory tokens
    (``..``) will be ignored.

  - exclude-files

    List of space separated file or directory names to be excluded from the backup.  Use ``exclude-files =`` to
    specify that no files should be excluded.  Similarly to ``include-files`` these paths are relative to ``path``.

.. end_format



.. |usage_ref| replace:: :ref:`usage`
.. |external_reference_example| replace:: :ref:`referring_to_external_archive_specification_example`

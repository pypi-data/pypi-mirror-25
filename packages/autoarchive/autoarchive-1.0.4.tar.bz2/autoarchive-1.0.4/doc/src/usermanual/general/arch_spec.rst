.. arch_spec.rst
.. 
.. Project: AutoArchive
.. License: GNU GPLv3
.. 
.. Copyright (C) 2003 - 2012 Róbert Čerňanský



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

When specifying the value it is possible to refer to other variables in the form ``%(variable-name)s``.

Lines beginning with ``#`` or ``;`` are ignored and may be used for comments.

Two sections are valid: ``[Archive]`` (optional) and ``[Content]``.



Section ``[Archive]``
---------------------

This section can contain configuration options which are, when specified, overriding the ones specified in
configuration files and command line.

**Options valid in the [Archive] section:**

  - archiver

  - incremental

  - restarting

  - restart-after-level

  - restart-after-age

  - full-restart-after-count

  - full-restart-after-age

  - max-restart-level-size

  - remove-obsolete-backups

  - compression-level

  - dest-dir

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

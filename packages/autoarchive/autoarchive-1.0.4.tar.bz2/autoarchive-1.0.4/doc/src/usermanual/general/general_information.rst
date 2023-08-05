.. general_information.rst
.. 
.. Project: AutoArchive
.. License: GNU GPLv3
.. 
.. Copyright (C) 2003 - 2012 Róbert Čerňanský



.. User documentation - General Information



===================
General Information
===================

Versioning Scheme
=================

AutoArchive version has form *X.Y.Z*, where *X* is the **major**, *Y* is **minor** and *Z* the **bugfix** version
number.

A major version is released when all features for it are implemented.  When it happens *X* is increased and other
numbers are set to 0 (e. g. from 0.14.5 to 1.0.0).  No new features are being added to that version anymore, only bug
fixes.  The version is supported until the next major version is released.

After a new major version is released the development of the next one starts.  It has the same major version number
(\ *X*\ ) as current stable, however the minor (\ *Y*\ ) is greater than 0 and is increasing (e. g. after 1.0.0 is
released, the development of 2.0.\ *z* starts with version 1.1.0).

This is how releases may look like::

   0.0.0, 0.0.1, 0.1.0, 0.2.0, 0.2.1, 0.2.2, 1.0.0, 1.0.1, 1.0.2, 1.0.3, 1.0.4
   |                                      |  |   |  |                        |
   ----------------------------------------  -----  --------------------------
                      |                        |                 |
         development of version 1.0   ver. 1.0 released   support for ver. 1.0

                                                 1.1.0, 1.2.0, 1.2.1, 1.3.0, 2.0.0, 2.0.1, 2.0.2, ...
                                                 |                        |  |   |  |
                                                 --------------------------  -----  --------------...
                                                              |                |
                                                 development of ver. 2.0   ver. 2.0 released

                                                                                 ...

Generally, increasing *X* or *Y* means that new features were introduced.  They may bring incompatibilities with
previous releases (such as change of the configuration file format and so on).  A migration may be necessary after the
update.

Increasing *Z* means that only bugs were fixed and the release is compatible with the previous one.  Update is seamless,
no migration is necessary.



License
=======

.. begin_license

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
License version 3 as published by the Free Software Foundation.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see
<http://www.gnu.org/licenses/>.

.. end_license



Contacting the Author
=====================

.. begin_author

Comments, bug reports, wishes, donations for this piece of software are welcomed.  You can send them via the project
page at http://sourceforge.net/projects/autoarchive/ or use e-mail openhs@users.sourceforge.net.

Homepage: http://autoarchive.sourceforge.net/.

.. end_author



.. |tar_ref| replace:: :command:`tar`

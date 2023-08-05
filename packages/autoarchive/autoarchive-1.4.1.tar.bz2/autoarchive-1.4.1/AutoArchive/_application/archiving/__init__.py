# __init__.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2017 Róbert Čerňanský



""":term:`Archiving` :term:`component`.

Provides the core functionality of the application.  Executes an :term:`archiver` and creates a :term:`backup` based
on provided :term:`archive specification file` and configuration.  It also allows to read various information about
:term:`configured <configured archive>` and :term:`stored <stored archive>` archives. It requires archiver service
(:class:`.ArchiverServiceIdentification`) for the backup creation."""



from .archiving_application import *



__all__ = archiving_application.__all__[:]

# __init__.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2012 Róbert Čerňanský



""":term:`Archiving` :term:`component`.

Provides the core functionality of the application.  Executes an :term:`archiver` and creates a :term:`backup` based
on provided :term:`archive specification file` and configuration (:class:`.IAppConfig`).  It also allows to read
various information about :term:`configured <configured archive>` and :term:`stored <stored archive>` archives.

It requires archiver service (:class:`.IArchiver` implementation) for the backup creation."""



from .iarchiver import *
from .iarchiving import *



__all__ = iarchiver.__all__ + iarchiving.__all__

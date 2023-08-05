# __init__.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2017 Róbert Čerňanský



""":term:`ArchiveSpec` :term:`component`.

Implements ability to read archive configuration from :term:`archive specification file`."""



from .archive_spec_options import *
from .config_constants import *
from .archive_spec import *



__all__ =  archive_spec_options.__all__ + config_constants.__all__ + archive_spec.__all__

# __init__.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2014 Róbert Čerňanský



"""Support framework for registering and accessing services."""



from .iservice_component import *
from .iservice import *
from .iservice_identification import *



__all__ = iservice_component.__all__ + iservice.__all__ + iservice_identification.__all__

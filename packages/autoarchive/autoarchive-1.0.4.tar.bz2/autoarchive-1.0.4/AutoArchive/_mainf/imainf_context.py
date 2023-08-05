# imainf_context.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2011 Róbert Čerňanský



""":class:`IMainfContext` interface."""



__all__ = ["IMainfContext"]



# {{{ INCLUDES

from abc import *
from . import *

# }}} INCLUDES



# {{{ CLASSES

class IMainfContext(IComponentInterface):
    "Provides access to a various program-related objects."

    @abstractproperty
    def appEnvironment(self):
        """Gets an ``appEnvironment`` object.

        This is the object that was passed to the :term:`Mainf` during its initialization.  It is an arbitrary object
        of which structure :term:`Mainf` has no knowledge.

        .. warning:: As passing the ``appEnvironment`` object to :term:`Mainf` is optional this property can be
           ``None``.

        :rtype: ``object``"""

# }}} CLASSES

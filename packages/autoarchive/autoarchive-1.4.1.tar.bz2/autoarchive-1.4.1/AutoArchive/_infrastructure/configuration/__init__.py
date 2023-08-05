# __init__.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2014 Róbert Čerňanský



""":term:`Configuration` component.

Provides access to configuration options read from :attr:`.ApplicationContext.appEnvironment.options`
(command-line options), :term:`user configuration file` and :term:`system configuration file`. For that purpose it
provides :class:`.ConfigurationBase` implementation via :class:`ConfigurationFactory`.  Configuration should be created
centrally by some common component and that instance distributed to other components.  Individual components should
not call :class:`ConfigurationFactory` directly.

For more information about :class:`.ConfigurationBase` provided interface see :class:`.ConfigurationFactory`."""



from .options import *
from .configuration_base import *



__all__ = options.__all__ + configuration_base.__all__

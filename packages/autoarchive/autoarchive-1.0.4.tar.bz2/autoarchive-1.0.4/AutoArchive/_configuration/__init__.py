# __init__.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2012 Róbert Čerňanský



""":term:`Configuration` :term:`component`.

Provides access to configuration options read from :attr:`.IMainfContext.appEnvironment.options` (command-line options),
:term:`user configuration file` and :term:`system configuration file`. For that purpose it provides
:class:`.IAppConfig` interface.

It also provides application's persistent storage in a form of :class:`.IStorage` component interface.

For more information about :class:`.IAppConfig` and :class:`.IStorage` provided interfaces see
:class:`.ConfigurationComponent`.

Component is designed to be used as the :term:`Mainf` :term:`component`.  For that purpose it provides
:class:`.IComponent` implementation in a form of :class:`.ConfigurationComponent` class."""



from .iconfiguration import *
from .iapp_config import *
from .options import *
from .configuration_base import *
from .istorage_portion import *
from .istorage import *



__all__ = iconfiguration.__all__ + iapp_config.__all__  + options.__all__ + configuration_base.__all__ + \
          istorage_portion.__all__ + istorage.__all__

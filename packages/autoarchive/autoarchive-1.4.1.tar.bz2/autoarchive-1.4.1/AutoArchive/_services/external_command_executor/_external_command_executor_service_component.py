# _external_command_executor_service_component.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2014 Róbert Čerňanský



""":class:`ExternalCommandExecutorServiceComponent` class."""

__all__ = ["ExternalCommandExecutorServiceComponent"]



# {{{ INCLUDES

from AutoArchive._infrastructure.service import IServiceComponent
from . import ExternalCommandExecutorServiceIdentification
from ._external_command_executor import ExternalCommandExecutor

# }}} INCLUDES



# {{{ CLASSES

class ExternalCommandExecutorServiceComponent(IServiceComponent):
    """Service component for external command executor.

    Registers service identified as :class:`.ExternalCommandExecutorServiceIdentification`."""

    def __init__(self, applicationContext, serviceAccessor):
        self.__serviceAccessor = serviceAccessor
        serviceAccessor.registerService(ExternalCommandExecutorServiceIdentification, ExternalCommandExecutor)



    def destroyServices(self):
        "See: :meth:`IServiceComponent.destroyServices()`"

        self.__serviceAccessor.unregisterService(ExternalCommandExecutorServiceIdentification)

# }}} CLASSES

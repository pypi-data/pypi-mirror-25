# external_command_executor_service_identification.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2014 Róbert Čerňanský



""":class:`ExternalCommandExecutorServiceIdentification` class."""



__all__ = ["ExternalCommandExecutorServiceIdentification"]



# {{{ INCLUDES

from AutoArchive._infrastructure.py_additions import staticproperty
from AutoArchive._infrastructure.service import IServiceIdentification
from ._external_command_executor import ExternalCommandExecutor

# }}} INCLUDES



# {{{ CLASSES

class ExternalCommandExecutorServiceIdentification(IServiceIdentification):
    """Identifies External Command Executor service."""

    @staticproperty
    def interface():
        """Gets interface type of the External Command Executor service.

        :rtype: ``type{``ExternalCommandExecutor``\ ``}``"""

        return ExternalCommandExecutor



    @staticproperty
    def providerIdentificationInterface():
        """Returns ``None`` as this service has only a single provider."""

        return None

# }}} CLASSES

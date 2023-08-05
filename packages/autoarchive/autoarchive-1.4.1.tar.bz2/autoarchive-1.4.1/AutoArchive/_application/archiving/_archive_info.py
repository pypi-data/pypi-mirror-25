# _archive_info.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2014 Róbert Čerňanský



""":attr:`_BackupLevelRestartReasons` enum and :class:`_ArchiveInfo` class."""



__all__ = ["_BackupLevelRestartReasons", "_ArchiveInfo"]



# {{{ INCLUDES

from abc import *

from AutoArchive._infrastructure.py_additions import Enum
from AutoArchive._infrastructure.configuration import ArchiverTypes

# }}} INCLUDES



# {{{ CONSTANTS

#: Reasons for restarting of the :term:`backup level`.
_BackupLevelRestartReasons = Enum(

    #: :term:`Backup level` restart did not occurred.
    "NoRestart",

    #: Maximal number of restarts to a lower :term:`backup level` was reached.  Full restart was done.
    "RestartCountLimitReached",

    #: Maximal age without full restart was reached.  Full restart was done.
    "LastFullRestartAgeLimitReached",

    #: Maximal :term:`backup level` reached.  Restart to a lower level was done.
    "BackupLevelLimitReached",

    #: Maximal age without a restart was reached.  Restart to a lower level was done.
    "LastRestartAgeLimitReached")

# }}} CONSTANTS



# {{{ CLASSES

class _ArchiveInfo(metaclass = ABCMeta):
    """Information about an archive.

    .. note:: Class should be instantiated by calling the :meth:`_Archiving.getArchiveInfo()` or \
       :meth:`_Archiving.getStoredArchiveInfo()` factory methods."""

    @abstractmethod
    def __init__(self, name):
        self._name = name
        self._path = None
        self._archiverType = ArchiverTypes.Tar
        self._destDir = ""
        self._incremental = None
        self._backupLevel = None
        self._nextBackupLevel = None
        self._restarting = None
        self._restartAfterLevel = None
        self._restartReason = None
        self._restartLevel = None
        self._restartCount = None
        self._fullRestartAfterCount = None
        self._lastRestart = None
        self._restartAfterAge = None
        self._lastFullRestart = None
        self._fullRestartAfterAge = None



    @property
    def name(self):
        """Gets the name of the archive.

        :rtype: ``str``"""

        return self._name



    @property
    def path(self):
        """Gets the path to the archive's root.

        .. note:: Will be ``None`` if the archive's root can not be retrieved.

        :rtype: ``str``"""

        return self._path



    @property
    def archiverType(self):
        """Gets the archiver type for this archive.

        .. note:: Value is guaranteed to be non-\ ``None``.

        :rtype: :attr:`ArchiverTypes`"""

        return self._archiverType



    @property
    def destDir(self):
        """Gets the archive's destination directory.

        .. note:: Value is guaranteed to be non-\ ``None``.

        :rtype: ``str``"""

        return self._destDir



    @property
    def incremental(self):
        """Gets the status of incremental archiving activation.

        .. note:: Will be ``None`` if the :attr:`archiverType` does not support incremental archiving.

        :rtype: ``bool``"""

        return self._incremental



    @property
    def backupLevel(self):
        """Gets the current :term:`backup level`.

        .. note:: Will be ``None`` if the archive is not incremental or used :attr:`archiverType` does not support
           incremental archiving.

        .. note:: For archiver types that supports incremental archiving, whether the return value will be ``None`` or \
           not does not depend on the *current* :attr:`incremental` value.  If the archive was configured and created \
           as incremental previously then the :term:`backup level` will be defined even if the current \
           :attr:`incremental` value would be ``False`` and vice versa.

        :rtype: ``int``"""

        return self._backupLevel



    @property
    def nextBackupLevel(self):
        """Gets the next :term:`backup level`.

        See also :attr:`backupLevel`.

        .. note:: Will be ``None`` if the archive is not incremental or used :attr:`archiverType` does not support
           incremental archiving.

        :rtype: ``int``"""

        return self._nextBackupLevel



    @property
    def restarting(self):
        """Gets the status of :term:`backup level` restarting activation.

        .. note:: Will be ``None`` if the :attr:`archiverType` does not support incremental archiving.

        :rtype: ``bool``"""

        return self._restarting



    @property
    def restartAfterLevel(self):
        """Gets the maximal :term:`backup level`; after it is reached it will be restarted to a lower value.

        .. note:: Will be ``None`` if the :attr:`archiverType` does not support incremental archiving.

        :rtype: ``int``"""

        return self._restartAfterLevel



    @property
    def restartReason(self):
        """Gets the reason for the upcoming :term:`backup level` restart.

        .. note:: Will be ``None`` if the :attr:`archiverType` does not support incremental archiving or the restart
           reason can not be determined.

        :rtype: :attr:`_BackupLevelRestartReasons`"""

        return self._restartReason



    @property
    def restartLevel(self):
        """Gets a :term:`backup level` to which a next restart would be done.

        .. note:: Will be ``None`` if the :attr:`archiverType` does not support incremental archiving.

        :rtype: ``int``"""

        return self._restartLevel



    @property
    def restartCount(self):
        """Gets the number of :term:`backup level` restarts already performed.

        .. note:: Will be ``None`` if the :attr:`archiverType` does not support incremental archiving or if \
           :attr:`restarting` was not enabled for the archive in the past.

        :rtype: ``int``"""

        return self._restartCount



    @property
    def fullRestartAfterCount(self):
        """Gets the number of restarts after which the :term:`backup level` will be restarted to 0.

        .. note:: Will be ``None`` if the :attr:`archiverType` does not support incremental archiving or if no value \
           is defined for :attr:`.Options.FULL_RESTART_AFTER_COUNT`.

        :rtype: ``int``"""

        return self._fullRestartAfterCount



    @property
    def lastRestart(self):
        """Gets the date when the last :term:`backup level` restart occurred.

        .. note:: Will be ``None`` if the :attr:`archiverType` does not support incremental archiving or if \
           :attr:`restarting` was not enabled for the archive in the past.

        :rtype: ``datetime.date``"""

        return self._lastRestart



    @property
    def restartAfterAge(self):
        """Gets the number of days after which the :term:`backup level` should be restarted.

        .. note:: Will be ``None`` if the :attr:`archiverType` does not support incremental archiving or if no value is
           defined for :attr:`.Options.RESTART_AFTER_AGE`.

        :rtype: ``int``"""

        return self._restartAfterAge



    @property
    def lastFullRestart(self):
        """Gets the date when the last :term:`backup level` restart to level 0 occurred.

        .. note:: Will be ``None`` if the :attr:`archiverType` does not support incremental archiving or if \
           :attr:`restarting` was not enabled for the archive in the past.

        :rtype: ``datetime.date``"""

        return self._lastFullRestart



    @property
    def fullRestartAfterAge(self):
        """Gets the number of days after which the :term:`backup level` should be restarted to level 0.

        .. note:: Will be ``None`` if the :attr:`archiverType` does not support incremental archiving or if no value is
           defined for :attr:`.Options.FULL_RESTART_AFTER_AGE`.

        :rtype: ``int``"""

        return self._fullRestartAfterAge

# }}} CLASSES

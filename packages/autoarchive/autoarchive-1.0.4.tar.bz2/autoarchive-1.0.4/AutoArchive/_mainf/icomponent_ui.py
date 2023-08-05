# icomponent_ui.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2012 Róbert Čerňanský



""":class:`IComponentUi` interface, :data:`UiMessageKinds` and :data:`VerbosityLevels` enums."""



__all__ = ["UiMessageKinds", "VerbosityLevels", "IComponentUi"]



# {{{ INCLUDES

from abc import *

from .._py_additions import *
from .iinterface_accessor import *

# }}} INCLUDES



# {{{ CONSTANTS

#: Kinds of user messages.
UiMessageKinds = Enum(
    "Verbose",
    "Notification",
    "Info",
    "Warning",
    "Error")



#: Verbosity levels.
VerbosityLevels = Enum(
    "Quiet",
    "Normal",
    "Verbose")

# }}} CONSTANTS



# {{{ CLASSES

class IComponentUi(IComponentInterface):
    """Basic interface for an :term:`UI` implementation.

    Defines basic methods for showing messages of various importance to a user.

    .. note:: There should be at least one :term:`component` that implements this interface in order to provide an \
       :term:`UI` access to other components.

    See also the description of _mainf package (:mod:`._mainf`)."""

    @abstractmethod
    @event
    def messageShown(messageKind):
        """Fired after a user message was shown.

        Event is fired when one of the message kinds from :data:`UiMessageKinds` enum was shown or would be shown (but
        was suppressed due to the verbosity level).

        :param messageKind: Kind of the message that was shown.
        :type messageKind: :data:`UiMessageKinds`"""



    @abstractproperty
    def verbosity(self):
        """Gets the verbosity level.

        If verbosity level is :data:`VerbosityLevels.Quiet` only messages of kind :data:`UiMessageKinds.Error` are
        shown.  For level :data:`VerbosityLevels.Normal` all messages kinds except :data:`UiMessageKinds.Verbose`
        are shown.  For level :data:`VerbosityLevels.Verbose` all message kinds are shown.

        :rtype: :data:`VerbosityLevels`"""



    @abstractmethod
    def showVerbose(self, msg):
        """Show a verbose-type message (:data:`UiMessageKinds.Verbose`) to the user.

        Verbose messages should be shown only if user enables it.  Although this method can be called regardless of
        current verbosity level, the concrete implementation can decide whether it will be shown or not if verbosity
        level is 0.  It is not recommended to call this method if verbosity level is 0 due to performance reasons.
        Current verbosity level can be obtained via :attr:`verbosity` property.

        See also: :attr:`verbosity`.

        :param msg: The message that should be shown to the user.
        :type msg: ``str``"""



    @abstractmethod
    def showNotification(self, msg):
        """Show an unintrusive notification message (:data:`UiMessageKinds.Notification`) to the user.

        .. note:: If user interface implementation does not have means to support notifications then it should be
           presented to the user similarly as :meth:`showInfo`.

        See also: :attr:`verbosity`.

        :param msg: The message that should be shown to the user.
        :type msg: ``str``"""



    @abstractmethod
    def showInfo(self, msg):
        """Show an information message (:data:`UiMessageKinds.Info`) to the user.

        See also: :attr:`verbosity`.

        :param msg: The message that should be shown to the user.
        :type msg: ``str``"""



    @abstractmethod
    def showWarning(self, msg):
        """Show a warning message (:data:`UiMessageKinds.Warning`) to the user.

        See also: :attr:`verbosity`.

        :param msg: The message that should be shown to the user.
        :type msg: ``str``"""



    @abstractmethod
    def showError(self, msg):
        """Show an error message to (:data:`UiMessageKinds.Error`) the user.

        See also: :attr:`verbosity`.

        :param msg: The message that should be shown to the user.
        :type msg: ``str``"""



    @abstractmethod
    def presentLine(self, line):
        """Present a line of text to the user.

        .. note:: The verbosity level has no effect on presenting the line.

        :param line: The text that shall be presented to the user.
        :type line: ``str``"""

# }}} CLASSES

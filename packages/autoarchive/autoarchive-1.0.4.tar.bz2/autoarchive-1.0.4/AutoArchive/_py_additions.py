# _py_additions.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2013 Róbert Čerňanský



"""Various enhancements to Python."""



__all__ = ["Enum", "event", "classproperty", "staticproperty"]



# {{{ INCLUDES

from collections import Iterable

# }}} INCLUDES



# {{{ CLASSES

class Enum(Iterable):
    """Simple enum class.

    Example Usage::

       codes = Enum("FOO", "BAR", "BAZ") # codes.BAZ will be 2 and so on and str.BAZ will be "BAZ"

    :param names: Iterable of Enum members.
    :type names: ``Iterator<str>``"""

    def __init__(self, *names):
        self.__names = names

        for number, name in enumerate(names):
            setattr(self, name, self._DescriptiveDecimalInt(number, name))



    def __repr__(self):
        return str.join(", ", self.__names)



    def __iter__(self):
        return iter(range(len(self.__names)))



    class _DescriptiveDecimalInt(int):

        def __new__(cls, value = 0, *args):
            return int.__new__(cls, value)



        def __init__(self, value = 0, description = None):
            self.description = description



        def __str__(self):
            if self.description is not None:
                return self.description
            else:
                return super().__str__()



        @property
        def description(self):
            return self.__description

        @description.setter
        def description(self, value):
            self.__description = value



class event:
    """Decorator that declares a function as an *event*.

    Implements a C#-like events (a call dispatchers).  Decorating a function or method with this decorator declares
    it as an *event*.  In order to subscribe a handler function to the event, one should use the “+=” operator
    and to unsubscribe the “-=” operator.  Such event can be fired by a calling the decorated function.  This will
    dispatch the event to all subscribers, i.e. subscribed handler methods are called.

    .. note:: Decorated function should implement only ``pass`` as its body.

    .. note:: Decorated function can take any number of parameters or keyword parameters.  Subscriber functions has
       to take same parameters as the event.

    Example usage::

       class Button:
          # ...
          @event
          def clicked(self, some_parameter):
              "Fired when the button was clicked."
              pass
          def _fireClicked(self, some_parameter):
              clicked(some_parameter)
          # ...

       class Ui:
           def __init__(self, button):
               button.clicked += self._onButtonClicked
           def _onButtonClicked(self, some_parameter):
               "Handle the button click."
               # play a sound...

    :param eventFunction: Decorated function or method that becomes an *event*.
    :type eventFunction: ``function``"""

    def __init__(self, eventFunction):
        self.__eventFunction = eventFunction
        self.__subscribers = set()



    def __call__(self, *args, **kwargs):
        "Fires the event."

        # call the event function just to check that the event is called with correct number of parameters; besides
        # that this call is not necessary
        self.__eventFunction(*args, **kwargs)

        # call subscriber methods
        for subscriber in self.__subscribers:
            subscriber(*args, **kwargs)



    def __iadd__(self, subscriber):
        """Subscribes the ``subscriber`` to the *event*.

        :param subscriber: A listener that wants to be subscribed to the event.
        :type subscriber: ``function``

        :note: Same object is subscribed only once, even if multiple attempts to subscribe it are performed."""

        self.__subscribers.add(subscriber)
        return self



    def __isub__(self, subscriber):
        """Unsubscribes the ``subscriber`` from the *event*.

        :param subscriber: A listener that wants to be unsubscribed from the event.
        :type subscriber: ``function``"""

        self.__subscribers.discard(subscriber)
        return self



class classproperty(property):
    """Decorator that makes the decorated method a class property."""

    def __get__(self, obj, type = None):
        return classmethod(self.fget).__get__(None, type)()



class staticproperty(property):
    """Decorator that makes the decorated method a static property."""

    def __get__(self, obj, type = None):
        return staticmethod(self.fget).__get__(None, type)()

# }}} CLASSES

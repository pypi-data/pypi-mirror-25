# __init__.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2011 Róbert Čerňanský



"""Main framework for :term:`AutoArchive`.

:term:`Mainf` helps to implement architecture where an application consists of several components (which can map the
logical structure).  In particular, it provides a way to prevents to see eachothers package internal implementation
objects and allows them to expose only public interfaces.

Each :term:`component` class has to derive from :class:`.IComponent` interface.  All :class:`.IComponent` classes has
to be passed to :class:`.MainfEngine` during its initialization using the :meth:`.MainfEngine.addComponent()` method.
Components have possibility to register instances of their public interfaces implementations using the
:class:`.IInterfaceAccessor` which is passed to them during their construction.  Doing so, they make them available to
other components (which can access them via the same interface).

Components should expose their interface definitions to others while classes that implements them should be hidden in
private packages/modules.

Additionally, :term:`Mainf` defines interface :class:`.IComponentUi` for a user interface that components should use to
access a UI (which has to implement it).

:term:`Mainf` framework is initialized by creating the :class:`.MainfEngine` by :func:`.createMainfEngine()` factory
method following by populating it by component classes.  Finally, calling :meth:`.MainfEngine.start()` method, starts
the application passing the ``appEnvironment`` which is an arbitrary object that will be available to components via
:class:`.IMainfContext` component interface.  :term:`Mainf` in turn, instantiates all components and executes them by
calling the :meth:`.IComponent.run()` method for each."""



from .main import *
from .icomponent import *
from .icomponent_ui import *
from .iinterface_accessor import *
from .imainf_context import *



__all__ = main.__all__ + icomponent.__all__ + icomponent_ui.__all__ + iinterface_accessor.__all__ + \
        imainf_context.__all__

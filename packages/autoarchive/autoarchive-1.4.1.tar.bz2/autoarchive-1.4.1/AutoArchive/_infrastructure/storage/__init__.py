# __init__.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2017 Róbert Čerňanský



""":term:`Storage` :term:`component`.



Implements application's persistent storage in a form of :class:`.FileStorage` class.  It should be constructed by some
infrastructure component and distributed to other components.  Individual components should not instantiate it
directly."""

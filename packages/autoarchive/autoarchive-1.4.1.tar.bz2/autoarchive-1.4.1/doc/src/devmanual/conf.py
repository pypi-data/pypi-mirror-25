# conf.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2017 Róbert Čerňanský



"""Sphinx configuration for developer manual."""



import sys, os

# add path to the AutoArchive sources to the first place
sys.path.insert(0, os.path.abspath('../../../'))


# {{{ general configuration

# general information about the project
project = 'AutoArchive'
copyright = '2003 - 2017, Róbert Čerňanský'
version = '1.4.1'
release = version

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode', 'sphinx.ext.autosummary']

# the master toctree document
master_doc = 'index'

default_role = "obj"

# }}} general configuration



# {{{ options for HTML output

html_theme = "classic"
html_title = project + " Developer Manual (ver. " + release + ")"
html_show_sourcelink = False

# }}} options for HTML output



# {{{ autodoc options

autodoc_default_flags = ['members', 'undoc-members', 'show-inheritance']
autodoc_member_order = 'groupwise'

# }}} autodoc options

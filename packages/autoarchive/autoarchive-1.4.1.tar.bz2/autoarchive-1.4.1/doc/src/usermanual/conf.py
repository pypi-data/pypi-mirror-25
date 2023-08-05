# conf.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2017 Róbert Čerňanský



"""Sphinx configuration for the user manual."""



# {{{ general configuration

# general information about the project
project = 'AutoArchive'
copyright = '2003 - 2017, Robert Cernansky'
version = '1.4.1'
release = version

# the master toctree document.
master_doc = 'index'

default_role = "term"

# }}} general configuration



# {{{ options for HTML output

html_theme = 'basic'
html_style = 'autoarchive.css'
html_theme_options = {"nosidebar": True}

html_title = project + " User Manual (ver. " + release + ")"

html_show_sourcelink = False

html_static_path = ['_static']

# }}} options for HTML output



# {{{ options for manual page output

# one entry per manual page. List of tuples (source start file, name, description, authors, manual section)
man_pages = [
    ('man/man_aa', 'aa', 'a simple backup utility', [], 1),
    ('man/man_aa_arch_spec', 'aa_arch_spec', 'Archive Specification File', [], 5),
    ('man/man_aa_conf', 'aa.conf', 'AutoArchive Configuration File', [], 5)
]

# }}} options for manual page output

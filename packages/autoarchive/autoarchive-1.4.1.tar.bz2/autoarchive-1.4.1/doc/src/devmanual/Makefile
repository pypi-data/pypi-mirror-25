# Makefile

# Project: AutoArchive
# License: GNU GPLv3

# Copyright (C) 2003 - 2014 Róbert Čerňanský



# Makefile for developer documentation.



# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
BUILDDIR      = ../../devel

# Internal variables.
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(SPHINXOPTS) .

.PHONY: help clean html

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  html       to make standalone HTML files"
	@echo "  clean      to clean the build directory"

all:	html

clean:
	-rm -rf $(BUILDDIR)/html

html:
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
	-rm -rf $(BUILDDIR)/html/{.buildinfo,_sources} $(BUILDDIR)/doctrees
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

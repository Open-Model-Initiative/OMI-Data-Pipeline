# Open Model Initiative Data Repository Documentation Makefile
#
# This minimal makefile is used to build the Open Model Initiative Data Repository documentation with Sphinx.
# You can set or override the following variables from the command line or the environment:
#   SPHINXOPTS, SPHINXBUILD, etc.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without an argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using "make mode".
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

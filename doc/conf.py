# -----------------------------------------------------------------------------
# Configuration file for the Sphinx documentation builder.
# For the full list of built-in configuration values, see:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
#
# SPDX-License-Identifier: Apache-2.0
# -----------------------------------------------------------------------------

# -- Project information -----------------------------------------------------
project = "Open Model Intitiative - Data Pipeline"
copyright = "The Linux Foundation®. All rights reserved."
author = "Open Model Intitiative"
release = "0.1"

# -- General configuration ---------------------------------------------------
extensions = ["myst_parser"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

pygments_style = 'sphinx'

# -- Options for HTML output -------------------------------------------------
html_theme = "pydata_sphinx_theme"
html_theme_options = {
    "navbar_align": "content",
    "navbar_center": ["navbar-nav"],
    "use_edit_page_button": False,
    "show_toc_level": 2,
    "navbar_start": ["navbar-logo"],
    "navbar_end": ["navbar-icon-links"],
}

html_title = "OMI Data Repository"

html_static_path = ["_static"]

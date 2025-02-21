# doc/conf.py
# -----------------------------------------------------------------------------
# Configuration file for the Sphinx documentation builder.
# For the full list of built-in configuration values, see:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
#
# SPDX-License-Identifier: Apache-2.0
# graphcap.module.doc.conf.py
# -----------------------------------------------------------------------------

# -- Project information -----------------------------------------------------
project = "Open Model Intitiative - Data Repository"
copyright = "2025, Open Model Intitiative Contributors"
author = "Open Model Intitiative"
release = "0.1"

# -- General configuration ---------------------------------------------------
extensions = ["myst_parser"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
# Update the theme to use pydata-sphinx-theme
html_theme = "pydata_sphinx_theme"

# Optional: Add pydata-sphinx-theme specific options
html_theme_options = {
    "navbar_start": ["navbar-logo"],
    "navbar_end": ["navbar-icon-links"],
    # Add additional customization options here as needed.
}

html_static_path = ["_static"]

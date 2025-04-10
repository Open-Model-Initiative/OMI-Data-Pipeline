#!/bin/bash
# SPDX-License-Identifier: Apache-2.0

# Change directory to the script's location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
pushd "$SCRIPT_DIR" > /dev/null

# Set SPHINXBUILD if not already set
if [ -z "$SPHINXBUILD" ]; then
    SPHINXBUILD=sphinx-build
fi

SOURCEDIR="."
BUILDDIR="_build"

# Check if the sphinx-build command exists
if ! command -v "$SPHINXBUILD" > /dev/null 2>&1; then
    echo
    echo "The 'sphinx-build' command was not found. Please ensure Sphinx is installed."
    echo "Set the SPHINXBUILD environment variable to the full path of the 'sphinx-build' executable."
    echo "Or add the Sphinx directory to your PATH."
    echo
    echo "Download Sphinx from https://www.sphinx-doc.org/"
    exit 1
fi

# If no argument is provided, use "help" mode
if [ -z "$1" ]; then
    MODE="help"
else
    MODE="$1"
fi

# Run the sphinx-build command with the specified mode
"$SPHINXBUILD" -M "$MODE" "$SOURCEDIR" "$BUILDDIR" ${SPHINXOPTS} ${O}

popd > /dev/null

Documentation Work
==================

Requirements
------------

Sphinx
~~~~~~
- Download `Sphinx <https://www.sphinx-doc.org/>`_

Sphinx Requirements
~~~~~~~~~~~~~~~~~~~

- Install `python-myst-parser <https://pypi.org/project/myst-parser/>`_

- Install `pydata_sphinx_theme <https://pypi.org/project/pydata-sphinx-theme/>`_


Making Changes
--------------

- Navigate to the /doc directory.

- Remove the current documentation build if present:

.. code-block:: bash

    rm -rf _build

- Make your changes.

- Rebuild the documentation:

On Linux/Mac use:

.. code-block:: bash

    ./make.sh html

On Windows use:

.. code-block:: bash

    ./make.bat html


- Ensure you get no warnings.

- Open the relevant html files from /doc/_build/html

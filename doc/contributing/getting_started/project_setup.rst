Project Setup
=============

Now that you're ready to get started, you'll want to get the project setup locally for development.

Prerequisites
-------------

Task
~~~~

We currently use https://github.com/go-task/task to manage our tasks.

To install task review docs here: https://taskfile.dev/installation/

Docker / Docker Compose
~~~~~~~~~~~~~~~~~~~~~~~

We utilize docker and docker compose to run our services locally.

To install docker review docs here: https://docs.docker.com/

Python / Virtual Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Please ensure you are running with Python 3.11 or higher with virtual environment installed.

Node.JS
~~~~~~~

`Node.js>=v22.2 <https://nodejs.org/en/download/package-manager>`_

PNPM
~~~~

`pnpm <https://pnpm.io/installation>`_

Dev Environment setup
---------------------

To setup your environment run ``task setup``

Along with installing the necessary components, this will copy the ``.env.template`` setup into a ``.env`` file.

You can update this file if you'd like to change any of the default values for your development environment. You will at minimum need to provide a valid ID and SECRET for at least one authentication method.

You will also need to manually copy the ``.env.template`` file in ``modules/odr_frontend`` to a ``.env`` file in the same folder, and make matching updates.

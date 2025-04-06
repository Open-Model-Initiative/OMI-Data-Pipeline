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
See the following 'Setup an Oauth Test Application' section for information on how to set these up.

You will also need to manually copy the ``.env.template`` file in ``modules/odr_frontend`` to a ``.env`` file in the same folder, and make matching updates.

Setup an Oauth Test Application
-------------------------------

The OMI Data Pipeline only supports authentication through Discord and GitHub Oauth at this time.

In order to develop locally, you will need to setup at least one method as a test application in order to authenticate locally.

Discord
~~~~~~~

Navigate to https://discord.com/developers/applications

In the top right, click the 'New Application' button.

Name your application anything you like, such as 'OMI Test'

On the left hand size, select 'OAuth2'

Add a redirect URL for 'http://localhost:5173/auth/callback/discord'

Copy the client ID and client secret into your .env files DISCORD_CLIENT_ID and DISCORD_CLIENT_SECRET respectively.


GitHub
~~~~~~

See the guide here for more information: https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authenticating-to-the-rest-api-with-an-oauth-app#registering-your-app

You will need to register your test application at https://github.com/settings/applications/new

Name your application anything you like, such as 'OMI Test'

Set the Homepage URL as 'http://localhost:5173'

Set the authorization callback URL to 'http://localhost:5173/auth/callback/github'

Click the 'Register application' button.

On this page, click generate a new client secret.

Copy the client ID and client secret into your .env files GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET respectively.

Take note of the client ID and client secret as you will need them for your .env file in the next step.

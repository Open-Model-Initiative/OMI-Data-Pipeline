# Getting Started

This guide is intended to help prospective contributors get setup and oriented with the project and its codebase.

Anyone is able to contribute to the OMI project!

# Wait, I just want to help with data/annotations/etc.

That's great and we look forward to your help!

Our hosted data environment where you'll be able to shared data, annotations, rate images, etc. is not yet available.

In the meantime, you can share datasets in the `Datasets` forum channel in the OMI [Discord server](https://discord.gg/vANKjzDDkQ)

(Which is also where we'd announce once the hosted data environment is available!)

# Contribution Guidelines

Before contributing to the project, you need to know a few things about requirements for the OMI project. Make sure you read and understand the [Contributing Guidelines](../CONTRIBUTING.md), including the requirements for [DCO](../DCO.md)

# Project Setup

Now that you're ready to get started, you'll want to get the project setup locally for development.

## Prerequisites

### Task

We currently use https://github.com/go-task/task to manage our tasks.

To install task review docs here: https://taskfile.dev/installation/

### Docker / Docker Compose

We utilize docker and docker compose to run our services locally.

To install docker review docs here: https://docs.docker.com/

### Python / Virtual Environment

Please ensure you are running with Python 3.11 or higher with virtual environment installed.

### Node.JS

[Node.js>=v22.2](https://nodejs.org/en/download/package-manager)

### PNPM

[pnpm](https://pnpm.io/installation)

## Dev Environment setup

To setup your environment run `task setup`

Along with installing the necessary components, this will copy the `.env.template` setup into a `.env` file.

You can update this file if you'd like to change any of the default values for your development environment. You will at minimum need to provide a valid ID and SECRET for at least one authentication method.

You will also need to manually copy the `.env.template` file in `modules/odr_frontend` to a `.env` file in the same folder, and make matching updates.

# Running The Local Environment

To start your virtual environment, run `task activate-venv` or `source ./venv/bin/activate`

Then to start all the required services, run `task dev`

This will spin up the required front end, api, and database containers.

Before the site will 'work' you will need to run `task data:migrate` to create the required data and tables

By default, you will have the following:

- A front end accessible at: http://localhost:5173/
(Note: The front end is currently only available in the feature/frontend branch.)
- An API at: http://localhost:31100/
    Note, since we use FastAPI, you also get
    - Interactive OpenAPI documentation at: http://localhost:31100/docs
    - Redoc documentation at: http://localhost:31100/redoc
- A PGAdmin interface at: http://localhost:35050
    To connect to the database, open http://localhost:35050/browser/

    Sign in with your PGADMIN_DEFAULT_EMAIL and PGADMIN_DEFAULT_PASSWORD from your .env file

    On the left, right click servers, and click Register > Server

    Name the DB something like omi-database, then switch to the connection tab

    The host name/address will be 'postgres', the username will be your .env POSTGRES_USER, and the password will be your .env POSTGRES_PASSWORD

# Running Tests

Before committing any changes, ensure you run all tests to be sure existing behaviour continues to work. If any tests require updates to pass with your changes, ensure you update them as well.

To run all tests, run `task test-all`. Note this is not working at the moment and needs some work but some tests are run via the pipeline automatically.

(Todo: Add instructions for how to run the different types individual as well to check work under development.)

# Committing Changes

Before committing any changes, remember DCO and sign offs! If any commits are not made following the required standard, they will need reverted or redone.


# Tearing Down your Development Environment

To stop the environment, start by using ctrl+c (or cmd+c) to stop the current processes.

Then use `task stop-all` to full stop the environment.

If you want to remove the docker volumes used by the database, run `task db:teardown`

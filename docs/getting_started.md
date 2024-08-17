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

You can update this file if you'd like to change any of the default values for your development environment.


# Running The Local Environment

To start your virtual environment, run `task activate-venv`

Then to start all the required services, run `task start-all`

This will spin up the required front end, api, and database components.

By default, you will have the following:

- A front end accessible at: http://localhost:5173/
- An API at: http://localhost:31100/
    Note, since we use FastAPI, you also get
    - Interactive OpenAPI documentation at: http://localhost:31100/docs
    - Redoc documentation at: http://localhost:31100/redoc
- A PGAdmin interface at: http://localhost:35050

(Note: The front end is currently only available in the feature/frontend branch.)


# Running Tests

Before committing any changes, ensure you run all tests to be sure existing behaviour continues to work. If any tests require updates to pass with your changes, ensure you update them as well.

(Todo: make a task to run all our different test types, add instructions for how to run the diffferent types as well.)


# Committing Changes

Before committing any changes, remember DCO and sign offs! If any commits are not made following the required standard, they will need reverted or redone.


# Tearing Down your Development Environment

To stop the environment, start by using ctrl+c (or cmd+c) to stop the current processes.

Then use `task stop-all` to full stop the environment.

If you want to remove the docker volumes used by the database, run `docker volume rm omi-postgres_pgadmin_data` and `docker volume rm omi-postgres_postgres_data`

(Todo: make a `db:teardown` task that removes the volumes)

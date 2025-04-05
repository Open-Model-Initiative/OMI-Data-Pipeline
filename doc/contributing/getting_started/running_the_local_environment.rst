Running The Local Environment
=============================

To start your virtual environment, run ``task activate-venv`` or ``source ./venv/bin/activate``

Then to start all the required services, run ``task dev``

This will spin up the required front end, api, and database containers.

Before the site will 'work' you will need to run ``task data:migrate`` to create the required data and tables

By default, you will have the following:

- A front end accessible at: http://localhost:5173/
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

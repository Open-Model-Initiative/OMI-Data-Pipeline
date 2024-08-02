# Setup

Test

## Prerequisites

### Task

We currently use https://github.com/go-task/task to manage our tasks.

To install task review docs here : https://taskfile.dev/installation/

### Docker / Docker Compose

We utilize docker and docker compose to run our services locally.

To install docker review docs here : https://docs.docker.com/

### Python / Virtual Environment

Please ensure you are running with Python 3.11 or higher with virtual environment installed.

## Dev Environment setup

To setup your environment run `task setup`
[Tested - Windows [x] | MacOS [ ] | Linux [ ]]

## Run database 

To run the database run `task db:start-postgres`  
[Tested - Windows [x] | MacOS [ ] | Linux [ ]]

## Run api server

To run the api server run `task api:start`  
[Tested - Windows [x] | MacOS [ ] | Linux [ ]]

## Connect to postgres and migrate 

To run the initial db migration run `task core:migrate`  
[Tested - Windows [] | MacOS [ ] | Linux [ ]]

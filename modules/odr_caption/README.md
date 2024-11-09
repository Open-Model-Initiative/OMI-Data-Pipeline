Prototype Captioning Pipeline
===========================

Run `task caption:build` to build the docker image.

Run `task caption:run` to run the docker image.

Loading the model and indexing the finite state machine takes a while, so be patient.

The docker image exposes a REST API at port 32100 with a single endpoint

The cookbook folder contains an example notebook that demonstrates how to use the REST API.

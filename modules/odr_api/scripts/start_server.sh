#!/bin/bash

# Run the FastAPI server with multiple workers and log output to a file
python modules/odr_api/server/main.py &
echo $! > server.pid

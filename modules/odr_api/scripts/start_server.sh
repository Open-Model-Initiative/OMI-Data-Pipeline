#!/bin/bash

# Run the FastAPI server with multiple workers and log output to a file
python server/server/main.py &
echo $! > server.pid
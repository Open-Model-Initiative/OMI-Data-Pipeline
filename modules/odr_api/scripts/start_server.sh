#!/bin/bash
# SPDX-License-Identifier: Apache-2.0

# Run the FastAPI server with multiple workers and log output to a file
python modules/odr_api/odr_api/main.py &
echo $! > server.pid

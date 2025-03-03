#!/bin/bash
# SPDX-License-Identifier: Apache-2.0

if [ -f server.pid ]; then
    pid=$(cat server.pid)
    kill $pid
    rm server.pid
    echo "Server stopped."
else
    echo "No server PID file found."
fi

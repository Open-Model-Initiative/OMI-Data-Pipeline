#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
set -e

task dev:migrate &
echo "Waiting for services to start..."

# Maximum wait time in seconds
max_wait=300
check_interval=5
start_time=$(date +%s)

while true; do
    if docker compose logs | grep -q "INFO:     Application startup complete."; then
        echo "Services started successfully."
        break
    fi

    current_time=$(date +%s)
    elapsed=$((current_time - start_time))

    if [ $elapsed -ge $max_wait ]; then
        echo "Timeout: Services did not start within $max_wait seconds."
        exit 1
    fi

    sleep $check_interval
done

cd modules/odr_frontend
npx playwright test

cd ../..
docker compose down

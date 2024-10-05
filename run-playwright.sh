#!/bin/bash
set -e

task dev &
echo "Waiting for services to start..."
sleep 300

cd modules/odr_frontend
npx playwright test

cd ../..
docker compose down

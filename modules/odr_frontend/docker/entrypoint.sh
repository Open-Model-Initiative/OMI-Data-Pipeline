#!/bin/sh
# SPDX-License-Identifier: Apache-2.0

set -eo pipefail

echo "Installing dependencies..."
# Only run pnpm install if node_modules doesn't exist or is empty
if [ ! -d "node_modules" ] || [ -z "$(ls -A node_modules)" ]; then
  echo "Node modules not found, installing dependencies..."
  pnpm install
else
  echo "Node modules found, skipping installation."
fi

# Check for database migrations
echo "Checking for database migrations..."
if [ "${RUN_MIGRATIONS:-false}" = "true" ]; then
  echo "Running database migrations..."

  # Wait for the database to be ready
  echo "Waiting for database to be ready..."
  max_retries=3
  retries=0

  # First, ensure the pgvector extension is installed
  while [ $retries -lt $max_retries ]; do
    if PGPASSWORD="${POSTGRES_PASSWORD}" psql -h "${POSTGRES_HOST}" -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" -c "CREATE EXTENSION IF NOT EXISTS vector;" 2>/dev/null; then
      echo "pgvector extension installed successfully."
      break
    else
      retries=$((retries+1))
      echo "Database not ready yet for extension installation. Retry $retries/$max_retries..."
      sleep 2
    fi
  done

  # Reset retries for migration
  retries=0

  # Now run the migrations
  while [ $retries -lt $max_retries ]; do
    if pnpm drizzle-kit push 2>/dev/null; then
      echo "Migrations completed successfully."
      break
    else
      retries=$((retries+1))
      echo "Database not ready yet for migrations. Retry $retries/$max_retries..."
      sleep 2
    fi
  done

  if [ $retries -eq $max_retries ]; then
    echo "WARNING: Could not run migrations after $max_retries attempts. Continuing anyway..."
  fi
else
  echo "Skipping migrations. Set RUN_MIGRATIONS=true to run migrations on startup."
  echo "You can also run migrations manually with: docker exec -it <container_name> pnpm drizzle-kit push"
fi

exec "$@"

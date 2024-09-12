#!/bin/sh

set -e

echo "Installing dependencies..."
pnpm install


exec "$@"

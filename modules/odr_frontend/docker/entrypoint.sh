#!/bin/sh

set -eo pipefail

echo "Installing dependencies..."
pnpm install


exec "$@"

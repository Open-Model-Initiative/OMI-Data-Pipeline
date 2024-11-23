#!/bin/sh
# SPDX-License-Identifier: Apache-2.0

set -eo pipefail

echo "Installing dependencies..."
pnpm install


exec "$@"

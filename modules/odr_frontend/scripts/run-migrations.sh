#!/bin/bash
# SPDX-License-Identifier: Apache-2.0

# Script to run database migrations manually

set -eo pipefail

echo "Running database migrations..."
pnpm drizzle-kit push:pg

echo "Seeding feature toggles..."
pnpm run db:seed-feature-toggles

echo "Migrations and seeding completed successfully."

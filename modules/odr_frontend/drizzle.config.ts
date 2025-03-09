/* SPDX-License-Identifier: Apache-2.0 */

import 'dotenv/config';
import { defineConfig } from 'drizzle-kit';
import type { Config } from 'drizzle-kit';

// Get database connection details from environment variables or use defaults
const POSTGRES_HOST = process.env.POSTGRES_HOST ?? 'localhost';
const POSTGRES_PORT = process.env.POSTGRES_PORT ?? '35432';
const POSTGRES_DB = process.env.POSTGRES_DB ?? 'opendatarepository';
const POSTGRES_USER = process.env.POSTGRES_USER ?? 'opendatarepository';
const POSTGRES_PASSWORD = process.env.POSTGRES_PASSWORD ?? 'opendatarepository';

const config: Config = {
  out: './drizzle',
  schema: './src/db/schemas/index.ts',
  dialect: 'postgresql',
  dbCredentials: {
    url: `postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}`,
  },
};

export default defineConfig(config);

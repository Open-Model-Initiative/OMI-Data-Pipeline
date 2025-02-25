/* SPDX-License-Identifier: Apache-2.0 */

import 'dotenv/config';
import { defineConfig } from 'drizzle-kit';
export default defineConfig({
  out: './drizzle',
  schema: './src/db/schemas/index.ts',
  dialect: 'postgresql',
  dbCredentials: {
    url: "postgresql://opendatarepository:opendatarepository@localhost:35432/opendatarepository",
  },
});

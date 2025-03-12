/*   SPDX-License-Identifier: Apache-2.0 */

import 'dotenv/config';
import { drizzle } from 'drizzle-orm/node-postgres';
const db = drizzle(process.env.DATABASE_URL!);

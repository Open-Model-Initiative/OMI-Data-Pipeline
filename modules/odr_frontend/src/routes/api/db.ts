/* SPDX-License-Identifier: Apache-2.0 */
import { drizzle } from 'drizzle-orm/node-postgres';
import { Pool } from 'pg';
import * as schema from '../../db/schemas';
import { env } from '$env/dynamic/private';

// Create a PostgreSQL connection pool
const pool = new Pool({
  connectionString: env.DATABASE_URL,
});

// Create a drizzle instance
export const db = drizzle(pool, { schema });

// Helper function to handle API errors
export function handleError(error: unknown) {
  console.error('API Error:', error);
  if (error instanceof Error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
  return new Response(JSON.stringify({ error: 'Unknown error occurred' }), {
    status: 500,
    headers: { 'Content-Type': 'application/json' }
  });
}

// Common headers for JSON responses
export const jsonHeaders = {
  'Content-Type': 'application/json'
};

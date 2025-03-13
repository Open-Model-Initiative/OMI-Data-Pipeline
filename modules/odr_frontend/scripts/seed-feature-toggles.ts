/* SPDX-License-Identifier: Apache-2.0 */
/**
 * Feature Toggle Seed Script
 *
 * Seeds the database with initial feature toggle values.
 * This ensures that all environments have the same set of feature toggles available.
 *
 * Usage:
 *   pnpm run db:seed-feature-toggles
 */

import { drizzle } from 'drizzle-orm/node-postgres';
import pg from 'pg';
import { featureToggles } from '../src/db/schemas/misc';
import { eq } from 'drizzle-orm';
import dotenv from 'dotenv';

// Load environment variables
dotenv.config();

const { Pool } = pg;

// Define the feature toggles to seed
const featureTogglesToSeed = [
  {
    featureName: 'HDR Image Upload',
    isEnabled: true,
    defaultState: true
  },
  {
    featureName: 'Show Datasets',
    isEnabled: false,
    defaultState: false
  }
];

async function main() {
  console.log('Connecting to database...');

  // Validate required environment variables
  const requiredEnvVars = ['POSTGRES_HOST', 'POSTGRES_PORT', 'POSTGRES_DB', 'POSTGRES_USER', 'POSTGRES_PASSWORD'];
  const missingEnvVars = requiredEnvVars.filter(varName => !process.env[varName]);

  if (missingEnvVars.length > 0) {
    console.error(`Error: Missing required environment variables: ${missingEnvVars.join(', ')}`);
    process.exit(1);
  }

  // Create a PostgreSQL connection using environment variables
  const pool = new Pool({
    host: process.env.POSTGRES_HOST,
    port: parseInt(process.env.POSTGRES_PORT || '5432'),
    database: process.env.POSTGRES_DB,
    user: process.env.POSTGRES_USER,
    password: process.env.POSTGRES_PASSWORD
  });

  // Create a Drizzle instance
  const db = drizzle(pool);

  console.log('Seeding feature toggles...');

  try {
    // Insert feature toggles with ON CONFLICT DO NOTHING logic
    for (const toggle of featureTogglesToSeed) {
      // Check if the feature toggle already exists
      const existingToggle = await db.select()
        .from(featureToggles)
        .where(eq(featureToggles.featureName, toggle.featureName));

      // If it doesn't exist, insert it
      if (existingToggle.length === 0) {
        await db.insert(featureToggles).values(toggle);
        console.log(`Added feature toggle: ${toggle.featureName}`);
      } else {
        console.log(`Feature toggle already exists: ${toggle.featureName}`);
      }
    }

    console.log('Feature toggles seeded successfully!');
  } catch (error) {
    console.error('Error seeding feature toggles:', error);
    process.exit(1);
  } finally {
    await pool.end();
  }
}

main().catch((error) => {
  console.error('Unhandled error:', error);
  process.exit(1);
});

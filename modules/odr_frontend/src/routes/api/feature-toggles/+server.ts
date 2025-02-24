/* SPDX-License-Identifier: Apache-2.0 */
import { db, handleError, jsonHeaders } from '../db';
import { featureToggles } from '../../../db/schemas/misc';
import { eq } from 'drizzle-orm';
import { json } from '@sveltejs/kit';

/**
 * GET /api/feature-toggles - Retrieve all feature toggles
 */
export async function GET({ url }) {
  try {
    const limit = Number(url.searchParams.get('limit') || '50');
    const offset = Number(url.searchParams.get('offset') || '0');
    const featureName = url.searchParams.get('featureName');
    const isEnabled = url.searchParams.has('isEnabled')
      ? url.searchParams.get('isEnabled') === 'true'
      : undefined;

    let query = db.select().from(featureToggles);

    // Apply filters if provided
    if (featureName) {
      query = query.where(eq(featureToggles.featureName, featureName));
    }

    if (isEnabled !== undefined) {
      query = query.where(eq(featureToggles.isEnabled, isEnabled));
    }

    // Apply pagination
    query = query.limit(limit).offset(offset);

    const data = await query;
    return json({ data, count: data.length });
  } catch (error) {
    return handleError(error);
  }
}

/**
 * POST /api/feature-toggles - Create a new feature toggle
 */
export async function POST({ request }) {
  try {
    const data = await request.json();

    // Validate required fields
    if (!data.featureName) {
      return new Response(
        JSON.stringify({ error: 'Feature name is required' }),
        { status: 400, headers: jsonHeaders }
      );
    }

    // Check for duplicate feature name
    const existingFeature = await db.select()
      .from(featureToggles)
      .where(eq(featureToggles.featureName, data.featureName))
      .limit(1);

    if (existingFeature.length) {
      return new Response(
        JSON.stringify({ error: 'Feature toggle with this name already exists' }),
        { status: 400, headers: jsonHeaders }
      );
    }

    // Insert new feature toggle
    const newFeature = await db.insert(featureToggles).values({
      featureName: data.featureName,
      isEnabled: data.isEnabled ?? false,
      defaultState: data.defaultState ?? false,
    }).returning();

    return json(newFeature[0], { status: 201 });
  } catch (error) {
    return handleError(error);
  }
}

/**
 * PUT /api/feature-toggles/:name - Update an existing feature toggle
 */
export async function PUT({ params, request }) {
  try {
    const featureName = params.name;
    const data = await request.json();

    if (!featureName) {
      return new Response(
        JSON.stringify({ error: 'Feature name is required' }),
        { status: 400, headers: jsonHeaders }
      );
    }

    // Check if feature exists
    const existingFeature = await db.select()
      .from(featureToggles)
      .where(eq(featureToggles.featureName, featureName))
      .limit(1);

    if (!existingFeature.length) {
      return new Response(
        JSON.stringify({ error: 'Feature toggle not found' }),
        { status: 404, headers: jsonHeaders }
      );
    }

    // Update feature toggle
    const updatedFeature = await db.update(featureToggles)
      .set({
        isEnabled: data.isEnabled,
        defaultState: data.defaultState,
      })
      .where(eq(featureToggles.featureName, featureName))
      .returning();

    return json(updatedFeature[0]);
  } catch (error) {
    return handleError(error);
  }
}

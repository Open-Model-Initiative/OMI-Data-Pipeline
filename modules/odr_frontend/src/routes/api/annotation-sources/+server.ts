/* SPDX-License-Identifier: Apache-2.0 */
import { db, handleError, jsonHeaders } from '../db';
import { annotationSources } from '../../../db/schemas/annotations';
import { eq } from 'drizzle-orm';
import { json } from '@sveltejs/kit';

/**
 * GET /api/annotation-sources - Retrieve all annotation sources with optional filtering
 */
export async function GET({ url }) {
  try {
    const limit = Number(url.searchParams.get('limit') || '50');
    const offset = Number(url.searchParams.get('offset') || '0');
    const name = url.searchParams.get('name');
    const ecosystem = url.searchParams.get('ecosystem');
    const type = url.searchParams.get('type');

    let query = db.select().from(annotationSources);

    // Apply filters if provided
    if (name) {
      query = query.where(eq(annotationSources.name, name));
    }

    if (ecosystem) {
      query = query.where(eq(annotationSources.ecosystem, ecosystem));
    }

    if (type) {
      query = query.where(eq(annotationSources.type, type));
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
 * POST /api/annotation-sources - Create a new annotation source
 */
export async function POST({ request }) {
  try {
    const sourceData = await request.json();

    // Validate required fields
    if (!sourceData.name) {
      return new Response(
        JSON.stringify({ error: 'Name is required' }),
        { status: 400, headers: jsonHeaders }
      );
    }

    // Insert new annotation source
    const newSource = await db.insert(annotationSources).values({
      name: sourceData.name,
      ecosystem: sourceData.ecosystem,
      type: sourceData.type,
      annotationSchema: sourceData.annotationSchema,
      license: sourceData.license,
      licenseUrl: sourceData.licenseUrl,
      addedById: sourceData.addedById,
      updatedAt: new Date().toISOString(),
    }).returning();

    return json(newSource[0], { status: 201 });
  } catch (error) {
    return handleError(error);
  }
}

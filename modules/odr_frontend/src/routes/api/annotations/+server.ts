/* SPDX-License-Identifier: Apache-2.0 */
import { db, handleError, jsonHeaders } from '../db';
import { annotations } from '../../../db/schemas/annotations';
import { eq } from 'drizzle-orm';
import { json } from '@sveltejs/kit';

/**
 * GET /api/annotations - Retrieve all annotations with optional filtering
 */
export async function GET({ url }) {
  try {
    const limit = Number(url.searchParams.get('limit') || '50');
    const offset = Number(url.searchParams.get('offset') || '0');
    const contentId = url.searchParams.get('contentId') ? parseInt(url.searchParams.get('contentId')) : null;
    const userId = url.searchParams.get('fromUserId') ? parseInt(url.searchParams.get('fromUserId')) : null;
    const teamId = url.searchParams.get('fromTeamId') ? parseInt(url.searchParams.get('fromTeamId')) : null;

    let query = db.select().from(annotations);

    // Apply filters if provided
    if (contentId) {
      query = query.where(eq(annotations.contentId, contentId));
    }

    if (userId) {
      query = query.where(eq(annotations.fromUserId, userId));
    }

    if (teamId) {
      query = query.where(eq(annotations.fromTeamId, teamId));
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
 * POST /api/annotations - Create a new annotation
 */
export async function POST({ request }) {
  try {
    const annotationData = await request.json();

    // Validate required fields
    if (!annotationData.contentId) {
      return new Response(
        JSON.stringify({ error: 'Content ID is required' }),
        { status: 400, headers: jsonHeaders }
      );
    }

    // Insert new annotation
    const newAnnotation = await db.insert(annotations).values({
      contentId: annotationData.contentId,
      annotation: annotationData.annotation,
      manuallyAdjusted: annotationData.manuallyAdjusted,
      overallRating: annotationData.overallRating,
      fromUserId: annotationData.fromUserId,
      fromTeamId: annotationData.fromTeamId,
    }).returning();

    return json(newAnnotation[0], { status: 201 });
  } catch (error) {
    return handleError(error);
  }
}

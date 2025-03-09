/* SPDX-License-Identifier: Apache-2.0 */
import { db, handleError, jsonHeaders } from '../../db';
import { annotations } from '../../../../db/schemas/annotations';
import { eq } from 'drizzle-orm';
import { json } from '@sveltejs/kit';

/**
 * GET /api/annotations/:id - Get a single annotation by ID
 */
export async function GET({ params }) {
  try {
    const annotationId = parseInt(params.id);

    if (isNaN(annotationId)) {
      return new Response(
        JSON.stringify({ error: 'Invalid annotation ID' }),
        { status: 400, headers: jsonHeaders }
      );
    }

    const annotation = await db.select().from(annotations).where(eq(annotations.id, annotationId)).limit(1);

    if (!annotation.length) {
      return new Response(
        JSON.stringify({ error: 'Annotation not found' }),
        { status: 404, headers: jsonHeaders }
      );
    }

    return json(annotation[0]);
  } catch (error) {
    return handleError(error);
  }
}

/**
 * PUT /api/annotations/:id - Update an annotation
 */
export async function PUT({ params, request }) {
  try {
    const annotationId = parseInt(params.id);
    const annotationData = await request.json();

    if (isNaN(annotationId)) {
      return new Response(
        JSON.stringify({ error: 'Invalid annotation ID' }),
        { status: 400, headers: jsonHeaders }
      );
    }

    // Check if annotation exists
    const existingAnnotation = await db.select().from(annotations).where(eq(annotations.id, annotationId)).limit(1);

    if (!existingAnnotation.length) {
      return new Response(
        JSON.stringify({ error: 'Annotation not found' }),
        { status: 404, headers: jsonHeaders }
      );
    }

    // Update annotation
    const updatedAnnotation = await db.update(annotations)
      .set({
        annotation: annotationData.annotation,
        manuallyAdjusted: annotationData.manuallyAdjusted,
        overallRating: annotationData.overallRating,
        fromUserId: annotationData.fromUserId,
        fromTeamId: annotationData.fromTeamId,
        updatedAt: new Date().toISOString(),
      })
      .where(eq(annotations.id, annotationId))
      .returning();

    return json(updatedAnnotation[0]);
  } catch (error) {
    return handleError(error);
  }
}

/**
 * DELETE /api/annotations/:id - Delete an annotation
 */
export async function DELETE({ params }) {
  try {
    const annotationId = parseInt(params.id);

    if (isNaN(annotationId)) {
      return new Response(
        JSON.stringify({ error: 'Invalid annotation ID' }),
        { status: 400, headers: jsonHeaders }
      );
    }

    // Check if annotation exists
    const existingAnnotation = await db.select().from(annotations).where(eq(annotations.id, annotationId)).limit(1);

    if (!existingAnnotation.length) {
      return new Response(
        JSON.stringify({ error: 'Annotation not found' }),
        { status: 404, headers: jsonHeaders }
      );
    }

    // Delete annotation
    await db.delete(annotations).where(eq(annotations.id, annotationId));

    return new Response(null, { status: 204 });
  } catch (error) {
    return handleError(error);
  }
}

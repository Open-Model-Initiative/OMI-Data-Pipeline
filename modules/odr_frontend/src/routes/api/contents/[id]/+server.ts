/* SPDX-License-Identifier: Apache-2.0 */
import { db, handleError, jsonHeaders } from '../../db';
import { contents } from '../../../../db/schemas/contents';
import { eq } from 'drizzle-orm';
import { json } from '@sveltejs/kit';
import type { RequestEvent } from '@sveltejs/kit';
import { contenttype } from '../../../../db/schemas/enums';

/**
 * GET /api/contents/:id - Get a single content item by ID
 */
export async function GET({ params }: RequestEvent) {
  try {
    const id = params.id ?? '';
    const contentId = parseInt(id);

    if (isNaN(contentId)) {
      return new Response(
        JSON.stringify({ error: 'Invalid content ID' }),
        { status: 400, headers: jsonHeaders }
      );
    }

    const content = await db.select().from(contents).where(eq(contents.id, contentId)).limit(1);

    if (!content.length) {
      return new Response(
        JSON.stringify({ error: 'Content not found' }),
        { status: 404, headers: jsonHeaders }
      );
    }

    return json(content[0]);
  } catch (error) {
    return handleError(error);
  }
}

/**
 * PUT /api/contents/:id - Update a content item
 */
export async function PUT({ params, request }: RequestEvent) {
  try {
    const id = params.id ?? '';
    const contentId = parseInt(id);
    const contentData = await request.json();

    if (isNaN(contentId)) {
      return new Response(
        JSON.stringify({ error: 'Invalid content ID' }),
        { status: 400, headers: jsonHeaders }
      );
    }

    // Check if content exists
    const existingContent = await db.select().from(contents).where(eq(contents.id, contentId)).limit(1);

    if (!existingContent.length) {
      return new Response(
        JSON.stringify({ error: 'Content not found' }),
        { status: 404, headers: jsonHeaders }
      );
    }

    // Validate content type if provided
    if (contentData.type && !contenttype.enumValues.includes(contentData.type)) {
      return new Response(
        JSON.stringify({
          error: `Invalid content type. Must be one of: ${contenttype.enumValues.join(', ')}`
        }),
        { status: 400, headers: jsonHeaders }
      );
    }

    // Update content
    const updatedContent = await db.update(contents)
      .set({
        name: contentData.name,
        type: contentData.type,
        hash: contentData.hash,
        phash: contentData.phash,
        width: contentData.width,
        height: contentData.height,
        format: contentData.format,
        size: contentData.size,
        status: contentData.status,
        license: contentData.license,
        licenseUrl: contentData.licenseUrl,
        flags: contentData.flags,
        meta: contentData.meta,
        url: [...(contentData.url ? [contentData.url] : [])],
        updatedAt: new Date().toISOString()
      })
      .where(eq(contents.id, contentId))
      .returning();

    return json(updatedContent[0]);
  } catch (error) {
    return handleError(error);
  }
}

/**
 * DELETE /api/contents/:id - Delete a content item
 */
export async function DELETE({ params }: RequestEvent) {
  try {
    const id = params.id ?? '';
    const contentId = parseInt(id);

    if (isNaN(contentId)) {
      return new Response(
        JSON.stringify({ error: 'Invalid content ID' }),
        { status: 400, headers: jsonHeaders }
      );
    }

    // Check if content exists
    const existingContent = await db.select().from(contents).where(eq(contents.id, contentId)).limit(1);

    if (!existingContent.length) {
      return new Response(
        JSON.stringify({ error: 'Content not found' }),
        { status: 404, headers: jsonHeaders }
      );
    }

    // Delete content
    await db.delete(contents).where(eq(contents.id, contentId));

    return new Response(null, { status: 204 });
  } catch (error) {
    return handleError(error);
  }
}

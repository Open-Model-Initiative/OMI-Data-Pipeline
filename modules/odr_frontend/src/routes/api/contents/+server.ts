/* SPDX-License-Identifier: Apache-2.0 */
import { db, handleError, jsonHeaders } from '../db';
import { contents } from '../../../db/schemas/contents';
import { eq, like, sql } from 'drizzle-orm';
import { json } from '@sveltejs/kit';
import type { RequestEvent } from '@sveltejs/kit';
import { contenttype, contentstatus } from '../../../db/schemas/enums';

/**
 * GET /api/contents - Retrieve all content items with optional filtering
 */
export async function GET({ url }: RequestEvent) {
  try {
    const limit = Number(url.searchParams.get('limit') ?? '50');
    const offset = Number(url.searchParams.get('offset') ?? '0');
    const name = url.searchParams.get('name');
    const typeParam = url.searchParams.get('type');
    const statusParam = url.searchParams.get('status');

    let query = db.select().from(contents) as any;

    // Apply filters if provided
    if (name) {
      query = query.where(like(contents.name, `%${name}%`));
    }

    if (typeParam) {
      // Type validation against enum values
      const type = typeParam as typeof contenttype.enumValues[number];
      if (contenttype.enumValues.includes(type)) {
        query = query.where(eq(contents.type, type));
      }
    }

    if (statusParam) {
      // Status validation against enum values
      const status = statusParam as typeof contentstatus.enumValues[number];
      if (contentstatus.enumValues.includes(status)) {
        query = query.where(eq(contents.status, status));
      }
    }

    // Apply pagination
    query = query.limit(limit).offset(offset);

    const data = await query;

    // Simplified count query with just the total number
    const countResult = await db.select({ count: sql<number>`count(*)` }).from(contents);
    const totalCount = Number(countResult[0]?.count || 0);

    return json({ data, count: totalCount });
  } catch (error) {
    return handleError(error);
  }
}

/**
 * POST /api/contents - Create a new content item
 */
export async function POST({ request }: RequestEvent) {
  try {
    const contentData = await request.json();

    // Validate required fields
    if (!contentData.name || !contentData.type) {
      return new Response(
        JSON.stringify({ error: 'Name and content type are required' }),
        { status: 400, headers: jsonHeaders }
      );
    }

    // Validate content type against enum values
    if (!contenttype.enumValues.includes(contentData.type)) {
      return new Response(
        JSON.stringify({
          error: `Invalid content type. Must be one of: ${contenttype.enumValues.join(', ')}`
        }),
        { status: 400, headers: jsonHeaders }
      );
    }

    // Insert new content
    const newContent = await db.insert(contents).values({
      name: contentData.name,
      type: contentData.type,
      hash: contentData.hash,
      phash: contentData.phash,
      width: contentData.width,
      height: contentData.height,
      format: contentData.format,
      size: contentData.size,
      status: contentData.status ?? 'PENDING', // Default status
      license: contentData.license,
      licenseUrl: contentData.licenseUrl,
      flags: contentData.flags,
      meta: contentData.meta,
      fromUserId: contentData.fromUserId,
      fromTeamId: contentData.fromTeamId,
      url: [...(contentData.url ? [contentData.url] : [])],
      updatedAt: new Date().toISOString()
    }).returning();

    return json(newContent[0], { status: 201 });
  } catch (error) {
    return handleError(error);
  }
}

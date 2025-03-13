/* SPDX-License-Identifier: Apache-2.0 */
import { db, handleError, jsonHeaders } from '../db';
import { embeddingEngines, contentEmbeddings } from '../../../db/schemas/embeddings';
import { eq } from 'drizzle-orm';
import { json } from '@sveltejs/kit';

/**
 * GET /api/embeddings/engines - Retrieve all embedding engines
 */
export async function GET({ url }) {
  try {
    // Handle embedding engines request
    if (url.pathname.endsWith('/engines')) {
      const limit = Number(url.searchParams.get('limit') || '50');
      const offset = Number(url.searchParams.get('offset') || '0');
      const type = url.searchParams.get('type');
      const supported = url.searchParams.get('supported') === 'true';

      let query = db.select().from(embeddingEngines);

      // Apply filters if provided
      if (type) {
        query = query.where(eq(embeddingEngines.type, type));
      }

      if (url.searchParams.has('supported')) {
        query = query.where(eq(embeddingEngines.supported, supported));
      }

      // Apply pagination
      query = query.limit(limit).offset(offset);

      const data = await query;
      return json({ data, count: data.length });
    }

    // Handle content embeddings request
    else {
      const limit = Number(url.searchParams.get('limit') || '50');
      const offset = Number(url.searchParams.get('offset') || '0');
      const contentId = url.searchParams.get('contentId') ? parseInt(url.searchParams.get('contentId')) : null;
      const engineId = url.searchParams.get('embeddingEngineId') ? parseInt(url.searchParams.get('embeddingEngineId')) : null;

      let query = db.select().from(contentEmbeddings);

      // Apply filters if provided
      if (contentId) {
        query = query.where(eq(contentEmbeddings.contentId, contentId));
      }

      if (engineId) {
        query = query.where(eq(contentEmbeddings.embeddingEngineId, engineId));
      }

      // Apply pagination
      query = query.limit(limit).offset(offset);

      const data = await query;
      return json({ data, count: data.length });
    }
  } catch (error) {
    return handleError(error);
  }
}

/**
 * POST /api/embeddings/engines - Create a new embedding engine
 */
export async function POST({ request, url }) {
  try {
    const data = await request.json();

    // Handle embedding engines creation
    if (url.pathname.endsWith('/engines')) {
      // Validate required fields
      if (!data.name || !data.type) {
        return new Response(
          JSON.stringify({ error: 'Name and type are required' }),
          { status: 400, headers: jsonHeaders }
        );
      }

      // Insert new embedding engine
      const newEngine = await db.insert(embeddingEngines).values({
        name: data.name,
        description: data.description,
        version: data.version,
        type: data.type,
        supported: data.supported ?? true,
        updatedAt: new Date().toISOString(),
      }).returning();

      return json(newEngine[0], { status: 201 });
    }

    // Handle content embedding creation
    else {
      // Validate required fields
      if (!data.contentId || !data.embeddingEngineId || !data.embedding) {
        return new Response(
          JSON.stringify({ error: 'Content ID, embedding engine ID, and embedding vector are required' }),
          { status: 400, headers: jsonHeaders }
        );
      }

      // Insert new content embedding
      const newEmbedding = await db.insert(contentEmbeddings).values({
        contentId: data.contentId,
        embeddingEngineId: data.embeddingEngineId,
        fromUserId: data.fromUserId,
        fromTeamId: data.fromTeamId,
        embedding: data.embedding,
      }).returning();

      return json(newEmbedding[0], { status: 201 });
    }
  } catch (error) {
    return handleError(error);
  }
}

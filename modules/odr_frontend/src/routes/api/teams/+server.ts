/* SPDX-License-Identifier: Apache-2.0 */
import { db, handleError, jsonHeaders } from '../db';
import { teams } from '../../../db/schemas/teams';
import { eq } from 'drizzle-orm';
import { json } from '@sveltejs/kit';

/**
 * GET /api/teams - Retrieve all teams with optional filtering
 */
export async function GET({ url }) {
  try {
    const limit = Number(url.searchParams.get('limit') || '50');
    const offset = Number(url.searchParams.get('offset') || '0');
    const name = url.searchParams.get('name');

    let query = db.select().from(teams);

    // Apply filters if provided
    if (name) {
      query = query.where(eq(teams.name, name));
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
 * POST /api/teams - Create a new team
 */
export async function POST({ request }) {
  try {
    const teamData = await request.json();

    // Validate required fields
    if (!teamData.name) {
      return new Response(
        JSON.stringify({ error: 'Team name is required' }),
        { status: 400, headers: jsonHeaders }
      );
    }

    // Insert new team
    const newTeam = await db.insert(teams).values({
      name: teamData.name,
    }).returning();

    return json(newTeam[0], { status: 201 });
  } catch (error) {
    return handleError(error);
  }
}

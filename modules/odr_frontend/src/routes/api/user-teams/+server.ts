/* SPDX-License-Identifier: Apache-2.0 */
import { db, handleError, jsonHeaders } from '../db';
import { userTeams } from '../../../db/schemas/userTeams';
import { users } from '../../../db/schemas/users';
import { teams } from '../../../db/schemas/teams';
import { eq, and } from 'drizzle-orm';
import { json } from '@sveltejs/kit';

/**
 * GET /api/user-teams - Get all user-team associations with optional filtering
 */
export async function GET({ url }) {
  try {
    const userId = url.searchParams.get('userId') ? parseInt(url.searchParams.get('userId')) : null;
    const teamId = url.searchParams.get('teamId') ? parseInt(url.searchParams.get('teamId')) : null;
    const limit = Number(url.searchParams.get('limit') || '50');
    const offset = Number(url.searchParams.get('offset') || '0');

    let query = db.select().from(userTeams);

    // Apply filters if provided
    if (userId) {
      query = query.where(eq(userTeams.userId, userId));
    }

    if (teamId) {
      query = query.where(eq(userTeams.teamId, teamId));
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
 * POST /api/user-teams - Add a user to a team
 */
export async function POST({ request }) {
  try {
    const data = await request.json();

    // Validate required fields
    if (!data.userId || !data.teamId) {
      return new Response(
        JSON.stringify({ error: 'User ID and Team ID are required' }),
        { status: 400, headers: jsonHeaders }
      );
    }

    // Check if user exists
    const userExists = await db.select().from(users).where(eq(users.id, data.userId)).limit(1);
    if (!userExists.length) {
      return new Response(
        JSON.stringify({ error: 'User not found' }),
        { status: 404, headers: jsonHeaders }
      );
    }

    // Check if team exists
    const teamExists = await db.select().from(teams).where(eq(teams.id, data.teamId)).limit(1);
    if (!teamExists.length) {
      return new Response(
        JSON.stringify({ error: 'Team not found' }),
        { status: 404, headers: jsonHeaders }
      );
    }

    // Check if the user is already in the team
    const existingAssociation = await db.select()
      .from(userTeams)
      .where(
        and(
          eq(userTeams.userId, data.userId),
          eq(userTeams.teamId, data.teamId)
        )
      )
      .limit(1);

    if (existingAssociation.length) {
      return new Response(
        JSON.stringify({ error: 'User is already a member of this team' }),
        { status: 400, headers: jsonHeaders }
      );
    }

    // Add user to team
    const newUserTeam = await db.insert(userTeams).values({
      userId: data.userId,
      teamId: data.teamId,
      role: data.role || 'member', // Default role
    }).returning();

    return json(newUserTeam[0], { status: 201 });
  } catch (error) {
    return handleError(error);
  }
}

/**
 * DELETE /api/user-teams - Remove a user from a team
 */
export async function DELETE({ url }) {
  try {
    const userId = url.searchParams.get('userId') ? parseInt(url.searchParams.get('userId')) : null;
    const teamId = url.searchParams.get('teamId') ? parseInt(url.searchParams.get('teamId')) : null;

    // Validate required fields
    if (!userId || !teamId) {
      return new Response(
        JSON.stringify({ error: 'User ID and Team ID are required' }),
        { status: 400, headers: jsonHeaders }
      );
    }

    // Check if the user is in the team
    const existingAssociation = await db.select()
      .from(userTeams)
      .where(
        and(
          eq(userTeams.userId, userId),
          eq(userTeams.teamId, teamId)
        )
      )
      .limit(1);

    if (!existingAssociation.length) {
      return new Response(
        JSON.stringify({ error: 'User is not a member of this team' }),
        { status: 404, headers: jsonHeaders }
      );
    }

    // Remove user from team
    await db.delete(userTeams)
      .where(
        and(
          eq(userTeams.userId, userId),
          eq(userTeams.teamId, teamId)
        )
      );

    return new Response(null, { status: 204 });
  } catch (error) {
    return handleError(error);
  }
}

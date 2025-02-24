/* SPDX-License-Identifier: Apache-2.0 */
import { db, handleError, jsonHeaders } from '../../db';
import { teams } from '../../../../db/schemas/teams';
import { userTeams } from '../../../../db/schemas/userTeams';
import { eq, and } from 'drizzle-orm';
import { json } from '@sveltejs/kit';

/**
 * GET /api/teams/:id - Get a single team by ID
 * GET /api/teams/:id/members - Get team members
 */
export async function GET({ params, url }) {
  try {
    const teamId = parseInt(params.id);

    if (isNaN(teamId)) {
      return new Response(
        JSON.stringify({ error: 'Invalid team ID' }),
        { status: 400, headers: jsonHeaders }
      );
    }

    // If the request is for team members
    if (url.pathname.endsWith('/members')) {
      // Get team members
      const members = await db.select()
        .from(userTeams)
        .where(eq(userTeams.teamId, teamId));

      return json({ data: members, count: members.length });
    }
    // Regular team request
    else {
      const team = await db.select().from(teams).where(eq(teams.id, teamId)).limit(1);

      if (!team.length) {
        return new Response(
          JSON.stringify({ error: 'Team not found' }),
          { status: 404, headers: jsonHeaders }
        );
      }

      return json(team[0]);
    }
  } catch (error) {
    return handleError(error);
  }
}

/**
 * PUT /api/teams/:id - Update a team
 */
export async function PUT({ params, request }) {
  try {
    const teamId = parseInt(params.id);
    const teamData = await request.json();

    if (isNaN(teamId)) {
      return new Response(
        JSON.stringify({ error: 'Invalid team ID' }),
        { status: 400, headers: jsonHeaders }
      );
    }

    // Check if team exists
    const existingTeam = await db.select().from(teams).where(eq(teams.id, teamId)).limit(1);

    if (!existingTeam.length) {
      return new Response(
        JSON.stringify({ error: 'Team not found' }),
        { status: 404, headers: jsonHeaders }
      );
    }

    // Update team
    const updatedTeam = await db.update(teams)
      .set({
        name: teamData.name,
        updatedAt: new Date().toISOString(),
      })
      .where(eq(teams.id, teamId))
      .returning();

    return json(updatedTeam[0]);
  } catch (error) {
    return handleError(error);
  }
}

/**
 * DELETE /api/teams/:id - Delete a team
 */
export async function DELETE({ params }) {
  try {
    const teamId = parseInt(params.id);

    if (isNaN(teamId)) {
      return new Response(
        JSON.stringify({ error: 'Invalid team ID' }),
        { status: 400, headers: jsonHeaders }
      );
    }

    // Check if team exists
    const existingTeam = await db.select().from(teams).where(eq(teams.id, teamId)).limit(1);

    if (!existingTeam.length) {
      return new Response(
        JSON.stringify({ error: 'Team not found' }),
        { status: 404, headers: jsonHeaders }
      );
    }

    // Delete team memberships first
    await db.delete(userTeams).where(eq(userTeams.teamId, teamId));

    // Delete team
    await db.delete(teams).where(eq(teams.id, teamId));

    return new Response(null, { status: 204 });
  } catch (error) {
    return handleError(error);
  }
}

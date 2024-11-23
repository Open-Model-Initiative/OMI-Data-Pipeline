// SPDX-License-Identifier: Apache-2.0
import { pgClient } from '$lib/server/pg';
import type { RequestHandler } from '@sveltejs/kit';

export const POST: RequestHandler = async ({ request }) => {
    const body = await request.json();
    const trimmedTeamName = body.newTeamName?.trim();

    if (!trimmedTeamName) {
        return new Response(JSON.stringify({ success: false, error: 'No Team name provided' }), {
            status: 400,
            headers: { 'Content-Type': 'application/json' }
        });
    }

    try {
        const result = await pgClient.query(
            'INSERT INTO teams (name) VALUES ($1) RETURNING id, name, created_at, updated_at',
            [trimmedTeamName]
        );
        const newTeam = result.rows[0];
        console.info(`Added team ${trimmedTeamName} with id ${newTeam.id}`);
        return new Response(JSON.stringify({ success: true, team: newTeam }), {
            status: 201,
            headers: { 'Content-Type': 'application/json' }
        });
    } catch (e) {
        console.error(`Failed to add team ${trimmedTeamName}:`, e);

        // Type assertion for TypeScript
        if ((e as { code?: string }).code === '23505') {  // PostgreSQL error code for unique constraint violation
            return new Response(JSON.stringify({ success: false, error: 'Team name already exists' }), {
                status: 400,
                headers: { 'Content-Type': 'application/json' }
            });
        }

        return new Response(JSON.stringify({ success: false, error: 'An unexpected error occurred' }), {
            status: 500,
            headers: { 'Content-Type': 'application/json' }
        });
    }
};

export const DELETE: RequestHandler = async ({ request }) => {
    const body = await request.json();
    const teamId = body.teamId;

    if (!teamId) {
        return new Response(JSON.stringify({ success: false, error: 'No team ID provided' }), {
            status: 400,
            headers: { 'Content-Type': 'application/json' }
        });
    }

    try {
        //Delete all user_teams entries for this team
        const deleted_users = await pgClient.query('DELETE FROM user_teams WHERE team_id = $1', [teamId]);
        console.info(`Deleted ${deleted_users.rowCount} user_teams entries for team ${teamId}`);

        //Delete the team
        const result = await pgClient.query('DELETE FROM teams WHERE id = $1 RETURNING id', [teamId]);
        const deletedTeamId = result.rows[0]?.id;
        console.info(`Deleted team ${deletedTeamId}`);
        return new Response(JSON.stringify({ success: true }), {
            status: 200,
            headers: { 'Content-Type': 'application/json' }
        });
    } catch (e) {
        console.error(`Failed to delete team ${teamId}:`, e);
        return new Response(JSON.stringify({ success: false, error: 'An unexpected error occurred' }), {
            status: 500,
            headers: { 'Content-Type': 'application/json' }
        });
    }
};

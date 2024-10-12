import { PG_API, pgClient } from '$lib/server/pg';
import type { RequestHandler } from '@sveltejs/kit';

export const POST: RequestHandler = async ({ request }) => {
    const body = await request.json();
    if (!body.userId) {
        return new Response(JSON.stringify({ success: false, error: 'No user ID provided' }), {
            status: 400,
            headers: { 'Content-Type': 'application/json' }
        });
    }
    if (!body.teamId) {
        return new Response(JSON.stringify({ success: false, error: 'No team ID provided' }), {
            status: 400,
            headers: { 'Content-Type': 'application/json' }
        });
    }

    const team_users = await PG_API.teams.getUsers(body.teamId);
    if (team_users.some((user) => user.user_id == body.userId)) {
        return new Response(JSON.stringify({ success: false, error: 'User already in team' }), {
            status: 400,
            headers: { 'Content-Type': 'application/json' }
        });
    }

    try {
        const result = await pgClient.query(
            'INSERT INTO user_teams (team_id, user_id, role) VALUES ($1, $2, $3) RETURNING *',
            [body.teamId, body.userId, 'member']
        );
        console.info(`Added user ${body.userId} to team ${body.teamId}`);
        return new Response(JSON.stringify({ success: true, team_user: result.rows[0] }), {
            status: 201,
            headers: { 'Content-Type': 'application/json' }
        });
    } catch (e) {
        console.error(`Failed to add user ${body.userId} to team ${body.teamId}:`, e);
        return new Response(JSON.stringify({ success: false, error: e.message }), {
            status: 500,
            headers: { 'Content-Type': 'application/json' }
        });
    }
};

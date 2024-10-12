import { pgClient } from '$lib/server/pg';
import type { RequestHandler } from '@sveltejs/kit';

export const POST: RequestHandler = async ({ request }) => {
    const body = await request.json();
    if (!body.newTeamName) {
        return new Response(JSON.stringify({ success: false, error: 'No Team name provided' }), {
            status: 400,
            headers: { 'Content-Type': 'application/json' }
        });
    }

    try {
        const result = await pgClient.query(
            'INSERT INTO teams (name) VALUES ($1) RETURNING id, name, created_at, updated_at',
            [body.newTeamName]
        );

        const newTeam = result.rows[0];
        console.info(`Added team ${body.newTeamName} with id ${newTeam.id}`);

        return new Response(JSON.stringify({ success: true, team: newTeam }), {
            status: 201,
            headers: { 'Content-Type': 'application/json' }
        });
    } catch (e) {
        console.error(`Failed to add team ${body.newTeamName}:`, e);
        return new Response(JSON.stringify({ success: false, error: e.message }), {
            status: 500,
            headers: { 'Content-Type': 'application/json' }
        });
    }
};

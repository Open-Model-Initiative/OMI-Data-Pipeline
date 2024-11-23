// SPDX-License-Identifier: Apache-2.0
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

    try {
        const result = await pgClient.query(
            'DELETE FROM user_teams WHERE team_id = $1 AND user_id = $2',
            [body.teamId, body.userId]
        );

        console.info(`Removed user ${body.userId} from team ${body.teamId}`);
        return new Response(JSON.stringify({ success: true }), {
            status: 200,
            headers: { 'Content-Type': 'application/json' }
        });
    }
    catch (e) {
        console.error(`Failed to remove user ${body.userId} from team ${body.teamId}:`, e);
        return new Response(JSON.stringify({ success: false, error: (e as Error).message }), {
            status: 500,
            headers: { 'Content-Type': 'application/json' }
        });
    }
};

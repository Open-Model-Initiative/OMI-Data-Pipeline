import { PG_API, pgClient } from '$lib/server/pg';
import type { RequestHandler } from '@sveltejs/kit';
export const POST: RequestHandler = async ({ request }) => {
	const body = await request.json();
	if (!body.userId) {
		return new Response(JSON.stringify({ success: false, error: 'No user ID provided' }));
	}
	if (!body.teamId) {
		return new Response(JSON.stringify({ success: false, error: 'No team ID provided' }));
	}

	const team_users = await PG_API.teams.getUsers(body.teamId);
	if (team_users.some((user) => user.user_id == body.userId)) {
		return new Response(JSON.stringify({ success: false, error: 'User already in team' }));
	}

	try {
		const result = await pgClient.query(
			'INSERT INTO user_teams (team_id, user_id, role) VALUES ($1, $2, $3)',
			[body.teamId, body.userId, 'member']
		);
		console.info(`Added user ${body.userId} to team ${body.teamId}`);
		return new Response(JSON.stringify({ success: true, result: result }));
	} catch (e) {
		console.error(`Failed to add user ${body.userId} to team ${body.teamId}`);
		return new Response(JSON.stringify({ success: false, error: e }));
	}
};

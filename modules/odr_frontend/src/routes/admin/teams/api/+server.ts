import { pgClient } from '$lib/server/pg';
import type { RequestHandler } from '@sveltejs/kit';
export const POST: RequestHandler = async ({ request }) => {
	const body = await request.json();
	if (!body.newTeamName) {
		return new Response(JSON.stringify({ success: false, error: 'No Team name provided' }));
	}
	try {
		const result = await pgClient.query('INSERT INTO teams (name) VALUES ($1)', [body.newTeamName]);
		console.info(`Added team ${body.newTeamName}`);
		return new Response(JSON.stringify({ success: true, result: result }));
	} catch (e) {
		console.error(`Failed to add team ${body.newTeamName}`);
		return new Response(JSON.stringify({ success: false, error: e }));
	}
};

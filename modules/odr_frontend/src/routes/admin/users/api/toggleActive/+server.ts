// SPDX-License-Identifier: Apache-2.0
import { pgClient, type IDBUser } from '$lib/server/pg';
import type { RequestHandler } from '@sveltejs/kit';
export const PUT: RequestHandler = async ({ request }) => {
	const body = await request.json();
	if (!body.user) {
		return new Response(JSON.stringify({ success: false, error: 'No user provided' }));
	}
	const user: IDBUser = body.user;
	try {
		const result = await pgClient.query('UPDATE users SET is_active=$1 WHERE id=$2', [
			user.is_active,
			user.id
		]);
		console.info(`Set user ${user.id} as ${user.is_active ? 'active' : 'not active'}`);
		return new Response(JSON.stringify({ success: true, result: result }));
	} catch (e) {
		console.error(
			`Failed to set user ${user.id} as ${user.is_active ? 'active' : 'not active'}`
		);
		return new Response(JSON.stringify({ success: false, error: e }));
	}
};

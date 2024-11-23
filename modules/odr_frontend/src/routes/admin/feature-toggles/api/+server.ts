// SPDX-License-Identifier: Apache-2.0
import { pgClient } from '$lib/server/pg';
import type { RequestHandler } from '@sveltejs/kit';

export const GET: RequestHandler = async () => {
    try {
        const result = await pgClient.query('SELECT * FROM feature_toggles');
        return new Response(JSON.stringify(result.rows));
    } catch (e) {
        console.error('Failed to fetch feature toggles:', e);
        return new Response(JSON.stringify({ error: 'Failed to fetch feature toggles' }), { status: 500 });
    }
};

// SPDX-License-Identifier: Apache-2.0
import { pgClient, type IFeatureToggle } from '$lib/server/pg';
import type { RequestHandler } from '@sveltejs/kit';

export const PUT: RequestHandler = async ({ request }) => {
    const body = await request.json();

    if (!body.feature) {
        return new Response(JSON.stringify({ success: false, error: 'No feature toggle provided' }), { status: 400 });
    }

    const toggle: IFeatureToggle = body.feature;

    try {
        const result = await pgClient.query(
            'UPDATE feature_toggles SET is_enabled = $1 WHERE id = $2 RETURNING *',
            [
                toggle.is_enabled,
                toggle.id
            ]
        );

        console.info(`Set feature toggle ${toggle.id} to ${toggle.is_enabled ? 'enabled' : 'disabled'}`);

        return new Response(JSON.stringify(result.rows[0]));
    } catch (e) {
        console.error('Failed to update feature toggle:', e);
        return new Response(JSON.stringify({ error: 'Failed to update feature toggle' }), { status: 500 });
    }
};

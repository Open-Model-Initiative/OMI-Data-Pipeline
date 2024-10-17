import { pgClient } from '$lib/server/pg';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
    try {
        const result = await pgClient.query('SELECT * FROM feature_toggles');
        return {
            featureToggles: result.rows
        };
    } catch (e) {
        console.error('Failed to fetch feature toggles:', e);
        return {
            featureToggles: []
        };
    }
};

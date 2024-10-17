import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { PG_API } from '$lib/server/pg';

export const load: PageServerLoad = async (event) => {
	const session = await event.locals.auth();
	if (!session?.user) throw redirect(303, '/auth');

	const featureToggles = await PG_API.featureToggles.getAll();

	const featureToggleMap = Object.fromEntries(
		featureToggles.map(toggle => [toggle.feature_name, toggle.is_enabled])
	);

	return {
		featureToggles: featureToggleMap
	};
};

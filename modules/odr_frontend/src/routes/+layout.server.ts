// SPDX-License-Identifier: Apache-2.0
import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async ({ locals }) => {
	return {
		session: await locals.auth()
	};
};

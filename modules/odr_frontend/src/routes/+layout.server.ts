// SPDX-License-Identifier: Apache-2.0
import type { LayoutServerLoad } from './$types';

// +layout.ts
export const load: LayoutServerLoad = async ({ locals }) => {
	return {
		session: await locals.auth()
	};
};

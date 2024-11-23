// SPDX-License-Identifier: Apache-2.0
import { PG_API } from '$lib/server/pg';
/** @type {import('./$types').PageLoad} */
export async function load() {
	const users = await PG_API.users.getAll();
	return {
		users: users
	};
}

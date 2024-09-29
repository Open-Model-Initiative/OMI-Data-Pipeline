import { PG_API } from '$lib/server/pg';
/** @type {import('./$types').PageLoad} */
export async function load({ params }: { params: { slug: string } }) {
	const user = await PG_API.users.get(params.slug);
	const teams = await PG_API.teams.getUser(user.id);
	return { user, teams };
}

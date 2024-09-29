import { PG_API } from '$lib/server/pg';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async (event) => {
	const teams = await PG_API.teams.getAll();
	const team_users = await PG_API.teams.getAllUsers();
	const users = await PG_API.users.getAll();
	return {
		teams: teams,
		teams_users: team_users,
		users: users
	};
};

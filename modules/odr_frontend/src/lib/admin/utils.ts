import type { IDBUser } from '$lib/server/pg';

export async function toggleSuperUser(user: IDBUser) {
	const req = await fetch('/admin/users/api', {
		method: 'PUT',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ user })
	});
	const res = await req.json();
	if (!res.success) {
		console.error(res.error); //TODO: Need to add a toast here
	}
}

export async function load({ locals }) {
	return {
		isSuperUser: locals.isSuperUser
	};
}

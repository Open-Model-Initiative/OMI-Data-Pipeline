export async function load({ locals, cookies }) {
	console.log('Logging out user...');
	cookies.delete('session', { path: '/' });
	locals.isAuthenticated = false;
	locals.isSuperUser = false;
	return {};
}

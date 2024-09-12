// +layout.ts
export async function load({ locals }) {
	console.log('Loading layout...on the server we got isAuthenticated as:', locals.isAuthenticated);
	return {
		isAuthenticated: locals.isAuthenticated,
		isSuperUser: locals.isSuperUser
	};
}

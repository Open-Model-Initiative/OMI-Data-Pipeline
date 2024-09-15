import { redirect } from '@sveltejs/kit';
import { ENV } from '$lib/server/env';
/** @type {import('./$types').Actions} */
export const actions = {
	default: async (event) => {
		const body = await event.request.formData();

		const username = body.get('username') as string;
		const password = body.get('password') as string;

		if (!username || !password) {
			return {
				status: 400,
				body: JSON.stringify({ message: 'Missing username or password' })
			};
		}

		const loginRequest = await fetch(`${ENV.API_SERVICE_URL}/auth/login`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ username, password })
		});

		const loginResponse: Record<string, string> = await loginRequest.json();

		if (loginRequest.status === 200) {
			event.cookies.set('session', loginResponse.id, {
			  expires: new Date(loginResponse.expires_at),
			  path: '/',
			//   httpOnly: true
			});
			event.locals.isAuthenticated = true;
			throw redirect(302, '/');
		  } else {
			return {
				status: 400,
				body: JSON.stringify({ message: 'Error logging in user' })
			};
		}
	}
};

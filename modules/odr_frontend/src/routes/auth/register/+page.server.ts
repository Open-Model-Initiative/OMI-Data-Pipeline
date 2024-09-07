/** @type {import('./$types').Actions} */
import { ENV } from '$lib/server/env';

export const actions = {
	default: async (event) => {
		console.log('Registering new user...');
		const body = await event.request.formData();
		console.log(`Got form data: ${[...body.keys()]} with values: ${[...body.values()]}`);
		if (!body.has('email')) {
			console.error('Missing email');
			return {
				status: 400,
				body: JSON.stringify({ message: 'Missing email' })
			};
		}
		if (!body.has('username')) {
			console.error('Missing username');
			return {
				status: 400,
				body: JSON.stringify({ message: 'Missing username' })
			};
		}
		if (body.get('password') !== body.get('password_confirmation')) {
			console.error('Passwords do not match');
			return {
				status: 400,
				body: JSON.stringify({ message: 'Passwords do not match' })
			};
		} else if (String(body.get('password')).length < 8) {
			console.error('Password must be at least 8 characters long');
			return {
				status: 400,
				body: JSON.stringify({ message: 'Password must be at least 8 characters long' })
			};
		} else {
			console.info('Creating new user...');
			//Use the python endpoint to create a new user
			const req = await fetch(`${ENV.API_SERVICE_URL}/users/`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					username: body.get('username'),
					password: body.get('password'),
					email: body.get('email')
				})
			});
			const res: Record<string, string | boolean | number> = await req.json();
			if (req.status === 200 && res?.username === body.get('username')) {
				console.log('User created successfully');
				const tokenReq = await fetch(`${ENV.API_SERVICE_URL}/auth/login`, {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json'
					},
					body: JSON.stringify({
						username: body.get('username'),
						password: body.get('password')
					})
				});
				const tokenRes: Record<string, string | boolean | number> = await tokenReq.json();
				console.log(`Login response: ${JSON.stringify(tokenRes)}`);
				if (tokenReq.status === 200 && tokenRes?.access_token) {
					console.log('User logged in successfully');
					return {
						status: 200,
						body: JSON.stringify({ message: 'Success', token: tokenRes.access_token })
					};
				} else {
					console.error('Failed to log in user');
					return {
						status: 500,
						body: JSON.stringify({ message: 'Failed to log in user' })
					};
				}
			} else {
				console.error('Failed to create user');
				return {
					status: 500,
					body: JSON.stringify({ message: 'Failed to create user' })
				};
			}
		}
	}
};

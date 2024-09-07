import { redirect, type Cookies } from '@sveltejs/kit';
import { API_URL } from '$lib/server/env';

interface User {
	username: string;
	email: string;
	is_active: boolean;
	is_superuser: boolean;
	id: number;
	created_at: string;
	updated_at: string;
	user_type: 'user' | 'bot';
}

async function checkApiHealth() {
	try {
		const response = await fetch(`${API_URL}/health`);
		if (response.ok) {
			console.log('API health check successful');
		} else {
			console.error('API health check failed:', response.status, await response.text());
		}
	} catch (error) {
		console.error('API health check error:', error);
	}
}

/** @type {import('@sveltejs/kit').Handle} */
export async function handle({ event, resolve }) {
	await checkApiHealth();
	const { route, cookies, locals } = event;
	const sessionCookie = cookies.get('session');

	if (route.id?.startsWith('/auth/logout')) {
		return await resolve(event);
	}

	if (route.id?.startsWith('/auth')) {
		if (locals.isAuthenticated) {
			throw redirect(302, '/'); // User is already authenticated, redirect to home
		}
		return await resolve(event);
	}

	if (!sessionCookie) {
		locals.isAuthenticated = false;
		throw redirect(302, '/auth/login');
	}

	const user = await validateTokenFunction(cookies);
	if (!user) {
		locals.isAuthenticated = false;
		throw redirect(302, '/auth/login');
	}

	locals.isAuthenticated = true;
	locals.isSuperUser = user.is_superuser;

	if (route.id?.startsWith('/auth')) {
		throw redirect(302, '/');
	}

	return await resolve(event);
}

const validateTokenFunction = async (cookies: Cookies): Promise<User | false> => {
	const currentToken = cookies.get('session');
	const req = await fetch(`${API_URL}/users/me`, {
		headers: {
			Cookie: `session=${currentToken}`
		}
	});

	if (req.status !== 200) {
		console.error('Error validating token');
		return false;
	}

	const res = await req.json();
	if (!res.username) {
		console.error('Error validating token');
		return false;
	}

	return res as User;
};
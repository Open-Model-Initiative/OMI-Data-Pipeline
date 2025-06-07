// SPDX-License-Identifier: Apache-2.0
import { redirect, type Handle } from '@sveltejs/kit';
import { handle as authenticationHandle } from './auth';
import { sequence } from '@sveltejs/kit/hooks';

const authorizationHandle:Handle = async ({ event, resolve }) => {
	const session = await event.locals.auth();

	console.log('AUTH_SECRET exists:', !!process.env.AUTH_SECRET);
	console.log('GITHUB_CLIENT_ID exists:', !!process.env.GITHUB_CLIENT_ID);
	console.log('GITHUB_CLIENT_SECRET exists:', !!process.env.GITHUB_CLIENT_SECRET);
	console.log('DISCORD_CLIENT_ID exists:', !!process.env.DISCORD_CLIENT_ID);
	console.log('DISCORD_CLIENT_SECRET exists:', !!process.env.DISCORD_CLIENT_SECRET);

	if (event.url.pathname.startsWith('/auth')) {
		return resolve(event);
	} else if (!session) {
		throw redirect(303, '/auth');
	} else if (!session.user) {
		throw redirect(303, '/auth');
	} else if (!event.url.pathname.startsWith('/inactive') && (!session.user.is_active)) {
		throw redirect(303, '/inactive');
	} else if (!event.url.pathname.startsWith('/dco') && (!session.user.dco_accepted)) {
		throw redirect(303, '/dco');
	} else if (event.url.pathname.startsWith('/admin') && (!session.user.is_superuser)) {
		throw redirect(303, '/');
	}

	// If the request is still here, just proceed as normally
	return resolve(event);
}

// First handle authentication, then authorization
// Each function acts as a middleware, receiving the request handle
// And returning a handle which gets passed to the next function
export const handle: Handle = sequence(authenticationHandle, authorizationHandle);

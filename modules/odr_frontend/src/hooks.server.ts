// SPDX-License-Identifier: Apache-2.0
import { redirect, type Handle } from '@sveltejs/kit';
import { handle as authenticationHandle } from './auth';
import { sequence } from '@sveltejs/kit/hooks';

const authorizationHandle:Handle = async ({ event, resolve }) => {
	const session = await event.locals.auth();

	console.log('Request URL:', event.url.href);
	console.log('Request Origin:', event.request.headers.get('origin'));
	console.log('ORIGIN env:', process.env.ORIGIN);

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

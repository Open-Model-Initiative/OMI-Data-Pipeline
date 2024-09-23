import { redirect, type Handle } from '@sveltejs/kit';
import { handle as authenticationHandle } from './auth';
import { sequence } from '@sveltejs/kit/hooks';

//@ts-expect-error
async function authorizationHandle({ event, resolve }) {
	// Protect any routes under /admin
	if (event.url.pathname.startsWith('/admin')) {
		const session = await event.locals.auth();
		if (!session) {
			// Redirect to the signin page
			throw redirect(303, '/auth');
		}
	}

	// If the request is still here, just proceed as normally
	return resolve(event);
}

// First handle authentication, then authorization
// Each function acts as a middleware, receiving the request handle
// And returning a handle which gets passed to the next function
export const handle: Handle = sequence(authenticationHandle, authorizationHandle);

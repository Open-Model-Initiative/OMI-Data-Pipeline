import { redirect, fail } from '@sveltejs/kit';
import { ENV } from '$lib/server/env';
import type { Actions } from './$types';

export const actions: Actions = {
  default: async (event) => {
    const formData = await event.request.formData();
    const acceptDCO = formData.get('acceptDCO');

    if (!acceptDCO) {
      return fail(400, { message: 'You must accept the DCO to continue' });
    }

    let response;

    try {
      response = await fetch(`${ENV.API_SERVICE_URL}/users/accept-dco`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Cookie: event.request.headers.get('cookie') || ''
        }
      });
    } catch (error) {
      console.error('Network error accepting DCO:', error);
      return fail(500, { message: 'A network error occurred while processing your request' });
    }

    if (response.ok) {
      throw redirect(302, '/');
    } else {
      const errorData = await response.json();
      return fail(response.status, { message: errorData.message || 'Failed to accept DCO' });
    }
  }
};

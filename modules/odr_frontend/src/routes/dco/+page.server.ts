import { ENV } from '$lib/server/env';
import type { Actions } from './$types';

export const actions: Actions = {
  default: async (event) => {
    const formData = await event.request.formData();
    const acceptDCO = formData.get('acceptDCO');

    if (!acceptDCO) {
      return {
        status: 400,
        body: JSON.stringify({ message: 'You must accept the DCO to continue' })
      };
    }

    try {
      const response = await fetch(`${ENV.API_SERVICE_URL}/users/accept-dco`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Cookie: event.request.headers.get('cookie') || '' // Forward the session cookie
        }
      });

      if (response.ok) {
        return {
          status: 200,
          body: JSON.stringify({ message: 'DCO accepted successfully' })
        };
      } else {
        const errorData = await response.json();
        return {
          status: response.status,
          body: JSON.stringify({ message: errorData.message || 'Failed to accept DCO' })
        };
      }
    } catch (error) {
      console.error('Error accepting DCO:', error);
      return {
        status: 500,
        body: JSON.stringify({ message: 'An error occurred while processing your request' })
      };
    }
  }
};

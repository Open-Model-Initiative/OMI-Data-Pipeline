// SPDX-License-Identifier: Apache-2.0
import { redirect, fail } from '@sveltejs/kit';
import { pgClient } from '$lib/server/pg';
import type { Actions } from './$types';

export const actions: Actions = {
  default: async (event) => {
    const formData = await event.request.formData();
    const acceptDCO = formData.get('acceptDCO');

    if (!acceptDCO) {
      return fail(400, { message: 'You must accept the DCO to continue' });
    }

    let result;

    try {
      const session = await event.locals.auth();

      if (!session || !session.user) {
        return fail(401, { message: 'User not authenticated' });
      }

      const userId = session.user.id;

      if (!userId) {
        return fail(401, { message: 'User ID not found in session' });
      }

      result = await pgClient.query(
        'UPDATE users SET dco_accepted = $1, updated_at = NOW() WHERE id = $2 RETURNING *',
        [true, userId]
      );
    } catch (error) {
      console.error('Error accepting DCO:', error);
      return fail(500, { message: 'An error occurred while processing your request' });
    }

    if (result.rowCount === 1) {
      throw redirect(302, '/');
    } else {
      return fail(404, { message: 'Error accepting DCO: User not found' });
    }
  }
};

import { pgClient } from '$lib/server/pg';
import type { RequestHandler } from '@sveltejs/kit';

export const PUT: RequestHandler = async ({ request }) => {
  const body = await request.json();
  if (!body.userId || body.dcoAccepted === undefined) {
    return new Response(JSON.stringify({ success: false, error: 'Invalid request body' }), { status: 400 });
  }

  const { userId, dcoAccepted } = body;

  try {
    const result = await pgClient.query(
      'UPDATE users SET dco_accepted = $1, updated_at = NOW() WHERE id = $2 RETURNING *',
      [dcoAccepted, userId]
    );

    if (result.rowCount === 1) {
      console.info(`Set user ${userId} DCO acceptance to ${dcoAccepted}`);
      return new Response(JSON.stringify({ success: true, user: result.rows[0] }));
    } else {
      return new Response(JSON.stringify({ success: false, error: 'User not found' }), { status: 404 });
    }
  } catch (e) {
    console.error(`Failed to set user ${userId} DCO acceptance to ${dcoAccepted}`, e);
    return new Response(JSON.stringify({ success: false, error: 'Internal server error' }), { status: 500 });
  }
};

/* SPDX-License-Identifier: Apache-2.0 */
import { db, handleError, jsonHeaders } from '../../db';
import { users } from '../../../../db/schemas/users';
import { eq } from 'drizzle-orm';
import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

/**
 * GET /api/users/:id - Get a single user by ID
 */
export const GET: RequestHandler = async ({ params }) => {
  try {
    const userId = parseInt(params.id);

    if (isNaN(userId)) {
      return new Response(
        JSON.stringify({ error: 'Invalid user ID' }),
        { status: 400, headers: jsonHeaders }
      );
    }

    const user = await db.select().from(users).where(eq(users.id, userId)).limit(1);

    if (!user.length) {
      return new Response(
        JSON.stringify({ error: 'User not found' }),
        { status: 404, headers: jsonHeaders }
      );
    }

    return json(user[0]);
  } catch (error) {
    return handleError(error);
  }
};

/**
 * PUT /api/users/:id - Update a user
 */
export const PUT: RequestHandler = async ({ params, request }) => {
  try {
    const userId = parseInt(params.id);
    const userData = await request.json();

    if (isNaN(userId)) {
      return new Response(
        JSON.stringify({ error: 'Invalid user ID' }),
        { status: 400, headers: jsonHeaders }
      );
    }

    // Check if user exists
    const existingUser = await db.select().from(users).where(eq(users.id, userId)).limit(1);

    if (!existingUser.length) {
      return new Response(
        JSON.stringify({ error: 'User not found' }),
        { status: 404, headers: jsonHeaders }
      );
    }

    // Update user
    const updatedUser = await db.update(users)
      .set({
        email: userData.email,
        name: userData.name,
        isActive: userData.isActive,
        isSuperuser: userData.isSuperuser,
        dcoAccepted: userData.dcoAccepted,
        updatedAt: new Date().toISOString(),
      })
      .where(eq(users.id, userId))
      .returning();

    return json(updatedUser[0]);
  } catch (error) {
    return handleError(error);
  }
};

/**
 * DELETE /api/users/:id - Delete a user
 */
export const DELETE: RequestHandler = async ({ params }) => {
  try {
    const userId = parseInt(params.id);

    if (isNaN(userId)) {
      return new Response(
        JSON.stringify({ error: 'Invalid user ID' }),
        { status: 400, headers: jsonHeaders }
      );
    }

    // Check if user exists
    const existingUser = await db.select().from(users).where(eq(users.id, userId)).limit(1);

    if (!existingUser.length) {
      return new Response(
        JSON.stringify({ error: 'User not found' }),
        { status: 404, headers: jsonHeaders }
      );
    }

    // Delete user
    await db.delete(users).where(eq(users.id, userId));

    return new Response(null, { status: 204 });
  } catch (error) {
    return handleError(error);
  }
};

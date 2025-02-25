/* SPDX-License-Identifier: Apache-2.0 */
import { db, handleError, jsonHeaders } from '../db';
import { users } from '../../../db/schemas/users';
import { eq } from 'drizzle-orm';
import { json } from '@sveltejs/kit';

/**
 * GET /api/users - Retrieve all users with optional filtering
 */
export async function GET({ url }) {
  try {
    const limit = Number(url.searchParams.get('limit') || '50');
    const offset = Number(url.searchParams.get('offset') || '0');
    const email = url.searchParams.get('email');

    let query = db.select().from(users);

    // Apply filters if provided
    if (email) {
      query = query.where(eq(users.email, email));
    }

    // Apply pagination
    query = query.limit(limit).offset(offset);

    const data = await query;
    return json({ data, count: data.length });
  } catch (error) {
    return handleError(error);
  }
}

/**
 * POST /api/users - Create a new user
 */
export async function POST({ request }) {
  try {
    const userData = await request.json();

    // Validate required fields
    if (!userData.email) {
      return new Response(
        JSON.stringify({ error: 'Email is required' }),
        { status: 400, headers: jsonHeaders }
      );
    }

    // Insert new user
    const newUser = await db.insert(users).values({
      email: userData.email,
      hashedPassword: userData.hashedPassword,
      name: userData.name,
      isActive: userData.isActive ?? true,
      isSuperuser: userData.isSuperuser ?? false,
      identityProvider: userData.identityProvider,
      dcoAccepted: userData.dcoAccepted ?? false,
    }).returning();

    return json(newUser[0], { status: 201 });
  } catch (error) {
    return handleError(error);
  }
}

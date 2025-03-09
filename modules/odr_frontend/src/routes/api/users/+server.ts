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

    // Build conditions array
    const conditions = [];
    if (email) {
      conditions.push(eq(users.email, email));
    }

    // Execute query with all conditions at once
    const data = await db.select()
      .from(users)
      .where(conditions.length ? conditions[0] : undefined)
      .limit(limit)
      .offset(offset);

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
      name: userData.name,
      isActive: userData.isActive ?? true,
      isSuperuser: userData.isSuperuser ?? false,
      dcoAccepted: userData.dcoAccepted ?? false,
    }).returning();

    return json(newUser[0], { status: 201 });
  } catch (error) {
    return handleError(error);
  }
}

import { SvelteKitAuth, type Session, type User } from '@auth/sveltekit';
import GitHub from '@auth/sveltekit/providers/github';
import discord from '@auth/sveltekit/providers/discord';
import {
	DISCORD_CLIENT_ID,
	DISCORD_CLIENT_SECRET,
	GITHUB_CLIENT_ID,
	GITHUB_CLIENT_SECRET
} from '$lib/server/env';
import PostgresAdapter from '@auth/pg-adapter';
import pg from 'pg';

const pool = new pg.Pool({
	host: process.env.POSTGRES_HOST,
	user: process.env.POSTGRES_USER,
	password: process.env.POSTGRES_PASSWORD,
	database: process.env.POSTGRES_DB,
	max: 20,
	idleTimeoutMillis: 30000,
	connectionTimeoutMillis: 2000
});

export const { handle, signIn, signOut } = SvelteKitAuth(async (event) => {
	const authOptions = {
		providers: [
			GitHub({
				clientId: GITHUB_CLIENT_ID,
				clientSecret: GITHUB_CLIENT_SECRET
			}),
			discord({
				clientId: DISCORD_CLIENT_ID,
				clientSecret: DISCORD_CLIENT_SECRET
			})
		],
		//@ts-expect-error
		secret: event?.platform?.env.AUTH_SECRET,
		trustHost: true,
		adapter: PostgresAdapter(pool),
		callbacks: {
			session({ session, user }: { session: Session; user: User }) {
				session.user = user;
				return session;
			}
		}
	};
	return authOptions;
});
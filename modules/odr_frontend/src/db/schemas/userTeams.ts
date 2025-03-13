/* SPDX-License-Identifier: Apache-2.0 */
import { pgTable, integer, timestamp, varchar, foreignKey, primaryKey } from 'drizzle-orm/pg-core';
import { teams } from './teams';
import { users } from './users';

export const userTeams = pgTable(
	'user_teams',
	{
		userId: integer('user_id').notNull(),
		teamId: integer('team_id').notNull(),
		role: varchar(),
		createdAt: timestamp('created_at', { withTimezone: true, mode: 'string' }).defaultNow(),
		updatedAt: timestamp('updated_at', { withTimezone: true, mode: 'string' }).defaultNow()
	},
	(table) => [
		foreignKey({
			columns: [table.teamId],
			foreignColumns: [teams.id],
			name: 'user_teams_team_id_fkey'
		}),
		foreignKey({
			columns: [table.userId],
			foreignColumns: [users.id],
			name: 'user_teams_user_id_fkey'
		}),
		primaryKey({ columns: [table.userId, table.teamId], name: 'user_teams_pkey' })
	]
);

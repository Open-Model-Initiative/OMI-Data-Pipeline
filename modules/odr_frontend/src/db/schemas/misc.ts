/* SPDX-License-Identifier: Apache-2.0 */
import {
	pgTable,
	serial,
	varchar,
	boolean,
	timestamp,
	primaryKey,
	unique
} from 'drizzle-orm/pg-core';

export const featureToggles = pgTable(
	'feature_toggles',
	{
		id: serial().primaryKey().notNull(),
		featureName: varchar('feature_name', { length: 255 }).notNull(),
		isEnabled: boolean('is_enabled').notNull(),
		defaultState: boolean('default_state').notNull()
	},
	(table) => [unique('feature_toggles_feature_name_key').on(table.featureName)]
);

export const verificationToken = pgTable(
	'verification_token',
	{
		identifier: varchar().notNull(),
		token: varchar().notNull(),
		expires: timestamp({ withTimezone: true, mode: 'string' }).notNull()
	},
	(table) => [
		primaryKey({ columns: [table.identifier, table.token], name: 'verification_token_pkey' })
	]
);

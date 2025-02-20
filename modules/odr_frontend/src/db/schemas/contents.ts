/* SPDX-License-Identifier: Apache-2.0 */
import {
	pgTable,
	serial,
	varchar,
	timestamp,
	integer,
	json,
	index,
	foreignKey,
	unique,
	primaryKey
} from 'drizzle-orm/pg-core';
import { contentstatus, contenttype, contentsourcetype, reportstatus } from './enums';
import { teams } from './teams';
import { users } from './users';

export const contents = pgTable(
	'contents',
	{
		id: serial().primaryKey().notNull(),
		name: varchar(),
		type: contenttype(),
		hash: varchar(),
		phash: varchar(),
		width: integer(),
		height: integer(),
		format: varchar(),
		size: integer(),
		status: contentstatus(),
		license: varchar(),
		licenseUrl: varchar('license_url'),
		flags: integer(),
		meta: json(),
		fromUserId: integer('from_user_id'),
		fromTeamId: integer('from_team_id'),
		createdAt: timestamp('created_at', { withTimezone: true, mode: 'string' }).defaultNow(),
		updatedAt: timestamp('updated_at', { withTimezone: true, mode: 'string' }),
		url: varchar()
	},
	(table) => [
		index('ix_contents_hash').using('btree', table.hash.asc().nullsLast().op('text_ops')),
		index('ix_contents_id').using('btree', table.id.asc().nullsLast().op('int4_ops')),
		index('ix_contents_phash').using('btree', table.phash.asc().nullsLast().op('text_ops')),
		foreignKey({
			columns: [table.fromTeamId],
			foreignColumns: [teams.id],
			name: 'contents_from_team_id_fkey'
		}),
		foreignKey({
			columns: [table.fromUserId],
			foreignColumns: [users.id],
			name: 'contents_from_user_id_fkey'
		})
	]
);

export const contentAuthors = pgTable(
	'content_authors',
	{
		id: serial().primaryKey().notNull(),
		name: varchar(),
		url: varchar(),
		contentId: integer('content_id'),
		createdAt: timestamp('created_at', { withTimezone: true, mode: 'string' }).defaultNow(),
		updatedAt: timestamp('updated_at', { withTimezone: true, mode: 'string' })
	},
	(table) => [
		index('ix_content_authors_id').using('btree', table.id.asc().nullsLast().op('int4_ops')),
		foreignKey({
			columns: [table.contentId],
			foreignColumns: [contents.id],
			name: 'content_authors_content_id_fkey'
		})
	]
);

export const contentSources = pgTable(
	'content_sources',
	{
		id: serial().primaryKey().notNull(),
		contentId: integer('content_id'),
		type: contentsourcetype(),
		value: varchar(),
		sourceMetadata: varchar('source_metadata'),
		createdAt: timestamp('created_at', { withTimezone: true, mode: 'string' }).defaultNow(),
		updatedAt: timestamp('updated_at', { withTimezone: true, mode: 'string' })
	},
	(table) => [
		index('ix_content_sources_id').using('btree', table.id.asc().nullsLast().op('int4_ops')),
		foreignKey({
			columns: [table.contentId],
			foreignColumns: [contents.id],
			name: 'content_sources_content_id_fkey'
		}),
		unique('content_sources_value_key').on(table.value)
	]
);

export const contentSets = pgTable(
	'content_sets',
	{
		id: serial().primaryKey().notNull(),
		name: varchar().notNull(),
		description: varchar(),
		createdById: integer('created_by_id').notNull(),
		createdAt: timestamp('created_at', { withTimezone: true, mode: 'string' }).defaultNow(),
		updatedAt: timestamp('updated_at', { withTimezone: true, mode: 'string' })
			.defaultNow()
			.notNull()
	},
	(table) => [
		index('ix_content_sets_id').using('btree', table.id.asc().nullsLast().op('int4_ops')),
		foreignKey({
			columns: [table.createdById],
			foreignColumns: [users.id],
			name: 'content_sets_created_by_id_fkey'
		})
	]
);

export const contentEvents = pgTable(
	'content_events',
	{
		id: serial().primaryKey().notNull(),
		contentId: integer('content_id').notNull(),
		status: contentstatus().notNull(),
		setBy: integer('set_by').notNull(),
		note: varchar(),
		createdAt: timestamp('created_at', { withTimezone: true, mode: 'string' }).defaultNow(),
		updatedAt: timestamp('updated_at', { withTimezone: true, mode: 'string' })
	},
	(table) => [
		index('ix_content_events_id').using('btree', table.id.asc().nullsLast().op('int4_ops')),
		foreignKey({
			columns: [table.contentId],
			foreignColumns: [contents.id],
			name: 'content_events_content_id_fkey'
		}),
		foreignKey({
			columns: [table.setBy],
			foreignColumns: [users.id],
			name: 'content_events_set_by_fkey'
		})
	]
);

export const contentReports = pgTable(
	'content_reports',
	{
		id: serial().primaryKey().notNull(),
		contentId: integer('content_id').notNull(),
		reporterId: integer('reporter_id').notNull(),
		reason: varchar().notNull(),
		description: varchar(),
		status: reportstatus(),
		createdAt: timestamp('created_at', { withTimezone: true, mode: 'string' }).defaultNow(),
		updatedAt: timestamp('updated_at', { withTimezone: true, mode: 'string' })
			.defaultNow()
			.notNull()
	},
	(table) => [
		index('ix_content_reports_id').using('btree', table.id.asc().nullsLast().op('int4_ops')),
		foreignKey({
			columns: [table.contentId],
			foreignColumns: [contents.id],
			name: 'content_reports_content_id_fkey'
		}),
		foreignKey({
			columns: [table.reporterId],
			foreignColumns: [users.id],
			name: 'content_reports_reporter_id_fkey'
		})
	]
);

export const contentSetItems = pgTable(
	'content_set_items',
	{
		contentSetId: integer('content_set_id').notNull(),
		contentId: integer('content_id').notNull(),
		addedAt: timestamp('added_at', { withTimezone: true, mode: 'string' }).defaultNow()
	},
	(table) => [
		foreignKey({
			columns: [table.contentId],
			foreignColumns: [contents.id],
			name: 'content_set_items_content_id_fkey'
		}),
		foreignKey({
			columns: [table.contentSetId],
			foreignColumns: [contentSets.id],
			name: 'content_set_items_content_set_id_fkey'
		}),
		// Composite primary key:
		// (Note: using primaryKey helper with an object literal)
		primaryKey({ columns: [table.contentSetId, table.contentId], name: 'content_set_items_pkey' })
	]
);

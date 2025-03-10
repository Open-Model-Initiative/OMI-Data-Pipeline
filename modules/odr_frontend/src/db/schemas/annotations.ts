/* SPDX-License-Identifier: Apache-2.0 */
import {
	pgTable,
	serial,
	varchar,
	timestamp,
	integer,
	json,
	boolean,
	doublePrecision,
	index,
	foreignKey,
	unique,
	vector,
	primaryKey
} from 'drizzle-orm/pg-core';
import { teams } from './teams';
import { users } from './users';
import { contents } from './contents';
import { embeddingEngines } from './embeddings';

export const annotationSources = pgTable(
	'annotation_sources',
	{
		id: serial().primaryKey().notNull(),
		name: varchar(),
		ecosystem: varchar(),
		type: varchar(),
		annotationSchema: json('annotation_schema'),
		license: varchar(),
		licenseUrl: varchar('license_url'),
		addedById: integer('added_by_id'),
		createdAt: timestamp('created_at', { withTimezone: true, mode: 'string' })
			.defaultNow()
			.notNull(),
		updatedAt: timestamp('updated_at', { withTimezone: true, mode: 'string' }).notNull()
	},
	(table) => [
		index('ix_annotation_sources_id').using('btree', table.id.asc().nullsLast().op('int4_ops')),
		index('ix_annotation_sources_name').using('btree', table.name.asc().nullsLast().op('text_ops')),
		foreignKey({
			columns: [table.addedById],
			foreignColumns: [users.id],
			name: 'annotation_sources_added_by_id_fkey'
		})
	]
);

export const annotations = pgTable(
	'annotations',
	{
		id: serial().primaryKey().notNull(),
		contentId: integer('content_id').notNull(),
		annotation: json(),
		manuallyAdjusted: boolean('manually_adjusted'),
		overallRating: doublePrecision('overall_rating'),
		fromUserId: integer('from_user_id'),
		fromTeamId: integer('from_team_id'),
		createdAt: timestamp('created_at', { withTimezone: true, mode: 'string' }).defaultNow(),
		updatedAt: timestamp('updated_at', { withTimezone: true, mode: 'string' })
	},
	(table) => [
		index('ix_annotations_id').using('btree', table.id.asc().nullsLast().op('int4_ops')),
		foreignKey({
			columns: [table.contentId],
			foreignColumns: [contents.id],
			name: 'annotations_content_id_fkey'
		}),
		foreignKey({
			columns: [table.fromTeamId],
			foreignColumns: [teams.id],
			name: 'annotations_from_team_id_fkey'
		}),
		foreignKey({
			columns: [table.fromUserId],
			foreignColumns: [users.id],
			name: 'annotations_from_user_id_fkey'
		})
	]
);

export const annotationEmbeddings = pgTable(
	'annotation_embeddings',
	{
		id: serial().primaryKey().notNull(),
		annotationId: integer('annotation_id'),
		embeddingEngineId: integer('embedding_engine_id'),
		fromUserId: integer('from_user_id'),
		fromTeamId: integer('from_team_id'),
		createdAt: timestamp('created_at', { withTimezone: true, mode: 'string' }).defaultNow(),
		embedding: vector('embedding', { dimensions: 384 })
	},
	(table) => [
		index('ix_annotation_embeddings_id').using('btree', table.id.asc().nullsLast().op('int4_ops')),
		index('embedding_hnsw_idx').using('hnsw', table.embedding.op('vector_cosine_ops')),
		foreignKey({
			columns: [table.annotationId],
			foreignColumns: [annotations.id],
			name: 'annotation_embeddings_annotation_id_fkey'
		}),
		foreignKey({
			columns: [table.embeddingEngineId],
			foreignColumns: [embeddingEngines.id],
			name: 'annotation_embeddings_embedding_engine_id_fkey'
		}),
		foreignKey({
			columns: [table.fromTeamId],
			foreignColumns: [teams.id],
			name: 'annotation_embeddings_from_team_id_fkey'
		}),
		foreignKey({
			columns: [table.fromUserId],
			foreignColumns: [users.id],
			name: 'annotation_embeddings_from_user_id_fkey'
		}),
		unique('ic_annotation_embedding_engine').on(table.annotationId, table.embeddingEngineId)
	]
);

export const annotationRatings = pgTable(
	'annotation_ratings',
	{
		id: serial().primaryKey().notNull(),
		annotationId: integer('annotation_id').notNull(),
		rating: integer().notNull(),
		reason: varchar(),
		ratedById: integer('rated_by_id'),
		createdAt: timestamp('created_at', { withTimezone: true, mode: 'string' })
			.defaultNow()
			.notNull(),
		updatedAt: timestamp('updated_at', { withTimezone: true, mode: 'string' }).notNull()
	},
	(table) => [
		index('ix_annotation_ratings_id').using('btree', table.id.asc().nullsLast().op('int4_ops')),
		foreignKey({
			columns: [table.annotationId],
			foreignColumns: [annotations.id],
			name: 'annotation_ratings_annotation_id_fkey'
		}),
		foreignKey({
			columns: [table.ratedById],
			foreignColumns: [users.id],
			name: 'annotation_ratings_rated_by_id_fkey'
		})
	]
);

export const annotationReports = pgTable(
	'annotation_reports',
	{
		id: serial().primaryKey().notNull(),
		annotationId: integer('annotation_id'),
		type: varchar().notNull(),
		reportedById: integer('reported_by_id'),
		createdAt: timestamp('created_at', { withTimezone: true, mode: 'string' })
			.defaultNow()
			.notNull(),
		updatedAt: timestamp('updated_at', { withTimezone: true, mode: 'string' }).notNull(),
		description: varchar()
	},
	(table) => [
		index('ix_annotation_reports_id').using('btree', table.id.asc().nullsLast().op('int4_ops')),
		foreignKey({
			columns: [table.annotationId],
			foreignColumns: [annotations.id],
			name: 'annotation_reports_annotation_id_fkey'
		}),
		foreignKey({
			columns: [table.reportedById],
			foreignColumns: [users.id],
			name: 'annotation_reports_reported_by_id_fkey'
		})
	]
);

export const annotationSourcesLink = pgTable(
	'annotation_sources_link',
	{
		annotationId: integer('annotation_id').notNull(),
		annotationSourceId: integer('annotation_source_id').notNull()
	},
	(table) => [
		foreignKey({
			columns: [table.annotationId],
			foreignColumns: [annotations.id],
			name: 'annotation_sources_link_annotation_id_fkey'
		}),
		foreignKey({
			columns: [table.annotationSourceId],
			foreignColumns: [annotationSources.id],
			name: 'annotation_sources_link_annotation_source_id_fkey'
		}),
		primaryKey({
			columns: [table.annotationId, table.annotationSourceId],
			name: 'annotation_sources_link_pkey'
		})
	]
);

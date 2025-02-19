/*   SPDX-License-Identifier: Apache-2.0 */
import { pgTable, varchar, index, unique, serial, timestamp, foreignKey, integer, json, boolean, doublePrecision, vector, bigint, primaryKey, pgEnum } from "drizzle-orm/pg-core"
import { sql } from "drizzle-orm"

export const contentsourcetype = pgEnum("contentsourcetype", ['URL', 'PATH', 'HUGGING_FACE'])
export const contentstatus = pgEnum("contentstatus", ['PENDING', 'AVAILABLE', 'UNAVAILABLE', 'DELISTED'])
export const contenttype = pgEnum("contenttype", ['IMAGE', 'VIDEO', 'VOICE', 'MUSIC', 'TEXT'])
export const embeddingenginetype = pgEnum("embeddingenginetype", ['IMAGE', 'VIDEO', 'VOICE', 'MUSIC', 'TEXT'])
export const reportstatus = pgEnum("reportstatus", ['PENDING', 'REVIEWED', 'RESOLVED'])
export const usertype = pgEnum("usertype", ['user', 'bot'])


export const alembicVersion = pgTable("alembic_version", {
	versionNum: varchar("version_num", { length: 32 }).primaryKey().notNull(),
});

export const teams = pgTable("teams", {
	id: serial().primaryKey().notNull(),
	name: varchar(),
	createdAt: timestamp("created_at", { withTimezone: true, mode: 'string' }).defaultNow(),
	updatedAt: timestamp("updated_at", { withTimezone: true, mode: 'string' }).defaultNow(),
}, (table) => [
	index("ix_teams_id").using("btree", table.id.asc().nullsLast().op("int4_ops")),
	index("ix_teams_name").using("btree", table.name.asc().nullsLast().op("text_ops")),
	unique("unique_team_name").on(table.name),
]);

export const contentAuthors = pgTable("content_authors", {
	id: serial().primaryKey().notNull(),
	name: varchar(),
	url: varchar(),
	contentId: integer("content_id"),
	createdAt: timestamp("created_at", { withTimezone: true, mode: 'string' }).defaultNow(),
	updatedAt: timestamp("updated_at", { withTimezone: true, mode: 'string' }),
}, (table) => [
	index("ix_content_authors_id").using("btree", table.id.asc().nullsLast().op("int4_ops")),
	foreignKey({
			columns: [table.contentId],
			foreignColumns: [contents.id],
			name: "content_authors_content_id_fkey"
		}),
]);

export const annotationSources = pgTable("annotation_sources", {
	id: serial().primaryKey().notNull(),
	name: varchar(),
	ecosystem: varchar(),
	type: varchar(),
	annotationSchema: json("annotation_schema"),
	license: varchar(),
	licenseUrl: varchar("license_url"),
	addedById: integer("added_by_id"),
	createdAt: timestamp("created_at", { withTimezone: true, mode: 'string' }).defaultNow().notNull(),
	updatedAt: timestamp("updated_at", { withTimezone: true, mode: 'string' }).notNull(),
}, (table) => [
	index("ix_annotation_sources_id").using("btree", table.id.asc().nullsLast().op("int4_ops")),
	index("ix_annotation_sources_name").using("btree", table.name.asc().nullsLast().op("text_ops")),
	foreignKey({
			columns: [table.addedById],
			foreignColumns: [users.id],
			name: "annotation_sources_added_by_id_fkey"
		}),
]);

export const annotations = pgTable("annotations", {
	id: serial().primaryKey().notNull(),
	contentId: integer("content_id").notNull(),
	annotation: json(),
	manuallyAdjusted: boolean("manually_adjusted"),
	overallRating: doublePrecision("overall_rating"),
	fromUserId: integer("from_user_id"),
	fromTeamId: integer("from_team_id"),
	createdAt: timestamp("created_at", { withTimezone: true, mode: 'string' }).defaultNow(),
	updatedAt: timestamp("updated_at", { withTimezone: true, mode: 'string' }),
}, (table) => [
	index("ix_annotations_id").using("btree", table.id.asc().nullsLast().op("int4_ops")),
	foreignKey({
			columns: [table.contentId],
			foreignColumns: [contents.id],
			name: "annotations_content_id_fkey"
		}),
	foreignKey({
			columns: [table.fromTeamId],
			foreignColumns: [teams.id],
			name: "annotations_from_team_id_fkey"
		}),
	foreignKey({
			columns: [table.fromUserId],
			foreignColumns: [users.id],
			name: "annotations_from_user_id_fkey"
		}),
]);

export const annotationEmbeddings = pgTable("annotation_embeddings", {
	id: serial().primaryKey().notNull(),
	annotationId: integer("annotation_id"),
	embeddingEngineId: integer("embedding_engine_id"),
	fromUserId: integer("from_user_id"),
	fromTeamId: integer("from_team_id"),
	createdAt: timestamp("created_at", { withTimezone: true, mode: 'string' }).defaultNow(),
	embedding: vector("embedding", { dimensions: 384 }),
}, (table) => [
	index("ix_annotation_embeddings_id").using("btree", table.id.asc().nullsLast().op("int4_ops")),
	index("embedding_hnsw_idx").using("hnsw", table.embedding.op("vector_cosine_ops")),
	foreignKey({
			columns: [table.annotationId],
			foreignColumns: [annotations.id],
			name: "annotation_embeddings_annotation_id_fkey"
		}),
	foreignKey({
			columns: [table.embeddingEngineId],
			foreignColumns: [embeddingEngines.id],
			name: "annotation_embeddings_embedding_engine_id_fkey"
		}),
	foreignKey({
			columns: [table.fromTeamId],
			foreignColumns: [teams.id],
			name: "annotation_embeddings_from_team_id_fkey"
		}),
	foreignKey({
			columns: [table.fromUserId],
			foreignColumns: [users.id],
			name: "annotation_embeddings_from_user_id_fkey"
		}),
	unique("ic_annotation_embedding_engine").on(table.annotationId, table.embeddingEngineId),
]);

export const contentEmbeddings = pgTable("content_embeddings", {
	id: serial().primaryKey().notNull(),
	contentId: integer("content_id"),
	embeddingEngineId: integer("embedding_engine_id"),
	fromUserId: integer("from_user_id"),
	fromTeamId: integer("from_team_id"),
	createdAt: timestamp("created_at", { withTimezone: true, mode: 'string' }).defaultNow(),
	embedding: vector("embedding", { dimensions: 512 }),
}, (table) => [
	index("ix_content_embeddings_id").using("btree", table.id.asc().nullsLast().op("int4_ops")),
	index("content_embedding_hnsw_idx").using("hnsw", table.embedding.op("vector_cosine_ops")),
	foreignKey({
			columns: [table.contentId],
			foreignColumns: [contents.id],
			name: "content_embeddings_content_id_fkey"
		}),
	foreignKey({
			columns: [table.embeddingEngineId],
			foreignColumns: [embeddingEngines.id],
			name: "content_embeddings_embedding_engine_id_fkey"
		}),
	foreignKey({
			columns: [table.fromTeamId],
			foreignColumns: [teams.id],
			name: "content_embeddings_from_team_id_fkey"
		}),
	foreignKey({
			columns: [table.fromUserId],
			foreignColumns: [users.id],
			name: "content_embeddings_from_user_id_fkey"
		}),
	unique("ic_content_embedding_engine").on(table.contentId, table.embeddingEngineId),
]);

export const embeddingEngines = pgTable("embedding_engines", {
	id: serial().primaryKey().notNull(),
	name: varchar(),
	description: varchar(),
	version: varchar(),
	createdAt: timestamp("created_at", { withTimezone: true, mode: 'string' }).defaultNow(),
	updatedAt: timestamp("updated_at", { withTimezone: true, mode: 'string' }).notNull(),
	type: embeddingenginetype(),
	supported: boolean(),
}, (table) => [
	index("ix_embedding_engines_id").using("btree", table.id.asc().nullsLast().op("int4_ops")),
	index("ix_embedding_engines_name").using("btree", table.name.asc().nullsLast().op("text_ops")),
	unique("uq_embedding_engine_name").on(table.name),
]);

export const annotationRatings = pgTable("annotation_ratings", {
	id: serial().primaryKey().notNull(),
	annotationId: integer("annotation_id").notNull(),
	rating: integer().notNull(),
	reason: varchar(),
	ratedById: integer("rated_by_id"),
	createdAt: timestamp("created_at", { withTimezone: true, mode: 'string' }).defaultNow().notNull(),
	updatedAt: timestamp("updated_at", { withTimezone: true, mode: 'string' }).notNull(),
}, (table) => [
	index("ix_annotation_ratings_id").using("btree", table.id.asc().nullsLast().op("int4_ops")),
	foreignKey({
			columns: [table.annotationId],
			foreignColumns: [annotations.id],
			name: "annotation_ratings_annotation_id_fkey"
		}),
	foreignKey({
			columns: [table.ratedById],
			foreignColumns: [users.id],
			name: "annotation_ratings_rated_by_id_fkey"
		}),
]);

export const accounts = pgTable("accounts", {
	id: serial().primaryKey().notNull(),
	userId: integer().notNull(),
	type: varchar({ length: 255 }).notNull(),
	provider: varchar({ length: 255 }).notNull(),
	providerAccountId: varchar({ length: 255 }).notNull(),
	refreshToken: varchar("refresh_token"),
	accessToken: varchar("access_token"),
	// You can use { mode: "bigint" } if numbers are exceeding js number limitations
	expiresAt: bigint("expires_at", { mode: "number" }),
	idToken: varchar("id_token"),
	scope: varchar(),
	sessionState: varchar("session_state"),
	tokenType: varchar("token_type"),
});

export const contentSets = pgTable("content_sets", {
	id: serial().primaryKey().notNull(),
	name: varchar().notNull(),
	description: varchar(),
	createdById: integer("created_by_id").notNull(),
	createdAt: timestamp("created_at", { withTimezone: true, mode: 'string' }).defaultNow(),
	updatedAt: timestamp("updated_at", { withTimezone: true, mode: 'string' }).defaultNow().notNull(),
}, (table) => [
	index("ix_content_sets_id").using("btree", table.id.asc().nullsLast().op("int4_ops")),
	foreignKey({
			columns: [table.createdById],
			foreignColumns: [users.id],
			name: "content_sets_created_by_id_fkey"
		}),
]);

export const contentEvents = pgTable("content_events", {
	id: serial().primaryKey().notNull(),
	contentId: integer("content_id").notNull(),
	status: contentstatus().notNull(),
	setBy: integer("set_by").notNull(),
	note: varchar(),
	createdAt: timestamp("created_at", { withTimezone: true, mode: 'string' }).defaultNow(),
	updatedAt: timestamp("updated_at", { withTimezone: true, mode: 'string' }),
}, (table) => [
	index("ix_content_events_id").using("btree", table.id.asc().nullsLast().op("int4_ops")),
	foreignKey({
			columns: [table.contentId],
			foreignColumns: [contents.id],
			name: "content_events_content_id_fkey"
		}),
	foreignKey({
			columns: [table.setBy],
			foreignColumns: [users.id],
			name: "content_events_set_by_fkey"
		}),
]);

export const contentReports = pgTable("content_reports", {
	id: serial().primaryKey().notNull(),
	contentId: integer("content_id").notNull(),
	reporterId: integer("reporter_id").notNull(),
	reason: varchar().notNull(),
	description: varchar(),
	status: reportstatus(),
	createdAt: timestamp("created_at", { withTimezone: true, mode: 'string' }).defaultNow(),
	updatedAt: timestamp("updated_at", { withTimezone: true, mode: 'string' }).defaultNow().notNull(),
}, (table) => [
	index("ix_content_reports_id").using("btree", table.id.asc().nullsLast().op("int4_ops")),
	foreignKey({
			columns: [table.contentId],
			foreignColumns: [contents.id],
			name: "content_reports_content_id_fkey"
		}),
	foreignKey({
			columns: [table.reporterId],
			foreignColumns: [users.id],
			name: "content_reports_reporter_id_fkey"
		}),
]);

export const annotationReports = pgTable("annotation_reports", {
	id: serial().primaryKey().notNull(),
	annotationId: integer("annotation_id"),
	type: varchar().notNull(),
	reportedById: integer("reported_by_id"),
	createdAt: timestamp("created_at", { withTimezone: true, mode: 'string' }).defaultNow().notNull(),
	updatedAt: timestamp("updated_at", { withTimezone: true, mode: 'string' }).notNull(),
	description: varchar(),
}, (table) => [
	index("ix_annotation_reports_id").using("btree", table.id.asc().nullsLast().op("int4_ops")),
	foreignKey({
			columns: [table.annotationId],
			foreignColumns: [annotations.id],
			name: "annotation_reports_annotation_id_fkey"
		}),
	foreignKey({
			columns: [table.reportedById],
			foreignColumns: [users.id],
			name: "annotation_reports_reported_by_id_fkey"
		}),
]);

export const contentSources = pgTable("content_sources", {
	id: serial().primaryKey().notNull(),
	contentId: integer("content_id"),
	type: contentsourcetype(),
	value: varchar(),
	sourceMetadata: varchar("source_metadata"),
	createdAt: timestamp("created_at", { withTimezone: true, mode: 'string' }).defaultNow(),
	updatedAt: timestamp("updated_at", { withTimezone: true, mode: 'string' }),
}, (table) => [
	index("ix_content_sources_id").using("btree", table.id.asc().nullsLast().op("int4_ops")),
	foreignKey({
			columns: [table.contentId],
			foreignColumns: [contents.id],
			name: "content_sources_content_id_fkey"
		}),
	unique("content_sources_value_key").on(table.value),
]);

export const contents = pgTable("contents", {
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
	licenseUrl: varchar("license_url"),
	flags: integer(),
	meta: json(),
	fromUserId: integer("from_user_id"),
	fromTeamId: integer("from_team_id"),
	createdAt: timestamp("created_at", { withTimezone: true, mode: 'string' }).defaultNow(),
	updatedAt: timestamp("updated_at", { withTimezone: true, mode: 'string' }),
	// TODO: failed to parse database type 'bytea'
	url: varchar(),
}, (table) => [
	index("ix_contents_hash").using("btree", table.hash.asc().nullsLast().op("text_ops")),
	index("ix_contents_id").using("btree", table.id.asc().nullsLast().op("int4_ops")),
	index("ix_contents_phash").using("btree", table.phash.asc().nullsLast().op("text_ops")),
	foreignKey({
			columns: [table.fromTeamId],
			foreignColumns: [teams.id],
			name: "contents_from_team_id_fkey"
		}),
	foreignKey({
			columns: [table.fromUserId],
			foreignColumns: [users.id],
			name: "contents_from_user_id_fkey"
		}),
]);

export const sessions = pgTable("sessions", {
	userId: integer().notNull(),
	expires: timestamp({ withTimezone: true, mode: 'string' }).notNull(),
	sessionToken: varchar({ length: 255 }).notNull(),
	id: serial().notNull(),
});

export const users = pgTable("users", {
	id: serial().primaryKey().notNull(),
	email: varchar(),
	hashedPassword: varchar("hashed_password"),
	isActive: boolean("is_active").default(true).notNull(),
	isSuperuser: boolean("is_superuser").default(false).notNull(),
	createdAt: timestamp("created_at", { withTimezone: true, mode: 'string' }).defaultNow(),
	updatedAt: timestamp("updated_at", { withTimezone: true, mode: 'string' }),
	identityProvider: varchar("identity_provider"),
	dcoAccepted: boolean("dco_accepted").default(false).notNull(),
	name: varchar({ length: 255 }),
	emailVerified: timestamp({ withTimezone: true, mode: 'string' }),
	image: varchar(),
}, (table) => [
	index("ix_users_identity_provider").using("btree", table.identityProvider.asc().nullsLast().op("text_ops")),
]);

export const featureToggles = pgTable("feature_toggles", {
	id: serial().primaryKey().notNull(),
	featureName: varchar("feature_name", { length: 255 }).notNull(),
	isEnabled: boolean("is_enabled").notNull(),
	defaultState: boolean("default_state").notNull(),
}, (table) => [
	unique("feature_toggles_feature_name_key").on(table.featureName),
]);

export const annotationSourcesLink = pgTable("annotation_sources_link", {
	annotationId: integer("annotation_id").notNull(),
	annotationSourceId: integer("annotation_source_id").notNull(),
}, (table) => [
	foreignKey({
			columns: [table.annotationId],
			foreignColumns: [annotations.id],
			name: "annotation_sources_link_annotation_id_fkey"
		}),
	foreignKey({
			columns: [table.annotationSourceId],
			foreignColumns: [annotationSources.id],
			name: "annotation_sources_link_annotation_source_id_fkey"
		}),
	primaryKey({ columns: [table.annotationId, table.annotationSourceId], name: "annotation_sources_link_pkey"}),
]);

export const verificationToken = pgTable("verification_token", {
	identifier: varchar().notNull(),
	token: varchar().notNull(),
	expires: timestamp({ withTimezone: true, mode: 'string' }).notNull(),
}, (table) => [
	primaryKey({ columns: [table.identifier, table.token], name: "verification_token_pkey"}),
]);

export const contentSetItems = pgTable("content_set_items", {
	contentSetId: integer("content_set_id").notNull(),
	contentId: integer("content_id").notNull(),
	addedAt: timestamp("added_at", { withTimezone: true, mode: 'string' }).defaultNow(),
}, (table) => [
	foreignKey({
			columns: [table.contentId],
			foreignColumns: [contents.id],
			name: "content_set_items_content_id_fkey"
		}),
	foreignKey({
			columns: [table.contentSetId],
			foreignColumns: [contentSets.id],
			name: "content_set_items_content_set_id_fkey"
		}),
	primaryKey({ columns: [table.contentSetId, table.contentId], name: "content_set_items_pkey"}),
]);

export const userTeams = pgTable("user_teams", {
	userId: integer("user_id").notNull(),
	teamId: integer("team_id").notNull(),
	role: varchar(),
	createdAt: timestamp("created_at", { withTimezone: true, mode: 'string' }).defaultNow(),
	updatedAt: timestamp("updated_at", { withTimezone: true, mode: 'string' }).defaultNow(),
}, (table) => [
	foreignKey({
			columns: [table.teamId],
			foreignColumns: [teams.id],
			name: "user_teams_team_id_fkey"
		}),
	foreignKey({
			columns: [table.userId],
			foreignColumns: [users.id],
			name: "user_teams_user_id_fkey"
		}),
	primaryKey({ columns: [table.userId, table.teamId], name: "user_teams_pkey"}),
]);

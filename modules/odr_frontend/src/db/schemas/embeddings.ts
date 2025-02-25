/* SPDX-License-Identifier: Apache-2.0 */
import { pgTable, serial, varchar, timestamp, boolean, index, unique, integer, vector, foreignKey } from "drizzle-orm/pg-core";
import { embeddingenginetype } from "./enums";
import { teams } from "./teams";
import { users } from "./users";
import { contents } from "./contents"; // used in contentEmbeddings below

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

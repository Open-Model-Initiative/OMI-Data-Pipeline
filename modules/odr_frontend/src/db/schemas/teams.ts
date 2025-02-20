/* SPDX-License-Identifier: Apache-2.0 */
import { pgTable, serial, varchar, timestamp, index, unique } from "drizzle-orm/pg-core";

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

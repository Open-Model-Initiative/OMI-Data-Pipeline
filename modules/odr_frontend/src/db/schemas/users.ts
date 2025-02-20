/* SPDX-License-Identifier: Apache-2.0 */
import { pgTable, serial, varchar, boolean, timestamp, index, integer, bigint } from "drizzle-orm/pg-core";

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

export const sessions = pgTable("sessions", {
  userId: integer().notNull(),
  expires: timestamp({ withTimezone: true, mode: 'string' }).notNull(),
  sessionToken: varchar({ length: 255 }).notNull(),
  id: serial().notNull(),
});

export const accounts = pgTable("accounts", {
  id: serial().primaryKey().notNull(),
  userId: integer().notNull(),
  type: varchar({ length: 255 }).notNull(),
  provider: varchar({ length: 255 }).notNull(),
  providerAccountId: varchar({ length: 255 }).notNull(),
  refreshToken: varchar("refresh_token"),
  accessToken: varchar("access_token"),
  expiresAt: bigint("expires_at", { mode: "number" }),
  idToken: varchar("id_token"),
  scope: varchar(),
  sessionState: varchar("session_state"),
  tokenType: varchar("token_type"),
});

/*   SPDX-License-Identifier: Apache-2.0 */

import { relations } from "drizzle-orm/relations";
import { contents, contentAuthors, users, annotationSources, annotations, teams, annotationEmbeddings, embeddingEngines, contentEmbeddings, annotationRatings, contentSets, contentEvents, contentReports, annotationReports, contentSources, annotationSourcesLink, contentSetItems, userTeams } from "./schema";

export const contentAuthorsRelations = relations(contentAuthors, ({one}) => ({
	content: one(contents, {
		fields: [contentAuthors.contentId],
		references: [contents.id]
	}),
}));

export const contentsRelations = relations(contents, ({one, many}) => ({
	contentAuthors: many(contentAuthors),
	annotations: many(annotations),
	contentEmbeddings: many(contentEmbeddings),
	contentEvents: many(contentEvents),
	contentReports: many(contentReports),
	contentSources: many(contentSources),
	team: one(teams, {
		fields: [contents.fromTeamId],
		references: [teams.id]
	}),
	user: one(users, {
		fields: [contents.fromUserId],
		references: [users.id]
	}),
	contentSetItems: many(contentSetItems),
}));

export const annotationSourcesRelations = relations(annotationSources, ({one, many}) => ({
	user: one(users, {
		fields: [annotationSources.addedById],
		references: [users.id]
	}),
	annotationSourcesLinks: many(annotationSourcesLink),
}));

export const usersRelations = relations(users, ({many}) => ({
	annotationSources: many(annotationSources),
	annotations: many(annotations),
	annotationEmbeddings: many(annotationEmbeddings),
	contentEmbeddings: many(contentEmbeddings),
	annotationRatings: many(annotationRatings),
	contentSets: many(contentSets),
	contentEvents: many(contentEvents),
	contentReports: many(contentReports),
	annotationReports: many(annotationReports),
	contents: many(contents),
	userTeams: many(userTeams),
}));

export const annotationsRelations = relations(annotations, ({one, many}) => ({
	content: one(contents, {
		fields: [annotations.contentId],
		references: [contents.id]
	}),
	team: one(teams, {
		fields: [annotations.fromTeamId],
		references: [teams.id]
	}),
	user: one(users, {
		fields: [annotations.fromUserId],
		references: [users.id]
	}),
	annotationEmbeddings: many(annotationEmbeddings),
	annotationRatings: many(annotationRatings),
	annotationReports: many(annotationReports),
	annotationSourcesLinks: many(annotationSourcesLink),
}));

export const teamsRelations = relations(teams, ({many}) => ({
	annotations: many(annotations),
	annotationEmbeddings: many(annotationEmbeddings),
	contentEmbeddings: many(contentEmbeddings),
	contents: many(contents),
	userTeams: many(userTeams),
}));

export const annotationEmbeddingsRelations = relations(annotationEmbeddings, ({one}) => ({
	annotation: one(annotations, {
		fields: [annotationEmbeddings.annotationId],
		references: [annotations.id]
	}),
	embeddingEngine: one(embeddingEngines, {
		fields: [annotationEmbeddings.embeddingEngineId],
		references: [embeddingEngines.id]
	}),
	team: one(teams, {
		fields: [annotationEmbeddings.fromTeamId],
		references: [teams.id]
	}),
	user: one(users, {
		fields: [annotationEmbeddings.fromUserId],
		references: [users.id]
	}),
}));

export const embeddingEnginesRelations = relations(embeddingEngines, ({many}) => ({
	annotationEmbeddings: many(annotationEmbeddings),
	contentEmbeddings: many(contentEmbeddings),
}));

export const contentEmbeddingsRelations = relations(contentEmbeddings, ({one}) => ({
	content: one(contents, {
		fields: [contentEmbeddings.contentId],
		references: [contents.id]
	}),
	embeddingEngine: one(embeddingEngines, {
		fields: [contentEmbeddings.embeddingEngineId],
		references: [embeddingEngines.id]
	}),
	team: one(teams, {
		fields: [contentEmbeddings.fromTeamId],
		references: [teams.id]
	}),
	user: one(users, {
		fields: [contentEmbeddings.fromUserId],
		references: [users.id]
	}),
}));

export const annotationRatingsRelations = relations(annotationRatings, ({one}) => ({
	annotation: one(annotations, {
		fields: [annotationRatings.annotationId],
		references: [annotations.id]
	}),
	user: one(users, {
		fields: [annotationRatings.ratedById],
		references: [users.id]
	}),
}));

export const contentSetsRelations = relations(contentSets, ({one, many}) => ({
	user: one(users, {
		fields: [contentSets.createdById],
		references: [users.id]
	}),
	contentSetItems: many(contentSetItems),
}));

export const contentEventsRelations = relations(contentEvents, ({one}) => ({
	content: one(contents, {
		fields: [contentEvents.contentId],
		references: [contents.id]
	}),
	user: one(users, {
		fields: [contentEvents.setBy],
		references: [users.id]
	}),
}));

export const contentReportsRelations = relations(contentReports, ({one}) => ({
	content: one(contents, {
		fields: [contentReports.contentId],
		references: [contents.id]
	}),
	user: one(users, {
		fields: [contentReports.reporterId],
		references: [users.id]
	}),
}));

export const annotationReportsRelations = relations(annotationReports, ({one}) => ({
	annotation: one(annotations, {
		fields: [annotationReports.annotationId],
		references: [annotations.id]
	}),
	user: one(users, {
		fields: [annotationReports.reportedById],
		references: [users.id]
	}),
}));

export const contentSourcesRelations = relations(contentSources, ({one}) => ({
	content: one(contents, {
		fields: [contentSources.contentId],
		references: [contents.id]
	}),
}));

export const annotationSourcesLinkRelations = relations(annotationSourcesLink, ({one}) => ({
	annotation: one(annotations, {
		fields: [annotationSourcesLink.annotationId],
		references: [annotations.id]
	}),
	annotationSource: one(annotationSources, {
		fields: [annotationSourcesLink.annotationSourceId],
		references: [annotationSources.id]
	}),
}));

export const contentSetItemsRelations = relations(contentSetItems, ({one}) => ({
	content: one(contents, {
		fields: [contentSetItems.contentId],
		references: [contents.id]
	}),
	contentSet: one(contentSets, {
		fields: [contentSetItems.contentSetId],
		references: [contentSets.id]
	}),
}));

export const userTeamsRelations = relations(userTeams, ({one}) => ({
	team: one(teams, {
		fields: [userTeams.teamId],
		references: [teams.id]
	}),
	user: one(users, {
		fields: [userTeams.userId],
		references: [users.id]
	}),
}));

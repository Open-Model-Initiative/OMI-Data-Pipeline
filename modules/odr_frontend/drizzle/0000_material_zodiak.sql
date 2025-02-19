-- Current sql file was generated after introspecting the database
-- If you want to run this migration please uncomment this code before executing migrations
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TYPE "public"."contentsourcetype" AS ENUM('URL', 'PATH', 'HUGGING_FACE');--> statement-breakpoint
CREATE TYPE "public"."contentstatus" AS ENUM('PENDING', 'AVAILABLE', 'UNAVAILABLE', 'DELISTED');--> statement-breakpoint
CREATE TYPE "public"."contenttype" AS ENUM('IMAGE', 'VIDEO', 'VOICE', 'MUSIC', 'TEXT');--> statement-breakpoint
CREATE TYPE "public"."embeddingenginetype" AS ENUM('IMAGE', 'VIDEO', 'VOICE', 'MUSIC', 'TEXT');--> statement-breakpoint
CREATE TYPE "public"."reportstatus" AS ENUM('PENDING', 'REVIEWED', 'RESOLVED');--> statement-breakpoint
CREATE TYPE "public"."usertype" AS ENUM('user', 'bot');--> statement-breakpoint

--> statement-breakpoint
CREATE TABLE "teams" (
	"id" serial PRIMARY KEY NOT NULL,
	"name" varchar,
	"created_at" timestamp with time zone DEFAULT now(),
	"updated_at" timestamp with time zone DEFAULT now(),
	CONSTRAINT "unique_team_name" UNIQUE("name")
);
--> statement-breakpoint
CREATE TABLE "content_authors" (
	"id" serial PRIMARY KEY NOT NULL,
	"name" varchar,
	"url" varchar,
	"content_id" integer,
	"created_at" timestamp with time zone DEFAULT now(),
	"updated_at" timestamp with time zone
);
--> statement-breakpoint
CREATE TABLE "annotation_sources" (
	"id" serial PRIMARY KEY NOT NULL,
	"name" varchar,
	"ecosystem" varchar,
	"type" varchar,
	"annotation_schema" json,
	"license" varchar,
	"license_url" varchar,
	"added_by_id" integer,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	"updated_at" timestamp with time zone NOT NULL
);
--> statement-breakpoint
CREATE TABLE "annotations" (
	"id" serial PRIMARY KEY NOT NULL,
	"content_id" integer NOT NULL,
	"annotation" json,
	"manually_adjusted" boolean,
	"overall_rating" double precision,
	"from_user_id" integer,
	"from_team_id" integer,
	"created_at" timestamp with time zone DEFAULT now(),
	"updated_at" timestamp with time zone
);
--> statement-breakpoint
CREATE TABLE "annotation_embeddings" (
	"id" serial PRIMARY KEY NOT NULL,
	"annotation_id" integer,
	"embedding_engine_id" integer,
	"from_user_id" integer,
	"from_team_id" integer,
	"created_at" timestamp with time zone DEFAULT now(),
	"embedding" vector(384),
	CONSTRAINT "ic_annotation_embedding_engine" UNIQUE("annotation_id","embedding_engine_id")
);
--> statement-breakpoint
CREATE TABLE "content_embeddings" (
	"id" serial PRIMARY KEY NOT NULL,
	"content_id" integer,
	"embedding_engine_id" integer,
	"from_user_id" integer,
	"from_team_id" integer,
	"created_at" timestamp with time zone DEFAULT now(),
	"embedding" vector(512),
	CONSTRAINT "ic_content_embedding_engine" UNIQUE("content_id","embedding_engine_id")
);
--> statement-breakpoint
CREATE TABLE "embedding_engines" (
	"id" serial PRIMARY KEY NOT NULL,
	"name" varchar,
	"description" varchar,
	"version" varchar,
	"created_at" timestamp with time zone DEFAULT now(),
	"updated_at" timestamp with time zone NOT NULL,
	"type" "embeddingenginetype",
	"supported" boolean,
	CONSTRAINT "uq_embedding_engine_name" UNIQUE("name")
);
--> statement-breakpoint
CREATE TABLE "annotation_ratings" (
	"id" serial PRIMARY KEY NOT NULL,
	"annotation_id" integer NOT NULL,
	"rating" integer NOT NULL,
	"reason" varchar,
	"rated_by_id" integer,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	"updated_at" timestamp with time zone NOT NULL
);
--> statement-breakpoint
CREATE TABLE "accounts" (
	"id" serial PRIMARY KEY NOT NULL,
	"userId" integer NOT NULL,
	"type" varchar(255) NOT NULL,
	"provider" varchar(255) NOT NULL,
	"providerAccountId" varchar(255) NOT NULL,
	"refresh_token" varchar,
	"access_token" varchar,
	"expires_at" bigint,
	"id_token" varchar,
	"scope" varchar,
	"session_state" varchar,
	"token_type" varchar
);
--> statement-breakpoint
CREATE TABLE "content_sets" (
	"id" serial PRIMARY KEY NOT NULL,
	"name" varchar NOT NULL,
	"description" varchar,
	"created_by_id" integer NOT NULL,
	"created_at" timestamp with time zone DEFAULT now(),
	"updated_at" timestamp with time zone DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "content_events" (
	"id" serial PRIMARY KEY NOT NULL,
	"content_id" integer NOT NULL,
	"status" "contentstatus" NOT NULL,
	"set_by" integer NOT NULL,
	"note" varchar,
	"created_at" timestamp with time zone DEFAULT now(),
	"updated_at" timestamp with time zone
);
--> statement-breakpoint
CREATE TABLE "content_reports" (
	"id" serial PRIMARY KEY NOT NULL,
	"content_id" integer NOT NULL,
	"reporter_id" integer NOT NULL,
	"reason" varchar NOT NULL,
	"description" varchar,
	"status" "reportstatus",
	"created_at" timestamp with time zone DEFAULT now(),
	"updated_at" timestamp with time zone DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "annotation_reports" (
	"id" serial PRIMARY KEY NOT NULL,
	"annotation_id" integer,
	"type" varchar NOT NULL,
	"reported_by_id" integer,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	"updated_at" timestamp with time zone NOT NULL,
	"description" varchar
);
--> statement-breakpoint
CREATE TABLE "content_sources" (
	"id" serial PRIMARY KEY NOT NULL,
	"content_id" integer,
	"type" "contentsourcetype",
	"value" varchar,
	"source_metadata" varchar,
	"created_at" timestamp with time zone DEFAULT now(),
	"updated_at" timestamp with time zone,
	CONSTRAINT "content_sources_value_key" UNIQUE("value")
);
--> statement-breakpoint
CREATE TABLE "contents" (
	"id" serial PRIMARY KEY NOT NULL,
	"name" varchar,
	"type" "contenttype",
	"hash" varchar,
	"phash" varchar,
	"width" integer,
	"height" integer,
	"format" varchar,
	"size" integer,
	"status" "contentstatus",
	"license" varchar,
	"license_url" varchar,
	"flags" integer,
	"meta" json,
	"from_user_id" integer,
	"from_team_id" integer,
	"created_at" timestamp with time zone DEFAULT now(),
	"updated_at" timestamp with time zone,
	"url" "bytea"
);
--> statement-breakpoint
CREATE TABLE "sessions" (
	"userId" integer NOT NULL,
	"expires" timestamp with time zone NOT NULL,
	"sessionToken" varchar(255) NOT NULL,
	"id" serial NOT NULL
);
--> statement-breakpoint
CREATE TABLE "users" (
	"id" serial PRIMARY KEY NOT NULL,
	"email" varchar,
	"hashed_password" varchar,
	"is_active" boolean DEFAULT true NOT NULL,
	"is_superuser" boolean DEFAULT false NOT NULL,
	"created_at" timestamp with time zone DEFAULT now(),
	"updated_at" timestamp with time zone,
	"identity_provider" varchar,
	"dco_accepted" boolean DEFAULT false NOT NULL,
	"name" varchar(255),
	"emailVerified" timestamp with time zone,
	"image" varchar
);
--> statement-breakpoint
CREATE TABLE "feature_toggles" (
	"id" serial PRIMARY KEY NOT NULL,
	"feature_name" varchar(255) NOT NULL,
	"is_enabled" boolean NOT NULL,
	"default_state" boolean NOT NULL,
	CONSTRAINT "feature_toggles_feature_name_key" UNIQUE("feature_name")
);
--> statement-breakpoint
CREATE TABLE "annotation_sources_link" (
	"annotation_id" integer NOT NULL,
	"annotation_source_id" integer NOT NULL,
	CONSTRAINT "annotation_sources_link_pkey" PRIMARY KEY("annotation_id","annotation_source_id")
);
--> statement-breakpoint
CREATE TABLE "verification_token" (
	"identifier" varchar NOT NULL,
	"token" varchar NOT NULL,
	"expires" timestamp with time zone NOT NULL,
	CONSTRAINT "verification_token_pkey" PRIMARY KEY("identifier","token")
);
--> statement-breakpoint
CREATE TABLE "content_set_items" (
	"content_set_id" integer NOT NULL,
	"content_id" integer NOT NULL,
	"added_at" timestamp with time zone DEFAULT now(),
	CONSTRAINT "content_set_items_pkey" PRIMARY KEY("content_set_id","content_id")
);
--> statement-breakpoint
CREATE TABLE "user_teams" (
	"user_id" integer NOT NULL,
	"team_id" integer NOT NULL,
	"role" varchar,
	"created_at" timestamp with time zone DEFAULT now(),
	"updated_at" timestamp with time zone DEFAULT now(),
	CONSTRAINT "user_teams_pkey" PRIMARY KEY("user_id","team_id")
);
--> statement-breakpoint
ALTER TABLE "content_authors" ADD CONSTRAINT "content_authors_content_id_fkey" FOREIGN KEY ("content_id") REFERENCES "public"."contents"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "annotation_sources" ADD CONSTRAINT "annotation_sources_added_by_id_fkey" FOREIGN KEY ("added_by_id") REFERENCES "public"."users"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "annotations" ADD CONSTRAINT "annotations_content_id_fkey" FOREIGN KEY ("content_id") REFERENCES "public"."contents"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "annotations" ADD CONSTRAINT "annotations_from_team_id_fkey" FOREIGN KEY ("from_team_id") REFERENCES "public"."teams"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "annotations" ADD CONSTRAINT "annotations_from_user_id_fkey" FOREIGN KEY ("from_user_id") REFERENCES "public"."users"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "annotation_embeddings" ADD CONSTRAINT "annotation_embeddings_annotation_id_fkey" FOREIGN KEY ("annotation_id") REFERENCES "public"."annotations"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "annotation_embeddings" ADD CONSTRAINT "annotation_embeddings_embedding_engine_id_fkey" FOREIGN KEY ("embedding_engine_id") REFERENCES "public"."embedding_engines"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "annotation_embeddings" ADD CONSTRAINT "annotation_embeddings_from_team_id_fkey" FOREIGN KEY ("from_team_id") REFERENCES "public"."teams"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "annotation_embeddings" ADD CONSTRAINT "annotation_embeddings_from_user_id_fkey" FOREIGN KEY ("from_user_id") REFERENCES "public"."users"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "content_embeddings" ADD CONSTRAINT "content_embeddings_content_id_fkey" FOREIGN KEY ("content_id") REFERENCES "public"."contents"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "content_embeddings" ADD CONSTRAINT "content_embeddings_embedding_engine_id_fkey" FOREIGN KEY ("embedding_engine_id") REFERENCES "public"."embedding_engines"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "content_embeddings" ADD CONSTRAINT "content_embeddings_from_team_id_fkey" FOREIGN KEY ("from_team_id") REFERENCES "public"."teams"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "content_embeddings" ADD CONSTRAINT "content_embeddings_from_user_id_fkey" FOREIGN KEY ("from_user_id") REFERENCES "public"."users"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "annotation_ratings" ADD CONSTRAINT "annotation_ratings_annotation_id_fkey" FOREIGN KEY ("annotation_id") REFERENCES "public"."annotations"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "annotation_ratings" ADD CONSTRAINT "annotation_ratings_rated_by_id_fkey" FOREIGN KEY ("rated_by_id") REFERENCES "public"."users"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "content_sets" ADD CONSTRAINT "content_sets_created_by_id_fkey" FOREIGN KEY ("created_by_id") REFERENCES "public"."users"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "content_events" ADD CONSTRAINT "content_events_content_id_fkey" FOREIGN KEY ("content_id") REFERENCES "public"."contents"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "content_events" ADD CONSTRAINT "content_events_set_by_fkey" FOREIGN KEY ("set_by") REFERENCES "public"."users"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "content_reports" ADD CONSTRAINT "content_reports_content_id_fkey" FOREIGN KEY ("content_id") REFERENCES "public"."contents"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "content_reports" ADD CONSTRAINT "content_reports_reporter_id_fkey" FOREIGN KEY ("reporter_id") REFERENCES "public"."users"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "annotation_reports" ADD CONSTRAINT "annotation_reports_annotation_id_fkey" FOREIGN KEY ("annotation_id") REFERENCES "public"."annotations"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "annotation_reports" ADD CONSTRAINT "annotation_reports_reported_by_id_fkey" FOREIGN KEY ("reported_by_id") REFERENCES "public"."users"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "content_sources" ADD CONSTRAINT "content_sources_content_id_fkey" FOREIGN KEY ("content_id") REFERENCES "public"."contents"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "contents" ADD CONSTRAINT "contents_from_team_id_fkey" FOREIGN KEY ("from_team_id") REFERENCES "public"."teams"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "contents" ADD CONSTRAINT "contents_from_user_id_fkey" FOREIGN KEY ("from_user_id") REFERENCES "public"."users"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "annotation_sources_link" ADD CONSTRAINT "annotation_sources_link_annotation_id_fkey" FOREIGN KEY ("annotation_id") REFERENCES "public"."annotations"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "annotation_sources_link" ADD CONSTRAINT "annotation_sources_link_annotation_source_id_fkey" FOREIGN KEY ("annotation_source_id") REFERENCES "public"."annotation_sources"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "content_set_items" ADD CONSTRAINT "content_set_items_content_id_fkey" FOREIGN KEY ("content_id") REFERENCES "public"."contents"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "content_set_items" ADD CONSTRAINT "content_set_items_content_set_id_fkey" FOREIGN KEY ("content_set_id") REFERENCES "public"."content_sets"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "user_teams" ADD CONSTRAINT "user_teams_team_id_fkey" FOREIGN KEY ("team_id") REFERENCES "public"."teams"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "user_teams" ADD CONSTRAINT "user_teams_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."users"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
CREATE INDEX "ix_teams_id" ON "teams" USING btree ("id" int4_ops);--> statement-breakpoint
CREATE INDEX "ix_teams_name" ON "teams" USING btree ("name" text_ops);--> statement-breakpoint
CREATE INDEX "ix_content_authors_id" ON "content_authors" USING btree ("id" int4_ops);--> statement-breakpoint
CREATE INDEX "ix_annotation_sources_id" ON "annotation_sources" USING btree ("id" int4_ops);--> statement-breakpoint
CREATE INDEX "ix_annotation_sources_name" ON "annotation_sources" USING btree ("name" text_ops);--> statement-breakpoint
CREATE INDEX "ix_annotations_id" ON "annotations" USING btree ("id" int4_ops);--> statement-breakpoint
CREATE INDEX "ix_annotation_embeddings_id" ON "annotation_embeddings" USING btree ("id" int4_ops);--> statement-breakpoint
CREATE INDEX "ix_content_embeddings_id" ON "content_embeddings" USING btree ("id" int4_ops);--> statement-breakpoint
CREATE INDEX "ix_embedding_engines_id" ON "embedding_engines" USING btree ("id" int4_ops);--> statement-breakpoint
CREATE INDEX "ix_embedding_engines_name" ON "embedding_engines" USING btree ("name" text_ops);--> statement-breakpoint
CREATE INDEX "ix_annotation_ratings_id" ON "annotation_ratings" USING btree ("id" int4_ops);--> statement-breakpoint
CREATE INDEX "ix_content_sets_id" ON "content_sets" USING btree ("id" int4_ops);--> statement-breakpoint
CREATE INDEX "ix_content_events_id" ON "content_events" USING btree ("id" int4_ops);--> statement-breakpoint
CREATE INDEX "ix_content_reports_id" ON "content_reports" USING btree ("id" int4_ops);--> statement-breakpoint
CREATE INDEX "ix_annotation_reports_id" ON "annotation_reports" USING btree ("id" int4_ops);--> statement-breakpoint
CREATE INDEX "ix_content_sources_id" ON "content_sources" USING btree ("id" int4_ops);--> statement-breakpoint
CREATE INDEX "ix_contents_hash" ON "contents" USING btree ("hash" text_ops);--> statement-breakpoint
CREATE INDEX "ix_contents_id" ON "contents" USING btree ("id" int4_ops);--> statement-breakpoint
CREATE INDEX "ix_contents_phash" ON "contents" USING btree ("phash" text_ops);--> statement-breakpoint
CREATE INDEX "ix_users_identity_provider" ON "users" USING btree ("identity_provider" text_ops);

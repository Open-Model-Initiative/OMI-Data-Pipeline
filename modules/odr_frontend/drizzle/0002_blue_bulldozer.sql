CREATE INDEX "embedding_hnsw_idx" ON "annotation_embeddings" USING hnsw ("embedding" vector_cosine_ops);--> statement-breakpoint
CREATE INDEX "content_embedding_hnsw_idx" ON "content_embeddings" USING hnsw ("embedding" vector_cosine_ops);

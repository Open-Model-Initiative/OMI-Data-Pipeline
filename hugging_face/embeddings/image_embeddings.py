import chromadb
from chromadb.config import Settings
from fastembed import ImageEmbedding
import numpy as np
from typing import List

# Initialize the embedding model (do this outside the function to avoid reinitializing for each image)
model_name = "Qdrant/resnet50-onnx"
cache_path = "cache"


def instantiate_model():
    embedding_model = ImageEmbedding(model_name=model_name, cache_dir=cache_path)
    chroma_client = chromadb.Client(Settings(anonymized_telemetry=False))
    collection = chroma_client.create_collection(name="image_embeddings")
    return embedding_model, model_name, collection


def calculate_image_embedding(model, image) -> np.ndarray:
    embedding_generator = model.embed([image])
    embedding = next(embedding_generator)
    return np.array(embedding)


def is_unique_image(collection, new_embedding: np.ndarray, image_id: str, similarity_threshold: float = 0.5) -> bool:
    results = collection.query(
        query_embeddings=[new_embedding.tolist()],
        n_results=1
    )

    if not results['distances'] or len(results['distances'][0]) == 0:
        # If there are no results (empty collection or no matches), consider the image unique
        collection.add(
            embeddings=[new_embedding.tolist()],
            ids=[image_id]
        )
        return True

    similarity = 1 - results['distances'][0][0]  # ChromaDB uses cosine distance, so we convert to similarity
    if similarity > similarity_threshold:
        return False

    # If the image is unique, add it to the collection
    collection.add(
        embeddings=[new_embedding.tolist()],
        ids=[image_id]
    )
    return True

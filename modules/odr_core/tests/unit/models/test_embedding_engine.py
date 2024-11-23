# SPDX-License-Identifier: Apache-2.0
from odr_core.models.embedding import EmbeddingEngine, ContentEmbedding, AnnotationEmbedding
import pytest
from sqlalchemy.exc import IntegrityError
from odr_core.enums import EmbeddingEngineType
from odr_core.config import settings


def test_embedding_engine_model(db):
    engine = EmbeddingEngine(
        name="Test Engine",
        description="A test embedding engine",
        version="1.0.0",
        type=EmbeddingEngineType.TEXT,
        supported=True
    )
    db.add(engine)
    db.commit()

    assert engine.id is not None
    assert engine.name == "Test Engine"
    assert engine.description == "A test embedding engine"
    assert engine.version == "1.0.0"
    assert engine.type == EmbeddingEngineType.TEXT
    assert engine.supported is True
    assert engine.created_at is not None
    assert engine.updated_at is not None


def test_embedding_engine_unique_name(db):
    engine1 = EmbeddingEngine(
        name="Unique Engine",
        version="1.0.0",
        type=EmbeddingEngineType.TEXT
    )
    db.add(engine1)
    db.commit()

    engine2 = EmbeddingEngine(
        name="Unique Engine",
        version="1.0.1",
        type=EmbeddingEngineType.TEXT
    )
    db.add(engine2)
    with pytest.raises(IntegrityError):
        db.commit()


def test_embedding_engine_relationships(db):
    engine = EmbeddingEngine(
        name="Relationship Test Engine",
        version="1.0.0",
        type=EmbeddingEngineType.TEXT
    )
    db.add(engine)
    db.commit()

    content_test_embedding = [0.1] * settings.CONTENT_EMBEDDING_DIMENSION
    annotation_test_embedding = [0.1] * settings.ANNOTATION_EMBEDDING_DIMENSION

    content_embedding = ContentEmbedding(
        embedding_engine_id=engine.id,
        content_id=1,
        embedding=content_test_embedding
    )
    db.add(content_embedding)

    annotation_embedding = AnnotationEmbedding(
        embedding_engine_id=engine.id,
        annotation_id=1,
        embedding=annotation_test_embedding
    )
    db.add(annotation_embedding)

    db.commit()
    db.refresh(engine)

    assert len(engine.content_embeddings) == 1
    assert len(engine.annotation_embeddings) == 1
    assert engine.content_embeddings[0].id == content_embedding.id
    assert engine.annotation_embeddings[0].id == annotation_embedding.id
    assert len(engine.content_embeddings[0].embedding) == settings.CONTENT_EMBEDDING_DIMENSION
    assert len(engine.annotation_embeddings[0].embedding) == settings.ANNOTATION_EMBEDDING_DIMENSION

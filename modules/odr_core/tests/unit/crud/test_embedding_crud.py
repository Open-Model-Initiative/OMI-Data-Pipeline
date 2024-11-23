# SPDX-License-Identifier: Apache-2.0
import pytest
from sqlalchemy.orm import Session
from odr_core.crud import embedding as embedding_crud
from odr_core.schemas.embedding import (
    EmbeddingEngineCreate,
    EmbeddingEngineUpdate,
    ContentEmbeddingCreate,
    AnnotationEmbeddingCreate,
    EmbeddingVectorQuery
)
from odr_core.models.embedding import EmbeddingEngine, ContentEmbedding, AnnotationEmbedding
from odr_core.enums import EmbeddingEngineType
from odr_core.config import settings
import numpy as np
from PIL import Image
from unittest.mock import patch


def create_test_image():
    image = Image.new('RGB', (100, 100), color='red')
    return image


def test_create_embedding_engine(db: Session):
    engine_data = EmbeddingEngineCreate(
        name="Test Engine",
        description="A test embedding engine",
        version="1.0.0",
        type=EmbeddingEngineType.TEXT,
        supported=True
    )
    created_engine = embedding_crud.create_embedding_engine(db, engine_data)
    assert created_engine.id is not None
    assert created_engine.name == "Test Engine"
    assert created_engine.type == EmbeddingEngineType.TEXT


def test_get_embedding_engine(db: Session):
    engine_data = EmbeddingEngineCreate(
        name="Test Engine",
        description="A test embedding engine",
        version="1.0.0",
        type=EmbeddingEngineType.TEXT,
        supported=True
    )
    created_engine = embedding_crud.create_embedding_engine(db, engine_data)
    retrieved_engine = embedding_crud.get_embedding_engine(db, created_engine.id)
    assert retrieved_engine is not None
    assert retrieved_engine.id == created_engine.id


def test_update_embedding_engine(db: Session):
    engine_data = EmbeddingEngineCreate(
        name="Test Engine",
        description="A test embedding engine",
        version="1.0.0",
        type=EmbeddingEngineType.TEXT,
        supported=True
    )
    created_engine = embedding_crud.create_embedding_engine(db, engine_data)
    update_data = EmbeddingEngineUpdate(
        name="Updated Engine",
        description="An updated test engine",
        version="1.1.0",
        type=EmbeddingEngineType.IMAGE,
        supported=False
    )
    updated_engine = embedding_crud.update_embedding_engine(db, created_engine.id, update_data)
    assert updated_engine.name == "Updated Engine"
    assert updated_engine.type == EmbeddingEngineType.IMAGE


def test_delete_embedding_engine(db: Session):
    engine_data = EmbeddingEngineCreate(
        name="Test Engine",
        description="A test embedding engine",
        version="1.0.0",
        type=EmbeddingEngineType.TEXT,
        supported=True
    )
    created_engine = embedding_crud.create_embedding_engine(db, engine_data)
    delete_result = embedding_crud.delete_embedding_engine(db, created_engine.id)
    assert delete_result is True
    retrieved_engine = embedding_crud.get_embedding_engine(db, created_engine.id)
    assert retrieved_engine is None


@pytest.mark.parametrize("engine_type,text,expected_length", [
    (EmbeddingEngineType.TEXT, "This is a test", settings.ANNOTATION_EMBEDDING_DIMENSION),
])
def test_generate_text_embedding(db: Session, engine_type, text, expected_length):
    engine_data = EmbeddingEngineCreate(
        name="BAAI/bge-small-en-v1.5",
        description="A test embedding engine",
        version="1.0.0",
        type=engine_type,
        supported=True
    )
    created_engine = embedding_crud.create_embedding_engine(db, engine_data)
    embedding = embedding_crud.generate_text_embedding(db, text, created_engine.id)
    assert len(embedding) == expected_length


@pytest.mark.parametrize("engine_type,expected_length", [
    (EmbeddingEngineType.IMAGE, settings.CONTENT_EMBEDDING_DIMENSION),
])
def test_generate_image_embedding(db: Session, engine_type, expected_length):
    engine_data = EmbeddingEngineCreate(
        name="Qdrant/clip-ViT-B-32-vision",
        description="A test embedding engine",
        version="1.0.0",
        type=engine_type,
        supported=True
    )
    created_engine = embedding_crud.create_embedding_engine(db, engine_data)
    test_image = create_test_image()
    embedding = embedding_crud.generate_image_embedding(db, test_image, created_engine.id)
    assert len(embedding) == expected_length


def test_create_content_embedding(db: Session):
    engine_data = EmbeddingEngineCreate(
        name="Test Engine",
        description="A test embedding engine",
        version="1.0.0",
        type=EmbeddingEngineType.IMAGE,
        supported=True
    )
    created_engine = embedding_crud.create_embedding_engine(db, engine_data)
    embedding_data = ContentEmbeddingCreate(
        content_id=1,
        embedding=[0.1] * settings.CONTENT_EMBEDDING_DIMENSION,
        embedding_engine_id=created_engine.id,
        from_user_id=1
    )
    created_embedding = embedding_crud.create_content_embedding(db, embedding_data)
    assert created_embedding.id is not None
    assert created_embedding.content_id == 1
    assert len(created_embedding.embedding) == settings.CONTENT_EMBEDDING_DIMENSION


def test_create_annotation_embedding(db: Session):
    engine_data = EmbeddingEngineCreate(
        name="Test Engine",
        description="A test embedding engine",
        version="1.0.0",
        type=EmbeddingEngineType.TEXT,
        supported=True
    )
    created_engine = embedding_crud.create_embedding_engine(db, engine_data)
    embedding_data = AnnotationEmbeddingCreate(
        annotation_id=1,
        embedding=[0.1] * settings.ANNOTATION_EMBEDDING_DIMENSION,
        embedding_engine_id=created_engine.id,
        from_user_id=1
    )
    created_embedding = embedding_crud.create_annotation_embedding(db, embedding_data)
    assert created_embedding.id is not None
    assert created_embedding.annotation_id == 1
    assert len(created_embedding.embedding) == settings.ANNOTATION_EMBEDDING_DIMENSION


def test_query_content_embedding(db: Session):
    engine_data = EmbeddingEngineCreate(
        name="Test Engine",
        description="A test embedding engine",
        version="1.0.0",
        type=EmbeddingEngineType.IMAGE,
        supported=True
    )
    created_engine = embedding_crud.create_embedding_engine(db, engine_data)
    for i in range(5):
        embedding_data = ContentEmbeddingCreate(
            content_id=i,
            embedding=np.random.rand(settings.CONTENT_EMBEDDING_DIMENSION).tolist(),
            embedding_engine_id=created_engine.id,
            from_user_id=1
        )
        embedding_crud.create_content_embedding(db, embedding_data)

    query = EmbeddingVectorQuery(
        embedding=np.random.rand(settings.CONTENT_EMBEDDING_DIMENSION).tolist(),
        embedding_engine_id=created_engine.id
    )

    with patch('sqlalchemy.orm.Query.order_by') as mock_order_by:
        mock_order_by.return_value = db.query(embedding_crud.ContentEmbedding).filter(
            embedding_crud.ContentEmbedding.embedding_engine_id == query.embedding_engine_id
        )
        results = embedding_crud.query_content_embedding(db, query)
        assert len(results) == 5
        mock_order_by.assert_called_once()


def test_query_annotation_embedding(db: Session):
    engine_data = EmbeddingEngineCreate(
        name="Test Engine",
        description="A test embedding engine",
        version="1.0.0",
        type=EmbeddingEngineType.TEXT,
        supported=True
    )
    created_engine = embedding_crud.create_embedding_engine(db, engine_data)
    for i in range(5):
        embedding_data = AnnotationEmbeddingCreate(
            annotation_id=i,
            embedding=np.random.rand(settings.ANNOTATION_EMBEDDING_DIMENSION).tolist(),
            embedding_engine_id=created_engine.id,
            from_user_id=1
        )
        embedding_crud.create_annotation_embedding(db, embedding_data)

    query = EmbeddingVectorQuery(
        embedding=np.random.rand(settings.ANNOTATION_EMBEDDING_DIMENSION).tolist(),
        embedding_engine_id=created_engine.id
    )

    with patch('sqlalchemy.orm.Query.order_by') as mock_order_by:
        mock_order_by.return_value = db.query(embedding_crud.AnnotationEmbedding).filter(
            embedding_crud.AnnotationEmbedding.embedding_engine_id == query.embedding_engine_id
        )
        results = embedding_crud.query_annotation_embedding(db, query)
        assert len(results) == 5
        mock_order_by.assert_called_once()

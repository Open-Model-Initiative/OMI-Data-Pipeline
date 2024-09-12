import pytest
from sqlalchemy.orm import Session
from odr_core.crud.embedding import (
    create_embedding_engine,
    get_embedding_engine,
    get_embedding_engines,
    update_embedding_engine,
    delete_embedding_engine
)
from odr_core.schemas.embedding import EmbeddingEngineCreate, EmbeddingEngineUpdate
from odr_core.enums import EmbeddingEngineType


def test_create_embedding_engine(db: Session):
    engine_data = EmbeddingEngineCreate(
        name="Test Engine",
        description="A test embedding engine",
        version="1.0.0",
        type=EmbeddingEngineType.TEXT,
        supported=True
    )
    engine = create_embedding_engine(db, engine_data)
    assert engine.id is not None
    assert engine.name == "Test Engine"
    assert engine.description == "A test embedding engine"
    assert engine.version == "1.0.0"
    assert engine.type == EmbeddingEngineType.TEXT
    assert engine.supported is True


def test_get_embedding_engine(db: Session):
    engine_data = EmbeddingEngineCreate(
        name="Get Test Engine",
        version="1.0.0",
        type=EmbeddingEngineType.IMAGE
    )
    created_engine = create_embedding_engine(db, engine_data)
    retrieved_engine = get_embedding_engine(db, embedding_engine_id=created_engine.id)
    assert retrieved_engine is not None
    assert retrieved_engine.id == created_engine.id
    assert retrieved_engine.name == "Get Test Engine"


def test_get_embedding_engines(db: Session):
    for i in range(3):
        engine_data = EmbeddingEngineCreate(
            name=f"Test Engine {i}",
            version=f"1.0.{i}",
            type=EmbeddingEngineType.TEXT
        )
        create_embedding_engine(db, engine_data)

    engines = get_embedding_engines(db)
    assert len(engines) >= 3


def test_update_embedding_engine(db: Session):
    engine_data = EmbeddingEngineCreate(
        name="Update Test Engine",
        version="1.0.0",
        type=EmbeddingEngineType.TEXT
    )
    created_engine = create_embedding_engine(db, engine_data)

    update_data = EmbeddingEngineUpdate(
        name="Updated Engine",
        description="An updated test engine",
        version="1.1.0",
        type=EmbeddingEngineType.IMAGE,
        supported=True
    )
    updated_engine = update_embedding_engine(db, created_engine.id, update_data)
    assert updated_engine.name == "Updated Engine"
    assert updated_engine.description == "An updated test engine"
    assert updated_engine.version == "1.1.0"
    assert updated_engine.type == EmbeddingEngineType.IMAGE
    assert updated_engine.supported is True


def test_delete_embedding_engine(db: Session):
    engine_data = EmbeddingEngineCreate(
        name="Delete Test Engine",
        version="1.0.0",
        type=EmbeddingEngineType.TEXT
    )
    created_engine = create_embedding_engine(db, engine_data)

    delete_result = delete_embedding_engine(db, created_engine.id)
    assert delete_result is True

    deleted_engine = get_embedding_engine(db, created_engine.id)
    assert deleted_engine is None

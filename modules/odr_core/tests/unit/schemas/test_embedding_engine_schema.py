# SPDX-License-Identifier: Apache-2.0
import pytest
from pydantic import ValidationError
from odr_core.schemas.embedding import EmbeddingEngineCreate, EmbeddingEngineUpdate, EmbeddingEngine
from odr_core.enums import EmbeddingEngineType
from datetime import datetime


def test_embedding_engine_create_schema():
    data = {
        "name": "Test Engine",
        "description": "A test embedding engine",
        "version": "1.0.0",
        "type": EmbeddingEngineType.TEXT,
        "supported": True
    }
    engine = EmbeddingEngineCreate(**data)
    assert engine.name == "Test Engine"
    assert engine.description == "A test embedding engine"
    assert engine.version == "1.0.0"
    assert engine.type == EmbeddingEngineType.TEXT
    assert engine.supported is True

    # Test invalid data
    with pytest.raises(ValidationError):
        EmbeddingEngineCreate(name="Invalid", version="1.0", type="INVALID_TYPE")


def test_embedding_engine_update_schema():
    data = {
        "name": "Updated Engine",
        "description": "An updated test embedding engine",
        "version": "1.1.0",
        "type": EmbeddingEngineType.IMAGE,
        "supported": False
    }
    engine = EmbeddingEngineUpdate(**data)
    assert engine.name == "Updated Engine"
    assert engine.description == "An updated test embedding engine"
    assert engine.version == "1.1.0"
    assert engine.type == EmbeddingEngineType.IMAGE
    assert engine.supported is False


def test_embedding_engine_schema():
    data = {
        "id": 1,
        "name": "Test Engine",
        "description": "A test embedding engine",
        "version": "1.0.0",
        "type": EmbeddingEngineType.TEXT,
        "supported": True,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    engine = EmbeddingEngine(**data)
    assert engine.id == 1
    assert engine.name == "Test Engine"
    assert engine.description == "A test embedding engine"
    assert engine.version == "1.0.0"
    assert engine.type == EmbeddingEngineType.TEXT
    assert engine.supported is True
    assert isinstance(engine.created_at, datetime)
    assert isinstance(engine.updated_at, datetime)

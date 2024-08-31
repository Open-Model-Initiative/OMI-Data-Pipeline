import pytest
from pydantic import ValidationError
from odr_core.schemas.content_set import ContentSetCreate, ContentSet, ContentSetWithContents
from datetime import datetime


def test_content_set_create_schema():
    valid_data = {
        "name": "Test Content Set",
        "description": "A test content set",
        "created_by_id": 1
    }
    content_set = ContentSetCreate(**valid_data)
    assert content_set.name == "Test Content Set"
    assert content_set.description == "A test content set"
    assert content_set.created_by_id == 1

    # Test invalid data
    with pytest.raises(ValidationError):
        ContentSetCreate(name=None, created_by_id=1)  # name is required

    with pytest.raises(ValidationError):
        ContentSetCreate(name="Test Set", created_by_id="invalid")  # created_by_id should be an integer


def test_content_set_schema():
    valid_data = {
        "id": 1,
        "name": "Test Content Set",
        "description": "A test content set",
        "created_by_id": 1,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    content_set = ContentSet(**valid_data)
    assert content_set.id == 1
    assert content_set.name == "Test Content Set"
    assert content_set.description == "A test content set"
    assert content_set.created_by_id == 1
    assert isinstance(content_set.created_at, datetime)
    assert isinstance(content_set.updated_at, datetime)

    # Test invalid data
    with pytest.raises(ValidationError):
        ContentSet(id="invalid", name="Test Set", created_by_id=1, created_at=datetime.now(), updated_at=datetime.now())


def test_content_set_with_contents_schema():
    valid_data = {
        "id": 1,
        "name": "Test Content Set",
        "description": "A test content set",
        "created_by_id": 1,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "contents": [1, 2, 3]
    }
    content_set = ContentSetWithContents(**valid_data)
    assert content_set.id == 1
    assert content_set.name == "Test Content Set"
    assert content_set.description == "A test content set"
    assert content_set.created_by_id == 1
    assert isinstance(content_set.created_at, datetime)
    assert isinstance(content_set.updated_at, datetime)
    assert content_set.contents == [1, 2, 3]

    # Test invalid data
    with pytest.raises(ValidationError):
        ContentSetWithContents(id=1, name="Test Set", created_by_id=1, created_at=datetime.now(),
                               updated_at=datetime.now(), contents="invalid")

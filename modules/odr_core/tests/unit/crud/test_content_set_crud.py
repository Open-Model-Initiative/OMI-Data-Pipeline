# SPDX-License-Identifier: Apache-2.0
import pytest
from odr_core.crud.content_set import (
    create_content_set, get_content_set, update_content_set, delete_content_set,
    add_content_to_set, remove_content_from_set, get_contents_in_set
)
from odr_core.schemas.content_set import ContentSetCreate, ContentSetUpdate
from odr_core.models.content import Content, ContentSet


def test_create_content_set(db):
    content_set_data = ContentSetCreate(
        name="Test Content Set",
        description="A test content set",
        created_by_id=1
    )
    content_set = create_content_set(db, content_set_data)
    assert content_set.id is not None
    assert content_set.name == "Test Content Set"
    assert content_set.created_by_id == 1


def test_get_content_set(db):
    content_set_data = ContentSetCreate(
        name="Test Content Set",
        description="A test content set",
        created_by_id=1
    )
    created_set = create_content_set(db, content_set_data)
    retrieved_set = get_content_set(db, content_set_id=created_set.id)
    assert retrieved_set is not None
    assert retrieved_set.id == created_set.id
    assert retrieved_set.name == "Test Content Set"


def test_update_content_set(db):
    content_set_data = ContentSetCreate(
        name="Test Content Set",
        description="A test content set",
        created_by_id=1
    )
    created_set = create_content_set(db, content_set_data)
    update_data = ContentSetUpdate(name="Updated Content Set", description="Updated description")
    updated_set = update_content_set(db, content_set_id=created_set.id, content_set=update_data)
    assert updated_set.name == "Updated Content Set"
    assert updated_set.description == "Updated description"


def test_delete_content_set(db):
    content_set_data = ContentSetCreate(
        name="Test Content Set",
        description="A test content set",
        created_by_id=1
    )
    created_set = create_content_set(db, content_set_data)
    delete_result = delete_content_set(db, content_set_id=created_set.id)
    assert delete_result is True
    deleted_set = get_content_set(db, content_set_id=created_set.id)
    assert deleted_set is None


def test_add_content_to_set(db):
    content_set = create_content_set(db, ContentSetCreate(name="Test Set", created_by_id=1))
    content = Content(name="Test Content", type="IMAGE", hash="test_hash", phash="test_phash",
                      format="jpg", size=1000, license="CC0", from_user_id=1)
    db.add(content)
    db.commit()

    result = add_content_to_set(db, content_set_id=content_set.id, content_id=content.id)
    assert result is True

    contents = get_contents_in_set(db, content_set_id=content_set.id)
    assert len(contents) == 1
    assert contents[0].id == content.id


def test_remove_content_from_set(db):
    content_set = create_content_set(db, ContentSetCreate(name="Test Set", created_by_id=1))
    content = Content(name="Test Content", type="IMAGE", hash="test_hash", phash="test_phash",
                      format="jpg", size=1000, license="CC0", from_user_id=1)
    db.add(content)
    db.commit()

    add_content_to_set(db, content_set_id=content_set.id, content_id=content.id)
    result = remove_content_from_set(db, content_set_id=content_set.id, content_id=content.id)
    assert result is True

    contents = get_contents_in_set(db, content_set_id=content_set.id)
    assert len(contents) == 0


def test_get_contents_in_set(db):
    content_set = create_content_set(db, ContentSetCreate(name="Test Set", created_by_id=1))
    contents = [
        Content(name=f"Test Content {i}", type="IMAGE", hash=f"test_hash_{i}",
                phash=f"test_phash_{i}", format="jpg", size=1000, license="CC0", from_user_id=1)
        for i in range(3)
    ]
    db.add_all(contents)
    db.commit()

    for content in contents:
        add_content_to_set(db, content_set_id=content_set.id, content_id=content.id)

    retrieved_contents = get_contents_in_set(db, content_set_id=content_set.id)
    assert len(retrieved_contents) == 3
    assert all(c.id in [content.id for content in contents] for c in retrieved_contents)


def test_get_contents_in_set_with_pagination(db):
    content_set = create_content_set(db, ContentSetCreate(name="Test Set", created_by_id=1))
    contents = [
        Content(name=f"Test Content {i}", type="IMAGE", hash=f"test_hash_{i}",
                phash=f"test_phash_{i}", format="jpg", size=1000, license="CC0", from_user_id=1)
        for i in range(10)
    ]
    db.add_all(contents)
    db.commit()

    for content in contents:
        add_content_to_set(db, content_set_id=content_set.id, content_id=content.id)

    # Test pagination
    first_page = get_contents_in_set(db, content_set_id=content_set.id, skip=0, limit=5)
    assert len(first_page) == 5

    second_page = get_contents_in_set(db, content_set_id=content_set.id, skip=5, limit=5)
    assert len(second_page) == 5

    assert all(c.id not in [content.id for content in first_page] for c in second_page)

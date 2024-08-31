import pytest
from sqlalchemy.orm import Session
from odr_core.crud.content import (
    create_content,
    get_content,
    get_contents,
    update_content,
    delete_content,
    get_content_by_hash,
    get_contents_by_user,
    create_content_source,
    get_content_sources,
    update_content_source,
    delete_content_source
)
from odr_core.schemas.content import (
    ContentCreate,
    ContentUpdate,
    ContentSourceCreate,
    ContentSourceUpdate,
    ContentType,
    ContentStatus,
    ContentSourceType
)


def test_create_content(db: Session):
    content_data = ContentCreate(
        name="Test Content",
        type=ContentType.IMAGE,
        hash="test_hash",
        phash="test_phash",
        width=100,
        height=100,
        url=["http://example.com/image.jpg"],
        format="jpg",
        size=1024,
        license="CC0",
        sources=[ContentSourceCreate(type=ContentSourceType.URL, value="http://example.com/image.jpg")]
    )
    content = create_content(db, content_data, from_user_id=1)
    assert content.id is not None
    assert content.name == "Test Content"
    print("content.type", content.type)
    assert content.type is ContentType.IMAGE
    assert content.hash == "test_hash"
    assert content.status is ContentStatus.PENDING
    assert len(content.sources) == 1


def test_get_content(db: Session):
    content_data = ContentCreate(
        name="Test Content",
        type=ContentType.IMAGE,
        hash="test_hash",
        phash="test_phash",
        format="jpg",
        size=1024,
        license="CC0",
        sources=[ContentSourceCreate(type=ContentSourceType.URL, value="http://example.com/image.jpg")]
    )
    created_content = create_content(db, content_data, from_user_id=1)
    retrieved_content = get_content(db, content_id=created_content.id)
    assert retrieved_content is not None
    assert retrieved_content.id == created_content.id
    assert retrieved_content.name == "Test Content"


def test_get_contents(db: Session):
    for i in range(5):
        content_data = ContentCreate(
            name=f"Test Content {i}",
            type=ContentType.IMAGE,
            hash=f"test_hash_{i}",
            phash=f"test_phash_{i}",
            format="jpg",
            size=1024,
            license="CC0",
            sources=[ContentSourceCreate(type=ContentSourceType.URL, value=f"http://example.com/image_{i}.jpg")]
        )
        create_content(db, content_data, from_user_id=1)

    contents = get_contents(db)
    assert len(contents) == 5


def test_update_content(db: Session):
    content_data = ContentCreate(
        name="Test Content",
        type=ContentType.IMAGE,
        hash="test_hash",
        phash="test_phash",
        format="jpg",
        size=1024,
        license="CC0",
        sources=[ContentSourceCreate(type=ContentSourceType.URL, value="http://example.com/image.jpg")]
    )
    created_content = create_content(db, content_data, from_user_id=1)

    update_data = ContentUpdate(
        name="Updated Content",
        status=ContentStatus.AVAILABLE
    )
    updated_content = update_content(db, created_content.id, update_data)
    assert updated_content.name == "Updated Content"
    assert updated_content.status == ContentStatus.AVAILABLE


def test_delete_content(db: Session):
    content_data = ContentCreate(
        name="Test Content",
        type=ContentType.IMAGE,
        hash="test_hash",
        phash="test_phash",
        format="jpg",
        size=1024,
        license="CC0",
        sources=[ContentSourceCreate(type=ContentSourceType.URL, value="http://example.com/image.jpg")]
    )
    created_content = create_content(db, content_data, from_user_id=1)

    delete_result = delete_content(db, created_content.id)
    assert delete_result is True

    deleted_content = get_content(db, created_content.id)
    assert deleted_content is None


def test_get_content_by_hash(db: Session):
    content_data = ContentCreate(
        name="Test Content",
        type=ContentType.IMAGE,
        hash="unique_hash",
        phash="test_phash",
        format="jpg",
        size=1024,
        license="CC0",
        sources=[ContentSourceCreate(type=ContentSourceType.URL, value="http://example.com/image.jpg")]
    )
    created_content = create_content(db, content_data, from_user_id=1)

    retrieved_content = get_content_by_hash(db, hash="unique_hash")
    assert retrieved_content is not None
    assert retrieved_content.id == created_content.id


def test_get_contents_by_user(db: Session):
    for i in range(3):
        content_data = ContentCreate(
            name=f"User Content {i}",
            type=ContentType.IMAGE,
            hash=f"user_hash_{i}",
            phash=f"user_phash_{i}",
            format="jpg",
            size=1024,
            license="CC0",
            sources=[ContentSourceCreate(type=ContentSourceType.URL, value=f"http://example.com/user_image_{i}.jpg")]
        )
        create_content(db, content_data, from_user_id=1)

    user_contents = get_contents_by_user(db, user_id=1)
    assert len(user_contents) == 3
    assert all(content.from_user_id == 1 for content in user_contents)


def test_create_content_source(db: Session):
    content_data = ContentCreate(
        name="Test Content",
        type=ContentType.IMAGE,
        hash="test_hash",
        phash="test_phash",
        format="jpg",
        size=1024,
        license="CC0",
        sources=[]
    )
    content = create_content(db, content_data, from_user_id=1)

    source_data = ContentSourceCreate(
        type=ContentSourceType.URL,
        value="http://example.com/new_image.jpg"
    )
    source = create_content_source(db, content.id, source_data)
    assert source.id is not None
    assert source.content_id == content.id
    assert source.type is ContentSourceType.URL
    assert source.value == "http://example.com/new_image.jpg"


def test_get_content_sources(db: Session):
    content_data = ContentCreate(
        name="Test Content",
        type=ContentType.IMAGE,
        hash="test_hash",
        phash="test_phash",
        format="jpg",
        size=1024,
        license="CC0",
        sources=[
            ContentSourceCreate(type=ContentSourceType.URL, value="http://example.com/image1.jpg"),
            ContentSourceCreate(type=ContentSourceType.URL, value="http://example.com/image2.jpg")
        ]
    )
    content = create_content(db, content_data, from_user_id=1)

    sources = get_content_sources(db, content.id)
    assert len(sources) == 2


def test_update_content_source(db: Session):
    content_data = ContentCreate(
        name="Test Content",
        type=ContentType.IMAGE,
        hash="test_hash",
        phash="test_phash",
        format="jpg",
        size=1024,
        license="CC0",
        sources=[ContentSourceCreate(type=ContentSourceType.URL, value="http://example.com/image.jpg")]
    )
    content = create_content(db, content_data, from_user_id=1)

    source_update = ContentSourceUpdate(
        id=content.sources[0].id,
        type=ContentSourceType.PATH,
        value="/path/to/image.jpg"
    )
    updated_source = update_content_source(db, content.sources[0].id, source_update)
    assert updated_source.type is ContentSourceType.PATH
    assert updated_source.value == "/path/to/image.jpg"


def test_delete_content_source(db: Session):
    content_data = ContentCreate(
        name="Test Content",
        type=ContentType.IMAGE,
        hash="test_hash",
        phash="test_phash",
        format="jpg",
        size=1024,
        license="CC0",
        sources=[ContentSourceCreate(type=ContentSourceType.URL, value="http://example.com/image.jpg")]
    )
    content = create_content(db, content_data, from_user_id=1)

    delete_result = delete_content_source(db, content.sources[0].id)
    assert delete_result is True

    sources = get_content_sources(db, content.id)
    assert len(sources) == 0

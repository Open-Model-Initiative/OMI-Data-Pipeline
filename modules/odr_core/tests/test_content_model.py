import pytest
from odr_core.models.content import Content, ContentType, ContentStatus, ContentAuthor
from odr_core.schemas.content import ContentCreate, Content as ContentSchema
from .test_db_manager import TestDBManager

@pytest.fixture(scope="module", autouse=True)
def setup_test_db():
    TestDBManager.setup_test_db()
    yield
    TestDBManager.drop_test_db()

@pytest.fixture(scope="function")
def db():
    session = TestDBManager.get_test_db_session()
    try:
        yield session
    finally:
        TestDBManager.teardown_test_db(session)
        session.close()

def test_create_content(db):
    content_data = ContentCreate(
        name="Test Image",
        type=ContentType.IMAGE,
        hash="abcdef123456",
        phash="123456abcdef",
        url=["http://example.com/image1.jpg", "http://example.com/image1.png"],
        format="png",
        size=1024,
        license="CC0",
        from_user_id=1
    )
    db_content = Content(
        name=content_data.name,
        type=content_data.type,
        hash=content_data.hash,
        phash=content_data.phash,
        url=content_data.url,
        format=content_data.format,
        size=content_data.size,
        license=content_data.license,
        from_user_id=content_data.from_user_id
    )
    db.add(db_content)
    db.commit()
    db.refresh(db_content)

    assert db_content.id is not None
    assert db_content.name == "Test Image"
    assert db_content.type == ContentType.IMAGE
    assert db_content.hash == "abcdef123456"
    assert db_content.status == ContentStatus.PENDING
    assert db_content.from_user_id == 1
    assert len(db_content.url) == 2
    assert "http://example.com/image1.jpg" in db_content.url

def test_content_author_relationship(db):
    content = Content(
        name="Test Image",
        type=ContentType.IMAGE,
        hash="abcdef123456",
        phash="123456abcdef",
        url=["http://example.com/image2.jpg"],
        format="png",
        size=1024,
        license="CC0",
        from_user_id=1
    )
    author = ContentAuthor(name="John Doe", url="http://example.com")
    content.content_authors.append(author)
    
    db.add(content)
    db.commit()
    db.refresh(content)

    assert len(content.content_authors) == 1
    assert content.content_authors[0].name == "John Doe"

def test_content_schema():
    content_data = {
        "id": 1,
        "name": "Test Image",
        "type": "image",
        "hash": "abcdef123456",
        "phash": "123456abcdef",
        "url": ["http://example.com/image3.jpg"],
        "format": "png",
        "size": 1024,
        "status": "pending",
        "license": "CC0",
        "from_user_id": 1,
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00"
    }
    content = ContentSchema(**content_data)
    assert content.id == 1
    assert content.name == "Test Image"
    assert content.type == ContentType.IMAGE
    assert content.hash == "abcdef123456"
    assert content.status == ContentStatus.PENDING
    assert len(content.url) == 1
    assert content.url[0] == "http://example.com/image3.jpg"

if __name__ == "__main__":
    pytest.main([__file__])
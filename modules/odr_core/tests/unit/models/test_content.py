import pytest
from odr_core.models.content import Content, ContentType, ContentStatus, ContentAuthor
from odr_core.schemas.content import ContentCreate, Content as ContentSchema


def test_create_content(db):
    content_data = ContentCreate(
        name="Test Image",
        type=ContentType.IMAGE,
        hash="abcdef123456",
        phash="123456abcdef",
        url=["http://example.com/image1.jpg", "http://example.com/image1.png"],
        sources=[],
        format="png",
        size=1024,
        license="CC0",
    )
    url_list = [str(url) for url in content_data.url]
    db_content = Content(
        name=content_data.name,
        type=content_data.type,
        hash=content_data.hash,
        phash=content_data.phash,
        url=' '.join(url_list),
        format=content_data.format,
        size=content_data.size,
        license=content_data.license,
    )
    db.add(db_content)
    db.commit()
    db.refresh(db_content)

    assert db_content.id is not None
    assert db_content.name == "Test Image"
    assert db_content.type == ContentType.IMAGE
    assert db_content.hash == "abcdef123456"
    assert db_content.status == ContentStatus.PENDING
    assert len(db_content.url.split(' ')) == 2
    assert "http://example.com/image1.jpg" in db_content.url


def test_content_author_relationship(db):
    content = Content(
        name="Test Image",
        type=ContentType.IMAGE,
        hash="abcdef123456",
        phash="123456abcdef",
        url="http://example.com/image2.jpg",
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


if __name__ == "__main__":
    pytest.main([__file__])

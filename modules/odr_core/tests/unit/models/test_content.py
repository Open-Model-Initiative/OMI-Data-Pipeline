from sqlalchemy.exc import IntegrityError
from odr_core.models.content import ContentReport, ContentSet, ContentSetItem, ReportStatus, Content, ContentType, ContentStatus, ContentAuthor
from odr_core.schemas.content import ContentCreate
import pytest


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
    assert db_content.type is ContentType.IMAGE
    assert db_content.hash == "abcdef123456"
    assert db_content.status is ContentStatus.PENDING
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


def test_content_report_model(db):
    content_report = ContentReport(
        content_id=1,
        reporter_id=1,
        reason="Inappropriate content",
        description="This content violates community guidelines.",
        status=ReportStatus.PENDING
    )
    db.add(content_report)
    db.commit()

    assert content_report.id is not None
    assert content_report.content_id == 1
    assert content_report.reporter_id == 1
    assert content_report.reason == "Inappropriate content"
    assert content_report.description == "This content violates community guidelines."
    assert content_report.status == ReportStatus.PENDING
    assert content_report.created_at is not None
    assert content_report.updated_at is not None


def test_content_report_model_constraints(db):
    with pytest.raises(IntegrityError):
        invalid_report = ContentReport(
            content_id=None,
            reporter_id=1,
            reason="Invalid report"
        )
        db.add(invalid_report)
        db.commit()

    db.rollback()

    with pytest.raises(IntegrityError):
        invalid_report = ContentReport(
            content_id=1,
            reporter_id=None,
            reason="Invalid report"
        )
        db.add(invalid_report)
        db.commit()

    db.rollback()


def test_content_set_model(db):
    content_set = ContentSet(
        name="Test Content Set",
        description="A test content set",
        created_by_id=1
    )
    db.add(content_set)
    db.commit()

    assert content_set.id is not None
    assert content_set.name == "Test Content Set"
    assert content_set.description == "A test content set"
    assert content_set.created_by_id == 1
    assert content_set.created_at is not None
    assert content_set.updated_at is not None


def test_content_set_item_model(db):
    content_set = ContentSet(name="Test Content Set", created_by_id=1)
    content = Content(name="Test Content", type="IMAGE", hash="test_hash", phash="test_phash",
                      format="jpg", size=1000, license="CC0", from_user_id=1)
    db.add(content_set)
    db.add(content)
    db.commit()

    content_set_item = ContentSetItem(content_set_id=content_set.id, content_id=content.id)
    db.add(content_set_item)
    db.commit()

    assert content_set_item.content_set_id == content_set.id
    assert content_set_item.content_id == content.id
    assert content_set_item.added_at is not None


def test_content_set_relationships(db):
    content_set = ContentSet(name="Test Content Set", created_by_id=1)
    content1 = Content(name="Test Content 1", type="IMAGE", hash="test_hash1",
                       phash="test_phash1", format="jpg", size=1000, license="CC0", from_user_id=1)
    content2 = Content(name="Test Content 2", type="IMAGE", hash="test_hash2",
                       phash="test_phash2", format="jpg", size=1000, license="CC0", from_user_id=1)

    db.add(content_set)
    db.add(content1)
    db.add(content2)
    db.commit()

    content_set.contents.extend([content1, content2])
    db.commit()

    assert len(content_set.contents) == 2
    assert content1 in content_set.contents
    assert content2 in content_set.contents
    assert content_set in content1.content_sets
    assert content_set in content2.content_sets


if __name__ == "__main__":
    pytest.main([__file__])

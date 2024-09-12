import pytest
from odr_core.models.content import ContentType, ContentStatus
from odr_core.schemas.content import Content as ContentSchema


def test_content_schema():
    content_data = {
        "id": 1,
        "name": "Test Image",
        "type": ContentType.IMAGE,
        "hash": "abcdef123456",
        "phash": "123456abcdef",
        "url": ["http://example.com/image3.jpg"],
        "format": "png",
        "size": 1024,
        "status": ContentStatus.PENDING,
        "license": "CC0",
        "from_user_id": 1,
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00"
    }
    content = ContentSchema(**content_data)
    assert content.id == 1
    assert content.name == "Test Image"
    assert content.type is ContentType.IMAGE
    assert content.hash == "abcdef123456"
    assert content.status is ContentStatus.PENDING
    assert len(content.url) == 1
    assert content.url[0].unicode_string() == "http://example.com/image3.jpg"


if __name__ == "__main__":
    pytest.main([__file__])

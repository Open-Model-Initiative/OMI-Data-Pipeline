from base_integration_test import BaseIntegrationTest, random_string
import json
from odr_api.logger import log_api_request, get_logger
import pytest
from odr_core.models import ContentSource
from odr_core.schemas.content import (
    ContentCreate,
    ContentUpdate,
    Content,
    ContentSourceCreate,
    ContentSourceType,
)

logger = get_logger(__name__)


def create_test_content_data():
    return {
        "name": f"test_content_{random_string()}",
        "type": "image",
        "hash": f"hash_{random_string()}",
        "phash": f"phash_{random_string()}",
        "format": "png",
        "size": 1024,
        "license": "CC0",
        "sources": [
            {
                "type": "path",
                "value": f"./test_assets/omi_logo_{random_string()}.png",
                "source_metadata": {"source": "test"},
            }
        ],
    }


def create_content(client, content_data, user_id):
    response = client.post(f"/content/?from_user_id={user_id}", json=content_data)
    logger.info(f"Response: {response}")
    log_api_request(
        logger,
        "POST",
        "/content/",
        response.status_code,
        content_data,
        response.json(),
    )
    assert (
        response.status_code == 200
    ), f"Failed to create content: {response.status_code}\nResponse body: {response.text}"
    created_content = response.json()
    logger.info(f"Created content: {created_content['id']}")
    return created_content


def get_content(client, content_id):
    response = client.get(f"/content/{content_id}")
    log_api_request(
        logger,
        "GET",
        f"/content/{content_id}",
        response.status_code,
        None,
        response.json(),
    )
    assert response.status_code == 200, f"Failed to get content: {response.status_code}"
    fetched_content = response.json()
    assert fetched_content["id"] == content_id
    logger.info(f"Retrieved content: {content_id}")
    return fetched_content


def update_content(client, content_id, update_data):
    response = client.put(
        f"/content/{content_id}",
        json=update_data
    )
    log_api_request(
        logger,
        "PUT",
        f"/content/{content_id}",
        response.status_code,
        update_data,
        response.json(),
    )
    assert (
        response.status_code == 200
    ), f"Failed to update content: {response.status_code}\nResponse body: {response.text}"
    updated_content = response.json()
    logger.info(f"Updated content: {content_id}")
    return updated_content


def delete_content(client, content_id):
    response = client.delete(f"/content/{content_id}")
    log_api_request(
        logger,
        "DELETE",
        f"/content/{content_id}",
        response.status_code,
        None,
        response.json(),
    )
    assert (
        response.status_code == 200
    ), f"Failed to delete content: {response.status_code}\nResponse body: {response.text}"
    logger.info(f"Deleted content: {content_id}")

    # Verify deletion
    response = client.get(f"/content/{content_id}")
    log_api_request(
        logger,
        "GET",
        f"/content/{content_id}",
        response.status_code,
        None,
        response.text,
    )
    assert (
        response.status_code == 404
    ), f"Failed to verify deletion of content: {response.status_code}\nResponse body: {response.text}"
    logger.info(f"Verified deletion of content: {content_id}")


class TestContentLifecycle(BaseIntegrationTest):
    def __init__(self):
        self.created_content_ids = []

    def setup(self):
        self.created_content_ids = []

    def tearDown(self):
        # Clean up created content
        for content_id in self.created_content_ids:
            try:
                delete_content(self.client, content_id)
            except Exception as e:
                self.logger.warning(f"Failed to delete content {content_id}: {str(e)}")

    def test_create_content(self):
        content_data = create_test_content_data()
        created_content = create_content(
            self.client, content_data, self.test_user.id
        )
        self.created_content_ids.append(created_content["id"])
        return created_content

    def test_get_content(self):
        created_content = self.test_create_content()
        return get_content(
            self.client, created_content["id"]
        )

    def test_update_content(self):
        created_content = self.test_create_content()
        content_id = created_content["id"]
        update_data = {
            "name": f"updated_content_{random_string()}",
            "meta": {"description": "Updated test content"},
            "sources": [
                {
                    "type": "path",
                    "value": f"./test_assets/updated_omi_logo_{random_string()}.png",
                    "source_metadata": {"source": "updated_test"},
                }
            ],
        }
        updated_content = update_content(
            self.client, content_id, update_data
        )
        assert updated_content["name"] == update_data["name"]
        assert (
            updated_content["meta"]["description"] == update_data["meta"]["description"]
        )

    def test_delete_content(self):
        created_content = self.test_create_content()
        delete_content(
            self.client, created_content["id"]
        )
        self.created_content_ids.remove(created_content["id"])

    # TODO: Check why this endpoint returns 307 instead of 400
    # def test_unique_content_source(self):
    #     # Create first content with a specific source
    #     # Ensure that the test database is empty before running this test
    #     content_value = "./test_assets/unique_test_image.png"
    #     self.db.query(ContentSource).filter(
    #         ContentSource.value == content_value
    #     ).delete()
    #     self.db.commit()

    #     content_data_1 = create_test_content_data()
    #     content_data_1["sources"][0]["value"] = content_value
    #     response_1 = self.client.post(
    #         f"/content/?from_user_id={self.test_user.id}", json=content_data_1
    #     )
    #     assert (
    #         response_1.status_code == 200
    #     ), f"Failed to create first content: {response_1.status_code}"
    #     created_content_1 = response_1.json()
    #     self.created_content_ids.append(created_content_1["id"])

    #     # Try to create second content with the same source
    #     content_data_2 = content_data_1.copy()
    #     content_data_2["name"] = f"test_content_{random_string()}"
    #     response_2 = self.client.post(
    #         f"/content?from_user_id={self.test_user.id}", json=content_data_2
    #     )
    #     assert (
    #         response_2.status_code == 400
    #     ), f"Expected 400 status code, got: {response_2.status_code}"
    #     assert (
    #         "already exists" in response_2.json()["detail"].lower()
    #     ), f"Expected 'already exists' in error message, got: {response_2.json()}"


@pytest.fixture(scope="module")
def content_lifecycle_test(request):
    base_url = request.config.getoption("--api-base-url")
    from odr_core.database import SessionLocal

    db = SessionLocal()
    test = TestContentLifecycle()
    TestContentLifecycle.setup_class(base_url, db, test.logger)
    yield test
    TestContentLifecycle.teardown_class()


def test_content_lifecycle(content_lifecycle_test):
    test = content_lifecycle_test
    test.setUp()
    try:
        test.test_create_content()
        test.test_get_content()
        test.test_update_content()
        test.test_delete_content()
        test.test_unique_content_source()
    finally:
        test.tearDown()

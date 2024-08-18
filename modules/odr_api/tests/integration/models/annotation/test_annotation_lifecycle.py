from base_integration_test import BaseIntegrationTest, random_string
from odr_api.logger import log_api_request, get_logger
import pytest
from odr_core.schemas.annotation import AnnotationCreate, AnnotationUpdate, Annotation
from odr_core.schemas.content import ContentCreate
from models.test_content_lifecycle import create_test_content_data, create_content

logger = get_logger(__name__)


def create_test_annotation_data(content_id, user_id):
    return {
        "content_id": content_id,
        "annotation": {"key": "value"},
        "manually_adjusted": False,
        "overall_rating": 7.5,
        "from_user_id": user_id,
        "annotation_source_ids": [],
    }


def create_annotation(client, annotation_data, auth_headers):
    response = client.post("/annotations/", json=annotation_data, headers=auth_headers)
    log_api_request(
        logger,
        "POST",
        "/annotations/",
        response.status_code,
        annotation_data,
        response.json(),
    )
    assert (
        response.status_code == 200
    ), f"Failed to create annotation: {response.status_code}"
    created_annotation = response.json()
    logger.info(f"Created annotation: {created_annotation['id']}")
    return created_annotation


def get_annotation(client, annotation_id, auth_headers):
    response = client.get(f"/annotations/{annotation_id}", headers=auth_headers)
    log_api_request(
        logger,
        "GET",
        f"/annotations/{annotation_id}",
        response.status_code,
        None,
        response.json(),
    )
    assert (
        response.status_code == 200
    ), f"Failed to get annotation: {response.status_code}"
    fetched_annotation = response.json()
    assert fetched_annotation["id"] == annotation_id
    logger.info(f"Retrieved annotation: {annotation_id}")
    return fetched_annotation


def update_annotation(client, annotation_id, update_data, auth_headers):
    response = client.put(
        f"/annotations/{annotation_id}",
        json=update_data,
        headers=auth_headers,
    )
    log_api_request(
        logger,
        "PUT",
        f"/annotations/{annotation_id}",
        response.status_code,
        update_data,
        response.json(),
    )
    assert (
        response.status_code == 200
    ), f"Failed to update annotation: {response.status_code}"
    updated_annotation = response.json()
    logger.info(f"Updated annotation: {annotation_id}")
    return updated_annotation


def delete_annotation(client, annotation_id, auth_headers):
    response = client.delete(f"/annotations/{annotation_id}", headers=auth_headers)
    log_api_request(
        logger,
        "DELETE",
        f"/annotations/{annotation_id}",
        response.status_code,
        None,
        response.json(),
    )
    assert (
        response.status_code == 200
    ), f"Failed to delete annotation: {response.status_code}"
    logger.info(f"Deleted annotation: {annotation_id}")

    # Verify deletion
    response = client.get(f"/annotations/{annotation_id}", headers=auth_headers)
    assert (
        response.status_code == 404
    ), f"Failed to verify deletion of annotation: {response.status_code}"
    logger.info(f"Verified deletion of annotation: {annotation_id}")


def get_annotations_by_content(client, content_id, auth_headers):
    response = client.get(f"/contents/{content_id}/annotations/", headers=auth_headers)
    log_api_request(
        logger,
        "GET",
        f"/contents/{content_id}/annotations/",
        response.status_code,
        None,
        response.json(),
    )
    assert (
        response.status_code == 200
    ), f"Failed to get annotations by content: {response.status_code}"
    annotations = response.json()
    assert len(annotations) > 0, "No annotations found for the content"
    logger.info(f"Retrieved annotations for content: {content_id}")
    return annotations


class TestAnnotationLifecycle(BaseIntegrationTest):
    def create_test_content(self):
        content_data = create_test_content_data()
        return create_content(
            self.client, content_data, self.get_session_auth_headers()
        )

    def test_create_annotation(self):
        content_id = self.create_test_content()["id"]
        annotation_data = create_test_annotation_data(content_id, self.test_user.id)
        return create_annotation(
            self.client, annotation_data, self.get_session_auth_headers()
        )

    def test_get_annotation(self):
        created_annotation = self.test_create_annotation()
        return get_annotation(
            self.client, created_annotation["id"], self.get_session_auth_headers()
        )

    def test_update_annotation(self):
        created_annotation = self.test_create_annotation()
        annotation_id = created_annotation["id"]
        update_data = {
            "annotation": {"updated_key": "updated_value"},
            "manually_adjusted": True,
            "overall_rating": 8.5,
        }
        updated_annotation = update_annotation(
            self.client, annotation_id, update_data, self.get_session_auth_headers()
        )
        assert updated_annotation["annotation"] == update_data["annotation"]
        assert (
            updated_annotation["manually_adjusted"] == update_data["manually_adjusted"]
        )
        assert updated_annotation["overall_rating"] == update_data["overall_rating"]

    def test_delete_annotation(self):
        created_annotation = self.test_create_annotation()
        delete_annotation(
            self.client, created_annotation["id"], self.get_session_auth_headers()
        )

    def test_get_annotations_by_content(self):
        created_annotation = self.test_create_annotation()
        content_id = created_annotation["content_id"]
        annotations = get_annotations_by_content(
            self.client, content_id, self.get_session_auth_headers()
        )
        assert len(annotations) > 0


@pytest.fixture(scope="module")
def annotation_lifecycle_test(request):
    base_url = request.config.getoption("--api-base-url")
    from odr_core.database import SessionLocal

    db = SessionLocal()
    test = TestAnnotationLifecycle()
    TestAnnotationLifecycle.setup_class(base_url, db, test.logger)
    yield test
    TestAnnotationLifecycle.teardown_class()


def test_annotation_lifecycle(annotation_lifecycle_test):
    test = annotation_lifecycle_test
    test.test_create_annotation()
    test.test_get_annotation()
    test.test_update_annotation()
    test.test_get_annotations_by_content()
    test.test_delete_annotation()

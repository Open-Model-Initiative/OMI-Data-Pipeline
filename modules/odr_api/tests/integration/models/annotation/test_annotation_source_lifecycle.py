from base_integration_test import BaseIntegrationTest, random_string
from odr_api.logger import log_api_request, get_logger
import pytest
from odr_core.schemas.annotation import (
    AnnotationSourceCreate,
    AnnotationSourceUpdate,
    AnnotationSource,
    AnnotationSourceType,
)

logger = get_logger(__name__)


class TestAnnotationSourceLifecycle(BaseIntegrationTest):
    def __init__(self):
        self.created_source_ids = []

    def setup(self):
        self.created_source_ids = []

    def tearDown(self):
        # Clean up created annotation sources
        for source_id in self.created_source_ids:
            try:
                self.client.delete(
                    f"/annotation_sources/{source_id}"
                )
            except Exception as e:
                self.logger.warning(
                    f"Failed to delete annotation source {source_id}: {str(e)}"
                )

    def test_create_annotation_source(self):
        annotation_source_data = {
            "name": f"test_source_{random_string()}",
            "ecosystem": "test_ecosystem",
            "type": AnnotationSourceType.CONTENT_DESCRIPTION.value,
            "annotation_schema": {"key": "value"},
            "license": "CC0",
            "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
            "added_by_id": self.test_user.id,
        }
        response = self.client.post(
            "/annotation_sources/",
            json=annotation_source_data
        )
        log_api_request(
            self.logger,
            "POST",
            "/annotation_sources/",
            response.status_code,
            annotation_source_data,
            response.json(),
        )
        assert (
            response.status_code == 200
        ), f"Failed to create annotation source: {response.status_code}"
        created_source = response.json()
        self.created_source_ids.append(created_source["id"])
        self.logger.info(f"Created annotation source: {created_source['id']}")
        return created_source

    def test_get_annotation_source(self):
        created_source = self.test_create_annotation_source()
        source_id = created_source["id"]
        response = self.client.get(
            f"/annotation_sources/{source_id}"
        )
        log_api_request(
            self.logger,
            "GET",
            f"/annotation_sources/{source_id}",
            response.status_code,
            None,
            response.json(),
        )
        assert (
            response.status_code == 200
        ), f"Failed to get annotation source: {response.status_code}"
        fetched_source = response.json()
        assert fetched_source["id"] == source_id
        self.logger.info(f"Retrieved annotation source: {source_id}")

    def test_update_annotation_source(self):
        created_source = self.test_create_annotation_source()
        source_id = created_source["id"]
        update_data = {
            "name": f"updated_source_{random_string()}",
            "ecosystem": "updated_ecosystem",
            "type": AnnotationSourceType.SPATIAL_ANALYSIS.value,
            "annotation_schema": {"updated_key": "updated_value"},
            "license": "MIT",
            "license_url": "https://opensource.org/licenses/MIT",
        }
        response = self.client.put(
            f"/annotation_sources/{source_id}",
            json=update_data
        )
        log_api_request(
            self.logger,
            "PUT",
            f"/annotation_sources/{source_id}",
            response.status_code,
            update_data,
            response.json(),
        )
        assert (
            response.status_code == 200
        ), f"Failed to update annotation source: {response.status_code}"
        updated_source = response.json()
        assert updated_source["name"] == update_data["name"]
        assert updated_source["ecosystem"] == update_data["ecosystem"]
        assert updated_source["type"] == update_data["type"]
        assert updated_source["annotation_schema"] == update_data["annotation_schema"]
        assert updated_source["license"] == update_data["license"]
        assert updated_source["license_url"] == update_data["license_url"]
        self.logger.info(f"Updated annotation source: {source_id}")

    def test_delete_annotation_source(self):
        created_source = self.test_create_annotation_source()
        source_id = created_source["id"]
        response = self.client.delete(
            f"/annotation_sources/{source_id}"
        )
        log_api_request(
            self.logger,
            "DELETE",
            f"/annotation_sources/{source_id}",
            response.status_code,
            None,
            response.json(),
        )
        assert (
            response.status_code == 200
        ), f"Failed to delete annotation source: {response.status_code}"
        self.logger.info(f"Deleted annotation source: {source_id}")
        self.created_source_ids.remove(source_id)

        # Verify deletion
        response = self.client.get(
            f"/annotation_sources/{source_id}"
        )
        assert (
            response.status_code == 404
        ), f"Failed to verify deletion of annotation source: {response.status_code}"
        self.logger.info(f"Verified deletion of annotation source: {source_id}")

    def test_list_annotation_sources(self):
        # Create a few annotation sources
        for _ in range(3):
            self.test_create_annotation_source()

        response = self.client.get(
            "/annotation_sources/"
        )
        log_api_request(
            self.logger,
            "GET",
            "/annotation_sources/",
            response.status_code,
            None,
            response.json(),
        )
        assert (
            response.status_code == 200
        ), f"Failed to list annotation sources: {response.status_code}"
        sources = response.json()
        assert len(sources) >= 3, "Expected at least 3 annotation sources"
        self.logger.info(f"Retrieved {len(sources)} annotation sources")


@pytest.fixture(scope="module")
def annotation_source_lifecycle_test(request):
    base_url = request.config.getoption("--api-base-url")
    from odr_core.database import SessionLocal

    db = SessionLocal()
    test = TestAnnotationSourceLifecycle()
    TestAnnotationSourceLifecycle.setup_class(base_url, db, test.logger)
    yield test
    TestAnnotationSourceLifecycle.teardown_class()


def test_annotation_source_lifecycle(annotation_source_lifecycle_test):
    test = annotation_source_lifecycle_test
    test.setUp()
    try:
        test.test_create_annotation_source()
        test.test_get_annotation_source()
        test.test_update_annotation_source()
        test.test_list_annotation_sources()
        test.test_delete_annotation_source()
    finally:
        test.tearDown()

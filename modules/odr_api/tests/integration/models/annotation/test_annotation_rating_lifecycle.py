from base_integration_test import BaseIntegrationTest, random_string
from odr_api.logger import log_api_request, get_logger
import pytest
from odr_core.schemas.annotation import (
    AnnotationRatingCreate,
    AnnotationRatingUpdate,
    AnnotationRating,
)
from models.test_content_lifecycle import create_test_content_data, create_content
from models.annotation.test_annotation_lifecycle import (
    create_test_annotation_data,
    create_annotation,
)
import random

logger = get_logger(__name__)


def create_test_annotation_rating_data(annotation_id, user_id):
    return {
        "annotation_id": annotation_id,
        "rated_by_id": user_id,
        "rating": random.randint(1, 10),
        "reason": f"Test rating {random_string()}",
    }


def create_annotation_rating(client, rating_data, auth_headers):
    response = client.post(
        "/annotation_ratings/", json=rating_data, headers=auth_headers
    )
    log_api_request(
        logger,
        "POST",
        "/annotation_ratings/",
        response.status_code,
        rating_data,
        response.json(),
    )
    assert (
        response.status_code == 200
    ), f"Failed to create annotation rating: {response.status_code}"
    created_rating = response.json()
    logger.info(f"Created annotation rating: {created_rating['id']}")
    return created_rating


def get_annotation_rating(client, rating_id, auth_headers):
    response = client.get(f"/annotation_ratings/{rating_id}", headers=auth_headers)
    log_api_request(
        logger,
        "GET",
        f"/annotation_ratings/{rating_id}",
        response.status_code,
        None,
        response.json(),
    )
    assert (
        response.status_code == 200
    ), f"Failed to get annotation rating: {response.status_code}"
    fetched_rating = response.json()
    assert fetched_rating["id"] == rating_id
    logger.info(f"Retrieved annotation rating: {rating_id}")
    return fetched_rating


def update_annotation_rating(client, rating_id, update_data, auth_headers):
    response = client.put(
        f"/annotation_ratings/{rating_id}",
        json=update_data,
        headers=auth_headers,
    )
    log_api_request(
        logger,
        "PUT",
        f"/annotation_ratings/{rating_id}",
        response.status_code,
        update_data,
        response.json(),
    )
    assert (
        response.status_code == 200
    ), f"Failed to update annotation rating: {response.status_code}"
    updated_rating = response.json()
    logger.info(f"Updated annotation rating: {rating_id}")
    return updated_rating


def delete_annotation_rating(client, rating_id, auth_headers):
    response = client.delete(f"/annotation_ratings/{rating_id}", headers=auth_headers)
    log_api_request(
        logger,
        "DELETE",
        f"/annotation_ratings/{rating_id}",
        response.status_code,
        None,
        response.json(),
    )
    assert (
        response.status_code == 200
    ), f"Failed to delete annotation rating: {response.status_code}"
    logger.info(f"Deleted annotation rating: {rating_id}")

    # Verify deletion
    response = client.get(f"/annotation_ratings/{rating_id}", headers=auth_headers)
    assert (
        response.status_code == 404
    ), f"Failed to verify deletion of annotation rating: {response.status_code}"
    logger.info(f"Verified deletion of annotation rating: {rating_id}")


def get_annotation_ratings(client, annotation_id, auth_headers):
    response = client.get(f"/annotations/{annotation_id}/ratings", headers=auth_headers)
    log_api_request(
        logger,
        "GET",
        f"/annotations/{annotation_id}/ratings",
        response.status_code,
        None,
        response.json(),
    )
    assert (
        response.status_code == 200
    ), f"Failed to list annotation ratings: {response.status_code}"
    ratings = response.json()
    logger.info(
        f"Retrieved {len(ratings)} annotation ratings for annotation {annotation_id}"
    )
    return ratings


class TestAnnotationRatingLifecycle(BaseIntegrationTest):
    def create_test_content(self):
        content_data = create_test_content_data()
        return create_content(
            self.client, content_data, self.get_session_auth_headers()
        )

    def create_test_annotation(self):
        content_id = self.create_test_content()["id"]
        annotation_data = create_test_annotation_data(content_id, self.test_user.id)
        return create_annotation(
            self.client, annotation_data, self.get_session_auth_headers()
        )

    def test_create_annotation_rating(self):
        annotation_id = self.create_test_annotation()["id"]
        rating_data = create_test_annotation_rating_data(
            annotation_id, self.test_user.id
        )
        return create_annotation_rating(
            self.client, rating_data, self.get_session_auth_headers()
        )

    def test_get_annotation_rating(self):
        created_rating = self.test_create_annotation_rating()
        return get_annotation_rating(
            self.client, created_rating["id"], self.get_session_auth_headers()
        )

    def test_update_annotation_rating(self):
        created_rating = self.test_create_annotation_rating()
        rating_id = created_rating["id"]
        update_data = {"rating": 9, "reason": "Updated: Very good annotation"}
        updated_rating = update_annotation_rating(
            self.client, rating_id, update_data, self.get_session_auth_headers()
        )
        assert updated_rating["rating"] == update_data["rating"]
        assert updated_rating["reason"] == update_data["reason"]

    def test_delete_annotation_rating(self):
        created_rating = self.test_create_annotation_rating()
        delete_annotation_rating(
            self.client, created_rating["id"], self.get_session_auth_headers()
        )

    def test_list_annotation_ratings(self):
        annotation_id = self.create_test_annotation()["id"]
        # Create a few annotation ratings
        for _ in range(3):
            rating_data = create_test_annotation_rating_data(
                annotation_id, self.test_user.id
            )
            create_annotation_rating(
                self.client, rating_data, self.get_session_auth_headers()
            )

        ratings = get_annotation_ratings(
            self.client, annotation_id, self.get_session_auth_headers()
        )
        assert len(ratings) >= 3, "Expected at least 3 annotation ratings"
        self.logger.info(
            f"Retrieved {len(ratings)} annotation ratings for annotation {annotation_id}"
        )


@pytest.fixture(scope="module")
def annotation_rating_lifecycle_test(request):
    base_url = request.config.getoption("--api-base-url")
    from odr_core.database import SessionLocal

    db = SessionLocal()
    test = TestAnnotationRatingLifecycle()
    TestAnnotationRatingLifecycle.setup_class(base_url, db, test.logger)
    yield test
    TestAnnotationRatingLifecycle.teardown_class()


def test_annotation_rating_lifecycle(annotation_rating_lifecycle_test):
    test = annotation_rating_lifecycle_test
    test.test_create_annotation_rating()
    test.test_get_annotation_rating()
    test.test_update_annotation_rating()
    test.test_list_annotation_ratings()
    test.test_delete_annotation_rating()

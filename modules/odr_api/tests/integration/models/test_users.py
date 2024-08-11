from base_integration_test import BaseIntegrationTest, random_string
import json
from odr_api.logger import log_api_request, get_logger
import pytest

logger = get_logger(__name__)


class TestUserLifecycle(BaseIntegrationTest):
    def test_create_user(self):
        user_data = {
            "username": f"testuser_{random_string()}",
            "email": f"testuser_{random_string()}@example.com",
            "password": "testpassword123",
            "is_active": True,
            "is_superuser": False,
        }
        response = self.client.post("/users/", json=user_data)
        log_api_request(
            self.logger,
            "POST",
            "/users/",
            response.status_code,
            user_data,
            response.json(),
        )
        assert (
            response.status_code == 200
        ), f"Failed to create user: {response.status_code}"
        created_user = response.json()
        self.logger.info(f"Created user: {created_user['id']}")
        return created_user

    def test_user_login_session(self):
        headers = self.get_session_auth_headers()
        response = self.client.get("/users/me", headers=headers)
        log_api_request(
            self.logger, "GET", "/users/me", response.status_code, None, response.json()
        )
        assert (
            response.status_code == 200
        ), f"Failed to access authenticated endpoint: {response.status_code}"
        assert response.json()["id"] == self.test_user.id
        self.logger.info("Session authentication successful")

    def test_user_basic_auth(self):
        auth = self.get_basic_auth_headers()
        logger.info(f"Test user auth: {auth}")
        logger.info(f"Auth token type: {type(auth)}")
        response = self.client.get("/users/me", auth=auth)
        log_api_request(
            self.logger, "GET", "/users/me", response.status_code, None, response.json()
        )
        assert (
            response.status_code == 200
        ), f"Failed to access authenticated endpoint: {response.status_code}"
        assert response.json()["id"] == self.test_user.id
        self.logger.info("Basic authentication successful")

    def test_bot_jwt_auth(self):
        auth_credentials = self.get_jwt_auth_headers()
        logger.info(f"Auth type : {type(auth_credentials)}")
        logger.info(f"Bot user auth credentials {auth_credentials}")
        headers = {
            "Authorization": f"{auth_credentials.scheme} {auth_credentials.credentials}"
        }
        try:
            response = self.client.get("/users/me", headers=headers)
            response_data = response.json() if response.text else {}
        except json.JSONDecodeError:
            response_data = {"error": "Invalid JSON response", "text": response.text}

        log_api_request(
            self.logger, "GET", "/users/me", response.status_code, None, response_data
        )
        assert (
            response.status_code == 200
        ), f"Failed to access authenticated endpoint: {response.status_code}"
        assert response_data.get("id") == self.bot_user.id
        self.logger.info("JWT authentication successful")

    def test_update_user(self):
        headers = self.get_session_auth_headers()
        update_data = {
            "username": f"updated_user_{random_string()}",
            "email": f"updated_user_{random_string()}@example.com",
            "is_active": True,
            "is_superuser": False,
        }
        response = self.client.put(
            f"/users/{self.test_user.id}", json=update_data, headers=headers
        )
        log_api_request(
            self.logger,
            "PUT",
            f"/users/{self.test_user.id}",
            response.status_code,
            update_data,
            response.json(),
        )
        assert (
            response.status_code == 200
        ), f"Failed to update user: {response.status_code}"
        updated_user = response.json()
        for key, value in update_data.items():
            assert updated_user[key] == value
        self.logger.info(f"Updated user: {self.test_user.id}")

    def test_user_logout(self):
        headers = self.get_session_auth_headers()
        response = self.client.post("/users/logout", headers=headers)
        log_api_request(
            self.logger,
            "POST",
            "/users/logout",
            response.status_code,
            None,
            response.json(),
        )
        assert (
            response.status_code == 200
        ), f"Failed to logout user: {response.status_code}"
        self.logger.info("User logout successful")

    def test_delete_user(self):
        # Create a user to delete
        created_user = self.test_create_user()
        user_id = created_user["id"]

        # Delete user (using superuser authentication)
        headers = self.get_superuser_auth_headers()
        response = self.client.delete(f"/users/{user_id}", headers=headers)
        log_api_request(
            self.logger,
            "DELETE",
            f"/users/{user_id}",
            response.status_code,
            None,
            response.json(),
        )
        assert (
            response.status_code == 200
        ), f"Failed to delete user: {response.status_code}"
        assert response.json() == {"message": "User deleted successfully"}
        self.logger.info(f"Deleted user: {user_id}")

        # Verify deletion
        response = self.client.get(f"/users/{user_id}", headers=headers)
        log_api_request(
            self.logger,
            "GET",
            f"/users/{user_id}",
            response.status_code,
            None,
            response.text,
        )
        assert (
            response.status_code == 404
        ), f"Failed to verify deletion of user: {response.status_code}"
        self.logger.info(f"Verified deletion of user: {user_id}")

    def test_superuser_auth(self):
        headers = self.get_superuser_auth_headers()
        response = self.client.get("/users/me", headers=headers)
        log_api_request(
            self.logger,
            "GET",
            "/users/me",
            response.status_code,
            None,
            response.json(),
        )
        assert (
            response.status_code == 200
        ), f"Failed to access authenticated endpoint as superuser: {response.status_code}"
        user_data = response.json()
        assert user_data["is_superuser"], "User is not a superuser"
        self.logger.info("Superuser authentication successful")


@pytest.fixture(scope="module")
def user_lifecycle_test(request):
    base_url = request.config.getoption("--api-base-url")
    from odr_core.database import SessionLocal

    db = SessionLocal()
    test = TestUserLifecycle()
    TestUserLifecycle.setup_class(base_url, db, test.logger)
    test.logger.info(f"Test user: {test.test_user}")
    test.logger.info(f"Bot user: {test.bot_user}")
    yield test
    TestUserLifecycle.teardown_class()


def test_user_lifecycle(user_lifecycle_test):
    test = user_lifecycle_test
    test.test_create_user()
    test.test_user_login_session()
    test.test_user_basic_auth()
    test.test_bot_jwt_auth()
    test.test_update_user()
    test.test_user_logout()
    test.test_superuser_auth()
    test.test_delete_user()

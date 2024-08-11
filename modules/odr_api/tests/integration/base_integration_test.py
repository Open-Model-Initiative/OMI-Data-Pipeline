import httpx
from odr_core.crud.user import create_user
from odr_core.schemas.user import UserCreate, UserType
from odr_api.api.auth.auth_jwt import create_access_token
from odr_api.logger import log_api_request, log_api_error
from fastapi.security import HTTPAuthorizationCredentials, OAuth2PasswordBearer
import random
import string
import os
from dotenv import load_dotenv
load_dotenv()


def random_string(length: int = 10) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


class BaseIntegrationTest:
    @classmethod
    def setup_class(cls, base_url, db, logger):
        cls.base_url = base_url
        cls.db = db
        cls.logger = logger
        cls.client = httpx.Client(base_url=base_url, timeout=30)
        cls.oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{base_url}/auth/token")

        # Create a regular user for session/basic auth tests
        cls.test_user = create_user(
            db,
            UserCreate(
                username=f"test_user_{random_string()}",
                email=f"test_user_{random_string()}@example.com",
                password="test_password",
                is_active=True,
                is_superuser=False,
                user_type=UserType.user,
            ),
        )

        # Create a bot user for JWT auth tests
        cls.bot_user = create_user(
            db,
            UserCreate(
                username=f"test_bot_{random_string()}",
                email=f"test_bot_{random_string()}@example.com",
                password="test_bot_password",
                is_active=True,
                is_superuser=False,
                user_type=UserType.bot,
            ),
        )

        # Ensure the bot_user is correctly set as a bot
        cls.bot_user.user_type = UserType.bot
        db.commit()
        db.refresh(cls.bot_user)

        try:
            cls.jwt_token = create_access_token(cls.bot_user)
        except Exception as e:
            cls.logger.error(f"Failed to create JWT token: {str(e)}")
            raise

    def get_session_auth_headers(self):
        try:
            response = self.client.post(
                "/auth/login",
                json={"username": self.test_user.username, "password": "test_password"},
            )
            log_api_request(
                self.logger,
                "POST",
                "/auth/login",
                response.status_code,
                None,
                response.text,
            )
            if response.status_code != 200:
                self.logger.error(
                    f"Login failed. Status: {response.status_code}, Response: {response.text}"
                )
                raise Exception(f"Failed to login: {response.status_code}")

            session_cookie = response.cookies.get('session')
            if session_cookie:
                return {"Cookie": f"session={session_cookie}"}
            else:
                return {"Authorization": response.text}
        except httpx.RequestError as e:
            self.logger.error(f"Request error during login: {str(e)}")
            raise

    def get_basic_auth_headers(self):
        return httpx.BasicAuth(self.test_user.username, "test_password")

    def get_jwt_auth_headers(self):
        return HTTPAuthorizationCredentials(scheme="Bearer", credentials=self.jwt_token)

    def get_superuser_auth_headers(self):
        load_dotenv()
        username = os.getenv('DEFAULT_SUPERUSER_USERNAME')
        password = os.getenv('DEFAULT_SUPERUSER_PASSWORD')

        try:
            response = self.client.post(
                "/auth/login",
                json={"username": username, "password": password},
            )
            log_api_request(
                self.logger,
                "POST",
                "/auth/login",
                response.status_code,
                None,
                response.text,
            )
            if response.status_code != 200:
                self.logger.error(
                    f"Superuser login failed. Status: {response.status_code}, Response: {response.text}"
                )
                raise Exception(f"Failed to login as superuser: {response.status_code}")

            session_cookie = response.cookies.get('session')
            if session_cookie:
                return {"Cookie": f"session={session_cookie}"}
            else:
                # If no session cookie, return the entire response content as Authorization header
                return {"Authorization": response.text}
        except httpx.RequestError as e:
            self.logger.error(f"Request error during superuser login: {str(e)}")
            raise

    @classmethod
    def teardown_class(cls):
        # Clean up created users
        cls.db.delete(cls.test_user)
        cls.db.delete(cls.bot_user)
        cls.db.commit()
        cls.client.close()

    def log_error(self, response):
        log_api_error(
            self.logger,
            Exception(f"API Error: Status {response.status_code}"),
            {
                "url": str(response.url),
                "method": response.request.method,
                "headers": dict(response.request.headers),
                "content": (
                    response.request.content.decode()
                    if response.request.content
                    else None
                ),
            },
            f"Response: {response.text}",
        )

    @classmethod
    def run_tests(cls):
        instance = cls()
        test_methods = [
            method
            for method in dir(instance)
            if method.startswith("test_") and callable(getattr(instance, method))
        ]
        results = []
        for method_name in test_methods:
            method = getattr(instance, method_name)
            result = cls.run_single_test(method, instance)
            results.append(result)
        return results

    @staticmethod
    def run_single_test(test_method, test_instance):
        from test_result import TestResult

        test_name = test_method.__name__
        try:
            test_method()
            return TestResult(test_name, True)
        except Exception as e:
            import traceback
            import sys

            exc_type, exc_value, exc_traceback = sys.exc_info()
            tb_entries = traceback.extract_tb(exc_traceback)
            our_code_entry = next(
                (
                    entry
                    for entry in reversed(tb_entries)
                    if "site-packages" not in entry.filename and "lib" not in entry.filename.lower()
                ),
                None,
            )
            if our_code_entry:
                error_location = f"{our_code_entry.filename}:{our_code_entry.lineno}"
                error_context = f"in {our_code_entry.name}: {our_code_entry.line}"
            else:
                error_location = "Unknown"
                error_context = "Context not available"
            error_message = f"{type(e).__name__}: {str(e)}"
            full_error_message = (
                f"{error_message}\nLocation: {error_location}\nContext: {error_context}"
            )
            return TestResult(test_name, False, full_error_message, error_location)

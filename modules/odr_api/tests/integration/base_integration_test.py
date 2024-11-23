# SPDX-License-Identifier: Apache-2.0
import httpx
from odr_api.logger import log_api_error
import random
import string
from dotenv import load_dotenv
load_dotenv()


def random_string(length: int = 10) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


class TestUser:
    def __init__(self) -> None:
        self.id = 1


class BaseIntegrationTest:
    @classmethod
    def setup_class(cls, base_url, db, logger):
        cls.base_url = base_url
        cls.db = db
        cls.logger = logger
        cls.client = httpx.Client(base_url=base_url, timeout=30)
        cls.test_user = TestUser()

    @classmethod
    def teardown_class(cls):
        # Clean up created users
        pass

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

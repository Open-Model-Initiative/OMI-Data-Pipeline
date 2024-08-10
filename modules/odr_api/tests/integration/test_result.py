import httpx
from odr_api.logger import get_logger, log_api_error, log_api_request
from typing import List
import traceback
import sys

logger = get_logger("integration_test_results")


class TestResult:
    def __init__(
        self,
        name: str,
        success: bool,
        error_message: str = None,
        error_location: str = None,
    ):
        self.name = name
        self.success = success
        self.error_message = error_message
        self.error_location = error_location


def run_test(test_method, test_instance) -> TestResult:
    test_name = test_method.__name__
    try:
        test_method(test_instance)
        return TestResult(test_name, True)
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()

        # Get the full traceback
        tb_entries = traceback.extract_tb(exc_traceback)

        # Find the last entry in our code
        our_code_entry = next(
            (
                entry
                for entry in reversed(tb_entries)
                if "site-packages" not in entry.filename
                and "lib" not in entry.filename.lower()
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


def log_test_results(results: List[TestResult]):
    logger.info("\033[92mIntegration Test Results:\033[0m")  # log in green
    logger.info("-------------------------")
    for result in results:
        status = "PASSED" if result.success else "FAILED"
        status_color = (
            "\033[92m" if result.success else "\033[91m"
        )  # green for PASSED, red for FAILED
        logger.info(f"{result.name}: {status_color}{status}\033[0m")
        if not result.success:
            logger.error(f"  Error: {result.error_message}")
            logger.error(f"  Location: {result.error_location}")
    logger.info("-------------------------")
    total_tests = len(results)
    passed_tests = sum(1 for result in results if result.success)
    logger.info(f"Total Tests: {total_tests}")
    logger.info(f"\033[92mPassed: {passed_tests}\033[0m")  # green
    logger.info(f"\033[91mFailed: {total_tests - passed_tests}\033[0m")  # red

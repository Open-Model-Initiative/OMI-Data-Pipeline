import argparse
import sys
from models import TestUserLifecycle, TestContentLifecycle

# Import other test classes here
from test_result import log_test_results
from odr_api.logger import get_logger
from odr_core.database import SessionLocal

logger = get_logger("integration_tests")


def main():
    parser = argparse.ArgumentParser(description="Run integration tests for odr_api")
    parser.add_argument(
        "--api-base-url", default="http://localhost:31100", help="Base URL of the API"
    )
    parser.add_argument(
        "--tests",
        nargs="+",
        default=["all"],
        help="Specific tests to run (users or all)",
    )
    parser.add_argument("--api-version", default="/api/v1", help="Api Version slug")
    args = parser.parse_args()

    API_BASE = f"{args.api_base_url}{args.api_version}"
    logger.info(f"Running integration tests against API at {API_BASE}")

    db = SessionLocal()

    test_classes = [
        TestUserLifecycle,
        TestContentLifecycle,
    ]  # Add other test classes to this list

    all_results = []

    for test_class in test_classes:
        if (
            "all" in args.tests
            or test_class.__name__.lower().replace("test", "") in args.tests
        ):
            logger.info(f"Running tests for {test_class.__name__}")
            test_class.setup_class(API_BASE, db, logger)
            results = test_class.run_tests()
            all_results.extend(results)
            test_class.teardown_class()

    log_test_results(all_results)

    if any(not result.success for result in all_results):
        sys.exit(1)

    logger.info("All integration tests completed successfully")


if __name__ == "__main__":
    main()

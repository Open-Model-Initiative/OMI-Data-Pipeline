import argparse
import sys
from models import TestContentLifecycle, TestAnnotationLifecycle, TestAnnotationSourceLifecycle, TestAnnotationRatingLifecycle


# Import other test classes here
from test_result import log_test_results
from odr_api.logger import get_logger
from odr_core.database import SessionLocal

logger = get_logger("integration_tests")


def main():
    parser = argparse.ArgumentParser(
        description="Run integration tests for odr_api",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--api-base-url",
        default="http://localhost:31100",
        help="Base URL of the API"
    )
    parser.add_argument(
        "--tests",
        nargs="+",
        default=["all"],
        help="Specific tests to run. Available options:\n"
             "  all: Run all tests\n"
             "  content: Run content lifecycle tests\n"
             "  annotation: Run annotation lifecycle tests\n"
             "  annotationsource: Run annotation source lifecycle tests\n"
             "  annotationrating: Run annotation rating lifecycle tests"
    )
    parser.add_argument(
        "--api-version",
        default="/api/v1",
        help="API Version slug"
    )
    args = parser.parse_args()

    API_BASE = f"{args.api_base_url}{args.api_version}"
    logger.info(f"Running integration tests against API at {API_BASE}")

    db = SessionLocal()

    test_classes = {
        "content": TestContentLifecycle,
        "annotation": TestAnnotationLifecycle,
        "annotationsource": TestAnnotationSourceLifecycle,
        "annotationrating": TestAnnotationRatingLifecycle,
    }  # Add other test classes to this list

    all_results = []

    for test_name in args.tests:
        if test_name.lower() == "all":
            classes_to_run = test_classes.values()
        else:
            class_to_run = test_classes.get(test_name.lower())
            if not class_to_run:
                logger.error(f"Unknown test: {test_name}")
                continue
            classes_to_run = [class_to_run]

        for test_class in classes_to_run:
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

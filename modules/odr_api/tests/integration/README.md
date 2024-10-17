# Open Data Repository API Integration Tests

This directory contains the integration tests for the Open Data Repository API. These tests ensure that the various components of the system work together correctly, including the API endpoints, database operations, and authentication mechanisms.

## Test Structure

The integration tests are organized as follows:

- `run_integration.py`: The main script to run all integration tests.
- `base_integration_test.py`: Contains the BaseIntegrationTest class with common setup and utility methods.
- `test_result.py`: Contains the TestResult class and utility functions for running tests and logging results.
- `models/`: Directory containing test files for different models:
  - (Add other test files as they are created)

## Running the Tests

To run the integration tests, use the following command from the root of the repo:

```bash
task api-test:test-all
```

Available options:

- `--api-base-url`: The base URL of the API (default: http://localhost:31100)
- `--tests`: Specific tests to run (options: users, or all)
- `--api-version`: API version slug (default: /api/v1)

## Test Result Handling

The `TestResult` class in `test_result.py` captures the outcome of each test, including:

- Test name
- Success status
- Error message (if any)
- Error location (file and line number)

The `run_single_test` function executes individual test methods and captures detailed error information, including the location in our code where an error occurred.

## Logging

Test results are logged using a custom logger defined in `odr_api.logger`. The `log_test_results` function provides a summary of all test results, including:

- Individual test outcomes (PASSED/FAILED)
- Error messages and locations for failed tests
- Total number of tests run, passed, and failed

## Adding New Tests

To add a new integration test:

1. Create a new test file in the `models/` directory.
2. Define a test class that inherits from `BaseIntegrationTest`.
3. Implement test methods that use the appropriate authentication method.
4. Use assertions to verify expected outcomes.
5. Add error handling and logging as demonstrated in existing tests.
6. Update the `run_integration.py` file to include the new test class.

## Best Practices

- Use descriptive names for test methods and variables.
- Include both positive and negative test cases.
- Test all CRUD operations for each model.
- Use random data generation to ensure tests are not dependent on specific data.
- Log API requests and responses for easier debugging.
- Handle and log errors appropriately to provide useful debugging information.
- Ensure each test uses the correct authentication method for the operation being tested.

## Troubleshooting

If you encounter issues while running the tests:

1. Check the API base URL and ensure the server is running.
2. Verify that the database is properly set up and accessible.
3. Review the error messages and stack traces in the test output.
4. Check the API logs for any server-side errors.
5. Ensure all required dependencies are installed and up to date.
6. Verify that the correct authentication method is being used for each test.

For any persistent issues, please contact the development team.

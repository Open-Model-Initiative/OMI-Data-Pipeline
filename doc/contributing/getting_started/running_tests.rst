Running Tests
=============

Before committing any changes, ensure you run all tests to be sure existing behaviour continues to work. If any tests require updates to pass with your changes, ensure you update them as well.

To run all tests, run ``task test-all``. Note this is not working at the moment and needs some work but some tests are run via the pipeline automatically.

To run our playwright tests, run ``task frontend:test-integration`` which should all pass at this time.

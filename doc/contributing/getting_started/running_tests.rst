Running Tests
=============

Before committing any changes, ensure you run all tests to be sure existing behaviour continues to work. If any tests require updates to pass with your changes, ensure you update them as well.

To run all tests, ensure the site is running locally already. Then in a new console window, run ``task test-all``.
Note some tests are not working at the moment and have been commented out so test-all is expected to all pass at the moment.

To run our various tests individually, you can use the individual tasks:

- ``task: monitoring:test``
- ``task: frontend:test-unit``
- ``task: frontend:test-integration``

Calculating Code Coverage
=========================

Unit test code coverage is currently available for the core and monitoring modules.

You can run them with the tasks:

- ``task core:coverage``
- ``task monitoring:coverage``

Note that these are currently throwing errors but you can still get an idea of covered lines.

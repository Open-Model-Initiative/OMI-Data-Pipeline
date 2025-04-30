Running Linting
===============

To run linting, a few jobs require you to activate your venv first.

On Linux/Mac, run `source venv/bin/activate`
On Windows, run `./venv/bin/activate`

Lint the frontend module with `task frontend:lint`
To fix the issues run `task frontend:format`

Lint the monitoring module using Flake8 with `task monitoring:lint`
Format the monitoring module using Black with the `task monitoring:format`

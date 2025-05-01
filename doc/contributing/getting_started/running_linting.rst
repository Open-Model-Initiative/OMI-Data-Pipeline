Running Linting
===============

To run linting, a few jobs require you to activate your venv first.

On Linux/Mac, run `source venv/bin/activate`
On Windows, run `./venv/bin/activate`

Lint the frontend module using prettier and eslint with `task frontend:lint`
To fix the issues run `task frontend:format`
You can also use `task frontend:check` to check the frontend with svelte-check.

Lint the monitoring module using Flake8 with `task monitoring:lint`
Format the monitoring module using Black with the `task monitoring:format`

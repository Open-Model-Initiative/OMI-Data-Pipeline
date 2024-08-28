# ODR Monitoring

ODR Monitoring is a logging and monitoring module for the Open Data Repository project. It provides a configurable logging system with custom formatters and handlers for both console and file output.

## Installation

To install the ODR Monitoring module, run:

```
pip install -e modules/odr_monitoring
```

## Usage

To use the ODR Monitoring logger in your code:

```python
from odr_monitoring import get_logger

logger = get_logger(__name__)

logger.info("This is an info message")
logger.error("This is an error message")
```

## Configuration

The Open Data Repository (ODR) Monitoring logging system can be configured using environment variables or a .env file. The following configuration options are available:

- `ODR_MONITORING_LOG_LEVEL`: The log level (DEBUG, INFO, WARNING, ERROR, CRITICAL). Default: DEBUG
- `ODR_MONITORING_LOG_FORMAT`: The log format string. Default: "%(levelname)s | %(asctime)s | %(message)s"
- `ODR_MONITORING_LOG_DATE_FORMAT`: The date format string for log messages. Default: "%Y-%m-%d %H:%M:%S"
- `ODR_MONITORING_CONSOLE_LOG_ENABLED`: Enable console logging. Default: True
- `ODR_MONITORING_FILE_LOG_ENABLED`: Enable file logging. Default: True
- `ODR_MONITORING_LOG_FILE_PATH`: The path to the log file. Default: "logs/odr_monitoring.log"
- `ODR_MONITORING_LOG_FILE_MAX_BYTES`: The maximum size of the log file before rotation. Default: 10485760 (10 MB)
- `ODR_MONITORING_LOG_FILE_BACKUP_COUNT`: The number of backup log files to keep. Default: 5
- `ODR_MONITORING_USE_COLORS`: Enable colored output for console logging. Default: True

To configure these options:

1. Create a `.env` file in the root directory of your project.
2. Add the desired configuration options to the `.env` file. For example:

   ```
   ODR_MONITORING_LOG_LEVEL=INFO
   ODR_MONITORING_FILE_LOG_ENABLED=False
   ODR_MONITORING_USE_COLORS=False
   ```

## Development

To set up the development environment:

1. Clone the repository
2. Install the requirements: `pip install -r requirements.txt`
3. Install the pre-commit hooks: `pre-commit install`

To run the tests:

```
task test
```

To run the tests with coverage:

```
task coverage
```

To run the linter:

```
task lint
```

To format the code:

```
task format
```

To run all checks:

```
task check
```

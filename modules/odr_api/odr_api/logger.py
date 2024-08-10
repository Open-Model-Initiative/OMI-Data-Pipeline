import logging
import sys
import json


def get_logger(name: str = "odr_api"):
    """
    Get a logger instance.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stderr)
        formatter = logging.Formatter(
            "%(levelname)s | %(asctime)s | %(message)s", "%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

        # Add color to log levels
        logging.addLevelName(
            logging.ERROR, f"\033[91m{logging.getLevelName(logging.ERROR)}\033[0m"
        )
        logging.addLevelName(
            logging.WARNING, f"\033[93m{logging.getLevelName(logging.WARNING)}\033[0m"
        )

    return logger


def log_api_error(
    logger, error: Exception, request_data: dict = None, additional_info: str = None
):
    """
    Log API errors with detailed information.
    """
    error_message = f"API Error: {str(error)}"

    if request_data:
        error_message += f"\nRequest Data: {json.dumps(request_data, indent=2)}"

    if additional_info:
        error_message += f"\nAdditional Info: {additional_info}"

    logger.error(error_message)


def log_api_request(
    logger,
    method: str,
    url: str,
    status_code: int,
    request_data: dict = None,
    response_data: dict = None,
):
    """
    Log API requests with method, URL, status code, and optional request/response data.
    """
    log_message = f"API Request: {method} {url} - Status: {status_code}"

    if request_data:
        log_message += f"\nRequest Data: \033[94m{json.dumps(request_data, indent=2)}\033[0m"  # log in light blue

    if response_data:
        log_message += f"\nResponse Data: \033[92m{json.dumps(response_data, indent=2)}\033[0m"  # log in light green

    logger.info(log_message)

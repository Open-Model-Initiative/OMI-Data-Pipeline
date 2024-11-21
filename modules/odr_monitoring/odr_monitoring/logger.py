# SPDX-License-Identifier: Apache-2.0
import logging
import json
from odr_monitoring.config import logging_config
from odr_monitoring.handlers import get_console_handler, get_file_handler


class ODRLogger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        self.setup_handlers()

    def setup_handlers(self):
        if logging_config.CONSOLE_LOG_ENABLED:
            self.logger.addHandler(get_console_handler())

        if logging_config.FILE_LOG_ENABLED:
            self.logger.addHandler(get_file_handler())

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)

    def log_api_error(self, error: Exception, request_data: dict = None, additional_info: str = None):
        error_message = f"API Error: {str(error)}"
        if request_data:
            error_message += f"\nRequest Data: {json.dumps(request_data, indent=2)}"
        if additional_info:
            error_message += f"\nAdditional Info: {additional_info}"
        self.error(error_message)

    def log_api_request(self, method: str, url: str, status_code: int, request_data: dict = None, response_data: dict = None):
        log_message = f"API Request: {method} {url} - Status: {status_code}"
        if request_data:
            log_message += f"\nRequest Data: {json.dumps(request_data, indent=2)}"
        if response_data:
            log_message += f"\nResponse Data: {json.dumps(response_data, indent=2)}"
        self.info(log_message)

    def close(self):
        for handler in self.logger.handlers[:]:
            handler.close()
            self.logger.removeHandler(handler)


def get_logger(name):
    return ODRLogger(name)


__all__ = ['get_logger']

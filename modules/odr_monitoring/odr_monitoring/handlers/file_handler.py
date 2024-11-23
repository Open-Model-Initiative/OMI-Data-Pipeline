# SPDX-License-Identifier: Apache-2.0
import os
import logging
from logging.handlers import RotatingFileHandler
from odr_monitoring.config import logging_config
from odr_monitoring.formatters.standard_formatter import StandardFormatter


class FileHandler(RotatingFileHandler):
    def __init__(self):
        log_dir = os.path.dirname(logging_config.LOG_FILE_PATH)
        os.makedirs(log_dir, exist_ok=True)
        super().__init__(
            filename=logging_config.LOG_FILE_PATH,
            maxBytes=logging_config.LOG_FILE_MAX_BYTES,
            backupCount=logging_config.LOG_FILE_BACKUP_COUNT
        )
        self.setLevel(logging.DEBUG)
        self.setFormatter(StandardFormatter(
            fmt=logging_config.LOG_FORMAT,
            datefmt=logging_config.LOG_DATE_FORMAT,
            use_colors=False
        ))


def get_file_handler():
    return FileHandler()

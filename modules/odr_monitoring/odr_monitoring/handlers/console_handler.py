# SPDX-License-Identifier: Apache-2.0
import logging
import sys
from odr_monitoring.config import logging_config
from odr_monitoring.formatters.standard_formatter import StandardFormatter


class ConsoleHandler(logging.StreamHandler):
    def __init__(self):
        super().__init__(stream=sys.stdout)
        self.setLevel(logging.getLevelName(logging_config.LOG_LEVEL))
        self.setFormatter(StandardFormatter(
            fmt=logging_config.LOG_FORMAT,
            datefmt=logging_config.LOG_DATE_FORMAT,
            use_colors=logging_config.USE_COLORS
        ))


def get_console_handler():
    return ConsoleHandler()

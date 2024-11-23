# SPDX-License-Identifier: Apache-2.0
import logging
from termcolor import colored


def setup_logger():
    class ColoredFormatter(logging.Formatter):
        COLORS = {
            "DEBUG": "blue",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red",
        }

        def format(self, record):
            levelname = record.levelname
            message = super().format(record)
            meta_message = f" ({record.pathname}:{record.lineno}): {message}"
            log_message = colored(meta_message, self.COLORS.get(levelname, "white"))

            return log_message

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()
    handler.setFormatter(
        ColoredFormatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    logger.addHandler(handler)

    return logger


logger = setup_logger()

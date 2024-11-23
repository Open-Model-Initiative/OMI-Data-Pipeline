# SPDX-License-Identifier: Apache-2.0
import os
import sys
import logging
import warnings
import traceback
from rich.theme import Theme
from rich.logging import RichHandler
from rich.console import Console
from rich.pretty import install as pretty_install
from rich.traceback import install as traceback_install


console = Console(log_time=True, log_time_format='%H:%M:%S-%f', theme=Theme({
    "traceback.border": "black",
    "traceback.border.syntax_error": "black",
    "inspect.value.border": "black",
}))


def trace():
    traceback_install()


def setup_logging():
    logging.getLogger("urllib3").setLevel(logging.ERROR)
    logging.getLogger("httpx").setLevel(logging.ERROR)
    logging.getLogger("diffusers").setLevel(logging.ERROR)
    logging.getLogger("torch").setLevel(logging.ERROR)
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s | %(name)s | %(levelname)s | %(module)s | %(message)s', handlers=[logging.NullHandler()])  # redirect default logger to null
    warnings.filterwarnings(action="ignore")

    def excepthook(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            log.info('KeyboardInterrupt')
            os._exit(0)
        log.error(f"exception: type={exc_type} value={exc_value}")
        if exc_traceback:
            format_exception = traceback.format_tb(exc_traceback)
            for line in format_exception:
                log.error(repr(line))

    log_instance = logging.getLogger("sd")
    pretty_install(console=console)
    traceback_install(console=console, extra_lines=1, max_frames=10, width=console.width, word_wrap=False, indent_guides=False, suppress=[])

    rh = RichHandler(show_time=True, omit_repeated_times=False, show_level=True, show_path=False, markup=False, rich_tracebacks=True, log_time_format='%H:%M:%S-%f', level=logging.DEBUG, console=console)
    log_instance.setLevel(logging.INFO)
    log_instance.addHandler(rh)

    fh = logging.FileHandler(filename='hdr.log', encoding='utf-8', delay=True)
    fh.formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(module)s | %(message)s')
    fh.setLevel(logging.DEBUG)
    log_instance.addHandler(fh)

    sys.excepthook = excepthook
    return log_instance


log = setup_logging()

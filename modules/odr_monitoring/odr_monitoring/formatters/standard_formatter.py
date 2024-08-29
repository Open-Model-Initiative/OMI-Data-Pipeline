import logging
import json


class StandardFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[94m',        # Blue
        'INFO': '\033[92m',         # Green
        'WARNING': '\033[93m',      # Yellow
        'ERROR': '\033[91m',        # Red
        'CRITICAL': '\033[95m',     # Magenta
        'RESET': '\033[0m'          # Reset color
    }

    def __init__(self, fmt=None, datefmt=None, style='%', validate=True, *, use_colors=True):
        super().__init__(fmt, datefmt, style, validate)
        self.use_colors = use_colors

    def format(self, record):
        log_data = {
            'timestamp': self.formatTime(record, self.datefmt),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)

        if self.use_colors:
            color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
            formatted_message = f"{color}{json.dumps(log_data)}{self.COLORS['RESET']}"
        else:
            formatted_message = json.dumps(log_data)

        return formatted_message

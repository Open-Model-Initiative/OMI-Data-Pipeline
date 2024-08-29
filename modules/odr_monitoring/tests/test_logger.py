import unittest
import os
import json
from odr_monitoring import get_logger
from odr_monitoring.config import logging_config


class TestODRLogger(unittest.TestCase):
    def setUp(self):
        self.logger = get_logger("test_logger")
        self.log_file = logging_config.LOG_FILE_PATH

    def test_logger_creation(self):
        self.assertIsNotNone(self.logger)

    def test_log_levels(self):
        self.logger.debug("Debug message")
        self.logger.info("Info message")
        self.logger.warning("Warning message")
        self.logger.error("Error message")
        self.logger.critical("Critical message")
        self.assertTrue(os.path.exists(self.log_file), f"Log file not created at {self.log_file}")

        with open(self.log_file, "r") as f:
            log_contents = f.readlines()

        log_messages = [json.loads(line)['message'] for line in log_contents]

        self.assertIn("Debug message", log_messages)
        self.assertIn("Info message", log_messages)
        self.assertIn("Warning message", log_messages)
        self.assertIn("Error message", log_messages)
        self.assertIn("Critical message", log_messages)

    def test_log_format(self):
        self.logger.info("Test message")
        self.assertTrue(os.path.exists(self.log_file), f"Log file not created at {self.log_file}")

        with open(self.log_file, "r") as f:
            last_log = json.loads(f.readlines()[-1])

        self.assertIn("timestamp", last_log)
        self.assertIn("level", last_log)
        self.assertIn("message", last_log)
        self.assertIn("module", last_log)
        self.assertIn("function", last_log)
        self.assertIn("line", last_log)

    def tearDown(self):
        self.logger.close()
        if os.path.exists(self.log_file):
            os.remove(self.log_file)


if __name__ == "__main__":
    unittest.main()

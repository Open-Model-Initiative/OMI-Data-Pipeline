# SPDX-License-Identifier: Apache-2.0
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class LoggingConfig(BaseSettings):
    LOG_LEVEL: str = "DEBUG"
    LOG_FORMAT: str = "%(levelname)s | %(asctime)s | %(message)s"
    LOG_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    CONSOLE_LOG_ENABLED: bool = True
    FILE_LOG_ENABLED: bool = True
    LOG_FILE_PATH: str = "logs/odr_monitoring.log"
    LOG_FILE_MAX_BYTES: int = 10 * 1024 * 1024  # 10 MB
    LOG_FILE_BACKUP_COUNT: int = 5
    USE_COLORS: bool = True

    model_config = ConfigDict(env_prefix="ODR_MONITORING_", env_file=".env")


logging_config = LoggingConfig()

__all__ = ['logging_config']

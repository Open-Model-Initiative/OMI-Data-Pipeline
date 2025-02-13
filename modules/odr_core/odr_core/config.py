# SPDX-License-Identifier: Apache-2.0
from pydantic_settings import BaseSettings
from dotenv import find_dotenv, load_dotenv
import os

# Load .env file, but don't override existing environment variables
if os.getenv("ENVIRONMENT") == "DOCKER":
    print("Docker environment detected")
    load_dotenv(dotenv_path=find_dotenv(".env"), override=False)
else:
    print("Local environment detected")
    load_dotenv(dotenv_path=find_dotenv(".env"), override=True)


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "OMI-DataModel"

    # Postgres
    POSTGRES_HOST: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: str

    # Auth - make sure to set this to False in production
    SKIP_AUTH: bool = False

    # Default Superuser - should be removed
    DEFAULT_SUPERUSER_EMAIL: str = None
    DEFAULT_SUPERUSER_PASSWORD: str = None
    DEFAULT_SUPERUSER_USERNAME: str = None

    # Test Database
    TEST_POSTGRES_DB: str = None
    TEST: bool = False

    ROOT_DIR: str

    # Models
    MODEL_CACHE_DIR: str

    # Embedding
    CONTENT_EMBEDDING_DIMENSION: int = 512
    ANNOTATION_EMBEDDING_DIMENSION: int = 384

    # Hugging Face
    HF_TOKEN: str = None
    HF_HDR_DATASET_NAME: str = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

    def get_db_url(self):
        print(f"{self}")
        db_name = self.TEST_POSTGRES_DB if self.TEST else self.POSTGRES_DB

        conn_str = f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{db_name}"
        return conn_str

# Create settings instance
settings = Settings()

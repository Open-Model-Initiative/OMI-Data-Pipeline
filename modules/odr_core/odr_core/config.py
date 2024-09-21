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

    # PGADMIN
    PGADMIN_DEFAULT_EMAIL: str
    PGADMIN_DEFAULT_PASSWORD: str

    # Auth - make sure to set this to False in production
    SKIP_AUTH: bool = False

    # Session
    SESSION_MAX_AGE_SECONDS: int = 60 * 60 * 24 * 7 * 4  # 4 weeks

    # Default Superuser
    DEFAULT_SUPERUSER_EMAIL: str
    DEFAULT_SUPERUSER_PASSWORD: str
    DEFAULT_SUPERUSER_USERNAME: str

    # JWT
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_SECONDS: int = 3600
    JWT_LEEWAY_SECONDS: int = 60

    # Test Database
    TEST_POSTGRES_DB: str
    TEST: bool = False

    ROOT_DIR: str

    # Models
    MODEL_CACHE_DIR: str

    # OUATH
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str

    GITHUB_CLIENT_ID: str
    GITHUB_CLIENT_SECRET: str

    DISCORD_CLIENT_ID: str
    DISCORD_CLIENT_SECRET: str

    OAUTH2_REDIRECT_PATH: str

    # Embedding
    CONTENT_EMBEDDING_DIMENSION: int = 512
    ANNOTATION_EMBEDDING_DIMENSION: int = 384

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

# Print loaded environment variables for debugging
print("Loaded environment variables:")
for key, value in settings.dict().items():
    print(f"{key}: {value}")

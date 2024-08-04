from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "OMI-DataModel"
    
    # Postgres
    POSTGRES_HOST: str = "localhost"
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: str

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

    class Config:
        env_file = ".env"

    def get_db_url(self):
        db_name = self.TEST_POSTGRES_DB if self.TEST else self.POSTGRES_DB
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{db_name}"

settings = Settings()
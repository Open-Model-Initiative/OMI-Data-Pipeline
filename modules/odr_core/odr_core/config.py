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
    
    # Test Database
    TEST_POSTGRES_DB: str

    ROOT_DIR: str

    class Config:
        env_file = ".env"

    def get_db_url(self, test: bool = False):
        db_name = self.TEST_POSTGRES_DB if test else self.POSTGRES_DB
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{db_name}"

settings = Settings()
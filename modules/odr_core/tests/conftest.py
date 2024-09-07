import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from odr_core.models.base import Base
from odr_core.schemas.user import UserCreate
from odr_core.crud.user import create_user

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="session")
def engine():
    return create_engine(SQLALCHEMY_DATABASE_URL)


@pytest.fixture(scope="session")
def TestingSessionLocal(engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db(TestingSessionLocal, engine):
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def test_user(db):
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="testpassword"
    )
    return create_user(db, user_data)
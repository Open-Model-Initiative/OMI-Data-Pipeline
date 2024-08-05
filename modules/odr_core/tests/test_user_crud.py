import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from odr_core.models.user import User
from odr_core.schemas.user import UserCreate
from odr_core.crud.user import create_user, get_user, get_user_by_email, get_user_by_username
from odr_core.models.base import Base

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    Base.metadata.drop_all(bind=engine)


def test_create_user(db):
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="testpassword"
    )
    db_user = create_user(db, user_data)
    assert db_user.id is not None
    assert db_user.username == "testuser"
    assert db_user.email == "test@example.com"
    assert db_user.hashed_password == "testpassword_notreallyhashed"
    assert db_user.is_active is True
    assert db_user.is_superuser is False


def test_get_user(db):
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="testpassword"
    )
    created_user = create_user(db, user_data)

    retrieved_user = get_user(db, created_user.id)
    assert retrieved_user is not None
    assert retrieved_user.id == created_user.id
    assert retrieved_user.username == "testuser"
    assert retrieved_user.email == "test@example.com"


def test_get_user_by_email(db):
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="testpassword"
    )
    created_user = create_user(db, user_data)

    retrieved_user = get_user_by_email(db, "test@example.com")
    assert retrieved_user is not None
    assert retrieved_user.id == created_user.id
    assert retrieved_user.username == "testuser"
    assert retrieved_user.email == "test@example.com"


def test_get_user_by_username(db):
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="testpassword"
    )
    created_user = create_user(db, user_data)

    retrieved_user = get_user_by_username(db, "testuser")
    assert retrieved_user is not None
    assert retrieved_user.id == created_user.id
    assert retrieved_user.username == "testuser"
    assert retrieved_user.email == "test@example.com"


def test_get_non_existent_user(db):
    non_existent_user = get_user(db, 999)  # Assuming 999 is not a valid user id
    assert non_existent_user is None


if __name__ == "__main__":
    pytest.main([__file__])

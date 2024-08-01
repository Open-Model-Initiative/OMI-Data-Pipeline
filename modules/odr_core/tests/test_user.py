import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from odr_core.models.user import User
from odr_core.schemas.user import UserCreate, User as UserSchema
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
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password="hashed_" + user_data.password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    assert db_user.id is not None
    assert db_user.username == "testuser"
    assert db_user.email == "test@example.com"
    assert db_user.hashed_password == "hashed_testpassword"
    assert db_user.is_active == True
    assert db_user.is_superuser == False

def test_user_schema():
    user_data = {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "is_active": True,
        "is_superuser": False,
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00"
    }
    user = UserSchema(**user_data)
    assert user.id == 1
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.is_active == True
    assert user.is_superuser == False

if __name__ == "__main__":
    pytest.main([__file__])
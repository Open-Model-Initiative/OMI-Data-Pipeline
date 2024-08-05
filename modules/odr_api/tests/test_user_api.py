import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from odr_core.database import Base, get_db
from server.main import app

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


@pytest.fixture(scope="module")
def client():
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def test_create_user(client):
    response = client.post(
        "/api/v1/users/",
        json={"username": "testuser", "email": "test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data


def test_create_existing_user(client):
    # Create a user
    client.post(
        "/api/v1/users/",
        json={"username": "testuser", "email": "test@example.com", "password": "testpassword"}
    )
    # Try to create the same user again
    response = client.post(
        "/api/v1/users/",
        json={"username": "testuser", "email": "test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_read_user(client):
    # First, create a user
    create_response = client.post(
        "/api/v1/users/",
        json={"username": "testuser", "email": "test@example.com", "password": "testpassword"}
    )
    created_user = create_response.json()

    # Now, try to retrieve the user
    response = client.get(f"/api/v1/users/{created_user['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert data["id"] == created_user["id"]


def test_read_non_existent_user(client):
    response = client.get("/api/v1/users/999")  # Assuming 999 is not a valid user id
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


if __name__ == "__main__":
    pytest.main([__file__])

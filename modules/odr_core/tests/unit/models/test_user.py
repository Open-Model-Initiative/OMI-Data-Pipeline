import pytest
from odr_core.models.user import User


def test_user_model_creation():
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="hashedpassword"
    )
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.hashed_password == "hashedpassword"

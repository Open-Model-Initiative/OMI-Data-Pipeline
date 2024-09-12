import pytest
from odr_core.crud.user import create_user, get_user, get_user_by_email, update_user, delete_user, get_user_by_username
from odr_core.schemas.user import UserCreate, UserUpdate


def test_create_user(db):
    user_data = UserCreate(
        username="newuser",
        email="newuser@example.com",
        password="newpassword"
    )
    user = create_user(db, user_data)
    assert user.id is not None
    assert user.username == "newuser"
    assert user.email == "newuser@example.com"
    assert user.hashed_password != "newpassword"
    assert user.is_active is True
    assert user.is_superuser is False


def test_get_user(db):
    user_data = UserCreate(
        username="getuser",
        email="getuser@example.com",
        password="getpassword"
    )
    created_user = create_user(db, user_data)
    retrieved_user = get_user(db, user_id=created_user.id)
    assert retrieved_user is not None
    assert retrieved_user.id == created_user.id
    assert retrieved_user.username == "getuser"
    assert retrieved_user.email == "getuser@example.com"


def test_update_user(db):
    user_data = UserCreate(
        username="updateuser_before",
        email="updateuser_before@example.com",
        password="updatepassword"
    )
    created_user = create_user(db, user_data)
    update_data = UserUpdate(username="updateduser_after", email="updateuser_after@example.com")
    updated_user = update_user(db, user_id=created_user.id, user=update_data)
    assert updated_user.username == "updateduser_after"
    assert updated_user.email == "updateuser_after@example.com"


def test_delete_user(db):
    user_data = UserCreate(
        username="deleteuser",
        email="deleteuser@example.com",
        password="deletepassword"
    )
    created_user = create_user(db, user_data)
    delete_user(db, user_id=created_user.id)
    deleted_user = get_user(db, user_id=created_user.id)
    assert deleted_user is None


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

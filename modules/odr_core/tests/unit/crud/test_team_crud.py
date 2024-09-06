import pytest
import random
import string
from sqlalchemy.orm import Session
from odr_core.crud import team as team_crud
from odr_core.schemas.team import TeamCreate, TeamUpdate
from odr_core.models.team import Team, UserTeam
from odr_core.schemas.user import UserCreate
from odr_core.crud.user import create_user


def random_string(length: int = 10) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def create_test_user(db: Session):
    return create_user(
        db,
        UserCreate(
            username=f"test_user_{random_string()}",
            email=f"test_user_{random_string()}@example.com",
            password="test_password",
            is_active=True,
            is_superuser=False,
        ),
    )


def test_create_team(db: Session):
    team_data = TeamCreate(name="Test Team")
    created_team = team_crud.create_team(db, team_data)
    assert created_team.id is not None
    assert created_team.name == "Test Team"


def test_get_team(db: Session):
    team_data = TeamCreate(name="Test Team")
    created_team = team_crud.create_team(db, team_data)
    retrieved_team = team_crud.get_team(db, created_team.id)
    assert retrieved_team is not None
    assert retrieved_team.id == created_team.id
    assert retrieved_team.name == "Test Team"


def test_get_teams(db: Session):
    for i in range(5):
        team_data = TeamCreate(name=f"Test Team {i}")
        team_crud.create_team(db, team_data)
    teams = team_crud.get_teams(db)
    assert len(teams) >= 5


def test_update_team(db: Session):
    team_data = TeamCreate(name="Test Team")
    created_team = team_crud.create_team(db, team_data)
    update_data = TeamUpdate(name="Updated Team")
    updated_team = team_crud.update_team(db, created_team.id, update_data)
    assert updated_team.name == "Updated Team"


def test_delete_team(db: Session):
    team_data = TeamCreate(name="Test Team")
    created_team = team_crud.create_team(db, team_data)
    team_crud.delete_team(db, created_team.id)
    deleted_team = team_crud.get_team(db, created_team.id)
    assert deleted_team is None


def test_add_user_to_team(db: Session):
    user = create_test_user(db)
    team_data = TeamCreate(name="Test Team")
    created_team = team_crud.create_team(db, team_data)
    user_team = team_crud.add_user_to_team(db, created_team.id, user.id, role="member")
    assert user_team.user_id == user.id
    assert user_team.team_id == created_team.id
    assert user_team.role == "member"


def test_remove_user_from_team(db: Session):
    user = create_test_user(db)
    team_data = TeamCreate(name="Test Team")
    created_team = team_crud.create_team(db, team_data)
    team_crud.add_user_to_team(db, created_team.id, user.id, role="member")
    team_crud.remove_user_from_team(db, created_team.id, user.id)
    users_in_team = team_crud.get_users_in_team(db, created_team.id)
    assert user not in users_in_team


def test_get_users_in_team(db: Session):
    team_data = TeamCreate(name="Test Team")
    created_team = team_crud.create_team(db, team_data)
    for i in range(3):
        user = create_test_user(db)
        team_crud.add_user_to_team(db, created_team.id, user.id, role="member")
    users_in_team = team_crud.get_users_in_team(db, created_team.id)
    assert len(users_in_team) == 3


def test_get_teams_for_user(db: Session):
    user = create_test_user(db)
    for i in range(3):
        team_data = TeamCreate(name=f"Test Team {i}")
        created_team = team_crud.create_team(db, team_data)
        team_crud.add_user_to_team(db, created_team.id, user.id, role="member")
    user_teams = team_crud.get_teams_for_user(db, user.id)
    assert len(user_teams) == 3


def test_get_nonexistent_team(db: Session):
    nonexistent_team = team_crud.get_team(db, 9999)
    assert nonexistent_team is None


def test_update_nonexistent_team(db: Session):
    update_data = TeamUpdate(name="Updated Team")
    updated_team = team_crud.update_team(db, 9999, update_data)
    assert updated_team is None


def test_delete_nonexistent_team(db: Session):
    team_crud.delete_team(db, 9999)


def test_get_users_in_nonexistent_team(db: Session):
    users_in_team = team_crud.get_users_in_team(db, 9999)
    assert len(users_in_team) == 0


def test_get_teams_for_nonexistent_user(db: Session):
    user_teams = team_crud.get_teams_for_user(db, 9999)
    assert len(user_teams) == 0

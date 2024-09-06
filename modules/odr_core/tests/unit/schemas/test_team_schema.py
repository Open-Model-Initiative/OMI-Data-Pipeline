import pytest
from pydantic import ValidationError
from datetime import datetime
from odr_core.schemas.team import TeamBase, TeamCreate, TeamUpdate, Team, TeamWithMembers


def test_team_base():
    team = TeamBase(name="Test Team")
    assert team.name == "Test Team"

    with pytest.raises(ValidationError):
        TeamBase()


def test_team_create():
    team = TeamCreate(name="Test Team")
    assert team.name == "Test Team"

    with pytest.raises(ValidationError):
        TeamCreate()


def test_team_update():
    team = TeamUpdate(name="Updated Team")
    assert team.name == "Updated Team"

    with pytest.raises(ValidationError):
        TeamUpdate()


def test_team():
    team_data = {
        "id": 1,
        "name": "Test Team",
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "permissions": ["read", "write"],
        "limits": {"max_members": 10}
    }
    team = Team(**team_data)
    assert team.id == 1
    assert team.name == "Test Team"
    assert isinstance(team.created_at, datetime)
    assert isinstance(team.updated_at, datetime)
    assert team.permissions == ["read", "write"]
    assert team.limits == {"max_members": 10}

    with pytest.raises(ValidationError):
        Team(name="Invalid Team")


def test_team_with_members():
    team_data = {
        "id": 1,
        "name": "Test Team",
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "permissions": ["read", "write"],
        "limits": {"max_members": 10},
        "members": [1, 2, 3]
    }
    team = TeamWithMembers(**team_data)
    assert team.id == 1
    assert team.name == "Test Team"
    assert isinstance(team.created_at, datetime)
    assert isinstance(team.updated_at, datetime)
    assert team.permissions == ["read", "write"]
    assert team.limits == {"max_members": 10}
    assert team.members == [1, 2, 3]

    with pytest.raises(ValidationError):
        TeamWithMembers(name="Invalid Team", members="not a list")


def test_team_permissions_and_limits_optional():
    team_data = {
        "id": 1,
        "name": "Test Team",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    team = Team(**team_data)
    assert team.permissions == []
    assert team.limits == {}


def test_team_invalid_data():
    with pytest.raises(ValidationError):
        Team(
            id="not an integer",
            name="Invalid Team",
            created_at="not a datetime",
            updated_at="not a datetime"
        )

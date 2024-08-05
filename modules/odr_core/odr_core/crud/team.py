# odr_core/crud/team.py
from sqlalchemy.orm import Session
from odr_core.models.team import Team, UserTeam
from odr_core.models.user import User
from odr_core.schemas.team import TeamCreate, TeamUpdate
from typing import List, Optional


def create_team(db: Session, team: TeamCreate) -> Team:
    db_team = Team(name=team.name)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


def get_team(db: Session, team_id: int) -> Optional[Team]:
    return db.query(Team).filter(Team.id == team_id).first()


def get_teams(db: Session, skip: int = 0, limit: int = 100) -> List[Team]:
    return db.query(Team).offset(skip).limit(limit).all()


def update_team(db: Session, team_id: int, team: TeamUpdate) -> Team:
    db_team = get_team(db, team_id)
    if db_team:
        for key, value in team.dict(exclude_unset=True).items():
            setattr(db_team, key, value)
        db.commit()
        db.refresh(db_team)
    return db_team


def delete_team(db: Session, team_id: int) -> None:
    db.query(Team).filter(Team.id == team_id).delete()
    db.commit()


def add_user_to_team(db: Session, team_id: int, user_id: int, role: str = "member") -> UserTeam:
    db_user_team = UserTeam(user_id=user_id, team_id=team_id, role=role)
    db.add(db_user_team)
    db.commit()
    db.refresh(db_user_team)
    return db_user_team


def remove_user_from_team(db: Session, team_id: int, user_id: int) -> None:
    db.query(UserTeam).filter(UserTeam.team_id == team_id, UserTeam.user_id == user_id).delete()
    db.commit()


def get_users_in_team(db: Session, team_id: int) -> List[User]:
    team = db.query(Team).filter(Team.id == team_id).first()
    if team:
        return team.members
    return []


def get_teams_for_user(db: Session, user_id: int) -> List[Team]:
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        return user.teams
    return []

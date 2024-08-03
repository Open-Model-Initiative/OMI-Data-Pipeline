from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from odr_core.crud import team as team_crud
from odr_core.schemas.team import Team, TeamCreate, TeamUpdate, TeamWithMembers
from odr_core.schemas.user import User
from odr_core.database import get_db

from ..auth.auth_provider import authorized_user, authorized_superuser

router = APIRouter(tags=["teams"])

@router.post("/teams/", response_model=Team)
def create_team(team: TeamCreate, db: Session = Depends(get_db), current_user = Depends(authorized_user)):
    return team_crud.create_team(db=db, team=team)

@router.get("/teams/{team_id}", response_model=TeamWithMembers)
def read_team(team_id: int, db: Session = Depends(get_db)):
    db_team = team_crud.get_team(db, team_id=team_id)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return db_team

@router.get("/teams/", response_model=List[Team])
def read_teams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    teams = team_crud.get_teams(db, skip=skip, limit=limit)
    return teams

@router.put("/teams/{team_id}", response_model=Team)
def update_team(team_id: int, team: TeamUpdate, db: Session = Depends(get_db), current_user = Depends(authorized_user)):
    db_team = team_crud.update_team(db, team_id=team_id, team=team)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return db_team

@router.delete("/teams/{team_id}")
def delete_team(team_id: int, db: Session = Depends(get_db), current_user = Depends(authorized_user)):
    team_crud.delete_team(db, team_id=team_id)
    return {"message": "Team deleted successfully"}

@router.post("/teams/{team_id}/users/{user_id}")
def add_user_to_team(team_id: int, user_id: int, role: str = "member", db: Session = Depends(get_db), current_user = Depends(authorized_user)):
    return team_crud.add_user_to_team(db, team_id=team_id, user_id=user_id, role=role)

@router.delete("/teams/{team_id}/users/{user_id}")
def remove_user_from_team(team_id: int, user_id: int, db: Session = Depends(get_db), current_user = Depends(authorized_user)):
    team_crud.remove_user_from_team(db, team_id=team_id, user_id=user_id)
    return {"message": "User removed from team successfully"}

@router.get("/teams/{team_id}/users", response_model=List[User])
def get_users_in_team(team_id: int, db: Session = Depends(get_db)):
    users = team_crud.get_users_in_team(db, team_id=team_id)
    if not users:
        raise HTTPException(status_code=404, detail="Team not found or has no users")
    return users

@router.get("/users/{user_id}/teams", response_model=List[Team])
def get_teams_for_user(user_id: int, db: Session = Depends(get_db)):
    teams = team_crud.get_teams_for_user(db, user_id=user_id)
    if not teams:
        raise HTTPException(status_code=404, detail="User not found or is not in any teams")
    return teams
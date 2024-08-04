# server/api/endpoints/user.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from odr_core.crud import user as user_crud
from odr_core.schemas.user import User, UserCreate, UserUpdate
from odr_core.schemas.team import Team
from odr_core.database import get_db
from loguru import logger

from ..auth.auth_provider import AuthProvider

router = APIRouter(tags=["users"])

@router.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_crud.create_user(db=db, user=user)

@router.get("/users/me", response_model=User)
def read_users_me(current_user: User = Depends(AuthProvider())):
    return current_user

@router.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/users", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = user_crud.get_users(db, skip=skip, limit=limit)
    logger.info(f"Retrieved {len(users)} users")
    logger.info(f"Users: {users}")
    return users

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), _: User = Depends(AuthProvider(superuser=True))):
    user_crud.delete_user(db, user_id=user_id)
    return {"message": "User deleted successfully"}

# update user
@router.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db), _: User = Depends(AuthProvider(superuser=True))):
    return user_crud.update_user(db, user=user, user_id=user_id)

@router.get("/users/{user_id}/teams", response_model=List[Team])
def read_user_teams(user_id: int, db: Session = Depends(get_db)):
    teams = user_crud.get_user_teams(db, user_id=user_id)
    if not teams:
        raise HTTPException(status_code=404, detail="User not found or is not in any teams")
    return teams
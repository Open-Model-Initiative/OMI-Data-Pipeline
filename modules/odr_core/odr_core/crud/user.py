# odr_core/crud/user.py
from sqlalchemy.orm import Session
from odr_core.models.user import User
from odr_core.models.team import Team
from odr_core.schemas.user import UserCreate
from typing import Optional, List
from datetime import datetime

def create_user(db: Session, user: UserCreate) -> User:
    # In a real application, you'd want to hash the password here
    fake_hashed_password = user.password + "_notreallyhashed"
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=fake_hashed_password,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user: User) -> User:
    db.merge(user)
    db.commit()
    return user

def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()

def delete_user(db: Session, user_id: int) -> None:
    db.query(User).filter(User.id == user_id).delete()
    db.commit()
    
def get_user_teams(db: Session, user_id: int) -> List[Team]:
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        return user.teams
    return []
# odr_core/crud/user.py
from sqlalchemy.orm import Session
from odr_core.models.user import User
from odr_core.models.team import Team
from odr_core.schemas.user import UserCreate, UserUpdate
from typing import Optional, List
from datetime import datetime
from argon2 import PasswordHasher

__password_hasher = PasswordHasher()

def create_user(db: Session, user: UserCreate) -> User:

    hashed_password = __password_hasher.hash(user.password)

    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user: UserUpdate, user_id: int) -> User:
    db_user = db.query(User).filter(User.id == user_id).first()

    if db_user:
        db_user.username = user.username
        db_user.email = user.email
        db_user.is_active = user.is_active
        db_user.is_superuser = user.is_superuser
        db_user.updated_at = datetime.now()
        db_user.hashed_password = __password_hasher.hash(user.password)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    return None

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


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = get_user_by_username(db, username)
    if not user:
        return None
    
    if not user.is_active:
        return None

    try:
        if __password_hasher.verify(user.hashed_password, password):
            return user
    except:
        # Password verification failed
        # TODO: Implement maximum number of failed login attempts
        pass
    return None
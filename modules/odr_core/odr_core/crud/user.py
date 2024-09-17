# odr_core/crud/user.py
from fastapi_sso import OpenID
from sqlalchemy.orm import Session
from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError
from odr_core.models.user import User, UserSession
from odr_core.models.team import Team
from odr_core.schemas.user import UserCreate, UserUpdate
from odr_core.config import settings
from typing import Optional, List
from datetime import datetime, timedelta, timezone
from argon2 import PasswordHasher

import uuid

password_hasher = PasswordHasher()


def create_user(db: Session, user: UserCreate) -> User:

    hashed_password = password_hasher.hash(user.password)

    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_user_from_openid(db: Session, openid: OpenID) -> User:
    desired_username = openid.display_name or openid.email.split("@")[0]

    username = desired_username
    i = 1
    while get_user_by_username(db, username):
        username = f"{desired_username}.{i}"
        i += 1

    db_user = User(
        username=username,
        email=openid.email,
        identity_provider=openid.provider,
        is_active=True,
        is_superuser=False,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
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
        db_user.updated_at = datetime.now(timezone.utc)

        if user.password:
            db_user.hashed_password = password_hasher.hash(user.password)
        db.commit()
        db.refresh(db_user)

        if not user.is_active or user.password:
            delete_user_sessions(db, user_id)

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

    delete_user_sessions(db, user_id)


def get_user_teams(db: Session, user_id: int) -> List[Team]:
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        return user.teams
    return []


def delete_user_sessions(db: Session, user_id: int) -> None:
    db.query(UserSession).filter(UserSession.user_id == user_id).delete()
    db.commit()


def get_user_session(db: Session, session_id: str) -> Optional[UserSession]:
    return db.query(UserSession).filter(UserSession.id == session_id).first()


def create_user_session(db: Session, user: User) -> UserSession:
    session = UserSession(
        id=str(uuid.uuid4()),
        user_id=user.id,
        created_at=datetime.now(timezone.utc),
        expires_at=datetime.now(timezone.utc) + timedelta(seconds=settings.SESSION_MAX_AGE_SECONDS)
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


def login_user(db: Session, username: str, password: str) -> Optional[UserSession]:
    user = verify_user(db, username, password)
    if not user:
        return None

    return create_user_session(db, user)


def login_openid_user(db: Session, openid: OpenID) -> Optional[UserSession]:
    user = verify_openid_user(db, openid)
    if not user:
        return None

    return create_user_session(db, user)


def logout_user(db: Session, session_id: str) -> bool:
    count = db.query(UserSession).filter(UserSession.id == session_id).delete()
    db.commit()
    if count == 0:
        return False
    else:
        return True


def verify_user(db: Session, username: str, password: str) -> Optional[User]:
    user = get_user_by_username(db, username)
    if not user:
        return None

    if not user.is_active:
        return None

    try:
        if password_hasher.verify(user.hashed_password, password):
            return user
    except ValueError as e:
        # Password verification failed
        # TODO: Implement maximum number of failed login attempts
        print(f"Password verification failed: {e}")
    except Exception as e:
        # Unexpected error occurred
        print(f"An unexpected error occurred during password verification: {e}")

    return None


def verify_openid_user(db: Session, openid: OpenID) -> Optional[User]:
    user = get_user_by_email(db, openid.email)
    if not user:
        return None

    if not user.is_active:
        return None

    if user.identity_provider != openid.provider:
        return None

    return user


# DCO
def update_user_dco_acceptance(db: Session, user_id: int, accepted: bool) -> Optional[User]:
    try:
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(dco_accepted=accepted, updated_at=datetime.now(timezone.utc))
            .returning(User)
        )
        result = db.execute(stmt)
        db.commit()
        return result.scalar_one_or_none()
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error updating user DCO acceptance: {e}")
        return None


def get_user_dco_status(db: Session, user_id: int) -> Optional[bool]:
    user = get_user(db, user_id)

    if user:
        return user.dco_accepted

    return None

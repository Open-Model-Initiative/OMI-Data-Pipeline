# odr_core/crud/user.py
from sqlalchemy.orm import Session
from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError
from odr_core.models.user import User
from typing import Optional
from datetime import datetime, timezone
from argon2 import PasswordHasher


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
    user = db.query(User).filter(User.id == user_id).first()

    if user:
        return user.dco_accepted

    return None

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyCookie
from typing import Annotated, Optional
from datetime import datetime, timezone

from odr_core.schemas.user import User
from odr_core.crud.user import get_user_session, logout_user
from odr_core.database import get_db

security = APIKeyCookie(name="session", auto_error=False)


def get_session_cookie(
    session: Annotated[Optional[str], Depends(security)]
) -> Optional[str]:
    return session


def get_session_user(
    session: Annotated[Optional[str], Depends(get_session_cookie)],
    db=Depends(get_db)
) -> Optional[User]:

    if session is None:
        return None

    session = get_user_session(db, session)
    if session is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session",
            headers={"WWW-Authenticate": "Cookie"},
        )

    if session.expires_at and session.expires_at < datetime.now(timezone.utc):
        logout_user(db, session.id)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired",
            headers={"WWW-Authenticate": "Cookie"},
        )

    return session.user

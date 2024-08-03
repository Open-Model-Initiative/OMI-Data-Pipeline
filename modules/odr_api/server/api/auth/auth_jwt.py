import jwt
from datetime import datetime, timedelta, timezone

from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPAuthorizationCredentials

from odr_core.config import settings
from odr_core.schemas.user import User
from odr_core.crud.user import get_user_by_username
from odr_core.database import get_db

from fastapi.security import OAuth2PasswordBearer

security = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/token")

def create_access_token(user: User, expires_delta: Optional[timedelta] = None):

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(seconds=settings.JWT_EXPIRATION_SECONDS)
    to_encode = {
        "sub": user.email,
        "username": user.username,
        "is_superuser": user.is_superuser,
        "exp": expire,
    }
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    except Exception:
        return None

def get_jwt_user(
    bearer: Annotated[Optional[HTTPAuthorizationCredentials], Depends(security)] = None,
    db=Depends(get_db)
) -> Optional[User]:
    if bearer is None:
        return None
    
    token = bearer.credentials
    payload = decode_access_token(token)

    user = None

    if payload:
        username = payload.get("username")
        user = get_user_by_username(db, username)

        # jwt tokens are stateless, so we need to check if the user is still active
        if user is not None and not user.is_active:
            user = None

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    return user
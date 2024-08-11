import jwt
from datetime import datetime, timedelta, timezone

from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPAuthorizationCredentials

from odr_core.config import settings
from odr_core.schemas.user import User, UserType
from odr_api.logger import get_logger
logger = get_logger(__name__)
security = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/token", auto_error=False)


def create_access_token(user: User, scope=[], expires_delta: Optional[timedelta] = None):
    logger.info(f"Getting token for {user}")
    if scope is None:
        scope = []

    if user.user_type != UserType.bot:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Only bots can authenticate with JWT. User type: {user.user_type}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(seconds=settings.JWT_EXPIRATION_SECONDS)

    def datetime_to_str(dt):
        return dt.isoformat() if dt else None

    to_encode = {
        "sub": {
            "username": user.username,
            "id": user.id,
            "email": user.email,
            "user_type": user.user_type.value,  # Convert enum to string
            "is_active": user.is_active,
            "created_at": datetime_to_str(user.created_at),
            "updated_at": datetime_to_str(user.updated_at),
            "is_superuser": user.is_superuser,
        },
        "exp": expire,
        "scope": scope,
        "iss": "odr",
        "aud": "odr",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(
            jwt=token,
            key=settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
            audience="odr",
            leeway=timedelta(seconds=settings.JWT_LEEWAY_SECONDS)
        )
        # Convert string dates back to datetime objects
        for date_field in ['created_at', 'updated_at']:
            if payload['sub'].get(date_field):
                payload['sub'][date_field] = datetime.fromisoformat(payload['sub'][date_field])
        payload['sub']['user_type'] = UserType(payload['sub']['user_type'])  # Convert back to enum
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    except Exception:
        return None


def get_jwt_user_with_scopes(
    bearer: Annotated[Optional[str], Depends(security)] = None,
) -> Optional[User]:

    if bearer is None:
        return None
    if type(bearer) is str:
        token = bearer
    else:
        token = bearer.credentials
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = User(**payload["sub"])
    scope: list[str] = payload["scope"]
    return user, scope

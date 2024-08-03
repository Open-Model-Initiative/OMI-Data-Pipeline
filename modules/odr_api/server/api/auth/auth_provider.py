from fastapi.security import OAuth2PasswordBearer, HTTPBasic
from fastapi import Depends, HTTPException
from typing import Annotated, Optional

from odr_core.schemas.user import User

basic_auth = HTTPBasic(auto_error=False)

from .auth_jwt import get_jwt_user
from .auth_basic import get_basic_auth_user


def authorized_user(
    jwt_user: Annotated[Optional[User], Depends(get_jwt_user)] = None,
    basic_user: Annotated[Optional[User], Depends(get_basic_auth_user)] = None
) -> Optional[User]:
    if jwt_user:
        return jwt_user
    if basic_user:
        return basic_user
    
    raise HTTPException(
        status_code=401,
        detail="Unauthorized"
    )

def authorized_superuser(
    user: User = Depends(authorized_user)
) -> Optional[User]:
    if user and user.is_superuser:
        return user
    return None
from fastapi import Depends, HTTPException
from typing import Annotated, Any, Optional

from odr_core.schemas.user import User

from .auth_jwt import get_jwt_user_with_scopes
from .auth_basic import get_basic_auth_user
from .auth_cookie_session import get_session_user

# import settings
from odr_core.config import settings


class AuthProvider:
    def __init__(self, superuser = False, scope: Optional[str] = None):
        self.superuser = superuser
        self.scope = scope
        pass

    def __call__(
        self,
        jwt_user_with_scope: Annotated[Optional[User], Depends(get_jwt_user_with_scopes)] = None,
        basic_user: Annotated[Optional[User], Depends(get_basic_auth_user)] = None,
        session_user: Annotated[Optional[User], Depends(get_session_user)] = None
    ) -> Optional[User]:

        if settings.SKIP_AUTH:
            if jwt_user_with_scope:
                return jwt_user_with_scope[0]
            if basic_user:
                return basic_user
            if session_user:
                return session_user
            return None

        user = None
        if jwt_user_with_scope:
            user, scopes = jwt_user_with_scope

            if self.scope and self.scope not in scopes:
                raise HTTPException(
                    status_code=403,
                    detail="Forbidden"
                )

        elif basic_user:
            user = basic_user
        elif session_user:
            user = session_user

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Unauthorized"
            )

        if self.superuser and not user.is_superuser:
            raise HTTPException(
                status_code=403,
                detail="Forbidden"
            )

        return user

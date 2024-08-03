from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Annotated, Optional

from odr_core.schemas.user import User
from odr_core.crud.user import authenticate_user
from odr_core.database import get_db

security = HTTPBasic(auto_error=False)


def get_basic_auth_user(
    credentials: Annotated[Optional[HTTPBasicCredentials], Depends(security)],
    db=Depends(get_db)
):
    if credentials is None:
        return None
    
    user = authenticate_user(db, credentials.username, credentials.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user
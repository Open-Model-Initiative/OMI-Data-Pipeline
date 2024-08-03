from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from odr_core.crud import user as user_crud
from odr_core.database import get_db
from odr_core.schemas.user import Token

from ..auth.auth_jwt import create_access_token

router = APIRouter(tags=["auth"])

@router.post("/auth/token", response_model=Token)
def login_for_access_token(db=Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = user_crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token = create_access_token(user=user)
    
    return Token(access_token=access_token, token_type="bearer")

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm

from odr_core.crud import user as user_crud
from odr_core.database import get_db
from odr_core.schemas.user import UserToken, UserLoginSession, UserLogin, UserLogout, User

from odr_api.api.auth.auth_jwt import create_access_token
from odr_api.api.auth.auth_cookie_session import get_session_cookie
from odr_api.api.auth import AuthProvider

router = APIRouter(tags=["auth"])


@router.post("/auth/token", response_model=UserToken)
def login_for_access_token(db=Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = user_crud.verify_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    scopes = form_data.scopes
    access_token = create_access_token(user=user, scopes=scopes)

    return UserToken(access_token=access_token, token_type="bearer")


@router.post("/auth/login", response_model=UserLoginSession)
def login(response: Response, user: UserLogin, db=Depends(get_db)):
    session = user_crud.login_user(db, user.username, user.password)

    if not session:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    response.set_cookie(key="session", value=session.id, httponly=True)

    return session


@router.post("/auth/logout")
def logout(db=Depends(get_db), session_cookie: str = Depends(get_session_cookie)):
    succesful = user_crud.logout_user(db, session_cookie)
    if not succesful:
        raise HTTPException(status_code=400, detail="Logout failed")

    return UserLogout()


@router.get("/auth/logout/all")
def logout_all(db=Depends(get_db), current_user: User = Depends(AuthProvider())):
    user_crud.delete_user_sessions(db, current_user.id)

    return UserLogout()

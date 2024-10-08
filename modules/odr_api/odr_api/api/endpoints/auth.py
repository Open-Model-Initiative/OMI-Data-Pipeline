from typing import Any, Dict, Union
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_sso.sso.base import OpenID, DiscoveryDocument
from httpx import AsyncClient

from odr_core.crud import user as user_crud
from odr_core.database import get_db
from odr_core.schemas.user import (
    UserToken,
    UserLoginSession,
    UserLogin,
    UserLogout,
    User,
)

from odr_api.api.auth.auth_jwt import create_access_token
from odr_api.api.auth.auth_cookie_session import get_session_cookie
from odr_api.api.auth import AuthProvider

from fastapi_sso.sso.google import GoogleSSO
from fastapi_sso.sso.github import GithubSSO
from fastapi_sso.sso.generic import create_provider

from sqlalchemy.orm import Session

from odr_core.config import settings


router = APIRouter(tags=["auth"])


@router.post("/auth/token", response_model=UserToken)
def login_for_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = user_crud.verify_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    scopes = form_data.scopes
    access_token = create_access_token(user=user, scope=scopes)

    return UserToken(access_token=access_token, token_type="bearer")


@router.post("/auth/login", response_model=UserLoginSession)
def login(response: Response, user: UserLogin, db: Session = Depends(get_db)):
    session = user_crud.login_user(db, user.username, user.password)

    if not session:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    response.set_cookie(key="session", value=session.id, httponly=True, secure=True)

    return session


@router.post("/auth/logout")
def logout(session_cookie: str = Depends(get_session_cookie), db: Session = Depends(get_db)):
    succesful = user_crud.logout_user(db, session_cookie)
    if not succesful:
        raise HTTPException(status_code=400, detail="Logout failed")

    return UserLogout()


@router.get("/auth/logout/all")
def logout_all(current_user: User = Depends(AuthProvider()), db: Session = Depends(get_db)):
    user_crud.delete_user_sessions(db, current_user.id)

    return UserLogout()


def oauth2_login_and_signup(
    request: Request,
    openid_user: OpenID,
    db: Session
):
    if not openid_user.email:
        raise HTTPException(status_code=400, detail="Unable to get user email")

    existing_user = user_crud.get_user_by_email(db, openid_user.email)
    if not existing_user:
        existing_user = user_crud.create_user_from_openid(db, openid_user)

    session = user_crud.login_openid_user(db, openid_user)
    if not session:
        raise HTTPException(status_code=401, detail="Different provider already used")

    response = RedirectResponse(url=f"{request.base_url}{settings.OAUTH2_REDIRECT_PATH}")
    response.set_cookie(key="session", value=session.id, httponly=True, secure=True)

    return response


# Google SSO
google_sso = GoogleSSO(
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
)


@router.get("/auth/google/login")
async def google_login(request: Request):
    with google_sso:
        return await google_sso.get_login_redirect(
            redirect_uri=request.url_for("google_callback")
        )


@router.get("/auth/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    with google_sso:
        try:
            user = await google_sso.verify_and_process(request)
        except Exception:
            raise HTTPException(status_code=401, detail="Failed to login with Google")
        return oauth2_login_and_signup(request, user, db)


# Github SSO
github_sso = GithubSSO(
    client_id=settings.GITHUB_CLIENT_ID,
    client_secret=settings.GITHUB_CLIENT_SECRET,
)


@router.get("/auth/github/login", description="Login with Github")
async def github_login(request: Request):
    with github_sso:
        return await github_sso.get_login_redirect(
            redirect_uri=request.url_for("github_callback")
        )


@router.get("/auth/github/callback")
async def github_callback(request: Request, db: Session = Depends(get_db)):
    with github_sso:
        try:
            user = await github_sso.verify_and_process(request)
        except Exception:
            raise HTTPException(status_code=401, detail="Failed to login with Github")
        return oauth2_login_and_signup(request, user, db)


# Discord SSO
def convert_discord_openid(
    response: Dict[str, Any], _client: Union[AsyncClient, None]
) -> OpenID:
    """Convert user information returned by OIDC"""

    if "user" not in response:
        raise HTTPException(status_code=400, detail="Invalid response from Discord")

    user = response["user"]

    return OpenID(
        id=user.get("id"),
        name=user.get("username"),
        email=user.get("email"),
        picture=user.get("avatar"),
        provider="discord",
    )


discovery_document: DiscoveryDocument = {
    "authorization_endpoint": "https://discord.com/oauth2/authorize",
    "token_endpoint": "https://discord.com/api/oauth2/token",
    "userinfo_endpoint": "https://discord.com/api/oauth2/@me",
}


DiscordSSO = create_provider(
    name="discord",
    default_scope=["identify", "email"],
    discovery_document=discovery_document,
    response_convertor=convert_discord_openid,
)


discord_sso = DiscordSSO(
    client_id=settings.DISCORD_CLIENT_ID,
    client_secret=settings.DISCORD_CLIENT_SECRET,
)


@router.get("/auth/discord/login")
async def discord_login(request: Request):
    with discord_sso:
        return await discord_sso.get_login_redirect(
            redirect_uri=request.url_for("discord_callback")
        )


@router.get("/auth/discord/callback")
async def discord_callback(request: Request, db: Session = Depends(get_db)):
    with discord_sso:
        try:
            user = await discord_sso.verify_and_process(request)
        except Exception:
            raise HTTPException(status_code=401, detail="Failed to login with Discord")
        return oauth2_login_and_signup(request, user, db)

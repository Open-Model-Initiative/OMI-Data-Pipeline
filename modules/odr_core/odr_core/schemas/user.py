from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from enum import Enum
import uuid

class UserType(str, Enum):
    user = "user"
    bot = "bot"

class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDBBase(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class User(UserInDBBase):
    user_type: UserType = UserType.user

class UserTeam(BaseModel):
    user_id: int
    team_id: int
    role: str

class UserInDB(UserInDBBase):
    hashed_password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserLoginSession(BaseModel):
    id: uuid.UUID
    created_at: datetime
    expires_at: Optional[datetime]

class UserLogout(BaseModel):
    pass    

class UserToken(BaseModel):
    access_token: str
    token_type: str

from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class TeamBase(BaseModel):
    name: str


class TeamCreate(TeamBase):
    pass


class TeamUpdate(TeamBase):
    pass


class TeamInDBBase(TeamBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Team(TeamInDBBase):
    name: str
    permissions: Optional[List[str]] = []
    limits: Optional[dict] = {}


class TeamWithMembers(Team):
    members: List[int]  # List of user IDs

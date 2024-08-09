from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime
from enum import Enum


class ContentType(str, Enum):
    IMAGE = "image"
    VIDEO = "video"
    VOICE = "voice"
    MUSIC = "music"
    TEXT = "text"


class ContentStatus(str, Enum):
    PENDING = "pending"
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    DELISTED = "delisted"


class ContentAuthorBase(BaseModel):
    name: str
    url: Optional[HttpUrl] = None


class ContentAuthorCreate(ContentAuthorBase):
    pass


class ContentAuthor(ContentAuthorBase):
    id: int
    content_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attribute = True


class ContentBase(BaseModel):
    name: Optional[str] = None
    type: ContentType
    hash: str
    phash: str
    url: Optional[List[HttpUrl]] = None
    width: Optional[int] = None
    height: Optional[int] = None
    format: str
    size: int
    status: ContentStatus = ContentStatus.PENDING
    license: str
    license_url: Optional[HttpUrl] = None
    flags: int = 0
    meta: Optional[dict] = None


class ContentCreate(ContentBase):
    from_user_id: int
    from_team_id: Optional[int] = None
    content_authors: Optional[List[ContentAuthorCreate]] = None


class ContentUpdate(ContentBase):
    pass


class Content(ContentBase):
    id: int
    from_user_id: int
    from_team_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    content_authors: List[ContentAuthor] = []
    # TODO: It is raising errors, fix it
    # annotations_id: List[int] = []  # List of annotation IDs
    # embeddings: List[int] = []  # List of embedding IDs

    class Config:
        from_attribute = True


def httpurl_to_str(url: Optional[HttpUrl]) -> Optional[str]:
    return str(url) if url else None

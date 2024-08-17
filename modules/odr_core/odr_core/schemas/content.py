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


class ContentSourceType(str, Enum):
    URL = "url"
    PATH = "path"
    HUGGING_FACE = "hugging_face"


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


class ContentSourceBase(BaseModel):
    type: ContentSourceType
    value: str
    source_metadata: Optional[dict] = None


class ContentSourceCreate(ContentSourceBase):
    id: Optional[int] = None


class ContentSourceUpdate(ContentSourceBase):
    id: int


class ContentSource(ContentSourceBase):
    id: int
    content_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attribute = True


class ContentBase(BaseModel):
    name: Optional[str] = None
    type: ContentType
    hash: str
    phash: str
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
    content_authors: Optional[List[ContentAuthorCreate]] = None
    sources: List[ContentSourceCreate]


class ContentUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[ContentType] = None
    hash: Optional[str] = None
    phash: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    format: Optional[str] = None
    size: Optional[int] = None
    status: Optional[ContentStatus] = None
    license: Optional[str] = None
    license_url: Optional[HttpUrl] = None
    flags: Optional[int] = None
    meta: Optional[dict] = None
    sources: Optional[List[ContentSourceCreate]] = None


class Content(ContentBase):
    id: int
    from_user_id: int
    from_team_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    content_authors: List[ContentAuthor] = []
    sources: List[ContentSource] = []

    class Config:
        from_attribute = True


def httpurl_to_str(url: Optional[HttpUrl]) -> Optional[str]:
    return str(url) if url else None

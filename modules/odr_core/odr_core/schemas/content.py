from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime
from enum import Enum


class ContentType(str, Enum):
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    VOICE = "VOICE"
    MUSIC = "MUSIC"
    TEXT = "TEXT"


class ContentStatus(str, Enum):
    PENDING = "PENDING"
    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"
    DELISTED = "DELISTED"


class ContentSourceType(str, Enum):
    URL = "URL"
    PATH = "PATH"
    HUGGING_FACE = "HUGGING_FACE"


class ContentAuthorBase(BaseModel):
    name: str
    url: Optional[HttpUrl] = None


class ContentAuthorCreate(ContentAuthorBase):
    pass


class ContentAuthorUpdate(ContentAuthorBase):
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
    url: List[HttpUrl] = []
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


class ContentEventBase(BaseModel):
    content_id: int
    status: ContentStatus
    set_by: int
    note: Optional[str] = None


class ContentEventCreate(ContentEventBase):
    pass


class ContentEventUpdate(BaseModel):
    status: Optional[ContentStatus] = None
    note: Optional[str] = None


class ContentEvent(ContentEventBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


def httpurl_to_str(url: Optional[HttpUrl]) -> Optional[str]:
    return str(url) if url else None

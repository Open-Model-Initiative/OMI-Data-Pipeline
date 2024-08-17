from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Enum,
    JSON,
    Boolean,
    ForeignKey,
    ARRAY,
    DateTime,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from odr_core.models.base import Base
import enum


class ContentType(enum.Enum):
    IMAGE = "image"
    VIDEO = "video"
    VOICE = "voice"
    MUSIC = "music"
    TEXT = "text"


class ContentStatus(enum.Enum):
    PENDING = "pending"
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    DELISTED = "delisted"


class ContentSourceType(enum.Enum):
    URL = "url"
    PATH = "path"
    HUGGING_FACE = "hugging_face"


class Content(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    type = Column(Enum(ContentType))
    hash = Column(String, index=True)
    phash = Column(String, index=True)
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    format = Column(String)
    size = Column(Integer)
    status = Column(Enum(ContentStatus), default=ContentStatus.PENDING)
    license = Column(String)
    license_url = Column(String, nullable=True)
    flags = Column(Integer, default=0)
    meta = Column(JSON, nullable=True)
    from_user_id = Column(Integer, ForeignKey("users.id"))
    from_team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    from_user = relationship("User", back_populates="contents")
    from_team = relationship("Team", back_populates="contents")
    content_authors = relationship("ContentAuthor", back_populates="content")
    annotations = relationship("Annotation", back_populates="content")
    embeddings = relationship("ContentEmbedding", back_populates="content")
    sources = relationship("ContentSource", back_populates="content", cascade="all,delete-orphan")


class ContentAuthor(Base):
    __tablename__ = "content_authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    url = Column(String, nullable=True)
    content_id = Column(Integer, ForeignKey("contents.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    content = relationship("Content", back_populates="content_authors")


class ContentSource(Base):
    __tablename__ = "content_sources"

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("contents.id"))
    type = Column(Enum(ContentSourceType))
    value = Column(String, unique=True)
    source_metadata = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    content = relationship("Content", back_populates="sources")

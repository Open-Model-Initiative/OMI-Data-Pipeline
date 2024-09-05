from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum,
    JSON,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from odr_core.models.base import Base
from odr_core.enums import ContentType, ContentStatus, ContentSourceType, ReportStatus
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import PickleType


class Content(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    type = Column(Enum(ContentType))
    type = Column(Enum(ContentType))
    hash = Column(String, index=True)
    phash = Column(String, index=True)
    url = Column(MutableList.as_mutable(PickleType), nullable=True)
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
    annotations = relationship("Annotation", back_populates="content")
    embeddings = relationship("ContentEmbedding", back_populates="content")
    sources = relationship("ContentSource", back_populates="content", cascade="all,delete-orphan")
    events = relationship("ContentEvents", back_populates="content")
    reports = relationship("ContentReport", back_populates="content")
    content_authors = relationship("ContentAuthor", back_populates="content")
    content_sets = relationship("ContentSet", secondary="content_set_items", back_populates="contents")


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
    source_metadata = Column(String, nullable=True)  # JSON
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    content = relationship("Content", back_populates="sources")


class ContentEvents(Base):
    __tablename__ = "content_events"

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("contents.id"), nullable=False)
    status = Column(Enum(ContentStatus), nullable=False)
    set_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    note = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    content = relationship("Content", back_populates="events")
    user = relationship("User", back_populates="content_events")


class ContentReport(Base):
    __tablename__ = "content_reports"

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("contents.id"), nullable=False)
    reporter_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reason = Column(String, nullable=False)
    description = Column(String)
    status = Column(Enum(ReportStatus), default=ReportStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=False, server_default=func.now())

    content = relationship("Content", back_populates="reports")
    reporter = relationship("User", back_populates="content_reports")


class ContentSet(Base):
    __tablename__ = "content_sets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=False, server_default=func.now())

    created_by = relationship("User", back_populates="content_sets")
    contents = relationship("Content", secondary="content_set_items", back_populates="content_sets")


class ContentSetItem(Base):
    __tablename__ = "content_set_items"

    content_set_id = Column(Integer, ForeignKey("content_sets.id"), primary_key=True)
    content_id = Column(Integer, ForeignKey("contents.id"), primary_key=True)
    added_at = Column(DateTime(timezone=True), server_default=func.now())

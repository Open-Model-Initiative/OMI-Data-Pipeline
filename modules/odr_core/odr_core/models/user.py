from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    ForeignKey,
    UUID,
    Enum,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from odr_core.models.base import Base
from odr_core.schemas.user import UserType


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    identity_provider = Column(String, index=True, default="omi")
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    teams = relationship("Team", secondary="user_teams", back_populates="members")
    contents = relationship("Content", back_populates="from_user")
    annotations = relationship("Annotation", back_populates="from_user")
    annotation_embeddings = relationship(
        "AnnotationEmbedding", back_populates="from_user"
    )
    content_embeddings = relationship("ContentEmbedding", back_populates="from_user")
    annotation_ratings = relationship("AnnotationRating", back_populates="rated_by")
    annotation_reports = relationship("AnnotationReport", back_populates="reported_by")
    added_annotation_sources = relationship(
        "AnnotationSource", back_populates="added_by"
    )
    sessions = relationship("UserSession", back_populates="user")
    user_type = Column(Enum(UserType), default=UserType.user)

    content_events = relationship("ContentEvents", back_populates="user")
    content_reports = relationship("ContentReport", back_populates="reporter")
    content_sets = relationship("ContentSet", back_populates="created_by")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"


class UserSession(Base):
    __tablename__ = "sessions"

    id = Column(UUID, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="sessions")

    def __repr__(self):
        return f"<UserSession(id={self.id}, user_id={self.user_id}, created_at={self.created_at}, expires_at={self.expires_at})>"

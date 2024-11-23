# SPDX-License-Identifier: Apache-2.0
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    ForeignKey,
    UUID,
    Enum,
    BigInteger
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from odr_core.models.base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    email = Column(String(255))
    emailVerified = Column(DateTime(timezone=True))
    image = Column(String)
    identity_provider = Column(String, index=True, default="omi")
    hashed_password = Column(String)
    is_active = Column(Boolean, nullable=False, default=True)
    is_superuser = Column(Boolean, nullable=False, default=False)
    dco_accepted = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    image = Column(String, nullable=True)
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

    content_events = relationship("ContentEvents", back_populates="user")
    content_reports = relationship("ContentReport", back_populates="reporter")
    content_sets = relationship("ContentSet", back_populates="created_by")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.name}, email={self.email})>"


class VerificationToken(Base):
    __tablename__ = 'verification_token'

    identifier = Column(String, primary_key=True)
    token = Column(String, primary_key=True)
    expires = Column(DateTime(timezone=True), nullable=False)


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(String(255), nullable=False)
    provider = Column(String(255), nullable=False)
    providerAccountId = Column(String(255), nullable=False)
    refresh_token = Column(String)
    access_token = Column(String)
    expires_at = Column(BigInteger)
    id_token = Column(String)
    scope = Column(String)
    session_state = Column(String)
    token_type = Column(String)


class UserSession(Base):
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer, ForeignKey("users.id"), nullable=False)
    expires = Column(DateTime(timezone=True), nullable=False)
    sessionToken = Column(String(255), nullable=False)

    user = relationship("User", back_populates="sessions")

    def __repr__(self):
        return f"<UserSession(id={self.id}, userId={self.userId}, expires_at={self.expires}, sessionToken={self.sessionToken})>"

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from odr_core.models.base import Base


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship with User
    members = relationship("User", secondary="user_teams", back_populates="teams")
    contents = relationship("Content", back_populates="from_team")
    annotations = relationship("Annotation", back_populates="from_team")
    annotation_embeddings = relationship("AnnotationEmbedding", back_populates="from_team")
    content_embeddings = relationship("ContentEmbedding", back_populates="from_team")


class UserTeam(Base):
    __tablename__ = "user_teams"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    team_id = Column(Integer, ForeignKey("teams.id"), primary_key=True)
    role = Column(String)  # e.g., 'admin', 'member'

    user = relationship("User", back_populates="team_users")
    team = relationship("Team", back_populates="team_users")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

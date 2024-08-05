from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from odr_core.models.base import Base


class Annotation(Base):
    __tablename__ = "annotations"

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey('contents.id'))
    annotation = Column(JSON)
    manually_adjusted = Column(Boolean, default=False)
    overall_rating = Column(Float, nullable=True)
    from_user_id = Column(Integer, ForeignKey('users.id'))
    from_team_id = Column(Integer, ForeignKey('teams.id'), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    content = relationship("Content", back_populates="annotations")
    from_user = relationship("User", back_populates="annotations")
    from_team = relationship("Team", back_populates="annotations")
    annotation_sources = relationship("AnnotationSource", secondary="annotation_sources_link", back_populates="annotations")
    embeddings = relationship("AnnotationEmbedding", back_populates="annotation")
    ratings = relationship("AnnotationRating", back_populates="annotation")
    reports = relationship("AnnotationReport", back_populates="annotation")


class AnnotationRating(Base):
    __tablename__ = "annotation_ratings"

    id = Column(Integer, primary_key=True, index=True)
    annotation_id = Column(Integer, ForeignKey('annotations.id'))
    rating = Column(Integer)  # Assuming a scale of 0-10
    reason = Column(String, nullable=True)
    rated_by_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    annotation = relationship("Annotation", back_populates="ratings")
    rated_by = relationship("User", back_populates="annotation_ratings")


class AnnotationReport(Base):
    __tablename__ = "annotation_reports"

    id = Column(Integer, primary_key=True, index=True)
    annotation_id = Column(Integer, ForeignKey('annotations.id'))
    type = Column(String)  # e.g., 'illegal content', 'malicious annotations'
    reported_by_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    annotation = relationship("Annotation", back_populates="reports")
    reported_by = relationship("User", back_populates="annotation_reports")


class AnnotationSource(Base):
    __tablename__ = "annotation_sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    ecosystem = Column(String, nullable=True)
    type = Column(String)  # e.g., 'content description', 'spatial analysis', 'tags'
    annotation_schema = Column(JSON)
    license = Column(String)
    license_url = Column(String, nullable=True)
    added_by_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    annotations = relationship("Annotation", secondary="annotation_sources_link", back_populates="annotation_sources")
    added_by = relationship("User", back_populates="added_annotation_sources")


class AnnotationSourceLink(Base):
    __tablename__ = "annotation_sources_link"

    annotation_id = Column(Integer, ForeignKey('annotations.id'), primary_key=True)
    annotation_source_id = Column(Integer, ForeignKey('annotation_sources.id'), primary_key=True)

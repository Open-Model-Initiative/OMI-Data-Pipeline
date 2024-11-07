from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timezone

from odr_core.models.annotation import AnnotationSource
from odr_core.schemas.annotation import AnnotationSourceCreate, AnnotationSourceUpdate
import logging

logger = logging.getLogger(__name__)


def create_annotation_source(
    db: Session, annotation_source: AnnotationSourceCreate
) -> AnnotationSource:
    db_annotation_source = AnnotationSource(
        name=annotation_source.name,
        ecosystem=annotation_source.ecosystem,
        type=annotation_source.type,
        annotation_schema=annotation_source.annotation_schema,
        license=annotation_source.license,
        license_url=annotation_source.license_url,
        added_by_id=annotation_source.added_by_id,
        updated_at=datetime.now(timezone.utc),
    )
    db.add(db_annotation_source)
    db.commit()
    db.refresh(db_annotation_source)
    return db_annotation_source


def get_annotation_source(
    db: Session, annotation_source_id: int
) -> Optional[AnnotationSource]:
    return (
        db.query(AnnotationSource)
        .filter(AnnotationSource.id == annotation_source_id)
        .first()
    )


def get_annotation_sources(
    db: Session, skip: int = 0, limit: int = 100
) -> List[AnnotationSource]:
    return db.query(AnnotationSource).offset(skip).limit(limit).all()


def update_annotation_source(
    db: Session,
    annotation_source_id: int,
    annotation_source_update: AnnotationSourceUpdate,
) -> Optional[AnnotationSource]:
    db_annotation_source = (
        db.query(AnnotationSource)
        .filter(AnnotationSource.id == annotation_source_id)
        .first()
    )
    if db_annotation_source is None:
        return None

    update_data = annotation_source_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_annotation_source, key, value)

    db_annotation_source.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(db_annotation_source)
    return db_annotation_source


def delete_annotation_source(db: Session, annotation_source_id: int) -> bool:
    db_annotation_source = (
        db.query(AnnotationSource)
        .filter(AnnotationSource.id == annotation_source_id)
        .first()
    )
    if db_annotation_source is None:
        return False

    db.delete(db_annotation_source)
    db.commit()
    return True

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from datetime import datetime

from odr_core.models.annotation import Annotation, AnnotationSource
from odr_core.schemas.annotation import AnnotationCreate, AnnotationUpdate

def create_annotation(db: Session, annotation: AnnotationCreate) -> Annotation:
    db_annotation = Annotation(
        content_id=annotation.content_id,
        annotation=annotation.annotation,
        manually_adjusted=annotation.manually_adjusted,
        overall_rating=annotation.overall_rating,
        from_user_id=annotation.from_user_id,
        from_team_id=annotation.from_team_id,
        updated_at=datetime.now()
    )
    
    if annotation.annotation_source_ids:
        db_annotation.annotation_sources = db.query(AnnotationSource).filter(
            AnnotationSource.id.in_(annotation.annotation_source_ids)
        ).all()
    
    db.add(db_annotation)
    db.commit()
    db.refresh(db_annotation)
    return db_annotation

def get_annotation(db: Session, annotation_id: int) -> Optional[Annotation]:
    return db.query(Annotation).filter(Annotation.id == annotation_id).first()

def get_annotations(db: Session, skip: int = 0, limit: int = 100) -> List[Annotation]:
    return db.query(Annotation).offset(skip).limit(limit).all()

def update_annotation(db: Session, annotation_id: int, annotation_update: AnnotationUpdate) -> Optional[Annotation]:
    db_annotation = db.query(Annotation).filter(Annotation.id == annotation_id).first()
    if db_annotation is None:
        return None
    
    update_data = annotation_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_annotation, key, value)
    
    if 'annotation_source_ids' in update_data:
        db_annotation.annotation_sources = db.query(AnnotationSource).filter(
            AnnotationSource.id.in_(update_data['annotation_source_ids'])
        ).all()
    
    db.commit()
    db.refresh(db_annotation)
    return db_annotation

def delete_annotation(db: Session, annotation_id: int) -> bool:
    db_annotation = db.query(Annotation).filter(Annotation.id == annotation_id).first()
    if db_annotation is None:
        return False
    
    db.delete(db_annotation)
    db.commit()
    return True

def get_annotations_by_content(db: Session, content_id: int, skip: int = 0, limit: int = 100) -> List[Annotation]:
    return db.query(Annotation).filter(Annotation.content_id == content_id).offset(skip).limit(limit).all()

def get_annotations_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Annotation]:
    return db.query(Annotation).filter(Annotation.from_user_id == user_id).offset(skip).limit(limit).all()

def get_annotations_by_team(db: Session, team_id: int, skip: int = 0, limit: int = 100) -> List[Annotation]:
    return db.query(Annotation).filter(Annotation.from_team_id == team_id).offset(skip).limit(limit).all()
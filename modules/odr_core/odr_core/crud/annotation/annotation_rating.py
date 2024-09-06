from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timezone

from odr_core.models.annotation import AnnotationRating
from odr_core.schemas.annotation import AnnotationRatingCreate, AnnotationRatingUpdate
from odr_core.schemas.user import User


def create_annotation_rating(
    db: Session, annotation_rating: AnnotationRatingCreate, current_user: User
) -> AnnotationRating:
    db_annotation_rating = AnnotationRating(
        annotation_id=annotation_rating.annotation_id,
        rated_by_id=annotation_rating.rated_by_id,
        rating=annotation_rating.rating,
        reason=annotation_rating.reason,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db.add(db_annotation_rating)
    db.commit()
    db.refresh(db_annotation_rating)
    return db_annotation_rating


def get_annotation_rating(db: Session, rating_id: int) -> Optional[AnnotationRating]:
    return db.query(AnnotationRating).filter(AnnotationRating.id == rating_id).first()


def get_annotation_ratings_by_annotation(
    db: Session, annotation_id: int, skip: int = 0, limit: int = 100
) -> List[AnnotationRating]:
    return (
        db.query(AnnotationRating)
        .filter(AnnotationRating.annotation_id == annotation_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_annotation_ratings(
    db: Session, skip: int = 0, limit: int = 100
) -> List[AnnotationRating]:
    return db.query(AnnotationRating).offset(skip).limit(limit).all()


def update_annotation_rating(
    db: Session,
    rating_id: int,
    annotation_rating_update: AnnotationRatingUpdate,
) -> Optional[AnnotationRating]:
    db_annotation_rating = (
        db.query(AnnotationRating).filter(AnnotationRating.id == rating_id).first()
    )
    if db_annotation_rating is None:
        return None

    update_data = annotation_rating_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_annotation_rating, key, value)
    db_annotation_rating.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(db_annotation_rating)
    return db_annotation_rating


def delete_annotation_rating(db: Session, rating_id: int) -> bool:
    db_annotation_rating = (
        db.query(AnnotationRating).filter(AnnotationRating.id == rating_id).first()
    )
    if db_annotation_rating is None:
        return False

    db.delete(db_annotation_rating)
    db.commit()
    return True

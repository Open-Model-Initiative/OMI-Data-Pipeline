from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from odr_core.crud.annotation.annotation_rating import (
    create_annotation_rating,
    get_annotation_rating,
    get_annotation_ratings_by_annotation,
    update_annotation_rating,
    delete_annotation_rating,
)
from odr_core.schemas.annotation import (
    AnnotationRatingCreate,
    AnnotationRatingUpdate,
    AnnotationRating,
)
from odr_core.database import get_db
from odr_core.schemas.user import User


router = APIRouter(tags=["annotation_rating"])


@router.post("/annotation_ratings/", response_model=AnnotationRating)
def create_annotation_rating_endpoint(
    annotation_rating: AnnotationRatingCreate,
    db: Session = Depends(get_db)
):
    return create_annotation_rating(
        db=db, annotation_rating=annotation_rating
    )


@router.get("/annotation_ratings/{rating_id}", response_model=AnnotationRating)
def read_annotation_rating_endpoint(rating_id: int, db: Session = Depends(get_db)):
    db_annotation_rating = get_annotation_rating(db, rating_id=rating_id)
    if db_annotation_rating is None:
        raise HTTPException(status_code=404, detail="Annotation rating not found")
    return db_annotation_rating


@router.get(
    "/annotations/{annotation_id}/ratings", response_model=List[AnnotationRating]
)
def read_annotation_ratings_by_annotation_endpoint(
    annotation_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    annotation_ratings = get_annotation_ratings_by_annotation(
        db, annotation_id=annotation_id, skip=skip, limit=limit
    )
    return annotation_ratings


@router.put("/annotation_ratings/{rating_id}", response_model=AnnotationRating)
def update_annotation_rating_endpoint(
    rating_id: int,
    annotation_rating: AnnotationRatingUpdate,
    db: Session = Depends(get_db)
):
    db_annotation_rating = update_annotation_rating(
        db,
        rating_id=rating_id,
        annotation_rating_update=annotation_rating
    )
    if db_annotation_rating is None:
        raise HTTPException(status_code=404, detail="Annotation rating not found")
    return db_annotation_rating


@router.delete("/annotation_ratings/{rating_id}", response_model=bool)
def delete_annotation_rating_endpoint(
    rating_id: int,
    db: Session = Depends(get_db)
):
    success = delete_annotation_rating(db, rating_id=rating_id)
    if not success:
        raise HTTPException(status_code=404, detail="Annotation rating not found")
    return success

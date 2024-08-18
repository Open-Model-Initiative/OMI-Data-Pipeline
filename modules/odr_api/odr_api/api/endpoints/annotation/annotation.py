from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from odr_core.crud.annotation import (
    create_annotation,
    get_annotation,
    get_annotations,
    update_annotation,
    delete_annotation,
    get_annotations_by_content,
)
from odr_core.schemas.annotation import AnnotationCreate, AnnotationUpdate, Annotation
from odr_core.database import get_db

from odr_api.api.auth import AuthProvider

router = APIRouter(tags=["annotation"])


@router.post("/annotations/", response_model=Annotation)
def create_annotation_endpoint(
    annotation: AnnotationCreate,
    db: Session = Depends(get_db),
    _=Depends(AuthProvider()),
):
    return create_annotation(db=db, annotation=annotation)


@router.get("/annotations/{annotation_id}", response_model=Annotation)
def read_annotation_endpoint(annotation_id: int, db: Session = Depends(get_db)):
    db_annotation = get_annotation(db, annotation_id=annotation_id)
    if db_annotation is None:
        raise HTTPException(status_code=404, detail="Annotation not found")
    return db_annotation


@router.get("/annotations/", response_model=List[Annotation])
def read_annotations_endpoint(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    annotations = get_annotations(db, skip=skip, limit=limit)
    return annotations


@router.put("/annotations/{annotation_id}", response_model=Annotation)
def update_annotation_endpoint(
    annotation_id: int,
    annotation: AnnotationUpdate,
    db: Session = Depends(get_db),
    _=Depends(AuthProvider()),
):
    db_annotation = update_annotation(
        db, annotation_id=annotation_id, annotation_update=annotation
    )
    if db_annotation is None:
        raise HTTPException(status_code=404, detail="Annotation not found")
    return db_annotation


@router.delete("/annotations/{annotation_id}", response_model=bool)
def delete_annotation_endpoint(
    annotation_id: int, db: Session = Depends(get_db), _=Depends(AuthProvider())
):
    success = delete_annotation(db, annotation_id=annotation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Annotation not found")
    return success


@router.get("/contents/{content_id}/annotations/", response_model=List[Annotation])
def read_annotations_by_content_endpoint(
    content_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    annotations = get_annotations_by_content(
        db, content_id=content_id, skip=skip, limit=limit
    )
    return annotations

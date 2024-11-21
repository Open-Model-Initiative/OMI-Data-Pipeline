# SPDX-License-Identifier: Apache-2.0
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from odr_core.crud.annotation.annotation_source import (
    create_annotation_source,
    get_annotation_source,
    get_annotation_sources,
    update_annotation_source,
    delete_annotation_source,
)
from odr_core.schemas.annotation import (
    AnnotationSourceCreate,
    AnnotationSourceUpdate,
    AnnotationSource,
)
from odr_core.database import get_db


router = APIRouter(tags=["annotation_source"])


@router.post("/annotation_sources/", response_model=AnnotationSource)
def create_annotation_source_endpoint(
    annotation_source: AnnotationSourceCreate,
    db: Session = Depends(get_db)
):
    return create_annotation_source(
        db=db, annotation_source=annotation_source
    )


@router.get(
    "/annotation_sources/{annotation_source_id}", response_model=AnnotationSource
)
def read_annotation_source_endpoint(
    annotation_source_id: int, db: Session = Depends(get_db)
):
    db_annotation_source = get_annotation_source(
        db, annotation_source_id=annotation_source_id
    )
    if db_annotation_source is None:
        raise HTTPException(status_code=404, detail="Annotation source not found")
    return db_annotation_source


@router.get("/annotation_sources/", response_model=List[AnnotationSource])
def read_annotation_sources_endpoint(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    annotation_sources = get_annotation_sources(db, skip=skip, limit=limit)
    return annotation_sources


@router.put(
    "/annotation_sources/{annotation_source_id}", response_model=AnnotationSource
)
def update_annotation_source_endpoint(
    annotation_source_id: int,
    annotation_source: AnnotationSourceUpdate,
    db: Session = Depends(get_db)
):
    db_annotation_source = update_annotation_source(
        db,
        annotation_source_id=annotation_source_id,
        annotation_source_update=annotation_source
    )
    if db_annotation_source is None:
        raise HTTPException(status_code=404, detail="Annotation source not found")
    return db_annotation_source


@router.delete("/annotation_sources/{annotation_source_id}", response_model=bool)
def delete_annotation_source_endpoint(
    annotation_source_id: int,
    db: Session = Depends(get_db)
):
    success = delete_annotation_source(db, annotation_source_id=annotation_source_id)
    if not success:
        raise HTTPException(status_code=404, detail="Annotation source not found")
    return success

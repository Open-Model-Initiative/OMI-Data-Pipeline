from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from odr_core.crud import content as content_crud
from odr_core.schemas.content import (
    Content,
    ContentCreate,
    ContentUpdate,
    ContentSource,
    ContentSourceCreate,
    ContentSourceUpdate,
)
from odr_core.database import get_db


router = APIRouter(tags=["content"])


@router.post("/content/", response_model=Content)
def create_content(
    content: ContentCreate,
    db: Session = Depends(get_db)
):
    try:
        return content_crud.create_content(
            db=db, content=content
        )
    except IntegrityError as e:
        if "content_sources_value_key" in str(e):
            raise HTTPException(
                status_code=400,
                detail="A content source with this value already exists."
            )
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


@router.get("/content/{content_id}", response_model=Content)
def read_content(content_id: int, db: Session = Depends(get_db)):
    db_content = content_crud.get_content(db, content_id=content_id)
    if db_content is None:
        raise HTTPException(status_code=404, detail="Content not found")
    return db_content


@router.get("/content/", response_model=List[Content])
def read_contents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contents = content_crud.get_contents(db, skip=skip, limit=limit)
    return contents


@router.put("/content/{content_id}", response_model=Content)
def update_content(
    content_id: int,
    content: ContentUpdate,
    db: Session = Depends(get_db)
):
    db_content = content_crud.update_content(db, content_id=content_id, content=content)
    if db_content is None:
        raise HTTPException(status_code=404, detail="Content not found")
    return db_content


@router.delete("/content/{content_id}")
def delete_content(
    content_id: int,
    db: Session = Depends(get_db)
):
    success = content_crud.delete_content(db, content_id=content_id)
    if not success:
        raise HTTPException(status_code=404, detail="Content not found")
    return {"message": "Content deleted successfully"}


@router.get("/content/hash/{hash}", response_model=Content)
def get_content_by_hash(hash: str, db: Session = Depends(get_db)):
    db_content = content_crud.get_content_by_hash(db, hash=hash)
    if db_content is None:
        raise HTTPException(status_code=404, detail="Content not found")
    return db_content


@router.get("/users/{user_id}/content", response_model=List[Content])
def get_contents_by_user(
    user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    contents = content_crud.get_contents_by_user(
        db, user_id=user_id, skip=skip, limit=limit
    )
    if not contents:
        raise HTTPException(status_code=404, detail="User not found or has no content")
    return contents


@router.get("/teams/{team_id}/content", response_model=List[Content])
def get_contents_by_team(
    team_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    contents = content_crud.get_contents_by_team(
        db, team_id=team_id, skip=skip, limit=limit
    )
    if not contents:
        raise HTTPException(status_code=404, detail="Team not found or has no content")
    return contents


# content source endpoints


@router.post("/content/{content_id}/sources/", response_model=ContentSource)
def create_content_source(
    content_id: int,
    source: ContentSourceCreate,
    db: Session = Depends(get_db)
):
    db_content = content_crud.get_content(db, content_id=content_id)
    if db_content is None:
        raise HTTPException(status_code=404, detail="Content not found")
    return content_crud.create_content_source(
        db=db, content_id=content_id, source=source
    )


@router.get("/content/{content_id}/sources/", response_model=List[ContentSource])
def read_content_sources(content_id: int, db: Session = Depends(get_db)):
    db_content = content_crud.get_content(db, content_id=content_id)
    if db_content is None:
        raise HTTPException(status_code=404, detail="Content not found")
    return content_crud.get_content_sources(db, content_id=content_id)


@router.get("/content/sources/{source_id}", response_model=ContentSource)
def read_content_source(source_id: int, db: Session = Depends(get_db)):
    db_source = content_crud.get_content_source(db, source_id=source_id)
    if db_source is None:
        raise HTTPException(status_code=404, detail="Content source not found")
    return db_source


@router.put("/content/sources/{source_id}", response_model=ContentSource)
def update_content_source(
    source_id: int,
    source: ContentSourceUpdate,
    db: Session = Depends(get_db)
):
    db_source = content_crud.update_content_source(
        db, source_id=source_id, source=source
    )
    if db_source is None:
        raise HTTPException(status_code=404, detail="Content source not found")
    return db_source


@router.delete("/content/sources/{source_id}")
def delete_content_source(
    source_id: int,
    db: Session = Depends(get_db)
):
    success = content_crud.delete_content_source(db, source_id=source_id)
    if not success:
        raise HTTPException(status_code=404, detail="Content source not found")
    return {"message": "Content source deleted successfully"}

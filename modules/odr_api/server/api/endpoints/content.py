from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from odr_core.crud import content as content_crud
from odr_core.schemas.content import Content, ContentCreate, ContentUpdate
from odr_core.database import get_db

from ..auth.auth_provider import authorized_user, authorized_superuser

router = APIRouter(tags=["content"])

@router.post("/content/", response_model=Content)
def create_content(content: ContentCreate, db: Session = Depends(get_db), current_user = Depends(authorized_user)):
    return content_crud.create_content(db=db, content=content)

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
def update_content(content_id: int, content: ContentUpdate, db: Session = Depends(get_db), current_user = Depends(authorized_user)):
    db_content = content_crud.update_content(db, content_id=content_id, content=content)
    if db_content is None:
        raise HTTPException(status_code=404, detail="Content not found")
    return db_content

@router.delete("/content/{content_id}")
def delete_content(content_id: int, db: Session = Depends(get_db), current_user = Depends(authorized_user)):
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
def get_contents_by_user(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contents = content_crud.get_contents_by_user(db, user_id=user_id, skip=skip, limit=limit)
    if not contents:
        raise HTTPException(status_code=404, detail="User not found or has no content")
    return contents

@router.get("/teams/{team_id}/content", response_model=List[Content])
def get_contents_by_team(team_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contents = content_crud.get_contents_by_team(db, team_id=team_id, skip=skip, limit=limit)
    if not contents:
        raise HTTPException(status_code=404, detail="Team not found or has no content")
    return contents
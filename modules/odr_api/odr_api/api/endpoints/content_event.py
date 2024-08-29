from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from odr_core.crud import content_event as content_event_crud
from odr_core.schemas.content import ContentEvent, ContentEventCreate, ContentEventUpdate
from odr_core.database import get_db
from odr_api.api.auth.auth_provider import AuthProvider
from odr_core.models.content import ContentStatus

router = APIRouter(tags=["content_events"])


@router.post("/content/{content_id}/events/", response_model=ContentEvent)
def create_content_event(
    content_id: int,
    event: ContentEventCreate,
    db: Session = Depends(get_db),
    current_user=Depends(AuthProvider())
):
    event.content_id = content_id
    event.set_by = current_user.id
    return content_event_crud.create_content_event(db=db, event=event)


@router.get("/content/{content_id}/events/{event_id}", response_model=ContentEvent)
def read_content_event(
    content_id: int,
    event_id: int,
    db: Session = Depends(get_db)
):
    db_event = content_event_crud.get_content_event(db, event_id=event_id)
    if db_event is None or db_event.content_id != content_id:
        raise HTTPException(status_code=404, detail="Content event not found")
    return db_event


@router.get("/content/{content_id}/events/", response_model=List[ContentEvent])
def read_content_events(
    content_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    events = content_event_crud.get_content_events(db, content_id=content_id, skip=skip, limit=limit)
    return events


@router.put("/content/{content_id}/events/{event_id}", response_model=ContentEvent)
def update_content_event(
    content_id: int,
    event_id: int,
    event: ContentEventUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(AuthProvider())
):
    db_event = content_event_crud.update_content_event(db, event_id=event_id, event=event)
    if db_event is None or db_event.content_id != content_id:
        raise HTTPException(status_code=404, detail="Content event not found")
    return db_event


@router.delete("/content/{content_id}/events/{event_id}", response_model=bool)
def delete_content_event(
    content_id: int,
    event_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(AuthProvider())
):
    success = content_event_crud.delete_content_event(db, event_id=event_id)
    if not success:
        raise HTTPException(status_code=404, detail="Content event not found")
    return success


@router.get("/content/{content_id}/status", response_model=ContentStatus)
def get_content_status(
    content_id: int,
    db: Session = Depends(get_db)
):
    status = content_event_crud.get_latest_content_status(db, content_id=content_id)
    if status is None:
        raise HTTPException(status_code=404, detail="Content not found or no status events")
    return status

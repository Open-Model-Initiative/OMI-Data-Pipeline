from sqlalchemy.orm import Session
from odr_core.models.content import ContentEvents, ContentStatus
from odr_core.schemas.content import ContentEventCreate, ContentEventUpdate
from typing import List, Optional


def create_content_event(db: Session, event: ContentEventCreate) -> ContentEvents:
    db_event = ContentEvents(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def get_content_event(db: Session, event_id: int) -> Optional[ContentEvents]:
    return db.query(ContentEvents).filter(ContentEvents.id == event_id).first()


def get_content_events(db: Session, content_id: int, skip: int = 0, limit: int = 100) -> List[ContentEvents]:
    return db.query(ContentEvents).filter(ContentEvents.content_id == content_id).offset(skip).limit(limit).all()


def update_content_event(db: Session, event_id: int, event: ContentEventUpdate) -> Optional[ContentEvents]:
    db_event = get_content_event(db, event_id)
    if db_event:
        update_data = event.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_event, key, value)
        db.commit()
        db.refresh(db_event)
    return db_event


def delete_content_event(db: Session, event_id: int) -> bool:
    db_event = get_content_event(db, event_id)
    if db_event:
        db.delete(db_event)
        db.commit()
        return True
    return False


def get_latest_content_status(db: Session, content_id: int) -> Optional[ContentStatus]:
    latest_event = db.query(ContentEvents).filter(ContentEvents.content_id
                                                  == content_id).order_by(ContentEvents.created_at.desc()).first()
    return latest_event.status if latest_event else None

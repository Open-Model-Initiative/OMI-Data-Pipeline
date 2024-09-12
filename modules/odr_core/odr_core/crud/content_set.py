from sqlalchemy.orm import Session
from odr_core.models.content import ContentSet, ContentSetItem, Content
from odr_core.schemas.content_set import ContentSetCreate, ContentSetUpdate
from typing import List, Optional


def create_content_set(db: Session, content_set: ContentSetCreate) -> ContentSet:
    db_content_set = ContentSet(**content_set.model_dump())
    db.add(db_content_set)
    db.commit()
    db.refresh(db_content_set)
    return db_content_set


def get_content_set(db: Session, content_set_id: int) -> Optional[ContentSet]:
    return db.query(ContentSet).filter(ContentSet.id == content_set_id).first()


def get_content_sets(db: Session, skip: int = 0, limit: int = 100) -> List[ContentSet]:
    return db.query(ContentSet).offset(skip).limit(limit).all()


def update_content_set(db: Session, content_set_id: int, content_set: ContentSetUpdate) -> Optional[ContentSet]:
    db_content_set = db.query(ContentSet).filter(ContentSet.id == content_set_id).first()
    if db_content_set:
        update_data = content_set.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_content_set, key, value)
        db.commit()
        db.refresh(db_content_set)
    return db_content_set


def delete_content_set(db: Session, content_set_id: int) -> bool:
    db_content_set = db.query(ContentSet).filter(ContentSet.id == content_set_id).first()
    if db_content_set:
        db.delete(db_content_set)
        db.commit()
        return True
    return False


def add_content_to_set(db: Session, content_set_id: int, content_id: int) -> bool:
    db_content_set_item = ContentSetItem(content_set_id=content_set_id, content_id=content_id)
    db.add(db_content_set_item)
    try:
        db.commit()
        return True
    except: # noqa
        db.rollback()
        return False


def remove_content_from_set(db: Session, content_set_id: int, content_id: int) -> bool:
    db_content_set_item = db.query(ContentSetItem).filter(
        ContentSetItem.content_set_id == content_set_id,
        ContentSetItem.content_id == content_id
    ).first()
    if db_content_set_item:
        db.delete(db_content_set_item)
        db.commit()
        return True
    return False


def get_contents_in_set(db: Session, content_set_id: int, skip: int = 0, limit: int = 100) -> List[Content]:
    return db.query(Content).join(ContentSetItem).filter(
        ContentSetItem.content_set_id == content_set_id
    ).offset(skip).limit(limit).all()

from sqlalchemy.orm import Session
from odr_core.models.content import Content
from odr_core.schemas.content import ContentCreate, ContentUpdate, httpurl_to_str
from typing import List, Optional
from sqlalchemy import Enum as SQLAlchemyEnum
from odr_core.models.content import ContentType, ContentStatus
from loguru import logger
from datetime import datetime, timezone

def create_content(db: Session, content: ContentCreate):
    logger.info(f"Creating content: {content}")
    logger.info(f"Content type: {content.type.value}")
    logger.info(f"Content status: {content.status.value}")
    db_content = Content(
        name=content.name,
        type=ContentType(content.type.value),  # Use the enum value directly
        hash=content.hash,
        phash=content.phash,
        url=[str(url) for url in content.url] if content.url else None,  # Convert HttpUrl to str
        width=content.width,
        height=content.height,
        format=content.format,
        size=content.size,
        status=ContentStatus(content.status.value),  # Use the enum value directly
        license=content.license,
        license_url=httpurl_to_str(content.license_url),  # Convert HttpUrl to str
        flags=content.flags,
        meta=content.meta,
        from_user_id=content.from_user_id,
        from_team_id=content.from_team_id,
        updated_at=datetime.now(timezone.utc)
    )
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    return db_content

def get_content(db: Session, content_id: int) -> Optional[Content]:
    return db.query(Content).filter(Content.id == content_id).first()

def get_contents(db: Session, skip: int = 0, limit: int = 100) -> List[Content]:
    return db.query(Content).offset(skip).limit(limit).all()

def update_content(db: Session, content_id: int, content: ContentUpdate) -> Optional[Content]:
    db_content = db.query(Content).filter(Content.id == content_id).first()
    if db_content:
        for key, value in content.model_dump(exclude_unset=True).items():
            setattr(db_content, key, value) 
        db_content.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(db_content)
    return db_content

def delete_content(db: Session, content_id: int) -> bool:
    db_content = db.query(Content).filter(Content.id == content_id).first()
    if db_content:
        db.delete(db_content)
        db.commit()
        return True
    return False

# Additional helper functions

def get_content_by_hash(db: Session, hash: str) -> Optional[Content]:
    return db.query(Content).filter(Content.hash == hash).first()

def get_contents_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Content]:
    return db.query(Content).filter(Content.from_user_id == user_id).offset(skip).limit(limit).all()

def get_contents_by_team(db: Session, team_id: int, skip: int = 0, limit: int = 100) -> List[Content]:
    return db.query(Content).filter(Content.from_team_id == team_id).offset(skip).limit(limit).all()

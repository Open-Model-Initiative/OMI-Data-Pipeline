from sqlalchemy.orm import Session
from odr_core.models.content import (
    Content,
    ContentSource,
    ContentType,
    ContentStatus,
    ContentSourceType,
)
from odr_core.schemas.content import (
    ContentCreate,
    ContentUpdate,
    ContentSourceCreate,
    ContentSourceUpdate,
    httpurl_to_str,
)
from typing import List, Optional
from loguru import logger
from datetime import datetime, timezone


def create_content_source(
    db: Session, content_id: int, source: ContentSourceCreate
) -> ContentSource:
    db_source = ContentSource(
        content_id=content_id,
        type=ContentSourceType(source.type.value),
        value=source.value,
        metadata=source.source_metadata or {},  # Ensure metadata is a dictionary
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db.add(db_source)
    db.commit()
    db.refresh(db_source)
    return db_source


def get_content_source(db: Session, source_id: int) -> Optional[ContentSource]:
    return db.query(ContentSource).filter(ContentSource.id == source_id).first()


def get_content_sources(db: Session, content_id: int) -> List[ContentSource]:
    return db.query(ContentSource).filter(ContentSource.content_id == content_id).all()


def update_content_source(
    db: Session, source_id: int, source: ContentSourceUpdate
) -> Optional[ContentSource]:
    db_source = db.query(ContentSource).filter(ContentSource.id == source_id).first()
    if db_source:
        update_data = source.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_source, key, value)
        db_source.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(db_source)
    return db_source


def delete_content_source(db: Session, source_id: int) -> bool:
    db_source = db.query(ContentSource).filter(ContentSource.id == source_id).first()
    if db_source:
        db.delete(db_source)
        db.commit()
        return True
    return False


def create_content(db: Session, content: ContentCreate, from_user_id: int):
    logger.info(f"Creating content: {content}")
    logger.info(f"Content type: {content.type.value}")
    logger.info(f"Content status: {content.status.value}")
    db_content = Content(
        name=content.name,
        type=ContentType(content.type.value),
        hash=content.hash,
        phash=content.phash,
        width=content.width,
        height=content.height,
        format=content.format,
        size=content.size,
        status=ContentStatus(content.status.value),
        license=content.license,
        license_url=httpurl_to_str(content.license_url),
        flags=content.flags,
        meta=content.meta,
        from_user_id=from_user_id,
        updated_at=datetime.now(timezone.utc),
    )
    db.add(db_content)
    db.flush()  # Flush to get the content_id

    # Create ContentSource objects
    for source in content.sources:
        db_source = create_content_source(db, db_content.id, source)
        db_content.sources.append(db_source)

    db.commit()
    db.refresh(db_content)
    return db_content


def get_content(db: Session, content_id: int) -> Optional[Content]:
    return db.query(Content).filter(Content.id == content_id).first()


def get_contents(db: Session, skip: int = 0, limit: int = 100) -> List[Content]:
    return db.query(Content).offset(skip).limit(limit).all()


def update_content(
    db: Session, content_id: int, content: ContentUpdate
) -> Optional[Content]:
    db_content = db.query(Content).filter(Content.id == content_id).first()
    if db_content:
        update_data = content.model_dump(exclude_unset=True)

        # Handle sources separately
        sources = update_data.pop("sources", None)

        for key, value in update_data.items():
            setattr(db_content, key, value)

        if sources is not None:
            existing_sources = {
                source.id: source for source in get_content_sources(db, content_id)
            }

            for source in sources:
                if source.id and source.id in existing_sources:
                    # Update existing source
                    update_content_source(db, source.id, source)
                else:
                    # Add new source
                    create_content_source(db, content_id, source)

            # Remove sources not in the update
            source_ids_to_keep = {
                source.id for source in sources if source.id is not None
            }
            for existing_id in existing_sources:
                if existing_id not in source_ids_to_keep:
                    delete_content_source(db, existing_id)

        db_content.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(db_content)
    return db_content


def delete_content(db: Session, content_id: int) -> bool:
    db_content = db.query(Content).filter(Content.id == content_id).first()
    if db_content:
        # Delete associated sources
        for source in get_content_sources(db, content_id):
            delete_content_source(db, source.id)

        db.delete(db_content)
        db.commit()
        return True
    return False


# Additional helper functions


def get_content_by_hash(db: Session, hash: str) -> Optional[Content]:
    return db.query(Content).filter(Content.hash == hash).first()


def get_contents_by_user(
    db: Session, user_id: int, skip: int = 0, limit: int = 100
) -> List[Content]:
    return (
        db.query(Content)
        .filter(Content.from_user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_contents_by_team(
    db: Session, team_id: int, skip: int = 0, limit: int = 100
) -> List[Content]:
    return (
        db.query(Content)
        .filter(Content.from_team_id == team_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

from typing import Iterable, List, Optional
from numpy import ndarray
from sqlalchemy.orm import Session
from odr_core.models.embedding import (
    EmbeddingEngine,
    AnnotationEmbedding,
    ContentEmbedding,
    EmbeddingEngineType,
)
from odr_core.schemas.embedding import (
    EmbeddingEngineCreate,
    EmbeddingEngineUpdate,
    ContentEmbeddingCreate,
    AnnotationEmbeddingCreate,
    AnnotationEmbeddingUpdate,
    ContentEmbeddingUpdate,
    EmbeddingVectorQuery,
)
from datetime import datetime, timezone, timedelta
from fastembed import TextEmbedding, ImageEmbedding
from odr_core.config import settings

from PIL import Image


class ModelCache:
    def __init__(self, ttl: float):
        self.ttl = ttl
        self.cache = {}
        self.expiry = {}
        self.ttl = timedelta(seconds=ttl)

    def expire(self):
        now = datetime.now(timezone.utc)
        for key, value in self.expiry.items():
            if now > value:
                del self.cache[key]
                del self.expiry[key]

    def __getitem__(self, key):
        item = self.cache.get(key)
        if item is None:
            self.expire()
            return None
        else:
            self.expiry[key] = datetime.now(timezone.utc) + self.ttl
            self.expire()
            return self.cache[key]

    def __setitem__(self, key, value):
        self.cache[key] = value
        self.expiry[key] = datetime.now(timezone.utc) + self.ttl
        self.expire()


embedding_model_cache = ModelCache(60 * 30)


# list of available embedding engines - https://huggingface.co/onnx-models
# if model is not on the list, mark it as unsupported with supported=False
def create_embedding_engine(
    db: Session, embedding_engine: EmbeddingEngineCreate
) -> EmbeddingEngine:
    db_embedding = EmbeddingEngine(
        name=embedding_engine.name,
        description=embedding_engine.description,
        version=embedding_engine.version,
        type=EmbeddingEngineType(embedding_engine.type),
        supported=embedding_engine.supported,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db.add(db_embedding)
    db.commit()
    db.refresh(db_embedding)
    return db_embedding


def update_embedding_engine(
    db: Session, embedding_id: int, embedding_engine: EmbeddingEngineUpdate
) -> Optional[EmbeddingEngine]:
    db_embedding = (
        db.query(EmbeddingEngine).filter(EmbeddingEngine.id == embedding_id).first()
    )
    if db_embedding:
        for key, value in embedding_engine.model_dump(exclude_unset=True).items():
            setattr(db_embedding, key, value)
        db_embedding.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(db_embedding)
    return db_embedding


def delete_embedding_engine(db: Session, embedding_engine_id: int) -> bool:
    db_embedding = (
        db.query(EmbeddingEngine)
        .filter(EmbeddingEngine.id == embedding_engine_id)
        .first()
    )
    if db_embedding:
        db.delete(db_embedding)
        db.commit()
        return True
    return False


def get_embedding_engine(
    db: Session, embedding_engine_id: int
) -> Optional[EmbeddingEngine]:
    return (
        db.query(EmbeddingEngine)
        .filter(EmbeddingEngine.id == embedding_engine_id)
        .first()
    )


def get_embedding_engines(
    db: Session, skip: int = 0, limit: int = 100
) -> List[EmbeddingEngine]:
    return db.query(EmbeddingEngine).offset(skip).limit(limit).all()


def generate_text_embedding(
    db: Session, text: str, embedding_engine_id: int
) -> Optional[List[float]]:
    embedding_engine: Optional[EmbeddingEngine] = get_embedding_engine(
        db, embedding_engine_id
    )

    if embedding_engine is None:
        raise ValueError("Invalid embedding engine id")

    if not embedding_engine.supported:
        raise ValueError("Unsupported embedding engine")

    if embedding_engine.type != EmbeddingEngineType.TEXT:
        raise ValueError(
            f"Invalid embedding engine, expected {EmbeddingEngineType.TEXT} got {embedding_engine.type}"
        )

    model: TextEmbedding | None = embedding_model_cache[embedding_engine.name]
    if model is None:
        model = TextEmbedding(embedding_engine.name, cache_dir=settings.MODEL_CACHE_DIR)
        embedding_model_cache[embedding_engine.name] = model

    embedding: Iterable[ndarray] = list(model.query_embed(text))
    return embedding[0].tolist()


def generate_image_embedding(
    db: Session, image: Image.Image, embedding_engine_id: int
) -> List[float]:
    embedding_engine: Optional[EmbeddingEngine] = get_embedding_engine(
        db, embedding_engine_id
    )

    if embedding_engine is None:
        raise ValueError("Invalid embedding engine id")

    if not embedding_engine.supported:
        raise ValueError("Unsupported embedding engine")

    if embedding_engine.type != EmbeddingEngineType.IMAGE:
        raise ValueError(
            f"Invalid embedding engine type, expected {EmbeddingEngineType.IMAGE} got {embedding_engine.type}"
        )

    model: ImageEmbedding | None = embedding_model_cache[embedding_engine.name]
    if model is None:
        model = ImageEmbedding(
            embedding_engine.name, cache_dir=settings.MODEL_CACHE_DIR
        )
        embedding_model_cache[embedding_engine.name] = model

    embedding: Iterable[ndarray] = list(model.embed(image))
    return embedding[0].tolist()


def create_content_embedding(
    db: Session, content_embedding: ContentEmbeddingCreate
) -> ContentEmbedding:
    db_content_embedding = ContentEmbedding(
        content_id=content_embedding.content_id,
        embedding=content_embedding.embedding,
        embedding_engine_id=content_embedding.embedding_engine_id,
        from_user_id=content_embedding.from_user_id,
        from_team_id=content_embedding.from_team_id,
        created_at=datetime.now(timezone.utc),
    )
    db.add(db_content_embedding)
    db.commit()
    db.refresh(db_content_embedding)
    return db_content_embedding


def update_content_embedding(
    db: Session, content_embedding_id: int, content_embedding: ContentEmbeddingUpdate
) -> ContentEmbedding:
    db_content_embedding = (
        db.query(ContentEmbedding)
        .filter(ContentEmbedding.id == content_embedding_id)
        .first()
    )
    if db_content_embedding:
        for key, value in content_embedding.model_dump(exclude_unset=True).items():
            setattr(db_content_embedding, key, value)
        db.commit()
        db.refresh(db_content_embedding)
    return db_content_embedding


def delete_content_embedding(db: Session, content_embedding_id: int) -> bool:
    db_content_embedding = (
        db.query(ContentEmbedding)
        .filter(ContentEmbedding.id == content_embedding_id)
        .first()
    )
    if db_content_embedding:
        db.delete(db_content_embedding)
        db.commit()
        return True
    return False


def query_content_embedding(
    db: Session, query: EmbeddingVectorQuery, skip: int = 0, limit: int = 100
) -> List[ContentEmbedding]:
    if len(query.embedding) != 512:
        raise ValueError(
            f"Invalid embedding length, expected 512 got {len(query.embedding)}"
        )

    return (
        db.query(ContentEmbedding)
        .filter(ContentEmbedding.embedding_engine_id == query.embedding_engine_id)
        .order_by(ContentEmbedding.embedding.l2_distance(query.embedding))
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_annotation_embedding(
    db: Session, annotation_embedding: AnnotationEmbeddingCreate
) -> AnnotationEmbedding:
    db_annotation_embedding = AnnotationEmbedding(
        annotation_id=annotation_embedding.annotation_id,
        embedding=annotation_embedding.embedding,
        embedding_engine_id=annotation_embedding.embedding_engine_id,
        from_user_id=annotation_embedding.from_user_id,
        from_team_id=annotation_embedding.from_team_id,
        created_at=datetime.now(timezone.utc),
    )
    db.add(db_annotation_embedding)
    db.commit()
    db.refresh(db_annotation_embedding)
    return db_annotation_embedding


def update_annotation_embedding(
    db: Session,
    annotation_embedding_id: int,
    annotation_embedding: AnnotationEmbeddingUpdate,
) -> AnnotationEmbedding:
    db_annotation_embedding = (
        db.query(AnnotationEmbedding)
        .filter(AnnotationEmbedding.id == annotation_embedding_id)
        .first()
    )
    if db_annotation_embedding:
        for key, value in annotation_embedding.model_dump(exclude_unset=True).items():
            setattr(db_annotation_embedding, key, value)
        db.commit()
        db.refresh(db_annotation_embedding)
    return db_annotation_embedding


def delete_annotation_embedding(db: Session, annotation_embedding_id: int) -> bool:
    db_annotation_embedding = (
        db.query(AnnotationEmbedding)
        .filter(AnnotationEmbedding.id == annotation_embedding_id)
        .first()
    )
    if db_annotation_embedding:
        db.delete(db_annotation_embedding)
        db.commit()
        return True
    return False


def query_annotation_embedding(
    db: Session, query: EmbeddingVectorQuery, skip: int = 0, limit: int = 100
) -> List[AnnotationEmbedding]:
    if len(query.embedding) != 384:
        raise ValueError(
            f"Invalid embedding length, expected 384 got {len(query.embedding)}"
        )

    return (
        db.query(AnnotationEmbedding)
        .filter(AnnotationEmbedding.embedding_engine_id == query.embedding_engine_id)
        .order_by(AnnotationEmbedding.embedding.l2_distance(query.embedding))
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_content_embedding(
    db: Session, content_embedding_id: int
) -> Optional[ContentEmbedding]:
    return (
        db.query(ContentEmbedding)
        .filter(ContentEmbedding.id == content_embedding_id)
        .first()
    )


def get_content_embeddings(
    db: Session, skip: int = 0, limit: int = 100
) -> List[ContentEmbedding]:
    return db.query(ContentEmbedding).offset(skip).limit(limit).all()


def get_annotation_embedding(
    db: Session, annotation_embedding_id: int
) -> Optional[AnnotationEmbedding]:
    return (
        db.query(AnnotationEmbedding)
        .filter(AnnotationEmbedding.id == annotation_embedding_id)
        .first()
    )


def get_annotation_embeddings(
    db: Session, skip: int = 0, limit: int = 100
) -> List[AnnotationEmbedding]:
    return db.query(AnnotationEmbedding).offset(skip).limit(limit).all()

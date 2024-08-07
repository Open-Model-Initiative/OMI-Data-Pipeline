
from typing import List, Optional, Any
from sqlalchemy import select, text
from sqlalchemy.orm import Session
from odr_core.models.embedding import EmbeddingEngine, AnnotationEmbedding, ContentEmbedding
from odr_core.models.annotation import Annotation
from odr_core.models.content import Content, ContentType
from odr_core.schemas.embedding import (
    EmbeddingEngineCreate, 
    EmbeddingEngineUpdate, 
    ContentEmbeddingCreate, 
    AnnotationEmbeddingCreate, 
    AnnotationEmbeddingUpdate, 
    ContentEmbeddingUpdate,
    EmbeddingQuery,
)
from datetime import datetime, timezone, timedelta
from fastembed import TextEmbedding, ImageEmbedding
from odr_core.config import settings


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

embedding_model_cache = ModelCache(60*30)


# list of available embedding engines - https://huggingface.co/onnx-models
def create_embedding_engine(db: Session, embedding: EmbeddingEngineCreate) -> EmbeddingEngine:
    db_embedding = EmbeddingEngine(
        name=embedding.name,
        description=embedding.description,
        version=embedding.version,
        created_at=datetime.now(timezone.utc)
    )
    db.add(db_embedding)
    db.commit()
    db.refresh(db_embedding)
    return db_embedding


def update_embedding_engine(db: Session, embedding_id: int, embedding: EmbeddingEngineUpdate) -> Optional[EmbeddingEngine]:
    db_embedding = db.query(EmbeddingEngine).filter(EmbeddingEngine.id == embedding_id).first()
    if db_embedding:
        for key, value in embedding.model_dump(exclude_unset=True).items():
            setattr(db_embedding, key, value)
        db_embedding.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(db_embedding)
    return db_embedding


def delete_embedding_engine(db: Session, embedding_id: int) -> bool:
    db_embedding = db.query(EmbeddingEngine).filter(EmbeddingEngine.id == embedding_id).first()
    if db_embedding:
        db.delete(db_embedding)
        db.commit()
        return True
    return False


def get_embedding_engine(db: Session, embedding_id: int) -> Optional[EmbeddingEngine]:
    return db.query(EmbeddingEngine).filter(EmbeddingEngine.id == embedding_id).first()


def get_embedding_engines(db: Session, skip: int = 0, limit: int = 100) -> List[EmbeddingEngine]:
    return db.query(EmbeddingEngine).offset(skip).limit(limit).all()


def generate_text_embedding(text: str, embedding_engine_id: int) -> List[float]:
    embedding_engine: Optional[EmbeddingEngine] = get_embedding_engine(embedding_engine_id)

    if embedding_engine is None:
        raise ValueError("Invalid embedding engine id")

    if embedding_engine.type != "text":
        raise ValueError("Invalid embedding engine type")
    
    if not embedding_engine.supported:
        raise ValueError("Unsupported embedding engine")
    
    model: TextEmbedding | None = embedding_model_cache[embedding_engine.name]
    if model is None:
        model = TextEmbedding(embedding_engine.name, cache_dir=settings.MODEL_CACHE_DIR)
        embedding_model_cache[embedding_engine.name] = model

    return model.query_embed(text)


def generate_image_embedding(image: Any, embedding_engine_id: int) -> List[float]:
    embedding_engine: Optional[EmbeddingEngine] = get_embedding_engine(embedding_engine_id)

    if embedding_engine is None:
        raise ValueError("Invalid embedding engine id")

    if embedding_engine.type != "image":
        raise ValueError("Invalid embedding engine type")
    
    if not embedding_engine.supported:
        raise ValueError("Unsupported embedding engine")
    
    model: ImageEmbedding | None = embedding_model_cache[embedding_engine.name]
    if model is None:
        model = ImageEmbedding(embedding_engine.name, cache_dir=settings.MODEL_CACHE_DIR)
        embedding_model_cache[embedding_engine.name] = model

    raise NotImplementedError("Image embedding not implemented")
    # waiting for release containig this commit - https://github.com/qdrant/fastembed/commit/9c72d2f59f91f87753da07c12a6f1082e233ecb3
    # return model.embed(image)


def create_content_embedding(db: Session, content_embedding: ContentEmbeddingCreate) -> ContentEmbedding:
    db_content_embedding = ContentEmbedding(
        content_id=content_embedding.content_id,
        embedding=content_embedding.embedding,
        embedding_engine_id=content_embedding.embedding_engine_id,
        from_user_id=content_embedding.from_user_id,
        from_team_id=content_embedding.from_team_id,
        created_at=datetime.now(timezone.utc)
    )
    db.add(db_content_embedding)
    db.commit()
    db.refresh(db_content_embedding)
    return db_content_embedding


def update_content_embedding(db: Session, content_embedding_id: int, content_embedding: ContentEmbeddingUpdate) -> Optional[ContentEmbedding]:
    db_content_embedding = db.query(ContentEmbedding).filter(ContentEmbedding.id == content_embedding_id).first()
    if db_content_embedding:
        for key, value in content_embedding.model_dump(exclude_unset=True).items():
            setattr(db_content_embedding, key, value)
        db.commit()
        db.refresh(db_content_embedding)
    return db_content_embedding


def delete_content_embedding(db: Session, content_embedding_id: int) -> bool:
    db_content_embedding = db.query(ContentEmbedding).filter(ContentEmbedding.id == content_embedding_id).first()
    if db_content_embedding:
        db.delete(db_content_embedding)
        db.commit()
        return True
    return False


def query_content_embedding(db: Session, query: EmbeddingQuery, skip: int = 0, limit: int = 100) -> List[ContentEmbedding]:
    if len(query.embedding) == 384:
        raise ValueError("Invalid embedding length")

    return db.query(ContentEmbedding) \
            .filter(ContentEmbedding.embedding_engine_id == query.embedding_engine_id) \
            .order_by(ContentEmbedding.embedding.l2_distance(query.embedding)) \
            .offset(skip).limit(limit).all()


def create_annotation_embedding(db: Session, annotation_embedding: AnnotationEmbeddingCreate) -> AnnotationEmbedding:
    db_annotation_embedding = AnnotationEmbedding(
        annotation_id=annotation_embedding.annotation_id,
        embedding=annotation_embedding.embedding,
        embedding_engine_id=annotation_embedding.embedding_engine_id,
        from_user_id=annotation_embedding.from_user_id,
        from_team_id=annotation_embedding.from_team_id,
        created_at=datetime.now(timezone.utc)
    )
    db.add(db_annotation_embedding)
    db.commit()
    db.refresh(db_annotation_embedding)
    return db_annotation_embedding


def update_annotation_embedding(db: Session, annotation_embedding_id: int, annotation_embedding: AnnotationEmbeddingUpdate) -> Optional[AnnotationEmbedding]:
    db_annotation_embedding = db.query(AnnotationEmbedding).filter(AnnotationEmbedding.id == annotation_embedding_id).first()
    if db_annotation_embedding:
        for key, value in annotation_embedding.model_dump(exclude_unset=True).items():
            setattr(db_annotation_embedding, key, value)
        db.commit()
        db.refresh(db_annotation_embedding)
    return db_annotation_embedding


def delete_annotation_embedding(db: Session, annotation_embedding_id: int) -> bool:
    db_annotation_embedding = db.query(AnnotationEmbedding).filter(AnnotationEmbedding.id == annotation_embedding_id).first()
    if db_annotation_embedding:
        db.delete(db_annotation_embedding)
        db.commit()
        return True
    return False


def query_annotation_embedding(db: Session, query: EmbeddingQuery, skip: int = 0, limit: int = 100) -> List[AnnotationEmbedding]:
    if len(query.embedding) == 384:
        raise ValueError("Invalid embedding length")

    return db.query(AnnotationEmbedding) \
            .filter(AnnotationEmbedding.embedding_engine_id == query.embedding_engine_id) \
            .order_by(AnnotationEmbedding.embedding.l2_distance(query.embedding)) \
            .offset(skip).limit(limit).all()


def get_content_embedding(db: Session, content_embedding_id: int) -> Optional[ContentEmbedding]:
    return db.query(ContentEmbedding).filter(ContentEmbedding.id == content_embedding_id).first()


def get_annotation_embedding(db: Session, annotation_embedding_id: int) -> Optional[AnnotationEmbedding]:
    return db.query(AnnotationEmbedding).filter(AnnotationEmbedding.id == annotation_embedding_id).first()

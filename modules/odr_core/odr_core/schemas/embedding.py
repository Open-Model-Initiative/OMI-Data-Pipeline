from pydantic import BaseModel
from typing import Optional, Any, List
from datetime import datetime
from enum import Enum


class EmbeddingEngineType(str, Enum):
    IMAGE = "image"
    VIDEO = "video"
    VOICE = "voice"
    MUSIC = "music"
    TEXT = "text"


class EmbeddingEngineBase(BaseModel):
    name: str
    type: EmbeddingEngineType
    version: str
    description: Optional[str] = None


class EmbeddingEngineCreate(EmbeddingEngineBase):
    pass


class EmbeddingEngineUpdate(EmbeddingEngineBase):
    pass


class EmbeddingEngine(EmbeddingEngineBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attribute = True


class TextEmbeddingGenerate(BaseModel):
    text: str
    embedding_engine_id: int


class ImageEmbeddingGenerate(BaseModel):
    image: Any
    embedding_engine_id: int


class ContentEmbeddingBase(BaseModel):
    content_id: int
    # list of floats
    embedding: List[float]
    embedding_engine_id: int
    from_user_id: int
    from_team_id: Optional[int] = None


class ContentEmbeddingCreate(ContentEmbeddingBase):
    pass


class ContentEmbeddingUpdate(ContentEmbeddingBase):
    pass


class ContentEmbedding(ContentEmbeddingBase):
    id: int
    created_at: datetime

    class Config:
        from_attribute = True


class AnnotationEmbeddingBase(BaseModel):
    annotation_id: int
    embedding: List[float]
    embedding_engine_id: int
    from_user_id: int
    from_team_id: Optional[int] = None


class AnnotationEmbeddingCreate(AnnotationEmbeddingBase):
    pass


class AnnotationEmbeddingUpdate(AnnotationEmbeddingBase):
    pass


class AnnotationEmbedding(AnnotationEmbeddingBase):
    id: int
    created_at: datetime

    class Config:
        from_attribute = True


class EmbeddingQuery(BaseModel):
    embedding: List[float]
    embedding_engine_id: int
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from odr_core.enums import AnnotationSourceType, ReportType


class AnnotationBase(BaseModel):
    annotation: Dict[str, Any]
    manually_adjusted: bool = False
    overall_rating: Optional[float] = Field(None, ge=0, le=10)


class AnnotationCreate(AnnotationBase):
    content_id: int
    from_user_id: int
    from_team_id: Optional[int] = None
    annotation_source_ids: List[int] = []


class AnnotationUpdate(AnnotationBase):
    pass


class Annotation(AnnotationBase):
    id: int
    content_id: int
    from_user_id: int
    from_team_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    annotation_source_ids: List[int] = []

    class Config:
        from_attributes = True


class AnnotationEmbeddingBase(BaseModel):
    embedding: List[float]


class AnnotationEmbeddingCreate(AnnotationEmbeddingBase):
    annotation_id: int
    embedding_engine_id: int
    from_user_id: int
    from_team_id: Optional[int] = None


class AnnotationEmbedding(AnnotationEmbeddingBase):
    id: int
    annotation_id: int
    embedding_engine_id: int
    from_user_id: int
    from_team_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class AnnotationRatingBase(BaseModel):
    rating: int = Field(..., ge=0, le=10)
    reason: Optional[str] = None


class AnnotationRatingCreate(AnnotationRatingBase):
    annotation_id: int
    rated_by_id: int


class AnnotationRatingUpdate(AnnotationRatingBase):
    pass


class AnnotationRating(AnnotationRatingBase):
    id: int
    annotation_id: int
    rated_by_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AnnotationReportBase(BaseModel):
    type: ReportType
    description: Optional[str] = None


class AnnotationReportCreate(AnnotationReportBase):
    annotation_id: int
    reported_by_id: int


class AnnotationReport(AnnotationReportBase):
    id: int
    annotation_id: int
    reported_by_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class AnnotationSourceBase(BaseModel):
    name: str
    ecosystem: Optional[str] = None
    type: AnnotationSourceType
    annotation_schema: Dict[str, Any]
    license: str
    license_url: Optional[str] = None


class AnnotationSourceCreate(AnnotationSourceBase):
    added_by_id: int


class AnnotationSourceUpdate(AnnotationSourceBase):
    pass


class AnnotationSource(AnnotationSourceBase):
    id: int
    added_by_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

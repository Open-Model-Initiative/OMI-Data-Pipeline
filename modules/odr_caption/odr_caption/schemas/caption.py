from pydantic import BaseModel, Field, confloat, constr
from pydantic.types import StringConstraints
from typing import List
from typing_extensions import Annotated

from enum import StrEnum


class TagType(StrEnum):
    ENTITY = "Entity"
    RELATIONSHIP = "Relationship"
    STYLE = "Style"
    ATTRIBUTE = "Attribute"
    COMPOSITION = "Composition"
    CONTEXTUAL = "Contextual"
    TECHNICAL = "Technical"
    SEMANTIC = "Semantic"


class ImageTag(BaseModel):
    tag: Annotated[
        constr(min_length=1, max_length=30),
        Field(description=("Descriptive keyword or phrase representing the tag.")),
    ]
    category: TagType
    confidence: Annotated[
        confloat(le=1.0),
        Field(
            description=(
                "Confidence score for the tag, between 0 (exclusive) and 1 (inclusive)."
            )
        ),
    ]


class ImageData(BaseModel):
    tags_list: List[ImageTag] = Field(..., min_items=8, max_items=20)
    short_caption: Annotated[str, StringConstraints(min_length=10, max_length=150)]
    verification: Annotated[str, StringConstraints(min_length=10, max_length=100)]
    dense_caption: Annotated[str, StringConstraints(min_length=100, max_length=2048)]

    class Config:
        populate_by_name = True

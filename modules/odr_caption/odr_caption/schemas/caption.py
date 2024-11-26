# SPDX-License-Identifier: Apache-2.0
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
    category: TagType
    tag: str = Field(
        description=("Descriptive keyword or phrase representing the tag.")
    )
    confidence: float = Field(
        0.0,
        description=(
            "Confidence score for the tag, between 0 (exclusive) and 1 (inclusive)."
        ),
    )


class ImageData(BaseModel):
    tags_list: List[ImageTag] = Field(..., min_items=8, max_items=20)
    short_caption: str
    verification: str
    dense_caption: str

    class Config:
        populate_by_name = True

# SPDX-License-Identifier: Apache-2.0
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ContentSetBase(BaseModel):
    name: str
    description: Optional[str] = None


class ContentSetCreate(ContentSetBase):
    created_by_id: int


class ContentSetUpdate(ContentSetBase):
    pass


class ContentSet(ContentSetBase):
    id: int
    created_by_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ContentSetWithContents(ContentSet):
    contents: List[int]  # List of content IDs

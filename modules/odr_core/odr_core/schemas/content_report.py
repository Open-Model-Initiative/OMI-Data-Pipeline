# SPDX-License-Identifier: Apache-2.0
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from odr_core.enums import ReportStatus


class ContentReportBase(BaseModel):
    content_id: int
    reporter_id: int
    reason: str
    description: Optional[str] = None


class ContentReportCreate(ContentReportBase):
    pass


class ContentReportUpdate(BaseModel):
    reason: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ReportStatus] = None


class ContentReport(ContentReportBase):
    id: int
    status: ReportStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

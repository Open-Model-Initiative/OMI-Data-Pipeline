# SPDX-License-Identifier: Apache-2.0
import pytest
from pydantic import ValidationError
from odr_core.schemas.content_report import ContentReportCreate, ContentReport, ReportStatus
from datetime import datetime


def test_content_report_create_schema():
    valid_data = {
        "content_id": 1,
        "reporter_id": 1,
        "reason": "Inappropriate content",
        "description": "This content violates community guidelines."
    }
    report = ContentReportCreate(**valid_data)
    assert report.content_id == 1
    assert report.reporter_id == 1
    assert report.reason == "Inappropriate content"
    assert report.description == "This content violates community guidelines."

    # Test invalid data
    with pytest.raises(ValidationError):
        ContentReportCreate(content_id="invalid", reporter_id=1, reason="Invalid report")

    with pytest.raises(ValidationError):
        ContentReportCreate(content_id=1, reporter_id=1, reason=None)


def test_content_report_schema():
    valid_data = {
        "id": 1,
        "content_id": 1,
        "reporter_id": 1,
        "reason": "Inappropriate content",
        "description": "This content violates community guidelines.",
        "status": ReportStatus.PENDING,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    report = ContentReport(**valid_data)
    assert report.id == 1
    assert report.content_id == 1
    assert report.reporter_id == 1
    assert report.reason == "Inappropriate content"
    assert report.description == "This content violates community guidelines."
    assert report.status == ReportStatus.PENDING
    assert isinstance(report.created_at, datetime)
    assert isinstance(report.updated_at, datetime)

    # Test invalid data
    with pytest.raises(ValidationError):
        ContentReport(id="invalid", content_id=1, reporter_id=1, reason="Invalid report",
                      status=ReportStatus.PENDING, created_at=datetime.now(), updated_at=datetime.now())

    with pytest.raises(ValidationError):
        ContentReport(id=1, content_id=1, reporter_id=1, reason="Invalid report",
                      status="invalid_status", created_at=datetime.now(), updated_at=datetime.now())

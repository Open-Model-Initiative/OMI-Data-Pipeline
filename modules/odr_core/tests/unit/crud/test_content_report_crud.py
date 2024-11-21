# SPDX-License-Identifier: Apache-2.0
import pytest
from odr_core.crud.content_report import create_content_report, get_content_report, update_content_report, delete_content_report
from odr_core.schemas.content_report import ContentReportCreate, ContentReportUpdate, ReportStatus


def test_create_content_report(db):
    report_data = ContentReportCreate(
        content_id=1,
        reporter_id=1,
        reason="Inappropriate content",
        description="This content violates community guidelines."
    )
    report = create_content_report(db, report_data)
    assert report.id is not None
    assert report.content_id == 1
    assert report.reporter_id == 1
    assert report.reason == "Inappropriate content"
    assert report.status == ReportStatus.PENDING


def test_get_content_report(db):
    report_data = ContentReportCreate(
        content_id=1,
        reporter_id=1,
        reason="Inappropriate content"
    )
    created_report = create_content_report(db, report_data)
    retrieved_report = get_content_report(db, report_id=created_report.id)
    assert retrieved_report is not None
    assert retrieved_report.id == created_report.id
    assert retrieved_report.reason == "Inappropriate content"


def test_update_content_report(db):
    report_data = ContentReportCreate(
        content_id=1,
        reporter_id=1,
        reason="Inappropriate content"
    )
    created_report = create_content_report(db, report_data)
    update_data = ContentReportUpdate(reason="Updated reason", status=ReportStatus.REVIEWED)
    updated_report = update_content_report(db, report_id=created_report.id, report=update_data)
    assert updated_report.reason == "Updated reason"
    assert updated_report.status == ReportStatus.REVIEWED


def test_delete_content_report(db):
    report_data = ContentReportCreate(
        content_id=1,
        reporter_id=1,
        reason="Inappropriate content"
    )
    created_report = create_content_report(db, report_data)
    delete_result = delete_content_report(db, report_id=created_report.id)
    assert delete_result is True
    deleted_report = get_content_report(db, report_id=created_report.id)
    assert deleted_report is None

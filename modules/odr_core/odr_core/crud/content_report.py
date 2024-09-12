from sqlalchemy.orm import Session
from odr_core.models.content import ContentReport
from odr_core.schemas.content_report import ContentReportCreate, ContentReportUpdate
from typing import List, Optional


def create_content_report(db: Session, report: ContentReportCreate) -> ContentReport:
    db_report = ContentReport(**report.model_dump())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report


def get_content_report(db: Session, report_id: int) -> Optional[ContentReport]:
    return db.query(ContentReport).filter(ContentReport.id == report_id).first()


def get_content_reports(db: Session, skip: int = 0, limit: int = 100) -> List[ContentReport]:
    return db.query(ContentReport).offset(skip).limit(limit).all()


def update_content_report(db: Session, report_id: int, report: ContentReportUpdate) -> Optional[ContentReport]:
    db_report = db.query(ContentReport).filter(ContentReport.id == report_id).first()
    if db_report:
        update_data = report.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_report, key, value)
        db.commit()
        db.refresh(db_report)
    return db_report


def delete_content_report(db: Session, report_id: int) -> bool:
    db_report = db.query(ContentReport).filter(ContentReport.id == report_id).first()
    if db_report:
        db.delete(db_report)
        db.commit()
        return True
    return False

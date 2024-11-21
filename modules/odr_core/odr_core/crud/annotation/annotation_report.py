# SPDX-License-Identifier: Apache-2.0
from sqlalchemy.orm import Session
from odr_core.models.annotation import AnnotationReport
from odr_core.schemas.annotation import AnnotationReportCreate, AnnotationReportUpdate


def create_annotation_report(db: Session, report: AnnotationReportCreate) -> AnnotationReport:
    db_report = AnnotationReport(**report.model_dump())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report


def get_annotation_report(db: Session, report_id: int) -> AnnotationReport | None:
    return db.query(AnnotationReport).filter(AnnotationReport.id == report_id).first()


def get_annotation_reports(db: Session, annotation_id: int, skip: int = 0, limit: int = 100):
    return db.query(AnnotationReport).filter(AnnotationReport.annotation_id == annotation_id).offset(skip).limit(limit).all()


def update_annotation_report(db: Session, report_id: int, report: AnnotationReportUpdate) -> AnnotationReport | None:
    db_report = db.query(AnnotationReport).filter(AnnotationReport.id == report_id).first()
    if db_report:
        update_data = report.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_report, key, value)
        db.commit()
        db.refresh(db_report)
    return db_report


def delete_annotation_report(db: Session, report_id: int) -> bool:
    db_report = db.query(AnnotationReport).filter(AnnotationReport.id == report_id).first()
    if db_report:
        db.delete(db_report)
        db.commit()
        return True
    return False

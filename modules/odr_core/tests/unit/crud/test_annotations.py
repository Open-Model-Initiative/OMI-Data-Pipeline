from sqlalchemy.orm import Session
from odr_core.crud.annotation import (
    create_annotation_rating, get_annotation_rating, update_annotation_rating, delete_annotation_rating, get_annotation_ratings,
    create_annotation_source, get_annotation_source, update_annotation_source, delete_annotation_source, get_annotation_sources,
    create_annotation_report, get_annotation_report, update_annotation_report, delete_annotation_report, get_annotation_reports
)
from odr_core.schemas.annotation import (
    AnnotationRatingCreate, AnnotationRatingUpdate,
    AnnotationSourceCreate, AnnotationSourceUpdate,
    AnnotationReportCreate, AnnotationReportUpdate,
    ReportType, ReportStatus, AnnotationSourceType
)

import random
import string


def random_string(length: int = 10) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def test_annotation_rating_crud(db: Session):
    # Create
    rating_data = AnnotationRatingCreate(annotation_id=1, rated_by_id=1, rating=5)
    rating = create_annotation_rating(db, rating_data)
    assert rating.id is not None
    assert rating.rating == 5

    # Read
    retrieved_rating = get_annotation_rating(db, rating.id)
    assert retrieved_rating is not None
    assert retrieved_rating.id == rating.id
    assert retrieved_rating.rating == 5

    # Update
    update_data = AnnotationRatingUpdate(rating=4)
    updated_rating = update_annotation_rating(db, rating.id, update_data)
    assert updated_rating is not None
    assert updated_rating.rating == 4

    # Delete
    assert delete_annotation_rating(db, rating.id) is True
    assert get_annotation_rating(db, rating.id) is None


def test_annotation_source_crud(db: Session):
    # Create
    source_data = AnnotationSourceCreate(
        name="Test Source",
        type=AnnotationSourceType.SPATIAL_ANALYSIS,
        annotation_schema={"type": "object"},
        license="CC-BY",
        added_by_id=1
    )
    source = create_annotation_source(db, source_data)
    assert source.id is not None
    assert source.name == "Test Source"
    assert source.type == AnnotationSourceType.SPATIAL_ANALYSIS

    # Read
    retrieved_source = get_annotation_source(db, source.id)
    assert retrieved_source is not None
    assert retrieved_source.id == source.id
    assert retrieved_source.name == "Test Source"

    # Update
    update_data = AnnotationSourceUpdate(
        name="Updated Source",
        type=AnnotationSourceType.CONTENT_DESCRIPTION,
        annotation_schema={"type": "object"},
        license="CC-BY",
    )
    updated_source = update_annotation_source(db, source.id, update_data)
    assert updated_source is not None
    assert updated_source.name == "Updated Source"
    assert updated_source.type == AnnotationSourceType.CONTENT_DESCRIPTION
    assert updated_source.annotation_schema == {"type": "object"}
    assert updated_source.license == "CC-BY"

    # Delete
    assert delete_annotation_source(db, source.id) is True
    assert get_annotation_source(db, source.id) is None


def test_annotation_report_crud(db: Session):
    # Create
    report_data = AnnotationReportCreate(
        type=ReportType.ILLEGAL_CONTENT,
        annotation_id=1,
        reported_by_id=1,
        description="This annotation contains offensive language"
    )
    report = create_annotation_report(db, report_data)
    assert report.id is not None
    assert report.type == ReportType.ILLEGAL_CONTENT
    assert report.annotation_id == 1
    assert report.reported_by_id == 1
    assert report.description == "This annotation contains offensive language"

    # Read
    retrieved_report = get_annotation_report(db, report.id)
    assert retrieved_report is not None
    assert retrieved_report.id == report.id
    assert retrieved_report.description == "This annotation contains offensive language"

    # Update
    update_data = AnnotationReportUpdate(status=ReportStatus.REVIEWED)
    updated_report = update_annotation_report(db, report.id, update_data)
    assert updated_report is not None

    # Delete
    assert delete_annotation_report(db, report.id) is True
    assert get_annotation_report(db, report.id) is None


def test_get_annotation_ratings(db: Session):
    # Create multiple ratings for the same annotation
    annotation_id = 1
    for i in range(3):
        rating_data = AnnotationRatingCreate(
            annotation_id=annotation_id,
            rated_by_id=i + 1,
            rating=i + 3,
            reason=f"Rating {i + 1}"
        )
        create_annotation_rating(db, rating_data)

    # Retrieve ratings
    ratings = get_annotation_ratings(db)
    assert len(ratings) == 3
    assert all(r.annotation_id == annotation_id for r in ratings)


def test_get_annotation_reports(db: Session):
    # Create multiple reports for the same annotation
    annotation_id = 1
    for i in range(3):
        report_data = AnnotationReportCreate(
            annotation_id=annotation_id,
            reported_by_id=i + 1,
            type=ReportType.ILLEGAL_CONTENT,
            description=f"Reason {i + 1}"
        )
        create_annotation_report(db, report_data)

    # Retrieve reports
    reports = get_annotation_reports(db, annotation_id)
    assert len(reports) == 3
    assert all(r.annotation_id == annotation_id for r in reports)


def test_get_annotation_sources(db: Session):
    # Create multiple sources
    for i in range(3):
        source_data = AnnotationSourceCreate(
            name=f"Source {i + 1}",
            type=AnnotationSourceType.CONTENT_DESCRIPTION,
            annotation_schema={"type": "object"},
            license="CC-BY",
            added_by_id=1
        )
        create_annotation_source(db, source_data)

    # Retrieve sources
    sources = get_annotation_sources(db)
    assert len(sources) >= 3
    assert any(s.name == "Source 1" for s in sources)
    assert any(s.name == "Source 2" for s in sources)
    assert any(s.name == "Source 3" for s in sources)

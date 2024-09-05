from sqlalchemy.orm import Session
from odr_core.crud import content_event as content_event_crud
from odr_core.schemas.content import ContentEventCreate, ContentEventUpdate
from odr_core.models.content import ContentEvents, ContentStatus
from odr_core.schemas.user import UserCreate, User
from odr_core.crud.user import create_user
from time import sleep
import random
import string


def random_string(length: int = 10) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def create_test_user(db: Session):
    user_data = UserCreate(
        username=f"test_user_{random_string()}",
        email=f"test_user_{random_string()}@example.com",
        password="test_password"
    )
    return create_user(db, user_data)


def test_create_content_event(db: Session):
    user = create_test_user(db)
    event_data = ContentEventCreate(
        content_id=1,
        status=ContentStatus.PENDING,
        set_by=user.id,
        note="Test event"
    )

    created_event = content_event_crud.create_content_event(db, event_data)
    assert created_event.id is not None
    assert created_event.content_id == 1
    assert created_event.status == ContentStatus.PENDING
    assert created_event.set_by == user.id
    assert created_event.note == "Test event"


def test_get_content_event(db: Session):
    user = create_test_user(db)
    event_data = ContentEventCreate(
        content_id=1,
        status=ContentStatus.PENDING,
        set_by=user.id,
        note="Test event"
    )
    created_event = content_event_crud.create_content_event(db, event_data)

    retrieved_event = content_event_crud.get_content_event(db, created_event.id)
    assert retrieved_event is not None
    assert retrieved_event.id == created_event.id
    assert retrieved_event.content_id == 1
    assert retrieved_event.status == ContentStatus.PENDING


def test_get_content_events(db: Session):
    user = create_test_user(db)
    for i in range(5):
        event_data = ContentEventCreate(
            content_id=1,
            status=ContentStatus.PENDING,
            set_by=user.id,
            note=f"Test event {i}"
        )
        content_event_crud.create_content_event(db, event_data)

    events = content_event_crud.get_content_events(db, content_id=1, skip=0, limit=10)
    assert len(events) == 5


def test_update_content_event(db: Session):
    user = create_test_user(db)
    event_data = ContentEventCreate(
        content_id=1,
        status=ContentStatus.PENDING,
        set_by=user.id,
        note="Test event"
    )
    created_event = content_event_crud.create_content_event(db, event_data)

    update_data = ContentEventUpdate(
        status=ContentStatus.AVAILABLE,
        note="Updated test event"
    )
    updated_event = content_event_crud.update_content_event(db, created_event.id, update_data)
    assert updated_event.status == ContentStatus.AVAILABLE
    assert updated_event.note == "Updated test event"


def test_delete_content_event(db: Session):
    user = create_test_user(db)
    event_data = ContentEventCreate(
        content_id=1,
        status=ContentStatus.PENDING,
        set_by=user.id,
        note="Test event"
    )
    created_event = content_event_crud.create_content_event(db, event_data)

    delete_result = content_event_crud.delete_content_event(db, created_event.id)
    assert delete_result is True

    deleted_event = content_event_crud.get_content_event(db, created_event.id)
    assert deleted_event is None


def test_get_latest_content_status(db: Session):
    user = create_test_user(db)
    # Create multiple events for the same content
    for status in [ContentStatus.PENDING, ContentStatus.AVAILABLE, ContentStatus.UNAVAILABLE]:
        event_data = ContentEventCreate(
            content_id=1,
            status=status,
            set_by=user.id,
            note=f"Test event {status}"
        )
        content_event_crud.create_content_event(db, event_data)
        sleep(1)

    latest_status = content_event_crud.get_latest_content_status(db, content_id=1)
    assert latest_status is ContentStatus.UNAVAILABLE


def test_get_content_events_empty(db: Session):
    events = content_event_crud.get_content_events(db, content_id=999, skip=0, limit=10)
    assert len(events) == 0


def test_get_latest_content_status_no_events(db: Session):
    latest_status = content_event_crud.get_latest_content_status(db, content_id=999)
    assert latest_status is None


def test_update_nonexistent_event(db: Session):
    update_data = ContentEventUpdate(
        status=ContentStatus.AVAILABLE,
        note="Updated test event"
    )
    updated_event = content_event_crud.update_content_event(db, 999, update_data)
    assert updated_event is None


def test_delete_nonexistent_event(db: Session):
    delete_result = content_event_crud.delete_content_event(db, 999)
    assert delete_result is False

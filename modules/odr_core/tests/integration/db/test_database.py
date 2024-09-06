import pytest
from sqlalchemy.orm import Session
from sqlalchemy import text
from odr_core.database import engine, get_db
from loguru import logger


def test_database_connection():
    # Test that we can connect to the database using get_db
    db = next(get_db())
    try:
        result = db.execute(text("SELECT 1")).scalar()
        logger.info(f"Connection successful: {db}")
        assert result == 1
    finally:
        db.close()


def test_get_db():
    # Test that get_db returns a valid session
    db = next(get_db())
    assert isinstance(db, Session)
    db.close()


if __name__ == "__main__":
    pytest.main([__file__])

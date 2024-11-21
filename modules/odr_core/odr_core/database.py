# SPDX-License-Identifier: Apache-2.0
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from odr_core.config import settings

# Create SQLAlchemy engine
url = settings.get_db_url()

engine = create_engine(settings.get_db_url())

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

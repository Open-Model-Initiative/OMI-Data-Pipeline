import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import sessionmaker
from alembic.config import Config
from alembic import command
import os
import time
from loguru import logger 
from odr_core.config import settings
from odr_core.models.base import Base
from sqlalchemy import inspect

class TestDBManager:
    @staticmethod
    def create_test_database():
        conn = psycopg2.connect(
            host=settings.POSTGRES_HOST,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            port=settings.POSTGRES_PORT
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute(f"CREATE DATABASE {settings.TEST_POSTGRES_DB}")
        cur.close()
        conn.close()

    @staticmethod
    def apply_migrations():
        logger.info("Applying database migrations...")
        alembic_cfg = Config(os.path.join(settings.ROOT_DIR, "modules", "odr_core", "alembic.ini"))
        db_url = settings.get_db_url(test=True)
        alembic_cfg.set_main_option("sqlalchemy.url", db_url)
        logger.info(f"Using database URL: {db_url}")
        
        try:
            command.upgrade(alembic_cfg, "head")
            logger.info("Alembic upgrade command completed.")
        except Exception as e:
            logger.error(f"Error during migration: {str(e)}")
            raise

        logger.info("Checking database state after migrations...")
        engine = create_engine(db_url)
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        logger.info(f"Found {len(tables)} tables after migrations: {', '.join(tables)}")
        
        if not tables:
            logger.error("No tables found after migrations. Migrations may have failed.")
            
            # Check if the database exists
            try:
                with engine.connect() as connection:
                    logger.info("Database connection successful.")
            except Exception as e:
                logger.error(f"Failed to connect to the database: {str(e)}")
            
            # Check Alembic version table
            try:
                alembic_version = inspector.get_table_names(schema='alembic')
                logger.info(f"Alembic version table: {alembic_version}")
            except Exception as e:
                logger.error(f"Failed to check Alembic version table: {str(e)}")
            
            raise Exception("No tables found after migrations. Migrations may have failed.")
        
        logger.info("Database migrations applied successfully.")

        @staticmethod
        def get_test_db_session():
            database_url = settings.get_db_url(test=True)
            engine = create_engine(database_url, pool_pre_ping=True)
            TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            return TestingSessionLocal()

    @staticmethod
    def setup_test_db():
        try:
            TestDBManager.create_test_database()
        except psycopg2.errors.DuplicateDatabase:
            pass  # Database already exists
        TestDBManager.apply_migrations()

    @staticmethod
    def teardown_test_db(session):
        # Truncate all tables
        for table in reversed(Base.metadata.sorted_tables):
            try:
                session.execute(table.delete())
            except ProgrammingError as e:
                if 'relation' in str(e) and 'does not exist' in str(e):
                    print(f"Warning: Table {table.name} does not exist. Skipping.")
                else:
                    raise
        session.commit()

    @staticmethod
    def drop_test_db():
        conn = psycopg2.connect(
            host=settings.POSTGRES_HOST,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            port=settings.POSTGRES_PORT
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute(f"DROP DATABASE IF EXISTS {settings.TEST_POSTGRES_DB}")
        cur.close()
        conn.close()

    @staticmethod
    def run_setup_and_teardown():
        print("Setting up test database...")
        TestDBManager.setup_test_db()
        
        session = TestDBManager.get_test_db_session()
        
        print("Test database setup complete.")
        print("Waiting for 5 seconds...")
        time.sleep(5)
        
        print("Tearing down test database...")
        TestDBManager.teardown_test_db(session)
        session.close()
        
        print("Dropping test database...")
        TestDBManager.drop_test_db()
        
        print("Test database teardown complete.")

if __name__ == "__main__":
    TestDBManager.run_setup_and_teardown()
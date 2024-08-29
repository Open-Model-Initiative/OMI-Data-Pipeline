import psycopg2
import pytest
import os
import logging
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_db_connection():
    """
    Smoke test for PostgreSQL database connection.

    This test attempts to connect to the PostgreSQL database using environment
    variables for configuration. It performs the following checks:
    1. Establishes a connection to the database
    2. Verifies the connection status
    3. Retrieves and prints the database version

    The test uses pytest for assertions and will fail if any step encounters an error.

    Environment Variables:
        POSTGRES_DB: The name of the database to connect to
        POSTGRES_USER: The username for database authentication
        POSTGRES_PASSWORD: The password for database authentication
        POSTGRES_HOST: The host address of the database (default: localhost)
        POSTGRES_PORT: The port number for the database connection (default: 35432)

    Raises:
        pytest.fail: If any database operation fails or assertions are not met
    """
    connection = None
    try:
        # Log connection attempt
        logger.info(f"Attempting to connect to database: {os.getenv('POSTGRES_DB')} "
                    f"on host: {os.getenv('POSTGRES_HOST', 'localhost')} "
                    f"port: {os.getenv('POSTGRES_PORT', '35432')}")

        # Attempt to connect
        connection = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=os.getenv("POSTGRES_PORT", "35432")
        )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        # Check connection status
        assert connection.status == psycopg2.extensions.STATUS_READY, "Database connection is not ready"

        # Perform a simple query to get version
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            db_version = cursor.fetchone()
            assert db_version, "Failed to fetch database version"
            logger.info(f"Connected to PostgreSQL version: {db_version[0]}")

        logger.info("Database connection and operations successful")

    except (psycopg2.Error, AssertionError) as e:
        logger.error(f"Database connection or operation failed: {str(e)}")
        pytest.fail(f"Database connection or operation failed: {str(e)}")
    finally:
        if connection:
            connection.close()
            logger.info("Database connection closed")


if __name__ == "__main__":
    test_db_connection()

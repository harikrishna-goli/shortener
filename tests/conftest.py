import os
import time
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

from app.database import Base, get_db
from app.main import app as fastapi_app
import app.models  # noqa: F401  # ensure models are registered

# Read DB URL from environment (set in .env.test or docker-compose)
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "mysql+pymysql://devuser:devpass@mysql:3306/mydb_test"
)

# Global engine/session
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def wait_for_db(url: str, timeout: int = 30):
    """Wait until DB is reachable before running tests."""
    start = time.time()
    while True:
        try:
            conn = engine.connect()
            conn.close()
            return
        except OperationalError:
            if time.time() - start > timeout:
                raise
            time.sleep(0.5)


# Wait for DB before tests start
wait_for_db(TEST_DATABASE_URL)


# Override FastAPI dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


fastapi_app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    """Create tables at test start, drop them at test end."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    """Provide a test client with overridden DB."""
    return TestClient(fastapi_app)

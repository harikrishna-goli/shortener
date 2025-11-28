# tests/conftest.py
import time
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

from app.config import settings
from app.database import Base            # Base = declarative_base() used by your models
# Import the FastAPI app instance and the get_db function from the module that defines them
from app.main import app as fastapi_app, get_db as original_get_db

# Import models so Base.metadata knows about them
import app.models  # noqa: F401

# Confirm we are pointing at the test DB
assert settings.DB_NAME.endswith("test") or settings.DB_NAME == "mydb_test", (
    "settings.DB_NAME should be the test DB (mydb_test) when running pytest"
)

TEST_DATABASE_URL = (
    f"mysql+mysqlconnector://{settings.DB_USER}:{settings.DB_PASS}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

# Wait for DB to be ready (useful when MySQL runs in Docker)
def wait_for_db(url, timeout=30):
    engine = create_engine(url)
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

wait_for_db(TEST_DATABASE_URL, timeout=30)

# Create engine/session for tests
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Override dependency to use test session
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Override the exact function object used by your app
fastapi_app.dependency_overrides[original_get_db] = override_get_db

# Create tables once per test session
@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    # Ensure models are imported (import app.models above)
    Base.metadata.create_all(bind=engine)
    yield
    # Optional: drop tables after tests
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(fastapi_app)

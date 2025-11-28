# tests/conftest.py
import time
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

from app.config import settings
from app.database import Base, get_db  # get_db should live in app.database
# Import the FastAPI instance from where it is defined
from app.main import app as fastapi_app

# Ensure all models are imported before create_all so metadata contains them
import app.models  # noqa: F401

TEST_DATABASE_URL = (
    f"mysql+mysqlconnector://{settings.DB_USER}:{settings.DB_PASS}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

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

# Test engine/session
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Override the dependency on the FastAPI instance
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

fastapi_app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(fastapi_app)

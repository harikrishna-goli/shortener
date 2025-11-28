# tests/conftest.py
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base  # ensure Base includes ShortURL model
from app.config import settings
from app.main import app
from fastapi.testclient import TestClient

# Build a test DB URL from env
TEST_DATABASE_URL = (
    f"mysql+mysqlconnector://{settings.DB_USER}:{settings.DB_PASS}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"  # DB_NAME is mydb_test during pytest
)

# Create a dedicated test engine/session
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# FastAPI dependency override
from app.database import get_db  # original dependency returning SessionLocal()

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session", autouse=True)
def create_test_schema():
    # Ensure all tables exist in mydb_test
    Base.metadata.create_all(bind=engine)
    yield
    # Optional: drop tables after the test session for a clean slate
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)

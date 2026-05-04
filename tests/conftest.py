import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.db.database import Base, get_db
from app.main import app
from fastapi.testclient import TestClient

# [LEARN] SQLite in-memory database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# [LEARN] Create test engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# [LEARN] Create session factory
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """
    [LEARN] Create fresh database for each test
    """
    # [LEARN] Create ALL tables BEFORE test runs
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        # [LEARN] Drop all tables after test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db: Session):
    """
    [LEARN] Provides API client with test database
    """

    # [LEARN] Override get_db dependency
    def override_get_db():
        try:
            yield db
        finally:
            pass  # Don't close, fixture handles it

    app.dependency_overrides[get_db] = override_get_db

    return TestClient(app)

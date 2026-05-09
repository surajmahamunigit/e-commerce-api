import os

os.environ["TESTING"] = "true"

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.db.database import Base, get_db
from app.main import app
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Use PostgreSQL in Docker, SQLite locally
DATABASE_URL = os.getenv(
    "DATABASE_URL", "sqlite:///:memory:"  # Default to SQLite for local testing
)

# For SQLite, use check_same_thread=False
if "sqlite" in DATABASE_URL:
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # PostgreSQL
    engine = create_engine(DATABASE_URL)

Base.metadata.create_all(bind=engine)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()


@pytest.fixture(autouse=True)
def mock_stripe():
    """
    Mock Stripe so tests don't make real API calls.

    """
    with patch("app.utils.stripe_handler.stripe.PaymentIntent.create") as mock_create:
        mock_intent = MagicMock()
        mock_intent.client_secret = "test_client_secret"
        mock_intent.id = "pi_test_123456"
        mock_create.return_value = mock_intent
        yield mock_create


@pytest.fixture(scope="function")
def client(db: Session):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

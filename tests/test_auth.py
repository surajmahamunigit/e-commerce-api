import pytest
from fastapi.testclient import TestClient
from app.main import app


def test_register_valid_user(client):

    payload = {"email": "testuser@example.com", "password": "password123"}

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert "id" in data


def test_register_duplicate_email(client):

    payload = {"email": "duplicate@example.com", "password": "password123"}

    response1 = client.post("/auth/register", json=payload)
    assert response1.status_code == 201

    response2 = client.post("/auth/register", json=payload)
    assert response2.status_code == 400


def test_login_valid_credentials(client):

    register_payload = {"email": "logintest@example.com", "password": "password123"}
    client.post("/auth/register", json=register_payload)

    login_payload = {"email": "logintest@example.com", "password": "password123"}
    response = client.post("/auth/login", json=login_payload)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_invalid_password(client):

    register_payload = {
        "email": "wrongpassword@example.com",
        "password": "correctpassword",
    }
    client.post("/auth/register", json=register_payload)

    login_payload = {"email": "wrongpassword@example.com", "password": "wrongpssword"}
    response = client.post("/auth/login", json=login_payload)

    assert response.status_code == 401
    assert "Invalid" in response.json()["detail"]

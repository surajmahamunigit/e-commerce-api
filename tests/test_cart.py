import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.db.database import get_db
from sqlalchemy.orm import Session


def test_add_to_cart(client):
    """Test adding a product to the cart"""

    # Create a product
    product_payload = {
        "name": "Laptop",
        "description": "Gaming Laptop",
        "price": 1299.99,
        "stock": 5,
        "category": "Electronics",
    }
    product_response = client.post("/products/", json=product_payload)
    product_id = product_response.json()["id"]

    # Register and login
    user_payload = {"email": "testuser@example.com", "password": "password123"}
    client.post("/auth/register", json=user_payload)
    login_response = client.post("/auth/login", json=user_payload)
    token = login_response.json()["access_token"]

    # Add to cart
    cart_payload = {
        "product_id": product_id,
        "quantity": 2,
    }
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/cart/add", json=cart_payload, headers=headers)

    assert response.status_code == 201
    data = response.json()
    assert data["product_id"] == product_id
    assert data["quantity"] == 2


def test_get_cart(client):
    """Retrieving the user's cart"""

    # Create a product
    product_payload = {
        "name": "Laptop",
        "description": "Gaming Laptop",
        "price": 1299.99,
        "stock": 5,
        "category": "Electronics",
    }
    product_response = client.post("/products/", json=product_payload)
    product_id = product_response.json()["id"]

    # Register and login
    user_payload = {"email": "cartuser@example.com", "password": "password123"}
    client.post("/auth/register", json=user_payload)
    login_response = client.post("/auth/login", json=user_payload)
    token = login_response.json()["access_token"]

    # Add to cart
    cart_payload = {
        "product_id": product_id,
        "quantity": 1,
    }
    headers = {"Authorization": f"Bearer {token}"}
    client.post("/cart/add", json=cart_payload, headers=headers)

    # Get cart
    response = client.get("/cart/", headers=headers)
    assert response.status_code == 200
    data = response.json()

    assert "items" in data
    assert len(data["items"]) >= 1
    assert data["items"][0]["product_id"] == product_id


def test_remove_from_cart(client):
    """Test removing a product from the cart"""

    # Create a product
    product_payload = {
        "name": "Monitor",
        "description": "4K Monitor",
        "price": 399.99,
        "stock": 10,
        "category": "Electronics",
    }
    product_response = client.post("/products/", json=product_payload)
    product_id = product_response.json()["id"]

    # Register and login
    user_payload = {"email": "removeuser@example.com", "password": "password123"}
    client.post("/auth/register", json=user_payload)
    login_response = client.post("/auth/login", json=user_payload)
    token = login_response.json()["access_token"]

    # Add to cart
    cart_payload = {
        "product_id": product_id,
        "quantity": 1,
    }
    headers = {"Authorization": f"Bearer {token}"}
    client.post("/cart/add", json=cart_payload, headers=headers)

    # Remove from cart (using product_id since that's what your route expects)
    response = client.delete(f"/cart/remove/{product_id}", headers=headers)
    assert response.status_code == 204

    # Verify it's gone
    verify_response = client.get("/cart/", headers=headers)
    assert verify_response.status_code == 200
    data = verify_response.json()

    # Verify product is no longer in cart
    product_ids = [item["product_id"] for item in data["items"]]
    assert product_id not in product_ids

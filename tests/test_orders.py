import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.db.database import get_db
from sqlalchemy.orm import Session


def test_checkout(client):
    """Test creating an order from cart"""
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
    user_payload = {"email": "orderuser@example.com", "password": "password123"}
    client.post("/auth/register", json=user_payload)
    login_response = client.post("/auth/login", json=user_payload)
    token = login_response.json()["access_token"]

    # Add to cart
    cart_payload = {
        "product_id": product_id,
        "quantity": 2,
    }
    headers = {"Authorization": f"Bearer {token}"}
    client.post("/cart/add", json=cart_payload, headers=headers)

    # Checkout
    checkout_payload = {
        "shipping_address": "123 Main St, New York, NY 10001",
    }
    response = client.post("/orders/checkout", json=checkout_payload, headers=headers)

    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["total_amount"] == "2599.98"  # 1299.99 * 2


def test_get_orders(client):
    """Test retrieving all user's orders"""
    # Create a product
    product_payload = {
        "name": "Mouse",
        "description": "Wireless Mouse",
        "price": 29.99,
        "stock": 50,
        "category": "Electronics",
    }
    product_response = client.post("/products/", json=product_payload)
    product_id = product_response.json()["id"]

    # Register and login
    user_payload = {"email": "getorders@example.com", "password": "password123"}
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

    # Checkout
    checkout_payload = {
        "shipping_address": "456 Oak Ave, Los Angeles, CA 90001",
    }
    client.post("/orders/checkout", json=checkout_payload, headers=headers)

    # Get orders
    response = client.get("/orders/", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["total_amount"] == "29.99"


def test_get_single_order(client):
    """Test retrieving a single order"""
    # Create a product
    product_payload = {
        "name": "Keyboard",
        "description": "Mechanical Keyboard",
        "price": 99.99,
        "stock": 20,
        "category": "Electronics",
    }
    product_response = client.post("/products/", json=product_payload)
    product_id = product_response.json()["id"]

    # Register and login
    user_payload = {"email": "singleorder@example.com", "password": "password123"}
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

    # Checkout
    checkout_payload = {
        "shipping_address": "789 Elm St, Chicago, IL 60601",
    }
    checkout_response = client.post(
        "/orders/checkout", json=checkout_payload, headers=headers
    )
    order_id = checkout_response.json()["id"]

    # Get single order
    response = client.get(f"/orders/{order_id}", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_id
    assert data["total_amount"] == "99.99"


def test_order_total_calculation(client):
    """Test that order total is calculated correctly"""
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
    user_payload = {"email": "totalstest@example.com", "password": "password123"}
    client.post("/auth/register", json=user_payload)
    login_response = client.post("/auth/login", json=user_payload)
    token = login_response.json()["access_token"]

    # Add to cart - quantity 3
    cart_payload = {
        "product_id": product_id,
        "quantity": 3,
    }
    headers = {"Authorization": f"Bearer {token}"}
    client.post("/cart/add", json=cart_payload, headers=headers)

    # Checkout
    checkout_payload = {
        "shipping_address": "999 Pine St, Seattle, WA 98101",
    }
    response = client.post("/orders/checkout", json=checkout_payload, headers=headers)

    assert response.status_code == 201
    data = response.json()
    # 399.99 * 3 = 1199.97
    assert data["total_amount"] == "1199.97"

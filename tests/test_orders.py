import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.db.database import get_db
from sqlalchemy.orm import Session


def test_checkout(client):
    """Test creating an order from cart"""

    # Register admin and get token
    admin_payload = {"email": "admin@example.com", "password": "password123"}
    client.post("/auth/register", json=admin_payload)
    admin_login = client.post("/auth/login", json=admin_payload)
    admin_token = admin_login.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    #  Create product as admin
    product_payload = {
        "name": "Laptop",
        "description": "Gaming Laptop",
        "price": 1299.99,
        "stock": 5,
        "category": "Electronics",
    }
    product_response = client.post(
        "/products/", json=product_payload, headers=admin_headers
    )
    product_id = product_response.json()["id"]

    #  Register regular user and login
    user_payload = {"email": "orderuser@example.com", "password": "password123"}
    client.post("/auth/register", json=user_payload)
    login_response = client.post("/auth/login", json=user_payload)
    token = login_response.json()["access_token"]
    user_headers = {"Authorization": f"Bearer {token}"}

    # Add to cart
    cart_payload = {
        "product_id": product_id,
        "quantity": 2,
    }
    client.post("/cart/add", json=cart_payload, headers=user_headers)

    # Checkout
    checkout_payload = {
        "shipping_address": "123 Main St, New York, NY 123451",
    }
    response = client.post(
        "/orders/checkout", json=checkout_payload, headers=user_headers
    )

    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["total_amount"] == "2599.98"  # 1299.99 * 2


def test_get_orders(client):
    """Test retrieving all user's orders"""

    #  Register admin and get token
    admin_payload = {"email": "admin@example.com", "password": "password123"}
    client.post("/auth/register", json=admin_payload)
    admin_login = client.post("/auth/login", json=admin_payload)
    admin_token = admin_login.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    #  Create product as admin
    product_payload = {
        "name": "Mouse",
        "description": "Wireless Mouse",
        "price": 29.99,
        "stock": 50,
        "category": "Electronics",
    }
    product_response = client.post(
        "/products/", json=product_payload, headers=admin_headers
    )
    product_id = product_response.json()["id"]

    #  Register regular user and login
    user_payload = {"email": "getorders@example.com", "password": "password123"}
    client.post("/auth/register", json=user_payload)
    login_response = client.post("/auth/login", json=user_payload)
    token = login_response.json()["access_token"]
    user_headers = {"Authorization": f"Bearer {token}"}

    # Add to cart
    cart_payload = {
        "product_id": product_id,
        "quantity": 1,
    }
    client.post("/cart/add", json=cart_payload, headers=user_headers)

    # Checkout
    checkout_payload = {
        "shipping_address": "456 Oak Ave, Los Angeles, CA 90001",
    }
    client.post("/orders/checkout", json=checkout_payload, headers=user_headers)

    # Get orders
    response = client.get("/orders/", headers=user_headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert any(order["total_amount"] == "29.99" for order in data)


def test_get_single_order(client):
    """Test retrieving a single order"""

    # Register admin and get token
    admin_payload = {"email": "admin@example.com", "password": "password123"}
    client.post("/auth/register", json=admin_payload)
    admin_login = client.post("/auth/login", json=admin_payload)
    admin_token = admin_login.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    #  Create product as admin
    product_payload = {
        "name": "Keyboard",
        "description": "Mechanical Keyboard",
        "price": 99.99,
        "stock": 20,
        "category": "Electronics",
    }
    product_response = client.post(
        "/products/", json=product_payload, headers=admin_headers
    )
    product_id = product_response.json()["id"]

    # Register regular user and login
    user_payload = {"email": "singleorder@example.com", "password": "password123"}
    client.post("/auth/register", json=user_payload)
    login_response = client.post("/auth/login", json=user_payload)
    token = login_response.json()["access_token"]
    user_headers = {"Authorization": f"Bearer {token}"}

    # Add to cart
    cart_payload = {
        "product_id": product_id,
        "quantity": 1,
    }
    client.post("/cart/add", json=cart_payload, headers=user_headers)

    # Checkout
    checkout_payload = {
        "shipping_address": "789 Elm St, Chicago, IL 60601",
    }
    checkout_response = client.post(
        "/orders/checkout", json=checkout_payload, headers=user_headers
    )
    order_id = checkout_response.json()["id"]

    # Get single order
    response = client.get(f"/orders/{order_id}", headers=user_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_id
    assert data["total_amount"] == "99.99"


def test_order_total_calculation(client):
    """Test that order total is calculated correctly"""

    #  Register admin and get token
    admin_payload = {"email": "admin@example.com", "password": "password123"}
    client.post("/auth/register", json=admin_payload)
    admin_login = client.post("/auth/login", json=admin_payload)
    admin_token = admin_login.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    #  Create product as admin
    product_payload = {
        "name": "Monitor",
        "description": "4K Monitor",
        "price": 399.99,
        "stock": 10,
        "category": "Electronics",
    }
    product_response = client.post(
        "/products/", json=product_payload, headers=admin_headers
    )
    product_id = product_response.json()["id"]

    #  Register regular user and login
    user_payload = {"email": "totalstest@example.com", "password": "password123"}
    client.post("/auth/register", json=user_payload)
    login_response = client.post("/auth/login", json=user_payload)
    token = login_response.json()["access_token"]
    user_headers = {"Authorization": f"Bearer {token}"}

    # Add to cart - quantity 3
    cart_payload = {
        "product_id": product_id,
        "quantity": 3,
    }
    client.post("/cart/add", json=cart_payload, headers=user_headers)

    # Checkout
    checkout_payload = {
        "shipping_address": "999 Pine St, Seattle, WA 98101",
    }
    response = client.post(
        "/orders/checkout", json=checkout_payload, headers=user_headers
    )

    assert response.status_code == 201
    data = response.json()
    # 399.99 * 3 = 1199.97
    assert data["total_amount"] == "1199.97"


def test_order_status_state_machine(client):
    """
    Test order status transition - (admin only)
    """

    # Register admin
    admin_payload = {"email": "admin@example.com", "password": "password123"}
    client.post("/auth/register", json=admin_payload)
    admin_login = client.post("/auth/login", json=admin_payload)
    admin_token = admin_login.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    # Create a product as admin
    product_payload = {
        "name": "test product",
        "description": "test",
        "price": 99.99,
        "stock": 10,
        "category": "electronics",
    }
    product_response = client.post(
        "/products/", json=product_payload, headers=admin_headers
    )
    product_id = product_response.json()["id"]

    # Register user
    user_payload = {
        "email": "statemachineuser@example.com",
        "password": "password123",
    }
    client.post("/auth/register", json=user_payload)
    user_login = client.post("/auth/login", json=user_payload)
    user_token = user_login.json()["access_token"]
    user_headers = {"Authorization": f"Bearer {user_token}"}

    # Add product to the cart and checkout
    client.post(
        "/cart/add",
        json={"product_id": product_id, "quantity": 1},
        headers=user_headers,
    )
    checkout_response = client.post("/orders/checkout", json={}, headers=user_headers)
    order_id = checkout_response.json()["id"]

    # Test valid transition: from pending -> confirmed
    response = client.patch(
        f"/orders/{order_id}/status",
        json={"status": "confirmed"},
        headers=admin_headers,
    )
    assert response.status_code == 200
    assert response.json()["status"] == "confirmed"

    # Test valid transition: from confirmed -> shipped
    response = client.patch(
        f"/orders/{order_id}/status",
        json={"status": "shipped"},
        headers=admin_headers,
    )
    assert response.status_code == 200
    assert response.json()["status"] == "shipped"

    # Test valid transition: from shipped -> delivered
    response = client.patch(
        f"/orders/{order_id}/status",
        json={"status": "delivered"},
        headers=admin_headers,
    )
    assert response.status_code == 200
    assert response.json()["status"] == "delivered"

    # Test invalid transition: from delivered -> cancelled (not allowed)
    response = client.patch(
        f"/orders/{order_id}/status",
        json={"status": "cancelled"},
        headers=admin_headers,
    )
    assert response.status_code == 400

    # Test user cannot update status
    response = client.patch(
        f"/orders/{order_id}/status",
        json={"status": "cancelled"},
        headers=user_headers,
    )
    assert response.status_code == 403

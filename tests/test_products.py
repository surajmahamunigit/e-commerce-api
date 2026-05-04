import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.db.database import get_db
from sqlalchemy.orm import Session


def test_create_product(client):
    """Test creating new product"""
    payload = {
        "name": "Laptop",
        "description": "High-performance laptop",
        "price": 999.0,
        "stock": 10,
        "category": "Electronics",
    }

    response = client.post("/products/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Laptop"
    assert data["price"] == "999.00"
    assert "id" in data


def test_create_product_missing_field(client):
    """Test creating a product without required fields"""

    payload = {
        "name": "laptop",
    }

    response = client.post("/products/", json=payload)

    assert response.status_code == 422  # VAlidation error


def test_list_products(client):
    """Test listing all the products"""

    product1 = {
        "name": "product1",
        "description": "descrption1",
        "price": 10.2,
        "stock": 2,
        "category": "Electronics",
    }

    product2 = {
        "name": "product2",
        "description": "description2",
        "price": 13.22,
        "stock": 14,
        "category": "Electronics",
    }

    client.post("/products/", json=product1)
    client.post("/products/", json=product2)

    # List products
    response = client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    assert data[0]["name"] in ["product1", "product2"]


def test_get_product(client):
    """Test retriveing a single product by product id"""

    # create a product
    payload = {
        "name": "HP pro",
        "description": "gaming laptop",
        "price": 299,
        "stock": 12,
        "category": "Electronics",
    }
    create_response = client.post("/products/", json=payload)
    product_id = create_response.json()["id"]

    # Get the product
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "HP pro"
    assert data["price"] == "299.00"
    assert data["id"] == product_id


def test_get_nonexistent_product(client):
    """Test retrieving a non-existing product"""

    response = client.get("/products/23212")
    assert response.status_code == 400


def test_update_product(client):
    """Test update a product"""

    # create a product
    payload = {
        "name": "original name",
        "description": "original description",
        "price": 50.0,
        "stock": 1,
        "category": "Electronics",
    }
    create_response = client.post("/products/", json=payload)
    product_id = create_response.json()["id"]

    # Update the product
    update_payload = {
        "name": "updated name",
        "description": "updated description",
        "price": 100.00,
        "stock": 0,
        "category": "Electronics",
    }
    response = client.put(f"/products/{product_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "updated name"
    assert data["price"] == "100.00"


def test_delete_product(client):
    """Test delete a product"""

    # Create a payload
    payload = {
        "name": " name",
        "description": " description",
        "price": 50.0,
        "stock": 1,
        "category": "Electronics",
    }
    create_response = client.post("/products/", json=payload)
    product_id = create_response.json()["id"]

    # Delete product
    response = client.delete(f"/products/{product_id}")
    assert response.status_code == 204

    # Verify
    verify_response = client.get(f"/products/{product_id}")
    assert verify_response.status_code == 404

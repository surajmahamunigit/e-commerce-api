# 🛒 E-Commerce API

A production-grade REST API for an e-commerce platform built with **FastAPI** and **PostgreSQL**. Features JWT authentication, role-based access control, shopping cart, order management, and full Docker containerization.

---

## 🚀 Features

- **JWT Authentication** — Secure register/login with Argon2 password hashing
- **Role-Based Access Control** — Admin-only product management, user-specific cart and orders
- **Product Management** — Full CRUD with filtering by category, price range, and pagination
- **Shopping Cart** — Add, view, and remove items tied to authenticated users
- **Order Management** — Checkout from cart, view order history, single order retrieval
- **Dockerized** — Full Docker + docker-compose setup with PostgreSQL
- **18 Passing Tests** — Comprehensive test suite covering auth, products, cart, and orders
- **Swagger UI** — Interactive API documentation with Bearer token authentication

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Auth | JWT (python-jose) + Argon2 |
| Validation | Pydantic v2 |
| Testing | pytest + httpx |
| Containerization | Docker + docker-compose |

---

## 📁 Project Structure

```
e-commerce-api/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Environment variables
│   ├── db/
│   │   └── database.py      # PostgreSQL connection & session
│   ├── models/              # SQLAlchemy models
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── cart_item.py
│   │   ├── order.py
│   │   └── order_item.py
│   ├── schemas/             # Pydantic request/response schemas
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── cart.py
│   │   └── order.py
│   ├── routes/              # API endpoints
│   │   ├── auth.py
│   │   ├── products.py
│   │   ├── cart.py
│   │   └── orders.py
│   └── utils/
│       ├── security.py      # Password hashing
│       └── dependencies.py  # JWT token validation
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_products.py
│   ├── test_cart.py
│   └── test_orders.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

---

## ⚙️ Quick Start

### Prerequisites
- Docker Desktop installed
- Git installed

### 1. Clone the repository
```bash
git clone https://github.com/surajmahamunigit/e-commerce-api.git
cd e-commerce-api
```

### 2. Set up environment variables
```bash
cp .env.example .env
```

### 3. Start with Docker
```bash
docker-compose up -d
```

### 4. Access the API
- **Swagger UI:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

---

## 📌 API Endpoints

### Auth
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/register` | Register a new user | No |
| POST | `/auth/login` | Login and get JWT token | No |

### Products
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/products/` | List all products (filter + paginate) | No |
| GET | `/products/{id}` | Get single product | No |
| POST | `/products/` | Create product | Admin only |
| PUT | `/products/{id}` | Update product | Admin only |
| DELETE | `/products/{id}` | Delete product | Admin only |

### Cart
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/cart/add` | Add item to cart | Yes |
| GET | `/cart/` | View cart | Yes |
| DELETE | `/cart/remove/{product_id}` | Remove item from cart | Yes |

### Orders
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/orders/checkout` | Checkout cart and create order | Yes |
| GET | `/orders/` | Get all orders for user | Yes |
| GET | `/orders/{id}` | Get single order | Yes |

---

## 🔐 Authentication

This API uses **JWT Bearer tokens**.

1. Register: `POST /auth/register`
2. Login: `POST /auth/login` → copy the `access_token`
3. Click **Authorize** in Swagger UI and paste the token
4. All protected endpoints will now work

### Admin Access
To access admin endpoints (create/update/delete products), register with:
```json
{
  "email": "admin@example.com",
  "password": "yourpassword"
}
```

---

## 🔍 Product Filtering & Pagination

```bash
# Filter by category
GET /products/?category=Electronics

# Filter by price range
GET /products/?min_price=100&max_price=500

# Pagination
GET /products/?skip=0&limit=10

# Combined
GET /products/?category=Electronics&min_price=100&max_price=500&skip=0&limit=10
```

---

## 🧪 Running Tests

```bash
# Run all tests
docker-compose exec app python -m pytest tests/ -v

# Run specific test file
docker-compose exec app python -m pytest tests/test_auth.py -v
```

### Test Coverage
```
tests/test_auth.py       ✅ 4/4 passing
tests/test_products.py   ✅ 7/7 passing
tests/test_cart.py       ✅ 3/3 passing
tests/test_orders.py     ✅ 4/4 passing
─────────────────────────────────────
Total                    ✅ 18/18 passing
```

---

## 🐳 Docker Commands

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# Stop and remove volumes (reset database)
docker-compose down -v

# View logs
docker-compose logs app

# Rebuild after code changes
docker-compose build --no-cache
docker-compose up -d
```

---

## 🌱 Environment Variables

Create a `.env` file based on `.env.example`:

```env
DATABASE_URL=postgresql://user:password@db:5432/ecommerce
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👤 Author

**Suraj Mahamuni**
- GitHub: [@surajmahamunigit](https://github.com/surajmahamunigit)

# 🛒 E-Commerce API

A production-grade REST API for an e-commerce platform built with **FastAPI** and **PostgreSQL**. Features JWT authentication, role-based access control, shopping cart, Stripe payment integration, order state machine, rate limiting, Alembic migrations, and full Docker containerization deployed on AWS.

## 🌐 Live Demo
- **Swagger UI:** http://54.165.161.13:8000/docs
- **Health Check:** http://54.165.161.13:8000/health

---

## 🚀 Features

- **JWT Authentication** — Secure register/login with Argon2 password hashing
- **Role-Based Access Control** — Admin-only product management, user-specific cart and orders
- **Product Management** — Full CRUD with filtering by category, price range, and pagination
- **Shopping Cart** — Add, view, and remove items tied to authenticated users
- **Stripe Payment Integration** — PaymentIntent creation on checkout
- **Order State Machine** — Enforces valid status transitions (pending → confirmed → shipped → delivered)
- **Rate Limiting** — Brute force protection on auth endpoints (5/min) and checkout (3/min)
- **Alembic Migrations** — Versioned database migrations with upgrade/downgrade support
- **19 Passing Tests** — Comprehensive test suite with PostgreSQL transaction rollback isolation
- **CI/CD Pipeline** — GitHub Actions auto-runs tests on every push
- **Docker** — Full Docker + docker-compose setup with PostgreSQL
- **AWS Deployment** — Live on EC2 with RDS PostgreSQL database

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| Auth | JWT (python-jose) + Argon2 |
| Validation | Pydantic v2 |
| Payments | Stripe |
| Rate Limiting | SlowAPI |
| Testing | pytest + httpx |
| Containerization | Docker + docker-compose |
| CI/CD | GitHub Actions |
| Cloud | AWS EC2 + RDS |

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
│       ├── security.py      # Argon2 password hashing
│       ├── dependencies.py  # JWT token validation
│       ├── stripe_handler.py # Stripe PaymentIntent creation
│       └── limiter.py       # SlowAPI rate limiter
├── migration/               # Alembic migrations
│   ├── env.py
│   └── versions/
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_products.py
│   ├── test_cart.py
│   └── test_orders.py
├── .github/
│   └── workflows/
│       └── tests.yml        # CI/CD pipeline
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
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

### 4. Run database migrations
```bash
docker-compose exec app python -m alembic upgrade head
```

### 5. Access the API
- **Swagger UI (Local):** http://localhost:8000/docs
- **Swagger UI (Live):** http://54.165.161.13:8000/docs
- **Health Check:** http://54.165.161.13:8000/health

---

## 📌 API Endpoints

### Auth
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/register` | Register a new user (5/min limit) | No |
| POST | `/auth/login` | Login and get JWT token (5/min limit) | No |

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
| POST | `/orders/checkout` | Checkout cart, create Stripe PaymentIntent (3/min limit) | Yes |
| GET | `/orders/` | Get all orders for user | Yes |
| GET | `/orders/{id}` | Get single order | Yes |
| PATCH | `/orders/{id}/status` | Update order status (state machine) | Admin only |

---

## 🔐 Authentication

1. Register: `POST /auth/register`
2. Login: `POST /auth/login` → copy the `access_token`
3. Click **Authorize** in Swagger UI and paste the token
4. All protected endpoints will now work

### Admin Access
Register with `admin@example.com` to access product management and order status endpoints.

---

## 🛡️ Rate Limiting

| Endpoint | Limit | Reason |
|----------|-------|--------|
| `POST /auth/register` | 5/minute | Prevent spam accounts |
| `POST /auth/login` | 5/minute | Prevent brute force attacks |
| `POST /orders/checkout` | 3/minute | Prevent payment fraud |

Exceeding the limit returns `429 Too Many Requests`.

---

## 🔄 Order State Machine

Orders follow strict transition rules:

```
pending → confirmed → shipped → delivered
pending → cancelled
confirmed → cancelled
```

Invalid transitions return `400 Bad Request` with allowed transitions listed.

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

## 🗄️ Database Migrations (Alembic)

```bash
# Apply all pending migrations
python -m alembic upgrade head

# Roll back one migration
python -m alembic downgrade -1

# Create new migration after model change
python -m alembic revision --autogenerate -m "description"

# View migration history
python -m alembic history
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
tests/test_orders.py     ✅ 5/5 passing
─────────────────────────────────────
Total                    ✅ 19/19 passing
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

## ☁️ AWS Deployment

The API is deployed on AWS:
- **EC2:** t3.micro (Ubuntu 24.04 LTS)
- **RDS:** PostgreSQL 15 (db.t4g.micro)
- **Live URL:** http://54.165.161.13:8000/docs

---

## 🌱 Environment Variables

Create a `.env` file based on `.env.example`:

```env
DATABASE_URL=postgresql://user:password@db:5432/ecommerce
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
STRIPE_SECRET_KEY=sk_test_your_stripe_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
ENVIRONMENT=development
```

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👤 Author

**Suraj Mahamuni**
- GitHub: [@surajmahamunigit](https://github.com/surajmahamunigit)

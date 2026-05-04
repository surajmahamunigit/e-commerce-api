from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.db.database import Base, engine
from app.routes import auth, products, cart, orders

app = FastAPI(
    title="E-Commerce API",
    description="Production-grade e-commerce REST API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(orders.router)


@app.get("/health")
def health_check():
    """To verify server is alive and responsive."""
    return {"status": "ok", "message": "Server is alive and responsive."}


def custom_openapi():
    """Custom OpenAPI schema with Bearer token security"""
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="E-Commerce API",
        version="1.0.0",
        description="Production-grade e-commerce REST API",
        routes=app.routes,
    )

    # Add Bearer token security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "bearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # Apply security to protected routes
    for path, path_item in openapi_schema["paths"].items():
        if "/products/" in path and path not in ["/products/"]:
            # POST, PUT, DELETE need auth
            if "post" in path_item:
                path_item["post"]["security"] = [{"bearer": []}]
            if "put" in path_item:
                path_item["put"]["security"] = [{"bearer": []}]
            if "delete" in path_item:
                path_item["delete"]["security"] = [{"bearer": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

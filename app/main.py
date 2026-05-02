from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import Base, engine

Base.metadata.create_all(bind=engine)

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


@app.get("/health")
def health_check():
    """To verify server is alive and responsive."""

    return {"status": "ok", "message": "Server is alive and responsive."}

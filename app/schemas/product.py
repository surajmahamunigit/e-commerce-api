from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from uuid import UUID


class ProductBase(BaseModel):
    """
    Class is inherited by ProductCreate and ProductRespose schemas
    """

    name: str
    price: Decimal
    stock: int
    category: str


class ProductCreate(ProductBase):
    """
    Used for POST /products endpoint
    """

    pass


class ProductResponse(ProductBase):
    """
    Used for returning product data
    """

    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductUpdate(BaseModel):
    """
    Used for PUT /products/{id} endpoint
    """

    name: str | None = None
    price: Decimal | None = None
    stock: int | None = None
    category: str | None = None

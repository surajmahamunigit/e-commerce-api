from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from uuid import UUID
from typing import Literal


class OrderItemBase(BaseModel):

    product_id: UUID
    quantity: int
    price_at_purchase: Decimal


class OrderItemResponse(OrderItemBase):

    id: UUID
    order_id: UUID
    subtotal: Decimal
    created_at: datetime

    class Config:
        from_attributes = True


class OrderBase(BaseModel):

    total_amount: Decimal
    status: str


class OrderCreate(BaseModel):

    # Pass the cart to the order
    pass


class OrderResponse(OrderBase):
    """
    Used for oder related response
    """

    id: UUID
    user_id: UUID
    stripe_payment_id: str | None = None
    items: list[OrderItemResponse]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    "Used for updating the order status"

    status: Literal[
        "confirmed", "shipped", "delivered", "cancelled"
    ]  # Pydantic only accepts these exact values

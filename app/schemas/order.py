from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from uuid import UUID


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
    stripe_payment_id: str | None
    items: list[OrderItemResponse]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

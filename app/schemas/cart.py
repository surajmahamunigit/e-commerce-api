from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from uuid import UUID


class CartItemBase(BaseModel):

    product_id: UUID
    quantity: int


class CartItemCreate(CartItemBase):
    """
    used for POST /cart/add/ endpoint
    """

    pass


class CartItemResponse(CartItemBase):
    """
    Used for returning the cart item contents
    """

    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    """
    Used for GET /cart endpoint
    Returns all the items in the users cart
    """

    items: list[CartItemResponse]
    total_items: int
    total_price: Decimal


class CartItemUpdate(BaseModel):
    """
    Used for PUT /cart/{item_id} endpoint
    """

    quantity: int

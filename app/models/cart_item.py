from sqlalchemy import Column, Integer, DateTime, func, ForeignKey
from sqlalchemy.dialects.prostgresql import UUID
import uuid

from app.db.database import Base


class CartItem(Base):
    """
    CartItem databse model represents "cart_items" table in db.
    """

    __tablename__ = "cart_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # oncascade="CASCADE" if user is deleted delete the carts
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    # oncascade="CASCADE" if product is deleted/removed delete it for all the carts
    product_id = Column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
    )

    quantity = Column(Integer, nullable=False, default=1)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    def __repr__(self):
        return f"<CartItem(user_id={self.user_id}, product_id={self.product_id}, qty={self.quantity})>"

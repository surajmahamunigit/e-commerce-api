from sqlalchemy import Column, Integer, Numeric, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.database import Base


class OrderItem(Base):
    """
    OrderItem database model represents "order_items" table in db.
    """

    __tablename__ = "order_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    order_id = Column(
        UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False
    )

    product_id = Column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
    )

    quantity = Column(Integer, nullable=False)

    price_at_purchase = Column(Numeric(precision=10, scale=2), nullable=False)

    subtotal = Column(Numeric(precision=10, scale=2), nullable=False)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    def __repr__(self):
        return f"<OrderItem( order_id={self.order_id}, product_id={self.product_id})>"

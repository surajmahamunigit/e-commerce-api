from sqlalchemy import Column, String, Numeric, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.database import Base


class Order(Base):
    """
    Order database model class represents "orders" table in the db.
    """

    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    total_amount = Column(Numeric(precision=10, scale=2), nullable=False)

    # String constaints because status value must be one of (pending, confirmed, shipped, delivered)
    status = Column(String(50), nullable=False, default="pending")

    stripe_payment_id = Column(String(255), nullable=True)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, total_amount={self.total_amount}, status={self.status})>"

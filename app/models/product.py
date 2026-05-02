from sqlalchemy import Column, String, Numeric, Integer, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.database import Base


class Product(Base):
    """
    Product database model representing "products table in the db.
    """

    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String(255), nullable=False, index=True)

    price = Column(Numeric(precision=10, scale=2), nullable=False)

    stock = Column(Integer, nullable=False, index=True)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, price={self.price}, stock={self.stock})>"

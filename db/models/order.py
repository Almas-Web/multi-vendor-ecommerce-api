from datetime import datetime

from sqlalchemy import (
    Column,
    Float,
    Integer,
    ForeignKey,
    String,
    DateTime
)

from sqlalchemy.orm import relationship

from db.base_class import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE")
    )

    status = Column(String, default="pending")

    created_at = Column(DateTime, default=datetime.utcnow)

    total_price = Column(Float, default=0)


    # SHIPPING SNAPSHOT
    shipping_full_name = Column(String, nullable=True)
    shipping_phone = Column(String, nullable=True)
    shipping_address = Column(String, nullable=True)
    shipping_city = Column(String, nullable=True)
    shipping_state = Column(String, nullable=True)
    shipping_postal_code = Column(String, nullable=True)
    shipping_country = Column(String, nullable=True)

    # RELATIONS
    user = relationship(
        "User",
        back_populates="orders"
    )

    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete"
    )

    payments = relationship(
        "Payment",
        back_populates="order"
    )
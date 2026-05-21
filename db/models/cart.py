from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    Float,
    DateTime,
    ForeignKey,
    Boolean
)

from sqlalchemy.orm import relationship

from db.base_class import Base


class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    total_price = Column(Float, default=0)

    is_checked_out = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship(
        "User",
        back_populates="cart"
    )

    cart_items = relationship(
        "CartItem",
        back_populates="cart",
        cascade="all, delete"
    )
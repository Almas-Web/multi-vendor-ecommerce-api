from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from db.base_class import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)

    price = Column(Integer, nullable=False)
    stock = Column(Integer, default=0)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # vendor
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    author = relationship("User", back_populates="products")

    # category (NEW RELATION FIXED)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    category = relationship("Category", back_populates="products")

    # relations
    
    cart_items = relationship("CartItem", back_populates="product")
    order_items = relationship(
    "OrderItem",
    back_populates="product",
    cascade="all, delete"
)
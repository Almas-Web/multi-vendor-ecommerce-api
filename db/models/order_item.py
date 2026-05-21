from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from db.base_class import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))

    quantity = Column(Integer, default=1)
    price = Column(Integer, nullable=False)
    order = relationship(
        "Order",
        back_populates="items"
    )

    product = relationship("Product", back_populates="order_items")
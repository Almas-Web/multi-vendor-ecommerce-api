from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from db.base_class import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    amount = Column(Float, nullable=False)

    method = Column(String, default="cod")  # cod, stripe, sslcommerz

    status = Column(String, default="pending")  # pending, success, failed

    transaction_id = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    order = relationship("Order",  back_populates="payments")
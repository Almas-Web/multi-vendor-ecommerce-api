from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from db.base_class import Base


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    full_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)

    address_line = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=True)
    postal_code = Column(String, nullable=True)
    country = Column(String, nullable=False)   

    is_default = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    # relation
    user = relationship("User", back_populates="addresses")
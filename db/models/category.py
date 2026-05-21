from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship

from db.base_class import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)

    is_active = Column(Boolean, default=True)

    # ✅ correct SQLAlchemy DateTime
    created_at = Column(DateTime, default=datetime.utcnow)
    products = relationship("Product", back_populates="category")
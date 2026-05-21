from db.base_class import Base
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)

    # roles
    is_superuser = Column(Boolean(), default=False)  # ADMIN
    is_vendor = Column(Boolean(), default=False)      # SELLER
    is_active = Column(Boolean(), default=True)

    # relationships
    products = relationship("Product", back_populates="author")
    cart = relationship(
    "Cart",
    back_populates="user"
)
    orders = relationship("Order", back_populates="user")
    addresses = relationship(
    "Address",
    back_populates="user",
    cascade="all, delete"
)
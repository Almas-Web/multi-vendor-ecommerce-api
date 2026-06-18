from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from db.base_class import Base


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE")
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id", ondelete="CASCADE")
    )

    cart_id = Column(
        Integer,
        ForeignKey("carts.id", ondelete="CASCADE")
    )

    quantity = Column(Integer, default=1)

    #  STORE PRODUCT PRICE SNAPSHOT
    price = Column(Float, nullable=False, default=0)


    # RELATIONSHIPS

    product = relationship(
        "Product",
        back_populates="cart_items"
    )

    cart = relationship(
        "Cart",
        back_populates="cart_items"
    )
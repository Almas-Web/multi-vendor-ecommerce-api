from pydantic import BaseModel
from typing import Optional

from schemas.product import ProductRead


# -------------------------
# CREATE SCHEMA
# -------------------------
class CartItemCreate(BaseModel):
    cart_id: int
    product_id: int
    quantity: int = 1


# -------------------------
# UPDATE SCHEMA
# -------------------------
class CartItemUpdate(BaseModel):
    quantity: Optional[int] = None


# -------------------------
# READ SCHEMA
# -------------------------
class CartItemRead(BaseModel):
    id: int
    cart_id: int
    product_id: int
    quantity: int

    product: Optional[ProductRead] = None

    class Config:
        from_attributes = True
from pydantic import BaseModel
from typing import Optional

from schemas.product import ProductProfileView


# -------------------------
# CREATE SCHEMA
# -------------------------
class OrderItemCreate(BaseModel):
    order_id: int
    product_id: int
    quantity: int = 1
    price: int


# -------------------------
# UPDATE SCHEMA
# -------------------------
class OrderItemUpdate(BaseModel):
    quantity: Optional[int] = None
    price: Optional[int] = None


# -------------------------
# READ SCHEMA
# -------------------------
class OrderItemRead(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    price: int

    product: Optional[ProductProfileView] = None

    class Config:
        from_attributes = True
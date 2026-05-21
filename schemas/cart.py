from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

from schemas.user import UserView
from schemas.cart_item import CartItemRead


# -------------------------
# CREATE SCHEMA
# -------------------------
class CartCreate(BaseModel):
    user_id: int
    total_price: Optional[float] = 0
    is_checked_out: bool = False


# -------------------------
# UPDATE SCHEMA
# -------------------------
class CartUpdate(BaseModel):
    total_price: Optional[float] = None
    is_checked_out: Optional[bool] = None


# -------------------------
# READ SCHEMA
# -------------------------
class CartRead(BaseModel):
    id: int
    user_id: int
    total_price: float
    is_checked_out: bool
    created_at: datetime

    user: Optional[UserView] = None
    cart_items: List[CartItemRead] = []

    class Config:
        from_attributes = True


# -------------------------
# PAGINATION SCHEMA
# -------------------------
class CartPagination(BaseModel):
    total_count: int
    skip: int
    limit: int
    data: List[CartRead]

    class Config:
        from_attributes = True
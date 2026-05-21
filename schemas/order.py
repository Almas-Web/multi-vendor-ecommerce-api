from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

from schemas.user import UserView
from schemas.order_item import OrderItemRead


# =========================
# CREATE SCHEMA
# =========================
class OrderCreate(BaseModel):
    status: str = "pending"
    total_price: float = 0

    class Config:
        from_attributes = True


# =========================
# UPDATE SCHEMA
# =========================
class OrderUpdate(BaseModel):
    status: Optional[str] = None
    total_price: Optional[float] = None

    class Config:
        from_attributes = True


# =========================
# STATUS UPDATE
# =========================
class OrderStatusUpdate(BaseModel):
    status: str


# =========================
# SHIPPING SNAPSHOT
# =========================
class ShippingAddressView(BaseModel):
    shipping_full_name: Optional[str] = None
    shipping_phone: Optional[str] = None
    shipping_address: Optional[str] = None
    shipping_city: Optional[str] = None
    shipping_state: Optional[str] = None
    shipping_postal_code: Optional[str] = None
    shipping_country: Optional[str] = None

    class Config:
        from_attributes = True


# =========================
# ORDER READ
# =========================
class OrderRead(ShippingAddressView):
    id: int
    status: str
    total_price: float
    created_at: datetime

    user: UserView

    items: List[OrderItemRead]

    class Config:
        from_attributes = True


# =========================
# PAGINATION
# =========================
class OrderPagination(BaseModel):
    total_count: int
    skip: int
    limit: int

    data: List[OrderRead]

    class Config:
        from_attributes = True


# =========================
# PROFILE VIEW
# =========================
class OrderProfileView(BaseModel):
    id: int
    status: str
    total_price: float

    class Config:
        from_attributes = True
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PaymentCreate(BaseModel):
    order_id: int
    amount: float
    method: str = "cod"


class PaymentRead(BaseModel):
    id: int
    order_id: int
    amount: float
    method: str
    status: str
    transaction_id: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
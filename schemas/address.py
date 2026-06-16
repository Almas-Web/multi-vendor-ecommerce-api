from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# CREATE
class AddressCreate(BaseModel):
    full_name: str
    phone: str
    address_line: str
    city: str
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: str
    is_default: bool = False


# UPDATE
class AddressUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    address_line: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    is_default: Optional[bool] = None


# READ
class AddressRead(BaseModel):
    id: int
    full_name: str
    phone: str
    address_line: str
    city: str
    state: Optional[str]
    postal_code: Optional[str]
    country: str
    is_default: bool
    created_at: datetime

    class Config:
        from_attributes = True
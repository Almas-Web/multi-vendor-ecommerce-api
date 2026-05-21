from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List
from slugify import slugify
import time

from schemas.user import UserView


# -------------------------
# CREATE SCHEMA
# -------------------------
class ProductCreate(BaseModel):
    title: str
    price: int
    stock: int = 0
    is_active: bool = True
    slug: Optional[str] = None

    # image_url: Optional[str] = None  # (COMMENTED FOR NOW - ADD LATER)

    @classmethod
    def create_slug(cls, title: str) -> str:
        _slugify = slugify(title)
        _time_hash = hash(time.time())
        return f"{_slugify}-{_time_hash}"

    def __init__(self, **data):
        super().__init__(**data)
        if self.title:
            self.slug = self.create_slug(self.title)


# -------------------------
# UPDATE SCHEMA
# -------------------------
class ProductUpdate(BaseModel):
    title: Optional[str] = None
    price: Optional[int] = None
    stock: Optional[int] = None
    is_active: Optional[bool] = None
    slug: Optional[str] = None

    # image_url: Optional[str] = None  # (COMMENTED FOR NOW - ADD LATER)

    @classmethod
    def create_slug(cls, title: str) -> str:
        _slugify = slugify(title)
        _time_hash = hash(time.time())
        return f"{_slugify}-{_time_hash}"

    def __init__(self, **data):
        super().__init__(**data)
        if self.title:
            self.slug = self.create_slug(self.title)


# -------------------------
# READ SCHEMA
# -------------------------
class ProductRead(BaseModel):
    id: int
    slug: str
    title: str
    price: int
    created_at: datetime
    author: UserView

    # image_url: Optional[str] = None  # (COMMENTED FOR FUTURE USE)

    class Config:
        from_attributes = True


# -------------------------
# PAGINATION SCHEMA
# -------------------------
class ProductPagination(BaseModel):
    total_count: int
    skip: int
    limit: int
    data: List[ProductRead]

    class Config:
        from_attributes = True


# -------------------------
# PRODUCT PROFILE VIEW
# -------------------------
class ProductProfileView(BaseModel):
    id: int
    title: str
    price: int
    stock: int
    is_active: bool

    # image_url: Optional[str] = None  # (COMMENTED FOR FUTURE USE)

    class Config:
        from_attributes = True
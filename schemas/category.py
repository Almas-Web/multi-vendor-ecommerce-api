from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List
from slugify import slugify
import time


# CREATE SCHEMA
class CategoryCreate(BaseModel):
    name: str
    is_active: bool = True
    slug: Optional[str] = None

    @classmethod
    def create_slug(cls, name: str) -> str:
        _slugify = slugify(name)
        _time_hash = hash(time.time())
        return f"{_slugify}-{_time_hash}"

    def __init__(self, **data):
        super().__init__(**data)
        if self.name:
            self.slug = self.create_slug(self.name)


# UPDATE SCHEMA
class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None
    slug: Optional[str] = None

    @classmethod
    def create_slug(cls, name: str) -> str:
        _slugify = slugify(name)
        _time_hash = hash(time.time())
        return f"{_slugify}-{_time_hash}"

    def __init__(self, **data):
        super().__init__(**data)
        if self.name:
            self.slug = self.create_slug(self.name)



# READ SCHEMA

class CategoryRead(BaseModel):
    id: int
    slug: str
    name: str
    created_at: datetime

    class Config:
        from_attributes = True


# PAGINATION SCHEMA
class CategoryPagination(BaseModel):
    total_count: int
    skip: int
    limit: int
    data: List[CategoryRead]

    class Config:
        from_attributes = True
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from sqlalchemy import func

from db.models.category import Category
from schemas.category import (
    CategoryCreate,
    CategoryPagination,
    CategoryUpdate
)


class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    # -------------------------
    # CREATE CATEGORY
    # -------------------------
    def create_category(self, category: CategoryCreate) -> Category:
        """
        Create a new category in the database.
        """

        db_category = Category(
            name=category.name,
            slug=category.slug,
            is_active=category.is_active
        )

        try:
            self.db.add(db_category)
            self.db.commit()
            self.db.refresh(db_category)

        except IntegrityError as e:
            print(e)
            self.db.rollback()
            raise HTTPException(status_code=400, detail="Something went wrong!")

        return db_category

    # -------------------------
    # GET CATEGORIES (PAGINATION)
    # -------------------------
    def get_categories(self, skip: int = 0, limit: int = 1000):
        """
        Retrieve a list of categories with pagination.
        """

        total_count = self.db.query(func.count(Category.id)).scalar()

        categories = (
            self.db.query(Category)
            .order_by(Category.created_at.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

        return CategoryPagination(
            total_count=total_count,
            skip=skip,
            limit=limit,
            data=categories
        )

    # -------------------------
    # GET SINGLE CATEGORY
    # -------------------------
    def get_category(self, category_id: int) -> Category:

        return (
            self.db.query(Category)
            .filter(Category.id == category_id)
            .first()
        )

    # -------------------------
    # UPDATE CATEGORY
    # -------------------------
    def update_category(self, category_id: int, category: CategoryUpdate) -> Category:

        db_category = (
            self.db.query(Category)
            .filter(Category.id == category_id)
            .first()
        )

        if not db_category:
            raise HTTPException(status_code=404, detail="Category not found!")

        if category.name:
            db_category.name = category.name
            db_category.slug = category.slug

        if category.is_active is not None:
            db_category.is_active = category.is_active

        try:
            self.db.commit()
            self.db.refresh(db_category)

        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e.orig))

        return db_category

    # -------------------------
    # DELETE CATEGORY
    # -------------------------
    def delete_category(self, category_id: int) -> bool:

        db_category = (
            self.db.query(Category)
            .filter(Category.id == category_id)
            .first()
        )

        if not db_category:
            raise HTTPException(status_code=404, detail="Category not found!")

        self.db.delete(db_category)
        self.db.commit()

        return True
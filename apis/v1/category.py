from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from apis.v1.user import get_current_user
from db.models.user import User
from db.session import get_db
from repositories.category import CategoryRepository
from schemas.category import (
    CategoryCreate,
    CategoryRead,
    CategoryPagination,
    CategoryUpdate
)

router = APIRouter()


# =========================
# CREATE CATEGORY
# =========================
@router.post("", response_model=CategoryRead)
def create_category(
    payload: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    category_repo = CategoryRepository(db=db)

    new_category = category_repo.create_category(
        category=payload
    )

    return new_category


# =========================
# GET CATEGORIES
# =========================
@router.get("", response_model=CategoryPagination)
def get_categories(
    skip: int = 0,
    limit: int = 1000,
    db: Session = Depends(get_db)
):
    category_repo = CategoryRepository(db=db)

    categories = category_repo.get_categories(
        skip=skip,
        limit=limit
    )

    return categories


# =========================
# GET SINGLE CATEGORY
# =========================
@router.get("/{category_id}", response_model=CategoryRead)
def get_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    category_repo = CategoryRepository(db=db)

    category = category_repo.get_category(category_id=category_id)

    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category not found!"
        )

    return category


# =========================
# UPDATE CATEGORY
# =========================
@router.put("/{category_id}")
def update_category(
    category_id: int,
    payload: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    category_repo = CategoryRepository(db=db)

    category_repo.update_category(
        category_id=category_id,
        category=payload
    )

    return {
        "success": "Category updated successfully"
    }


# =========================
# DELETE CATEGORY
# =========================
@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    category_repo = CategoryRepository(db=db)

    category_repo.delete_category(category_id=category_id)

    return {
        "success": "Category deleted successfully"
    }
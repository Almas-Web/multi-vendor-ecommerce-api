import os
from uuid import uuid4
from io import BytesIO

from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File
from sqlalchemy.orm import Session

from db.session import get_db
from db.models.user import User
from db.models.product import Product

from repositories.product import ProductRepository
from schemas.product import (
    ProductCreate,
    ProductRead,
    ProductPagination,
    ProductUpdate
)

from utils.deps import (
    get_current_user,
    get_current_vendor_user
)

router = APIRouter()

UPLOAD_FOLDER = "uploads/images"


# CREATE PRODUCT
@router.post("", response_model=ProductRead)
def create_product(
    payload: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_vendor_user)
):
    product_repo = ProductRepository(db=db)

    new_product = product_repo.create_product(
        product=payload,
        author_id=current_user.id
    )

    return new_product


# GET PRODUCTS
@router.get("", response_model=ProductPagination)
def get_products(
    skip: int = 0,
    limit: int = 1000,
    db: Session = Depends(get_db)
):
    product_repo = ProductRepository(db=db)

    products = product_repo.get_products(skip=skip, limit=limit)

    return products


# GET SINGLE PRODUCT
@router.get("/{product_id}", response_model=ProductRead)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product_repo = ProductRepository(db=db)

    product = product_repo.get_product(product_id=product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product not found!"
        )

    return product


# UPDATE PRODUCT
@router.put("/{product_id}")
def update_product(
    product_id: int,
    payload: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_vendor_user)
):
    product_repo = ProductRepository(db=db)

    product_repo.update_product(
        product_id=product_id,
        product=payload,
        current_user=current_user
    )

    return {
        "success": "Product updated successfully"
    }


# DELETE PRODUCT
@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_vendor_user)
):
    product_repo = ProductRepository(db=db)

    product_repo.delete_product(
        product_id=product_id,
        current_user=current_user
    )

    return {
        "success": "Product deleted successfully"
    }


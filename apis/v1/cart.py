from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.session import get_db
from db.models.user import User

from repositories.cart import CartRepository
from schemas.cart import CartRead, CartPagination, CartUpdate

from apis.v1.user import get_current_user


router = APIRouter()


# =========================
# CREATE / GET OR CREATE CART
# =========================
@router.post("", response_model=CartRead)
def create_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cart_repo = CartRepository(db=db)

    # always ensure one active cart per user
    cart = cart_repo.create_cart(user_id=current_user.id)

    return cart


# =========================
# GET MY CART
# =========================
@router.get("/me", response_model=CartRead)
def get_my_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cart_repo = CartRepository(db=db)

    cart = cart_repo.get_cart_by_user(user_id=current_user.id)

    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found!"
        )

    return cart


# =========================
# GET ALL CARTS (ADMIN ONLY)
# =========================
@router.get("", response_model=CartPagination)
def get_carts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # 🔒 ADMIN ONLY
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed"
        )

    cart_repo = CartRepository(db=db)

    return cart_repo.get_carts(skip=skip, limit=limit)


# =========================
# UPDATE CART
# =========================
@router.put("/{cart_id}")
def update_cart(
    cart_id: int,
    payload: CartUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    cart_repo = CartRepository(db=db)

    cart = cart_repo.get_cart(cart_id)

    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found!"
        )

    # 🔒 OWNERSHIP CHECK
    if cart.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed"
        )

    updated_cart = cart_repo.update_cart(
        cart_id=cart_id,
        cart=payload,
        user_id=current_user.id
    )

    return {
        "success": True,
        "data": updated_cart
    }


# =========================
# DELETE CART
# =========================
@router.delete("/{cart_id}")
def delete_cart(
    cart_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    cart_repo = CartRepository(db=db)

    cart = cart_repo.get_cart(cart_id)

    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found!"
        )

    # 🔒 OWNERSHIP CHECK
    if cart.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed"
        )

    cart_repo.delete_cart(cart_id=cart_id)

    return {
        "success": True,
        "message": "Cart deleted successfully"
    }
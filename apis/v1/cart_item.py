from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.session import get_db
from db.models.user import User
from db.models.cart import Cart

from repositories.cart_item import CartItemRepository
from schemas.cart_item import CartItemCreate, CartItemRead, CartItemUpdate

from apis.v1.user import get_current_user

router = APIRouter()


# =========================
# ADD ITEM (OWNERSHIP FIXED)
# =========================
@router.post("", response_model=CartItemRead)
def add_item(
    payload: CartItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # 🔥 OWNERSHIP CHECK
    cart = db.query(Cart).filter(
        Cart.id == payload.cart_id,
        Cart.user_id == current_user.id,
        Cart.is_checked_out == False
    ).first()

    if not cart:
        raise HTTPException(403, "Invalid cart access")

    repo = CartItemRepository(db=db)
    return repo.add_item(payload)


# =========================
# GET ITEMS (OWN CART ONLY)
# =========================
@router.get("/cart/{cart_id}")
def get_items_by_cart(
    cart_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    cart = db.query(Cart).filter(
        Cart.id == cart_id,
        Cart.user_id == current_user.id
    ).first()

    if not cart:
        raise HTTPException(403, "Invalid cart access")

    repo = CartItemRepository(db=db)
    return repo.get_items_by_cart(cart_id=cart_id)


# =========================
# UPDATE ITEM (SAFE)
# =========================
@router.put("/{item_id}")
def update_item(
    item_id: int,
    payload: CartItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    repo = CartItemRepository(db=db)

    item = repo.get_item(item_id)

    if not item:
        raise HTTPException(404, "Item not found")

    if item.cart.user_id != current_user.id:
        raise HTTPException(403, "Unauthorized access")

    repo.update_item(item_id=item_id, item=payload)

    return {"success": True}


# =========================
# DELETE ITEM (SAFE)
# =========================
@router.delete("/{item_id}")
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    repo = CartItemRepository(db=db)

    item = repo.get_item(item_id)

    if not item:
        raise HTTPException(404, "Item not found")

    if item.cart.user_id != current_user.id:
        raise HTTPException(403, "Unauthorized access")

    repo.delete_item(item_id=item_id)

    return {"success": True}
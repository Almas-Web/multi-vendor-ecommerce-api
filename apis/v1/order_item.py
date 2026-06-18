from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from db.session import get_db
from db.models.user import User

from repositories.order_item import OrderItemRepository
from schemas.order_item import (
    OrderItemCreate,
    OrderItemRead,
    OrderItemUpdate
)

from apis.v1.user import get_current_user


router = APIRouter()


# CREATE ORDER ITEM
@router.post("", response_model=OrderItemRead)
def create_order_item(
    payload: OrderItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order_item_repo = OrderItemRepository(db=db)

    new_item = order_item_repo.create_order_item(item=payload)

    return new_item


# GET ORDER ITEMS
@router.get("")
def get_order_items(
    skip: int = 0,
    limit: int = 1000,
    db: Session = Depends(get_db)
):
    order_item_repo = OrderItemRepository(db=db)

    items = order_item_repo.get_order_items(
        skip=skip,
        limit=limit
    )

    return items


# GET SINGLE ORDER ITEM
@router.get("/{item_id}", response_model=OrderItemRead)
def get_order_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    order_item_repo = OrderItemRepository(db=db)

    item = order_item_repo.get_order_item(item_id=item_id)

    if not item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order item not found!"
        )

    return item


# UPDATE ORDER ITEM
@router.put("/{item_id}")
def update_order_item(
    item_id: int,
    payload: OrderItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order_item_repo = OrderItemRepository(db=db)

    order_item_repo.update_order_item(
        item_id=item_id,
        item=payload
    )

    return {
        "success": "Order item updated successfully"
    }


# DELETE ORDER ITEM
@router.delete("/{item_id}")
def delete_order_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order_item_repo = OrderItemRepository(db=db)

    order_item_repo.delete_order_item(item_id=item_id)

    return {
        "success": "Order item deleted successfully"
    }
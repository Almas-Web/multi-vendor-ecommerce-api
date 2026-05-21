from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from db.session import get_db
from db.models.user import User

from repositories.order import OrderRepository

from schemas.order import (
    OrderCreate,
    OrderRead,
    OrderPagination,
    OrderUpdate,
    OrderStatusUpdate
)

from apis.v1.user import get_current_user


router = APIRouter()


# CREATE
@router.post("", response_model=OrderRead)
def create_order(
    payload: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    repo = OrderRepository(db)
    return repo.create_order(payload, current_user.id)


# GET ALL
@router.get("", response_model=OrderPagination)
def get_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    repo = OrderRepository(db)
    return repo.get_orders(skip, limit)


# GET ONE
@router.get("/{order_id}", response_model=OrderRead)
def get_order(order_id: int, db: Session = Depends(get_db)):

    repo = OrderRepository(db)
    order = repo.get_order(order_id)

    if not order:
        raise HTTPException(status_code=404, detail="Order not found!")

    return order


# UPDATE FULL
@router.put("/{order_id}")
def update_order(order_id: int, payload: OrderUpdate, db: Session = Depends(get_db)):

    repo = OrderRepository(db)
    repo.update_order(order_id, payload)

    return {"success": True}


# STATUS UPDATE (ADMIN ONLY)
@router.patch("/{order_id}/status")
def update_status(
    order_id: int,
    payload: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not allowed")

    repo = OrderRepository(db)

    order = repo.update_order_status(order_id, payload.status)

    return {
        "success": True,
        "data": order
    }


# DELETE
@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):

    repo = OrderRepository(db)
    repo.delete_order(order_id)

    return {"success": True}
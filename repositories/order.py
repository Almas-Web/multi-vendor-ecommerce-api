from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from sqlalchemy import func

from db.models.order import Order
from db.models.product import Product
from schemas.order import OrderCreate, OrderPagination, OrderUpdate


class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    # CREATE
    def create_order(self, order: OrderCreate, user_id: int) -> Order:

        db_order = Order(
            status=order.status,
            total_price=order.total_price,
            user_id=user_id
        )

        try:
            self.db.add(db_order)
            self.db.commit()
            self.db.refresh(db_order)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=400, detail="Something went wrong!")

        return db_order

    # GET ALL
    def get_orders(self, skip: int = 0, limit: int = 1000):

        total_count = self.db.query(func.count(Order.id)).scalar()

        orders = (
            self.db.query(Order)
            .order_by(Order.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

        return OrderPagination(
            total_count=total_count,
            skip=skip,
            limit=limit,
            data=orders
        )

    # GET ONE
    def get_order(self, order_id: int) -> Order:

        return self.db.query(Order).filter(Order.id == order_id).first()

    # UPDATE
    def update_order(self, order_id: int, order: OrderUpdate) -> Order:

        db_order = self.get_order(order_id)

        if not db_order:
            raise HTTPException(status_code=404, detail="Order not found!")

        if order.status:
            db_order.status = order.status

        if order.total_price is not None:
            db_order.total_price = order.total_price

        try:
            self.db.commit()
            self.db.refresh(db_order)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=400, detail="Update failed!")

        return db_order

    # DELETE
    def delete_order(self, order_id: int) -> bool:

        db_order = self.get_order(order_id)

        if not db_order:
            raise HTTPException(status_code=404, detail="Order not found!")

        self.db.delete(db_order)
        self.db.commit()
        return True

    # =========================
    # ADVANCED STATUS SYSTEM
    # =========================
    def update_order_status(self, order_id: int, status: str) -> Order:

        db_order = self.get_order(order_id)

        if not db_order:
            raise HTTPException(status_code=404, detail="Order not found!")

        valid_status = [
            "pending",
            "confirmed",
            "shipped",
            "delivered",
            "cancelled"
        ]

        if status not in valid_status:
            raise HTTPException(status_code=400, detail="Invalid status!")

        allowed = {
            "pending": ["confirmed", "cancelled"],
            "confirmed": ["shipped", "cancelled"],
            "shipped": ["delivered"],
            "delivered": [],
            "cancelled": []
        }

        if status not in allowed[db_order.status]:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot change {db_order.status} → {status}"
            )

        # STOCK RESTORE ON CANCEL
        if status == "cancelled":
            for item in db_order.items:
                product = self.db.query(Product).filter(Product.id == item.product_id).first()
                if product:
                    product.stock += item.quantity

        db_order.status = status

        try:
            self.db.commit()
            self.db.refresh(db_order)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=400, detail="Status update failed!")

        return db_order
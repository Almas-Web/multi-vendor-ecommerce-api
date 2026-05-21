from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from sqlalchemy import func

from db.models.order_item import OrderItem
from db.models.order import Order
from db.models.product import Product

from schemas.order_item import (
    OrderItemCreate,
    OrderItemUpdate
)


class OrderItemRepository:
    def __init__(self, db: Session):
        self.db = db

    # -------------------------
    # CREATE ORDER ITEM
    # -------------------------
    def create_order_item(self, item: OrderItemCreate) -> OrderItem:
        """
        Create a new order item in the database.
        """

        order = (
            self.db.query(Order)
            .filter(Order.id == item.order_id)
            .first()
        )

        if not order:
            raise HTTPException(status_code=404, detail="Order not found!")

        product = (
            self.db.query(Product)
            .filter(Product.id == item.product_id)
            .first()
        )

        if not product:
            raise HTTPException(status_code=404, detail="Product not found!")

        db_item = OrderItem(
            order_id=item.order_id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price
        )

        try:
            self.db.add(db_item)
            self.db.commit()
            self.db.refresh(db_item)

        except IntegrityError as e:
            print(e)
            self.db.rollback()
            raise HTTPException(status_code=400, detail="Something went wrong!")

        return db_item

    # -------------------------
    # GET ORDER ITEMS
    # -------------------------
    def get_order_items(self, skip: int = 0, limit: int = 1000):

        total_count = self.db.query(func.count(OrderItem.id)).scalar()

        items = (
            self.db.query(OrderItem)
            .offset(skip)
            .limit(limit)
            .all()
        )

        return {
            "total_count": total_count,
            "skip": skip,
            "limit": limit,
            "data": items
        }

    # -------------------------
    # GET SINGLE ORDER ITEM
    # -------------------------
    def get_order_item(self, item_id: int) -> OrderItem:

        return (
            self.db.query(OrderItem)
            .filter(OrderItem.id == item_id)
            .first()
        )

    # -------------------------
    # UPDATE ORDER ITEM
    # -------------------------
    def update_order_item(
        self,
        item_id: int,
        item: OrderItemUpdate
    ) -> OrderItem:

        db_item = (
            self.db.query(OrderItem)
            .filter(OrderItem.id == item_id)
            .first()
        )

        if not db_item:
            raise HTTPException(status_code=404, detail="Order item not found!")

        if item.quantity is not None:
            db_item.quantity = item.quantity

        if item.price is not None:
            db_item.price = item.price

        try:
            self.db.commit()
            self.db.refresh(db_item)

        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e.orig))

        return db_item

    # -------------------------
    # DELETE ORDER ITEM
    # -------------------------
    def delete_order_item(self, item_id: int) -> bool:

        db_item = (
            self.db.query(OrderItem)
            .filter(OrderItem.id == item_id)
            .first()
        )

        if not db_item:
            raise HTTPException(status_code=404, detail="Order item not found!")

        self.db.delete(db_item)
        self.db.commit()

        return True
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from sqlalchemy import func

from db.models.cart import Cart
from schemas.cart import CartPagination, CartUpdate


class CartRepository:
    def __init__(self, db: Session):
        self.db = db

    # =========================
    # CREATE / GET OR CREATE CART
    # =========================
    def create_cart(self, user_id: int) -> Cart:

        # GET ACTIVE CART
        existing_cart = (
            self.db.query(Cart)
            .filter(
                Cart.user_id == user_id,
                Cart.is_checked_out == False
            )
            .first()
        )

        if existing_cart:
            return existing_cart

        db_cart = Cart(
            user_id=user_id,
            total_price=0,
            is_checked_out=False
        )

        try:
            self.db.add(db_cart)
            self.db.commit()
            self.db.refresh(db_cart)

        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Cart creation failed!"
            )

        return db_cart

    # =========================
    # GET CART BY USER (SECURED)
    # =========================
    def get_cart_by_user(self, user_id: int) -> Cart:

        cart = (
            self.db.query(Cart)
            .filter(
                Cart.user_id == user_id,
                Cart.is_checked_out == False
            )
            .first()
        )

        if not cart:
            raise HTTPException(
                status_code=404,
                detail="Cart not found!"
            )

        return cart

    # =========================
    # GET SINGLE CART (OWNERSHIP FIX)
    # =========================
    def get_cart(self, cart_id: int, user_id: int = None) -> Cart:

        query = self.db.query(Cart).filter(Cart.id == cart_id)

        # 🔒 ownership protection
        if user_id:
            query = query.filter(Cart.user_id == user_id)

        cart = query.first()

        if not cart:
            raise HTTPException(
                status_code=404,
                detail="Cart not found!"
            )

        return cart

    # =========================
    # GET CARTS (PAGINATION)
    # =========================
    def get_carts(self, skip: int = 0, limit: int = 100):

        total_count = self.db.query(func.count(Cart.id)).scalar()

        carts = (
            self.db.query(Cart)
            .order_by(Cart.id.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

        return CartPagination(
            total_count=total_count,
            skip=skip,
            limit=limit,
            data=carts
        )

    # =========================
    # UPDATE CART (SECURE)
    # =========================
    def update_cart(self, cart_id: int, cart: CartUpdate, user_id: int) -> Cart:

        db_cart = self.get_cart(cart_id, user_id)

        if cart.total_price is not None:
            db_cart.total_price = cart.total_price

        if cart.is_checked_out is not None:
            db_cart.is_checked_out = cart.is_checked_out

        try:
            self.db.commit()
            self.db.refresh(db_cart)

        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Cart update failed!"
            )

        return db_cart

    # =========================
    # DELETE CART (SECURE)
    # =========================
    def delete_cart(self, cart_id: int, user_id: int) -> bool:

        db_cart = self.get_cart(cart_id, user_id)

        try:
            self.db.delete(db_cart)
            self.db.commit()

        except Exception:
            self.db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Cart delete failed!"
            )

        return True
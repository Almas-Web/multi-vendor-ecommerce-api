from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from db.models.cart_item import CartItem
from db.models.cart import Cart
from db.models.product import Product

from schemas.cart_item import CartItemCreate, CartItemUpdate


class CartItemRepository:
    def __init__(self, db: Session):
        self.db = db

    # =========================
    # INTERNAL: UPDATE CART TOTAL
    # =========================
    def _update_cart_total(self, cart_id: int):

        items = (
            self.db.query(CartItem)
            .filter(CartItem.cart_id == cart_id)
            .all()
        )

        total = sum(item.quantity * item.price for item in items)

        cart = (
            self.db.query(Cart)
            .filter(Cart.id == cart_id)
            .first()
        )

        if cart:
            cart.total_price = total

    # =========================
    # ADD ITEM
    # =========================
    def add_item(self, item: CartItemCreate) -> CartItem:

        if item.quantity <= 0:
            raise HTTPException(400, "Quantity must be greater than 0")

        cart = self.db.query(Cart).filter(Cart.id == item.cart_id).first()

        if not cart:
            raise HTTPException(404, "Cart not found")

        if cart.is_checked_out:
            raise HTTPException(400, "Cart already checked out")

        product = (
            self.db.query(Product)
            .filter(Product.id == item.product_id)
            .first()
        )

        if not product:
            raise HTTPException(404, "Product not found")

        if not product.is_active:
            raise HTTPException(400, "Product is inactive")

        if product.stock < item.quantity:
            raise HTTPException(400, "Not enough stock")

        existing_item = (
            self.db.query(CartItem)
            .filter(
                CartItem.cart_id == item.cart_id,
                CartItem.product_id == item.product_id
            )
            .first()
        )

        if existing_item:

            new_qty = existing_item.quantity + item.quantity

            if product.stock < new_qty:
                raise HTTPException(
                    400,
                    "Not enough stock for updated quantity"
                )

            existing_item.quantity = new_qty

            db_item = existing_item

        else:

            db_item = CartItem(
                cart_id=item.cart_id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=product.price
            )

            self.db.add(db_item)

        try:

            self.db.commit()
            self.db.refresh(db_item)

            # UPDATE CART TOTAL
            self._update_cart_total(item.cart_id)
            self.db.commit()

        except IntegrityError:

            self.db.rollback()

            raise HTTPException(
                400,
                "Failed to add cart item"
            )

        return db_item

    # =========================
    # GET ITEM
    # =========================
    def get_item(self, item_id: int):

        return (
            self.db.query(CartItem)
            .filter(CartItem.id == item_id)
            .first()
        )

    # =========================
    # GET ITEMS BY CART
    # =========================
    def get_items_by_cart(self, cart_id: int):

        return (
            self.db.query(CartItem)
            .filter(CartItem.cart_id == cart_id)
            .all()
        )

    # =========================
    # UPDATE ITEM
    # =========================
    def update_item(self, item_id: int, item: CartItemUpdate):

        db_item = self.get_item(item_id)

        if not db_item:
            raise HTTPException(404, "Cart item not found")

        if item.quantity is not None:

            if item.quantity <= 0:
                raise HTTPException(
                    400,
                    "Quantity must be greater than 0"
                )

            product = (
                self.db.query(Product)
                .filter(Product.id == db_item.product_id)
                .first()
            )

            if not product:
                raise HTTPException(404, "Product not found")

            if product.stock < item.quantity:
                raise HTTPException(400, "Not enough stock")

            db_item.quantity = item.quantity

        try:

            self.db.commit()
            self.db.refresh(db_item)

            # UPDATE CART TOTAL
            self._update_cart_total(db_item.cart_id)
            self.db.commit()

        except IntegrityError:

            self.db.rollback()

            raise HTTPException(
                400,
                "Update failed"
            )

        return db_item

    # =========================
    # DELETE ITEM
    # =========================
    def delete_item(self, item_id: int) -> bool:

        db_item = self.get_item(item_id)

        if not db_item:
            raise HTTPException(404, "Cart item not found")

        try:

            cart_id = db_item.cart_id

            self.db.delete(db_item)
            self.db.commit()

            # UPDATE CART TOTAL
            self._update_cart_total(cart_id)
            self.db.commit()

            return True

        except:

            self.db.rollback()

            raise HTTPException(
                400,
                "Delete failed"
            )
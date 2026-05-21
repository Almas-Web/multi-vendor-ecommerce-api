from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

from db.models.cart import Cart
from db.models.cart_item import CartItem
from db.models.order import Order
from db.models.order_item import OrderItem
from db.models.product import Product
from db.models.address import Address


class CheckoutRepository:
    def __init__(self, db: Session):
        self.db = db

    def checkout(self, user_id: int, address_id: int):

        try:

            # =========================
            # GET ACTIVE CART
            # =========================
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

            # =========================
            # GET ADDRESS
            # =========================
            address = (
                self.db.query(Address)
                .filter(
                    Address.id == address_id,
                    Address.user_id == user_id
                )
                .first()
            )

            if not address:
                raise HTTPException(
                    status_code=404,
                    detail="Address not found!"
                )

            # =========================
            # GET CART ITEMS
            # =========================
            cart_items = (
                self.db.query(CartItem)
                .filter(CartItem.cart_id == cart.id)
                .all()
            )

            if not cart_items:
                raise HTTPException(
                    status_code=400,
                    detail="Cart is empty!"
                )

            total_price = 0
            product_map = {}

            # =========================
            # VALIDATION PHASE
            # =========================
            for item in cart_items:

                product = (
                    self.db.query(Product)
                    .filter(Product.id == item.product_id)
                    .with_for_update()
                    .first()
                )

                if not product:
                    raise HTTPException(
                        status_code=404,
                        detail="Product not found!"
                    )

                if not product.is_active:
                    raise HTTPException(
                        status_code=400,
                        detail=f"{product.title} is inactive"
                    )

                if product.stock < item.quantity:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Not enough stock for {product.title}"
                    )

                product_map[item.product_id] = product

                total_price += (
                    product.price * item.quantity
                )

            # =========================
            # CREATE ORDER
            # =========================
            order = Order(
                user_id=user_id,
                status="pending",
                total_price=total_price,

                # SHIPPING SNAPSHOT
                shipping_full_name=address.full_name,
                shipping_phone=address.phone,
                shipping_address=address.address_line,
                shipping_city=address.city,
                shipping_state=address.state,
                shipping_postal_code=address.postal_code,
                shipping_country=address.country
            )

            self.db.add(order)

            self.db.flush()

            # =========================
            # CREATE ORDER ITEMS
            # =========================
            for item in cart_items:

                product = product_map[item.product_id]

                order_item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=item.quantity,
                    price=product.price
                )

                self.db.add(order_item)

                # STOCK REDUCE
                product.stock -= item.quantity

            # =========================
            # FINALIZE CART
            # =========================
            cart.is_checked_out = True

            # CLEAR CART ITEMS
            for item in cart_items:
                self.db.delete(item)

            # =========================
            # COMMIT
            # =========================
            self.db.commit()

            self.db.refresh(order)

            return order

        except HTTPException as e:
            self.db.rollback()
            raise e

        except SQLAlchemyError:
            self.db.rollback()

            raise HTTPException(
                status_code=500,
                detail="Database error during checkout!"
            )

        except Exception as e:
            self.db.rollback()

            raise HTTPException(
                status_code=500,
                detail=str(e)
            )
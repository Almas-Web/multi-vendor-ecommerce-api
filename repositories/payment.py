import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException

from db.models.payment import Payment
from db.models.order import Order


class PaymentRepository:

    def __init__(self, db: Session):
        self.db = db

    # ----------------------
    # CREATE PAYMENT (SAFE)
    # ----------------------
    def create_payment(self, order_id: int, user_id: int, amount: float):

        order = (
            self.db.query(Order)
            .filter(Order.id == order_id)
            .first()
        )

        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        # 🔒 ownership check
        if order.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not allowed")

        # 🔒 prevent duplicate payment
        existing_payment = (
            self.db.query(Payment)
            .filter(Payment.order_id == order_id)
            .first()
        )

        if existing_payment:
            raise HTTPException(status_code=400, detail="Payment already exists")

        # 🔒 amount validation
        if float(amount) != float(order.total_price):
            raise HTTPException(status_code=400, detail="Invalid payment amount")

        payment = Payment(
            order_id=order_id,
            user_id=user_id,
            amount=amount,
            method="cod",
            status="pending",
            transaction_id=str(uuid.uuid4())
        )

        self.db.add(payment)

        # update order status
        order.status = "payment_pending"

        self.db.commit()
        self.db.refresh(payment)

        return payment

    # ----------------------
    # MARK AS PAID (SAFE)
    # ----------------------
    def mark_as_paid(self, payment_id: int):

        payment = (
            self.db.query(Payment)
            .filter(Payment.id == payment_id)
            .first()
        )

        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")

        # 🔒 prevent double payment update
        if payment.status == "success":
            raise HTTPException(status_code=400, detail="Already paid")

        payment.status = "success"

        # update order safely
        payment.order.status = "confirmed"

        self.db.commit()
        self.db.refresh(payment)

        return payment
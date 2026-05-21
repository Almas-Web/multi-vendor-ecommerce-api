from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.session import get_db
from apis.v1.user import get_current_user
from db.models.user import User

from repositories.payment import PaymentRepository

router = APIRouter()


# ----------------------
# CREATE PAYMENT
# ----------------------
@router.post("")
def create_payment(
    order_id: int,
    amount: float,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    repo = PaymentRepository(db)

    payment = repo.create_payment(
        order_id=order_id,
        user_id=current_user.id,
        amount=amount
    )

    return {
        "success": True,
        "message": "Payment created successfully",
        "data": {
            "payment_id": payment.id,
            "order_id": payment.order_id,
            "status": payment.status,
            "amount": payment.amount,
            "transaction_id": payment.transaction_id
        }
    }


# ----------------------
# MARK AS PAID (ADMIN ONLY)
# ----------------------
@router.patch("/{payment_id}/success")
def mark_paid(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # 🔒 proper RBAC (FIXED)
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can confirm payment"
        )

    repo = PaymentRepository(db)

    payment = repo.mark_as_paid(payment_id)

    return {
        "success": True,
        "message": "Payment confirmed",
        "data": {
            "payment_id": payment.id,
            "status": payment.status,
            "order_status": payment.order.status
        }
    }
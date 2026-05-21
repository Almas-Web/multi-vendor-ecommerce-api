from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.session import get_db
from db.models.user import User
from apis.v1.user import get_current_user

from repositories.checkout import CheckoutRepository

router = APIRouter()


# =========================
# CHECKOUT API
# =========================
@router.post("")
def checkout(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    service = CheckoutRepository(db)

    try:

        order = service.checkout(
            user_id=current_user.id,
            address_id=address_id
        )

        return {
            "success": True,
            "message": "Checkout successful",
            "data": {
                "order_id": order.id,
                "status": order.status,
                "total_price": order.total_price,

                # SHIPPING INFO
                "shipping_full_name": order.shipping_full_name,
                "shipping_phone": order.shipping_phone,
                "shipping_address": order.shipping_address,
                "shipping_city": order.shipping_city,
                "shipping_country": order.shipping_country
            }
        }

    except HTTPException as e:
        raise e

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong during checkout"
        )
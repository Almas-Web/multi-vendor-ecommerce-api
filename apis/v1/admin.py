from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db

from utils.deps import get_current_admin_user

from repositories.user import UserRepository
from schemas.user import UserRoleUpdate

router = APIRouter()


# =========================
# ADMIN DASHBOARD
# =========================
@router.get("/dashboard")
def admin_dashboard(
    admin_user=Depends(get_current_admin_user)
):
    return {"msg": "Welcome Admin"}


# =========================
# UPDATE USER ROLE
# =========================
@router.patch("/users/{user_id}/role")
def update_user_role(
    user_id: int,
    payload: UserRoleUpdate,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user)
):

    user = UserRepository(db).update_user_role(
        user_id=user_id,
        is_vendor=payload.is_vendor,
        is_superuser=payload.is_superuser
    )

    return {
        "success": True,
        "user": user
    }
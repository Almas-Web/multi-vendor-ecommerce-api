from fastapi import APIRouter, Depends

from db.models.user import User
from utils.deps import get_current_user


router = APIRouter()


# =========================================================
# 🔐 PROTECTED ROUTE - CURRENT USER PROFILE
# =========================================================
@router.get("/me")
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user


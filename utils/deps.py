from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from db.session import get_db
from repositories.user import UserRepository
from utils.jwt_manager import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


# =========================================================
# 👤 GET CURRENT USER
# =========================================================
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    user = UserRepository(db).get_user_by_id(payload.get("sub"))

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


# =========================================================
# 👤 ACTIVE USER
# =========================================================
def get_current_active_user(
    current_user=Depends(get_current_user)
):
    if not current_user.is_active:
        raise HTTPException(
            status_code=400,
            detail="Inactive user"
        )
    return current_user


# =========================================================
# 👑 ADMIN ONLY
# =========================================================
def get_current_admin_user(
    current_user=Depends(get_current_active_user)
):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    return current_user


# =========================================================
# 🛍️ VENDOR ONLY
# =========================================================
def get_current_vendor_user(
    current_user=Depends(get_current_active_user)
):
    if not current_user.is_vendor:
        raise HTTPException(
            status_code=403,
            detail="Vendor access required"
        )
    return current_user
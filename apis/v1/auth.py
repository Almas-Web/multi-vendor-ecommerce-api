from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from db.session import get_db
from repositories.user import UserRepository

from schemas.user import UserCreate, UserView, Token

from utils.jwt_manager import create_access_token, create_refresh_token, verify_token

router = APIRouter()


# =========================================================
# 🆕 REGISTER USER (SECURE VERSION)
# =========================================================
@router.post("", response_model=UserView)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db)
):

    user_repo = UserRepository(db=db)

    # 🔍 check existing user
    existing_user = user_repo.get_user_by_email(email=payload.email)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # 🆕 create user (ROLE FIXED - NO USER INPUT ROLE)
    new_user = user_repo.create_user(
        email=payload.email,
        password=payload.password,

        # 🔐 SECURITY FIX: roles controlled by backend only
        is_vendor=False,
        is_superuser=False
    )

    return new_user


# =========================================================
# 🔐 LOGIN -> TOKEN
# =========================================================
@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = UserRepository(db=db).get_user_for_token(
        email=form_data.username,
        password=form_data.password
    )

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    refresh_token = create_refresh_token(
        data={"sub": str(user.id)}
    )

    return Token(
        access_token=access_token,
        refresh_token=refresh_token
    )


# =========================================================
# 🔄 REFRESH TOKEN
# =========================================================
@router.post("/refresh", response_model=Token)
async def refresh_access_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):

    payload = verify_token(refresh_token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )

    user = UserRepository(db=db).get_user_by_id(
        id=payload.get("sub")
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    new_refresh_token = create_refresh_token(
        data={"sub": str(user.id)}
    )

    return Token(
        access_token=access_token,
        refresh_token=new_refresh_token
    )
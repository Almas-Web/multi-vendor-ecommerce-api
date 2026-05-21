from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from db.models import user
from db.models.user import User
from db.session import get_db

from utils.password_manager import PasswordManager
from utils.jwt_manager import verify_token


# 🔐 OAuth2 scheme (Swagger login support)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    # =========================================================
    # 🔍 GET USER BY EMAIL
    # =========================================================
    def get_user_by_email(self, email: str) -> Optional[User]:
        return (
            self.db.query(User)
            .filter(func.lower(User.email) == func.lower(email))
            .first()
        )

    # =========================================================
    # 🆕 CREATE USER (REGISTER)
    # =========================================================
    def create_user(
        self,
        email: str,
        password: str,
        is_active: bool = True,
        is_superuser: bool = False,
        is_vendor: bool = False
    ) -> User:

        # 🔐 hash password
        hashed_password = PasswordManager.get_password_hash(password)

        # 🧾 create user object
        db_user = User(
            email=email,
            password=hashed_password,
            is_active=is_active,
            is_superuser=is_superuser,
            is_vendor=is_vendor
        )

        self.db.add(db_user)

        try:
            self.db.commit()
            self.db.refresh(db_user)

        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )

        return db_user

    # =========================================================
    # 🔍 GET USER BY ID
    # =========================================================
    def get_user_by_id(self, id: int) -> Optional[User]:
        return (
            self.db.query(User)
            .filter(User.id == id)
            .first()
        )

    # =========================================================
    # 🔐 LOGIN CHECK (FOR /TOKEN)
    # =========================================================
    def get_user_for_token(self, email: str, password: str) -> Optional[User]:

        user = self.get_user_by_email(email)

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )

        is_password_matched = PasswordManager.verify_password(
            password,
            user.password
        )

        if not is_password_matched:
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )

        return user

    # =========================================================
    # 🔐 CURRENT USER FROM JWT TOKEN
    # =========================================================
    @staticmethod
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

        user = db.query(User).filter(
            User.id == payload.get("sub")
        ).first()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return user
    
        # =========================
    # UPDATE USER ROLE
    # =========================
    def update_user_role(
        self,
        user_id: int,
        is_vendor: bool,
        is_superuser: bool
    ):

        user = (
            self.db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        user.is_vendor = is_vendor
        user.is_superuser = is_superuser

        try:
            self.db.commit()
            self.db.refresh(user)

        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Role update failed"
            )

    
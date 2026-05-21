from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

from db.models.address import Address
from schemas.address import AddressCreate, AddressUpdate


class AddressRepository:
    def __init__(self, db: Session):
        self.db = db

    # =========================
    # CREATE ADDRESS
    # =========================
    def create_address(self, payload: AddressCreate, user_id: int):

        try:

            # 🔥 only one default address
            if payload.is_default:
                (
                    self.db.query(Address)
                    .filter(Address.user_id == user_id)
                    .update({"is_default": False})
                )

            db_address = Address(
                user_id=user_id,
                full_name=payload.full_name,
                phone=payload.phone,
                address_line=payload.address_line,
                city=payload.city,
                state=payload.state,
                postal_code=payload.postal_code,
                country=payload.country,
                is_default=payload.is_default
            )

            self.db.add(db_address)
            self.db.commit()
            self.db.refresh(db_address)

            return db_address

        except SQLAlchemyError:
            self.db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Address creation failed!"
            )

    # =========================
    # GET MY ADDRESSES
    # =========================
    def get_my_addresses(self, user_id: int):

        return (
            self.db.query(Address)
            .filter(Address.user_id == user_id)
            .order_by(Address.id.desc())
            .all()
        )

    # =========================
    # GET SINGLE ADDRESS
    # =========================
    def get_address(self, address_id: int, user_id: int):

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

        return address

    # =========================
    # UPDATE ADDRESS
    # =========================
    def update_address(
        self,
        address_id: int,
        payload: AddressUpdate,
        user_id: int
    ):

        address = self.get_address(address_id, user_id)

        try:

            # 🔥 only one default address
            if payload.is_default:

                (
                    self.db.query(Address)
                    .filter(Address.user_id == user_id)
                    .update({"is_default": False})
                )

            for key, value in payload.dict(exclude_unset=True).items():
                setattr(address, key, value)

            self.db.commit()
            self.db.refresh(address)

            return address

        except SQLAlchemyError:
            self.db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Address update failed!"
            )

    # =========================
    # DELETE ADDRESS
    # =========================
    def delete_address(self, address_id: int, user_id: int):

        address = self.get_address(address_id, user_id)

        try:

            self.db.delete(address)
            self.db.commit()

            return True

        except SQLAlchemyError:
            self.db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Address delete failed!"
            )
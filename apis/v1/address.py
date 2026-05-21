from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db.session import get_db
from db.models.user import User
from apis.v1.user import get_current_user

from repositories.address import AddressRepository
from schemas.address import (
    AddressCreate,
    AddressRead,
    AddressUpdate
)

router = APIRouter()


# =========================
# CREATE ADDRESS
# =========================
@router.post(
    "",
    response_model=AddressRead,
    status_code=status.HTTP_201_CREATED
)
def create_address(
    payload: AddressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    repo = AddressRepository(db)

    return repo.create_address(
        payload=payload,
        user_id=current_user.id
    )


# =========================
# GET MY ADDRESSES
# =========================
@router.get("", response_model=list[AddressRead])
def get_my_addresses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    repo = AddressRepository(db)

    return repo.get_my_addresses(
        user_id=current_user.id
    )


# =========================
# UPDATE ADDRESS
# =========================
@router.put("/{address_id}", response_model=AddressRead)
def update_address(
    address_id: int,
    payload: AddressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    repo = AddressRepository(db)

    return repo.update_address(
        address_id=address_id,
        payload=payload,
        user_id=current_user.id
    )


# =========================
# DELETE ADDRESS
# =========================
@router.delete("/{address_id}")
def delete_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    repo = AddressRepository(db)

    repo.delete_address(
        address_id=address_id,
        user_id=current_user.id
    )

    return {
        "success": True,
        "message": "Address deleted successfully"
    }
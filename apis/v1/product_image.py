import os
from uuid import uuid4

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.session import get_db
from db.models.user import User
from db.models.product import Product
from apis.v1.user import get_current_user

from utils.const import UPLOAD_FOLDER
from repositories.product_image import ProductImageRepository

router = APIRouter()
def check_product_access(product: Product, user: User):
    if not user.is_superuser and product.author_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed"
        )
    
@router.post("/{product_id}")
async def upload_images(
    product_id: int,
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(404, "Product not found")

    # 🔐 permission check
    check_product_access(product, current_user)

    repo = ProductImageRepository(db)
    saved = []

    for file in files:

        if not file.content_type.startswith("image"):
            raise HTTPException(400, "Only image allowed")

        filename = f"{uuid4()}_{file.filename}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        image = repo.create_image(
            product_id=product_id,
            image_url=filename
        )

        saved.append(image)

    return {
        "success": True,
        "data": saved
    }

@router.get("/{product_id}")
def get_images(
    product_id: int,
    db: Session = Depends(get_db)
):

    repo = ProductImageRepository(db)
    images = repo.get_images(product_id)

    return {
        "product_id": product_id,
        "images": [
            {
                "id": img.id,
                "url": f"/static/{img.image_url}"
            }
            for img in images
        ]
    }
@router.delete("/{image_id}")
def delete_image(
    image_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    repo = ProductImageRepository(db)

    image = repo.get_image(image_id)

    if not image:
        raise HTTPException(404, "Image not found")

    product = db.query(Product).filter(Product.id == image.product_id).first()

    if not product:
        raise HTTPException(404, "Product not found")

    # 🔐 permission check
    check_product_access(product, current_user)

    # delete DB record
    repo.delete_image(image_id)

    # delete file from storage (IMPORTANT)
    file_path = os.path.join(UPLOAD_FOLDER, image.image_url)

    if os.path.exists(file_path):
        os.remove(file_path)

    return {
        "success": True,
        "message": "Image deleted successfully"
    }
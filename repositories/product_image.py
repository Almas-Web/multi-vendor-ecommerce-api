import os
from sqlalchemy.orm import Session
from fastapi import HTTPException

from db.models.product_image import ProductImage


class ProductImageRepository:

    def __init__(self, db: Session):
        self.db = db

    # =========================
    # CREATE IMAGE
    # =========================
    def create_image(self, product_id: int, image_url: str):

        image = ProductImage(
            product_id=product_id,
            image_url=image_url
        )

        self.db.add(image)
        self.db.commit()
        self.db.refresh(image)

        return image

    # =========================
    # GET ALL IMAGES BY PRODUCT
    # =========================
    def get_images(self, product_id: int):

        return (
            self.db.query(ProductImage)
            .filter(ProductImage.product_id == product_id)
            .all()
        )

    # =========================
    # GET SINGLE IMAGE
    # =========================
    def get_image(self, image_id: int):

        image = (
            self.db.query(ProductImage)
            .filter(ProductImage.id == image_id)
            .first()
        )

        if not image:
            raise HTTPException(status_code=404, detail="Image not found")

        return image

    # =========================
    # DELETE IMAGE
    # =========================
    def delete_image(self, image_id: int):

        image = self.get_image(image_id)

        # delete from DB
        self.db.delete(image)
        self.db.commit()

        return True
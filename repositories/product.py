import os
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from sqlalchemy import func

from db.models.product import Product
from db.models.user import User

from schemas.product import ProductCreate, ProductPagination, ProductUpdate

#UPLOAD_FOLDER = "uploads/images"


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    # -------------------------
    # CREATE PRODUCT
    # -------------------------
    def create_product(self, product: ProductCreate, author_id: int) -> Product:
        """
        Create a new product in the database.
        """

        db_product = Product(
            title=product.title,
            slug=product.slug,
            price=product.price,
            stock=product.stock,
            is_active=product.is_active,
            author_id=author_id
        )

        try:
            self.db.add(db_product)
            self.db.commit()
            self.db.refresh(db_product)

        except IntegrityError as e:
            print(e)
            self.db.rollback()
            raise HTTPException(status_code=400, detail="Something went wrong!")

        return db_product

    # -------------------------
    # GET PRODUCTS (PAGINATION)
    # -------------------------
    def get_products(self, skip: int = 0, limit: int = 1000):

        total_count = self.db.query(func.count(Product.id)).scalar()

        products = (
            self.db.query(Product)
            .order_by(Product.created_at.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

        return ProductPagination(
            total_count=total_count,
            skip=skip,
            limit=limit,
            data=products
        )

    # -------------------------
    # GET SINGLE PRODUCT
    # -------------------------
    def get_product(self, product_id: int) -> Product:

        return (
            self.db.query(Product)
            .filter(Product.id == product_id)
            .first()
        )

    # -------------------------
    # UPDATE PRODUCT
    # -------------------------
    def update_product(
        self,
        product_id: int,
        product: ProductUpdate,
        current_user: User
    ) -> Product:

        db_product = (
            self.db.query(Product)
            .filter(Product.id == product_id)
            .first()
        )

        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found!")

        # =========================
        # OWNER/VENDOR SECURITY
        # =========================
        if (
            db_product.author_id != current_user.id
            and not current_user.is_superuser
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not allowed to update this product"
            )

        if product.title:
            db_product.title = product.title
            db_product.slug = product.slug

        if product.price is not None:
            db_product.price = product.price

        if product.stock is not None:
            db_product.stock = product.stock

        if product.is_active is not None:
            db_product.is_active = product.is_active

        try:
            self.db.commit()
            self.db.refresh(db_product)

        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e.orig))

        return db_product

    # -------------------------
    # DELETE PRODUCT
    # -------------------------
    def delete_product(
        self,
        product_id: int,
        current_user: User
    ) -> bool:

        db_product = (
            self.db.query(Product)
            .filter(Product.id == product_id)
            .first()
        )

        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found!")

        # =========================
        # OWNER/VENDOR SECURITY
        # =========================
        if (
            db_product.author_id != current_user.id
            and not current_user.is_superuser
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not allowed to delete this product"
            )

        self.db.delete(db_product)
        self.db.commit()

        return True

    # -------------------------
    # IMAGE HANDLING (COMMENTED FOR NOW - FUTURE USE)
    # -------------------------

    # def remove_previous_image(self, old_image_path):
    #     """
    #     Remove old image from filesystem
    #     """
    #     try:
    #         old_image_file_path = os.path.join(UPLOAD_FOLDER, old_image_path)

    #         if os.path.exists(old_image_file_path):
    #             os.remove(old_image_file_path)

    #     except Exception as e:
    #         print(e)
    #         return False

    #     return True


    # def save_image_path_to_db(self, product: Product, new_image_path: str):
    #     """
    #     Save image path to product table
    #     """
    #     product.image_url = new_image_path

    #     try:
    #         self.db.commit()

    #     except:
    #         self.db.rollback()
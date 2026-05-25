from fastapi import HTTPException, status

from db.models.user import User
from db.models.product import Product


# =========================
# ROLE CHECK: ADMIN
# =========================
def is_admin(user: User) -> bool:
    return user.is_superuser


# =========================
# ROLE CHECK: PRODUCT OWNER
# =========================
def is_product_owner(user: User, product: Product) -> bool:
    return product.author_id == user.id


# =========================
# PRODUCT ACCESS CONTROL
# =========================
def require_product_access(user: User, product: Product):
    """
    Admin can access everything
    Vendor can access only own products
    """

    if not user.is_superuser and product.author_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to access this product"
        )


# =========================
# IMAGE ACCESS CONTROL
# =========================
def require_image_access(user: User, product: Product):
    """
    Image access depends on product ownership
    Admin can access all images
    Vendor can access only own product images
    """

    if not user.is_superuser and product.author_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to access this image"
        )


# =========================
# OPTIONAL: ADMIN ONLY ACCESS
# =========================
def require_admin(user: User):
    if not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
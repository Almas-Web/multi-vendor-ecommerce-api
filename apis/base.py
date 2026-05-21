from fastapi import APIRouter

from apis.v1 import address, auth, payment, user, admin, vendor,product,category,cart,cart_item,order,order_item,checkout


api_router = APIRouter()

api_router.include_router(auth.router,prefix="/auth",tags=["auth"])

api_router.include_router(user.router,prefix="/users",tags=["users"])

api_router.include_router(admin.router,prefix="/admin",tags=["admin"])

api_router.include_router(vendor.router,prefix="/vendor",tags=["vendor"])
api_router.include_router(product.router,prefix="/products",
                          tags=["products"])
api_router.include_router(category.router,prefix="/categories",
                          tags=["categories"])
api_router.include_router(cart.router,prefix="/carts",tags=["carts"])
api_router.include_router(cart_item.router,prefix="/cart-items",
                          tags=["cart-items"])
api_router.include_router(order.router,prefix="/orders",tags=["orders"])
api_router.include_router(order_item.router,prefix="/order-items",
                          tags=["order-items"])
api_router.include_router(checkout.router,prefix="/checkouts",
                          tags=["checkouts"])
api_router.include_router(payment.router,prefix="/payments",
                          tags=["payments"])
api_router.include_router(address.router,prefix="/addresses",
                          tags=["addresses"])

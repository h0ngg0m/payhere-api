from fastapi import APIRouter

from app.api.v1.endpoint import auth, product, user

api_v1_router = APIRouter()
api_v1_router.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
api_v1_router.include_router(user.router, prefix="/api/v1/users", tags=["User"])
api_v1_router.include_router(
    product.router, prefix="/api/v1/products", tags=["Product"]
)

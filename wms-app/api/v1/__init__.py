from fastapi import APIRouter

from core import settings
from .orders import router as order_router
from .products import router as products_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)

router.include_router(
    products_router,
    prefix=settings.api.v1.products,
)

router.include_router(
    order_router,
    prefix=settings.api.v1.orders,
)

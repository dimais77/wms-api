from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import db_helper
from services import OrderService
from services import ProductService


def _get_session() -> AsyncSession:
    return Depends(db_helper.get_transactional_session)


def get_product_service(
    session: AsyncSession = _get_session(),
) -> ProductService:
    return ProductService(session)


def get_order_service(
    session: AsyncSession = _get_session(),
) -> OrderService:
    return OrderService(session)

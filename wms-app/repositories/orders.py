from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import Order


class OrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, order: Order) -> Order:
        self.session.add(order)
        await self.session.flush()
        return order

    async def find_by_id(self, order_id: int) -> Optional[Order]:
        stmt = (
            select(Order).options(selectinload(Order.items)).where(Order.id == order_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def read_all(self) -> List[Order]:
        stmt = select(Order).options(selectinload(Order.items))
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def update_status(self, order: Order, new_status: str) -> Order:
        order.status = new_status
        await self.session.flush()
        return order

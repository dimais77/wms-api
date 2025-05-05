from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from models import OrderItem


class OrderItemRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_items(self, items: List[OrderItem]) -> None:
        self.session.add_all(items)
        await self.session.flush()

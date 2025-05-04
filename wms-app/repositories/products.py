from typing import Optional, List

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from models import Product


class ProductRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def read_all(self) -> List[Product]:
        result = await self.session.execute(select(Product))
        return list(result.scalars().all())

    async def find_by_id(self, product_id: int) -> Optional[Product]:
        return await self.session.get(Product, product_id)

    async def find_by_name(self, names: list[str]) -> List[Product]:
        # stmt = select(Product).where(Product.name.ilike(f"%{name}%"))
        # result = await self.session.execute(stmt)
        filters = [Product.name.ilike(f"%{name}%") for name in names]
        stmt = select(Product).where(or_(*filters))
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create(self, product: Product) -> Product:
        self.session.add(product)
        await self.session.flush()
        return product

    async def update(self, product: Product) -> Product:
        await self.session.flush()
        return product

    async def delete(self, product: Product) -> None:
        await self.session.delete(product)
        await self.session.flush()

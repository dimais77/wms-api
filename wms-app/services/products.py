from typing import Optional, List

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models.products import Product
from repositories.products import ProductRepository
from schemas.products import ProductCreateSchema, ProductUpdateSchema


class ProductService:
    def __init__(self, session: AsyncSession):
        self.repo = ProductRepository(session)
        self.session = session

    async def get_all_products(self) -> List[Product]:
        return await self.repo.read_all()

    async def get_product_by_id(self, product_id: int) -> Optional[Product]:
        return await self.repo.find_by_id(product_id)

    async def search_products_by_name(self, names: list[str]) -> List[Product]:
        return await self.repo.find_by_name(names)

    async def create_product(self, schema: ProductCreateSchema) -> Product:
        product = Product(**schema.model_dump())
        try:
            return await self.repo.create(product)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product with this name already exists",
            )

    async def update_product(
        self, product_id: int, schema: ProductUpdateSchema
    ) -> Optional[Product]:
        existing = await self.repo.find_by_id(product_id)
        if not existing:
            return None
        for field, value in schema.model_dump(exclude_unset=True).items():
            setattr(existing, field, value)
        try:
            return await self.repo.update(existing)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product with this name already exists",
            )

    async def delete_product(self, product_id: int) -> bool:
        existing = await self.repo.find_by_id(product_id)
        if not existing:
            return False
        await self.repo.delete(existing)
        return True

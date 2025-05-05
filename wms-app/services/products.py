from typing import Optional, List

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from dto import ProductDTO, ProductCreateDTO, ProductUpdateDTO
from models import Product
from repositories import ProductRepository


class ProductService:
    def __init__(self, session: AsyncSession):
        self.repo = ProductRepository(session)

    async def get_all_products(self) -> List[ProductDTO]:
        products = await self.repo.read_all()
        return [ProductDTO.model_validate(p) for p in products]

    async def get_product_by_id(self, product_id: int) -> Optional[ProductDTO]:
        product = await self.repo.find_by_id(product_id)
        return ProductDTO.model_validate(product) if product else None

    async def search_products_by_name(self, names: list[str]) -> List[ProductDTO]:
        products = await self.repo.find_by_name(names)
        return [ProductDTO.model_validate(p) for p in products]

    async def create_product(self, dto: ProductCreateDTO) -> ProductDTO:
        product = Product(**dto.model_dump())
        try:
            created = await self.repo.create(product)
            return ProductDTO.model_validate(created)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product with this name already exists",
            )

    async def update_product(
        self, product_id: int, dto: ProductUpdateDTO
    ) -> Optional[ProductDTO]:
        existing = await self.repo.find_by_id(product_id)
        if not existing:
            return None
        for k, v in dto.model_dump(exclude_unset=True).items():
            setattr(existing, k, v)
        try:
            updated = await self.repo.update(existing)
            return ProductDTO.model_validate(updated)
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

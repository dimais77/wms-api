from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_helper import db_helper
from schemas.products import (
    ProductResponseSchema,
    ProductCreateSchema,
    ProductUpdateSchema,
)
from services.products import ProductService

router = APIRouter(tags=["Products"])


def get_service(
    session: AsyncSession = Depends(db_helper.get_transactional_session),
) -> ProductService:
    return ProductService(session)


@router.post(
    "/",
    response_model=ProductResponseSchema,
    summary="Добавить продукт",
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    payload: ProductCreateSchema,
    service: ProductService = Depends(get_service),
) -> ProductResponseSchema:
    try:
        product = await service.create_product(payload)
        return ProductResponseSchema.model_validate(product)
    except HTTPException:
        raise


@router.get(
    "/",
    response_model=list[ProductResponseSchema],
    summary="Список всех продуктов",
)
async def read_all_products(
    service: ProductService = Depends(get_service),
) -> list[ProductResponseSchema]:
    products = await service.get_all_products()
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Products not found",
        )
    return [ProductResponseSchema.model_validate(p) for p in products]


@router.get(
    "/search",
    response_model=list[ProductResponseSchema],
    summary="Поиск продуктов по имени",
)
async def search_products(
    names: Annotated[
        list[str],
        Query(
            ...,
            alias="product_name",
            min_length=1,
            max_length=100,
            description="Подстроки для поиска в названии (можно несколько)",
        ),
    ],
    service: ProductService = Depends(get_service),
) -> list[ProductResponseSchema]:
    products = await service.search_products_by_name(names)
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Products not found",
        )
    return [ProductResponseSchema.model_validate(p) for p in products]


@router.get(
    "/{product_id}",
    response_model=ProductResponseSchema,
    summary="Детали продукта по ID  ",
)
async def read_product_by_id(
    product_id: Annotated[
        int, Path(..., ge=1, description="Уникальный ID продукта, целое ≥1")
    ],
    service: ProductService = Depends(get_service),
) -> ProductResponseSchema:
    product = await service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return ProductResponseSchema.model_validate(product)


@router.put(
    "/{product_id}",
    response_model=ProductResponseSchema,
    summary="Обновить продукт",
)
async def update_product(
    product_id: Annotated[
        int,
        Path(
            ...,
            ge=1,
            description="ID продукта для обновления",
        ),
    ],
    payload: ProductUpdateSchema,
    service: ProductService = Depends(get_service),
) -> ProductResponseSchema:
    updated = await service.update_product(product_id, payload)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return ProductResponseSchema.model_validate(updated)


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить продукт",
)
async def delete_product(
    product_id: Annotated[
        int,
        Path(
            ...,
            description="ID продукта для удаления",
        ),
    ],
    service: ProductService = Depends(get_service),
) -> None:
    deleted = await service.delete_product(product_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

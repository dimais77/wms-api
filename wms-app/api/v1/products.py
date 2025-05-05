from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from api.v1.dependencies import get_product_service
from dto.products import ProductCreateDTO, ProductUpdateDTO
from schemas.products import (
    ProductResponseSchema,
    ProductCreateSchema,
    ProductUpdateSchema,
)
from services.products import ProductService

router = APIRouter(
    tags=["Products"],
)


@router.post(
    "/",
    response_model=ProductResponseSchema,
    summary="Добавить продукт",
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    payload: ProductCreateSchema,
    service: ProductService = Depends(get_product_service),
) -> ProductResponseSchema:
    dto = ProductCreateDTO(**payload.model_dump())
    created = await service.create_product(dto)
    return ProductResponseSchema.model_validate(created)


@router.get(
    "/",
    response_model=list[ProductResponseSchema],
    summary="Список всех продуктов",
)
async def read_all_products(
    service: ProductService = Depends(get_product_service),
) -> list[ProductResponseSchema]:
    products = await service.get_all_products()
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
    service: ProductService = Depends(get_product_service),
) -> list[ProductResponseSchema]:
    products = await service.search_products_by_name(names)
    if not products:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Products not found",
        )
    return [ProductResponseSchema.model_validate(p) for p in products]


@router.get(
    "/{product_id}",
    response_model=ProductResponseSchema,
    summary="Детали продукта по ID",
)
async def read_product_by_id(
    product_id: Annotated[
        int,
        Path(..., ge=1, description="Уникальный ID продукта, целое ≥1"),
    ],
    service: ProductService = Depends(get_product_service),
) -> ProductResponseSchema:
    product = await service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Product not found")
    return ProductResponseSchema.model_validate(product)


@router.put(
    "/{product_id}",
    response_model=ProductResponseSchema,
    summary="Обновить продукт",
)
async def update_product(
    product_id: Annotated[
        int,
        Path(..., ge=1, description="ID продукта для обновления"),
    ],
    payload: ProductUpdateSchema,
    service: ProductService = Depends(get_product_service),
) -> ProductResponseSchema:
    dto = ProductUpdateDTO(**payload.model_dump(exclude_unset=True))
    updated = await service.update_product(product_id, dto)
    if not updated:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Product not found")
    return ProductResponseSchema.model_validate(updated)


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить продукт",
)
async def delete_product(
    product_id: Annotated[
        int,
        Path(..., ge=1, description="ID продукта для удаления"),
    ],
    service: ProductService = Depends(get_product_service),
) -> None:
    deleted = await service.delete_product(product_id)
    if not deleted:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Product not found")

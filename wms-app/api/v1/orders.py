from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Path, status

from api.v1.dependencies import get_order_service
from dto.orders import OrderCreateDTO, OrderUpdateStatusDTO
from schemas.orders import (
    OrderCreateSchema,
    OrderResponseSchema,
    OrderUpdateStatusSchema,
)
from services.orders import OrderService

router = APIRouter(
    tags=["Orders"],
)


@router.post(
    "/",
    response_model=OrderResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Создать заказ",
)
async def create_order(
    payload: OrderCreateSchema,
    service: OrderService = Depends(get_order_service),
) -> OrderResponseSchema:
    dto = OrderCreateDTO(**payload.model_dump())
    order = await service.create_order(dto)
    return OrderResponseSchema.model_validate(order)


@router.get(
    "/",
    response_model=List[OrderResponseSchema],
    summary="Список всех заказов",
)
async def read_all_orders(
    service: OrderService = Depends(get_order_service),
) -> List[OrderResponseSchema]:
    orders = await service.get_all_orders()
    return [OrderResponseSchema.model_validate(o) for o in orders]


@router.get(
    "/{order_id}",
    response_model=OrderResponseSchema,
    summary="Детали заказа",
)
async def read_order_by_id(
    order_id: Annotated[int, Path(..., ge=1, description="ID заказа")],
    service: OrderService = Depends(get_order_service),
) -> OrderResponseSchema:
    order = await service.get_order_by_id(order_id)
    if not order:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Order not found")
    return OrderResponseSchema.model_validate(order)


@router.patch(
    "/{order_id}/status",
    response_model=OrderResponseSchema,
    summary="Обновить статус заказа",
)
async def patch_order_status(
    order_id: Annotated[int, Path(..., ge=1, description="ID заказа")],
    payload: OrderUpdateStatusSchema,
    service: OrderService = Depends(get_order_service),
) -> OrderResponseSchema:
    dto = OrderUpdateStatusDTO(**payload.model_dump())
    updated = await service.update_order_status(order_id, dto)
    return OrderResponseSchema.model_validate(updated)

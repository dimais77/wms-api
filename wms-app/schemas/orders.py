from datetime import datetime
from typing import Annotated, List

from pydantic import BaseModel, ConfigDict, Field

from models import OrderStatusEnum
from .order_items import OrderItemResponseSchema


class OrderCreateSchema(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "items": [
                    {"product_id": 1, "quantity": 1},
                    {"product_id": 2, "quantity": 2},
                    {"product_id": 3, "quantity": 3},
                ]
            }
        },
    )

    items: Annotated[
        List[dict[str, int]],
        Field(..., description="Список элементов заказа", min_length=1),
    ]


class OrderUpdateStatusSchema(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={"example": {"status": OrderStatusEnum.pending.value}},
    )

    status: Annotated[
        OrderStatusEnum,
        Field(..., description="Новый статус заказа"),
    ]


class OrderResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    status: str
    items: List[OrderItemResponseSchema]

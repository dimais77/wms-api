from datetime import datetime
from typing import Annotated, List

from pydantic import BaseModel, ConfigDict, Field

from .order_items import OrderItemResponseSchema


class OrderCreateSchema(BaseModel):
    model_config = ConfigDict(extra="ignore")

    items: Annotated[
        list[dict[str, int]],
        Field(..., description="[{product_id, quantity}]", min_length=1),
    ]


class OrderUpdateStatusSchema(BaseModel):
    model_config = ConfigDict(extra="ignore")

    status: Annotated[str, Field(..., description="Новый статус заказа")]


class OrderResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    status: str
    items: List[OrderItemResponseSchema]

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from dto.order_items import OrderItemDTO


class OrderDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    status: str
    items: list[OrderItemDTO]


class OrderCreateDTO(BaseModel):
    model_config = ConfigDict(extra="forbid")

    items: list[dict[str, int]]


class OrderUpdateStatusDTO(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: str

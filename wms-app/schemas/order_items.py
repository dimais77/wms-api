from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class OrderItemBase(BaseModel):
    model_config = ConfigDict(extra="ignore")

    product_id: Annotated[int, Field(..., gt=0, description="ID товара")]
    quantity: Annotated[int, Field(..., gt=0, description="Количество товара в заказе")]


class OrderItemResponseSchema(OrderItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_id: int
    price: float

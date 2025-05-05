from pydantic import BaseModel, ConfigDict


class OrderItemDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_id: int
    product_id: int
    quantity: int
    price: float

from pydantic import BaseModel, ConfigDict


class ProductDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    price: float
    quantity: int


class ProductCreateDTO(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    description: str | None
    price: float
    quantity: int


class ProductUpdateDTO(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None
    description: str | None
    price: float | None
    quantity: int | None

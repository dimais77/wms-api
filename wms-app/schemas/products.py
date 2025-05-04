from pydantic import BaseModel, Field, ConfigDict


class ProductBase(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name: str = Field(..., max_length=100)
    description: str | None = Field(None)
    price: float = Field(..., gt=0)
    quantity: int = Field(..., ge=0)


class ProductCreateSchema(ProductBase):
    pass


class ProductUpdateSchema(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name: str | None = Field(None, max_length=100)
    description: str | None = Field(None)
    price: float | None = Field(None, gt=0)
    quantity: int | None = Field(None, ge=0)


class ProductResponseSchema(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

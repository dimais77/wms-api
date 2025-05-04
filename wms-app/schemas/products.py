from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name: Annotated[
        str,
        Field(..., max_length=100, description="Название товара"),
    ]
    description: Annotated[
        Optional[str],
        Field(None, description="Описание товара"),
    ]
    price: Annotated[
        float,
        Field(..., gt=0, description="Цена, больше 0"),
    ]
    quantity: Annotated[
        int,
        Field(..., ge=0, description="Количество на складе, ≥0"),
    ]


class ProductCreateSchema(ProductBase):
    pass


class ProductUpdateSchema(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name: Annotated[
        Optional[str],
        Field(None, max_length=100, description="Новое название"),
    ]
    description: Annotated[
        Optional[str],
        Field(None, description="Новое описание"),
    ]
    price: Annotated[
        Optional[float],
        Field(None, gt=0, description="Новая цена"),
    ]
    quantity: Annotated[
        Optional[int],
        Field(None, ge=0, description="Новое количество"),
    ]


class ProductResponseSchema(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

from sqlalchemy import String, Text, Numeric, Integer, CheckConstraint, func, Index
from sqlalchemy.orm import Mapped, mapped_column

from models import IntIdPkMixin, TimestampsMixin, Base


class Products(IntIdPkMixin, TimestampsMixin, Base):
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
    )
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[float] = mapped_column(
        Numeric(precision=12, scale=2),
        CheckConstraint('price > 0', name="ck_products_price"),
    )
    quantity: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint('quantity >= 0', name="ck_products_quantity"),
    )

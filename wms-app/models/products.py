from decimal import Decimal

from sqlalchemy import String, Text, Numeric, Integer, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base, IntIdPkMixin, TimestampsMixin
from models import OrderItem


class Product(IntIdPkMixin, TimestampsMixin, Base):
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )
    price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        CheckConstraint(
            "price > 0",
            name="ck_products_price",
        ),
        nullable=False,
    )
    quantity: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint(
            "quantity >= 0",
            name="ck_products_quantity",
        ),
        nullable=False,
    )

    items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="product",
    )

    def __repr__(self) -> str:
        return (
            f"<Product(id={self.id!r}, name={self.name!r}, "
            f"price={self.price!r}, quantity={self.quantity!r})>"
        )

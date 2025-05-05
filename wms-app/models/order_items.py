from typing import TYPE_CHECKING

from sqlalchemy import Integer, ForeignKey, Numeric, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base, IntIdPkMixin, TimestampsMixin

if TYPE_CHECKING:
    from models import Order, Product


class OrderItem(IntIdPkMixin, TimestampsMixin, Base):
    order_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    product_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("products.id"),
        nullable=False,
        index=True,
    )
    quantity: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint("quantity > 0", name="ck_order_items_quantity"),
        nullable=False,
    )
    price: Mapped[float] = mapped_column(
        Numeric(12, 2),
        CheckConstraint("price >= 0", name="ck_order_items_price"),
        nullable=False,
    )

    order: Mapped["Order"] = relationship(
        "Order",
        back_populates="items",
    )
    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="items",
    )

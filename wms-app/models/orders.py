from typing import TYPE_CHECKING

from sqlalchemy import String, DateTime, func, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base, IntIdPkMixin, TimestampsMixin
from .enums import OrderStatusEnum

if TYPE_CHECKING:
    from models import OrderItem


class Order(IntIdPkMixin, TimestampsMixin, Base):
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
    )
    status: Mapped[str] = mapped_column(
        SQLEnum(OrderStatusEnum, name="order_status_enum"),
        default=OrderStatusEnum.draft,
        nullable=False,
        index=True,
    )

    items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
    )

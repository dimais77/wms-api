from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from dto import OrderCreateDTO, OrderUpdateStatusDTO, OrderDTO
from models import Order, OrderItem
from repositories import OrderRepository, ProductRepository


class OrderService:
    def __init__(self, session: AsyncSession):
        self.repo = OrderRepository(session)
        self.product_repo = ProductRepository(session)

    async def get_all_orders(self) -> List[OrderDTO]:
        orders = await self.repo.read_all()
        return [OrderDTO.model_validate(o) for o in orders]

    async def get_order_by_id(self, order_id: int) -> Optional[OrderDTO]:
        o = await self.repo.find_by_id(order_id)
        return OrderDTO.model_validate(o) if o else None

    async def create_order(self, dto: OrderCreateDTO) -> OrderDTO:
        items = []
        for entry in dto.items:
            product = await self.product_repo.find_by_id(entry["product_id"])
            if not product:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST,
                    detail=f"Product {entry['product_id']} not found",
                )
            if product.quantity < entry["quantity"]:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient stock for product {product.id}",
                )
            product.quantity -= entry["quantity"]
            items.append(
                OrderItem(
                    product_id=product.id,
                    quantity=entry["quantity"],
                    price=float(product.price),
                )
            )

        order = Order(status="pending")
        order.items = items
        created = await self.repo.create(order)
        return OrderDTO.model_validate(created)

    async def update_order_status(
        self, order_id: int, dto: OrderUpdateStatusDTO
    ) -> OrderDTO:
        order = await self.repo.find_by_id(order_id)
        if not order:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Order not found")
        updated = await self.repo.update_status(order, dto.status)
        return OrderDTO.model_validate(updated)

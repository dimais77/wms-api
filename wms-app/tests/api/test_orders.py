import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import OrderCreateSchema, OrderItemBase
from models import Product
from services import OrderService


@pytest.mark.asyncio
async def test_create_order(db_session: AsyncSession):
    product = Product(
        id=1,
        name="Test Product",
        description="Test Product Desc",
        price=10,
        quantity=100,
    )
    db_session.add(product)
    await db_session.commit()

    order_create = OrderCreateSchema(
        items=[OrderItemBase(product_id=product.id, quantity=product.quantity)]
    )

    order = await OrderService.create_order(db_session, order_create)

    assert order is not None
    assert len(order.items) == 1
    assert order.items[0].product_id == 1
    assert order.items[0].quantity == 2
    assert product.quantity == 98


@pytest.mark.asyncio
async def test_read_all_orders(db_session: AsyncSession):
    product = Product(
        id=1,
        name="Test Product",
        description="Test Product Desc",
        price=10,
        quantity=100,
    )
    db_session.add(product)
    await db_session.commit()

    order_create = OrderCreateSchema(
        items=[OrderItemBase(product_id=product.id, quantity=product.quantity)]
    )
    await OrderService.create_order(db_session, order_create)

    orders = await OrderService.get_all_orders(db_session)

    assert len(orders) > 0
    assert orders[0].items[0].product_id == 1


@pytest.mark.asyncio
async def test_get_order(db_session: AsyncSession):
    product = Product(
        id=1,
        name="Test Product",
        description="Test Product Desc",
        price=10,
        quantity=100,
    )
    db_session.add(product)
    await db_session.commit()

    order_create = OrderCreateSchema(
        items=[OrderItemBase(product_id=product.id, quantity=product.quantity)]
    )
    order = await OrderService.create_order(db_session, order_create)

    retrieved_order = await OrderService.get_order_by_id(db_session, order.id)

    assert retrieved_order is not None
    assert retrieved_order.id == order.id


@pytest.mark.asyncio
async def test_update_order_status(db_session: AsyncSession):
    product = Product(
        id=1,
        name="Test Product",
        description="Test Product Desc",
        price=10,
        quantity=100,
    )
    db_session.add(product)
    await db_session.commit()

    order_create = OrderCreateSchema(
        items=[OrderItemBase(product_id=product.id, quantity=product.quantity)]
    )
    order = await OrderService.create_order(db_session, order_create)

    new_status = OrderService.update_order_status().send
    updated_order = await OrderService.update_order_status(
        db_session, order.id, new_status
    )

    assert updated_order.status == new_status.name

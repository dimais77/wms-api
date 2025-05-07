import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import ProductCreateSchema, ProductUpdateSchema
from models import Product


@pytest.mark.asyncio
async def test_create_product(db_session: AsyncSession, ac: AsyncClient):
    product_data = ProductCreateSchema(
        name="Test Product", description="Test Product Desc", price=10, quantity=100
    )

    response = await ac.post(
        "/api/v1/products", json=product_data.model_dump(mode="json")
    )

    assert response.status_code == 201
    created_product = response.json()
    assert created_product["name"] == product_data.name
    assert created_product["description"] == product_data.description
    assert created_product["price"] == product_data.price
    assert created_product["quantity"] == product_data.quantity


@pytest.mark.asyncio
async def test_read_all_products(db_session: AsyncSession, ac: AsyncClient):
    product = Product(
        id=1,
        name="Test Product",
        description="Test Product Desc",
        price=10,
        quantity=100,
    )
    db_session.add(product)
    await db_session.commit()

    response = await ac.get("/api/v1/products")

    assert response.status_code == 200
    products = response.json()
    assert len(products) > 0
    assert products[0]["name"] == product.name
    assert products[0]["description"] == product.description


@pytest.mark.asyncio
async def test_update_product(db_session: AsyncSession, ac: AsyncClient):
    product = Product(
        id=1,
        name="Test Product",
        description="Test Product Desc",
        price=10,
        quantity=100,
    )
    db_session.add(product)
    await db_session.commit()

    updated_product_data = ProductUpdateSchema(
        name="Updated Product",
        description="Updated Product",
        price=10,
        quantity=150,
    )
    response = await ac.put(
        "/api/v1/products/1", json=updated_product_data.model_dump(mode="json")
    )

    assert response.status_code == 200
    updated_product = response.json()
    assert updated_product["name"] == updated_product_data.name
    assert updated_product["description"] == updated_product_data.description
    assert updated_product["quantity"] == updated_product_data.quantity


@pytest.mark.asyncio
async def test_delete_product(db_session: AsyncSession, ac: AsyncClient):
    product = Product(
        id=1,
        name="Test Product",
        description="Test Product Desc",
        price=10,
        quantity=100,
    )
    db_session.add(product)
    await db_session.commit()

    response = await ac.delete("/api/v1/products/1")

    assert response.status_code == 204

    response = await ac.get("/api/v1/products/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"

import httpx
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.core.db_connection import get_db
from app.models.product_model import ProductModel
from tests.conftest import TestingSessionLocal


# Override the FastAPI dependency to use a test database session
@pytest.fixture(scope="function")
async def test_db_session():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = test_db_session


@pytest.mark.asyncio
async def test_get_by_id_existing_product(db_session: AsyncSession):
    """Test fetching a product by ID"""

    # 1. Setup test data
    test_product = ProductModel(name="Test Product", price=10.99, stock=20)
    db_session.add(test_product)
    await db_session.commit()
    await db_session.refresh(test_product)

    # 2. Create an async client using ASGITransport
    async with AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        # 3. Make the request
        response = await client.get("/get_product_by_id/1")

    # 4. Verify response
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Product"

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.db_connection import Base, get_db
from app.main import app

# Database setup
TEST_DATABASE_URL = (
    "postgresql+asyncpg://postgres:gai3905@localhost:5432/test_grocery_store_db"
)
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = async_sessionmaker(
    bind=test_engine, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture(scope="function")
async def async_db() -> AsyncSession:
    """Fixture to provide a clean async database session."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        try:
            yield session  # ✅ Yield actual session, not async generator
        finally:
            await session.close()

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def async_client(async_db):
    """Fixture to override FastAPI's get_db dependency with test session."""

    async def override_get_db():
        yield async_db  # ✅ Now properly yielding the AsyncSession instance

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://localhost") as client:
        yield client

import pytest
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.db_connection import Base, get_db
from app.main import app

import os
import sys

# Add the project root (one directory up) to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# Test database URL (Separate DB or In-Memory for SQLite)
TEST_DATABASE_URL = URL.create(
    drivername="postgresql+asyncpg",
    host="localhost",
    username="postgres",
    password="gai3905",
    port=5432,
    database="test_grocery_store_db",  # Use a separate test database
)

# Create async test engine
test_engine = create_async_engine(TEST_DATABASE_URL, echo=True)

# Create session factory (Fixing session handling issues)
TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    expire_on_commit=False,  # Prevents objects from expiring after commit
    autoflush=False,
    autocommit=False
)

# # Override get_db for test cases
#
#
# async def override_get_db():
#     async with TestingSessionLocal() as session:
#         yield session
#
# app.dependency_overrides[get_db] = override_get_db


# Run migrations before tests
@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # Create tables
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # Cleanup after tests


@pytest.fixture(scope="function")
async def db_session():
    """Creates a fresh database session for each test"""
    async with TestingSessionLocal() as session:
        yield session  # Provide session to test
        await session.rollback()  # Rollback any changes after test

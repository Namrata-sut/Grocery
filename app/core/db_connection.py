from sqlalchemy import URL
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

DATABASE_URL = URL.create(
    drivername="postgresql+asyncpg",
    host="localhost",
    username="postgres",
    password="gai3905",
    port=5432,
    database="grocery_store_db",
)

engine = create_async_engine(DATABASE_URL)

session = async_sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


async def get_db():
    db = session()
    try:
        yield db
    finally:
        await db.close()

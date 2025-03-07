import asyncio
from logging.config import fileConfig
import aiofiles
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context

# Alembic Config object, providing access to the .ini file.
config = context.config

# Import models and Base metadata
from app.models.order_model import OrderModel  # Ensure all models are imported
from app.models.product_model import ProductModel  # Ensure all models are imported
from app.models.user_model import UserModel  # Ensure all models are imported
# from app.models.quiz_model import Quiz  # Ensure all models are imported
# from app.models.score_model import Score  # Ensure all models are imported
from app.core.db_connection import Base

# Set up logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata for autogeneration
target_metadata = Base.metadata


async def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""

    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    async with aiofiles.open('migration.sql', 'w') as f:
        with context.begin_transaction():
            context.run_migrations()
            await f.write("--migration script generated--\n")


def do_run_migrations(connection):
    """Helper function to run migrations with the given connection."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode with an async engine."""

    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"), poolclass=pool.NullPool
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()  # Clean up the engine


if context.is_offline_mode():
    asyncio.run(run_migrations_offline())
else:
    asyncio.run(run_migrations_online())

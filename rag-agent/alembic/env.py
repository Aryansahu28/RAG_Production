
import asyncio

from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import get_settings
from app.infrastructure.database.base import Base

# Import models so they are registered with Base.metadata.
from app.infrastructure.database import models  # noqa: F401


# Alembic configuration object.
config = context.config


# Configure Python logging using alembic.ini.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Load application settings.
settings = get_settings()


# SQLAlchemy metadata used by Alembic autogenerate.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Run migrations without creating a database connection.

    Alembic generates SQL statements using the configured URL.
    """

    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:
    """
    Configure Alembic using an active synchronous
    connection provided by SQLAlchemy's async bridge.
    """

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """
    Create an asynchronous database engine
    and execute migrations.
    """

    connectable = create_async_engine(
        settings.DATABASE_URL,
        poolclass=pool.NullPool,
    )

    try:
        async with connectable.connect() as connection:

            await connection.run_sync(
                do_run_migrations
            )

    finally:
        await connectable.dispose()


def run_migrations_online() -> None:
    """
    Run migrations using an asynchronous connection.
    """

    asyncio.run(run_async_migrations())


if context.is_offline_mode():

    run_migrations_offline()

else:

    run_migrations_online()

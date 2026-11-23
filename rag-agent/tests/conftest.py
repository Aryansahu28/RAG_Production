
from collections.abc import AsyncGenerator

import pytest_asyncio
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings


# --------------------------------------------------
# Safety check: never run integration tests on dev DB
# --------------------------------------------------

database_name = make_url(settings.DATABASE_URL).database

if database_name != "rag_agent_test":
    raise RuntimeError(
        "Integration tests must use the 'rag_agent_test' database. "
        f"Current database: {database_name!r}"
    )


# Import the application engine only after the safety check.
from app.infrastructure.database.session import engine


# --------------------------------------------------
# Database session fixture
# --------------------------------------------------

@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide an isolated async database session for each test.

    Each test runs inside an outer transaction.
    Even if the test calls session.commit(), the outer
    transaction is rolled back after the test.
    """

    async with engine.connect() as connection:

        transaction = await connection.begin()

        session = AsyncSession(
            bind=connection,
            autoflush=False,
            expire_on_commit=False,
            join_transaction_mode="create_savepoint",
        )

        try:
            yield session

        finally:
            await session.close()

            if transaction.is_active:
                await transaction.rollback()

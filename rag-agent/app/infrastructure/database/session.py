from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import async_sessionmaker,AsyncSession,create_async_engine

from app.core.config import settings


engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,
    pool_size= settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_timeout=settings.DB_POOL_TIMEOUT,
    pool_recycle=settings.DB_POOL_RECYCLE,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False

)

async def get_db_session():
    """
    Provides an asynchronous database session.

    A separate session is provided to each request.
    The session is automatically closed after use.
    """

    async with AsyncSessionLocal() as session:
        yield session


# async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
#     async with AsyncSessionLocal() as session:
#         yield session

async def close_db_connection() -> None :
    """
    Dispose of the database engine and its connection pool.
    """
    await engine.dispose()
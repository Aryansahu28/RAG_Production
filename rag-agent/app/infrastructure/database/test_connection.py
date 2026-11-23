
import asyncio

from sqlalchemy import text

from app.infrastructure.database.session import engine


async def test_database_connection():

    try:
        async with engine.connect() as connection:

            result = await connection.execute(
                text("SELECT 1")
            )

            value = result.scalar_one()

            print("Database connection successful!")
            print(f"Query result: {value}")

    except Exception as exc:

        print(f"Database connection failed: {exc}")

        raise

    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(test_database_connection())

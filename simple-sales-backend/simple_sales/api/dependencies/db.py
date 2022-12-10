import asyncpg

from simple_sales.api.app import db


async def get_db() -> asyncpg.Connection:
    async with db.connection() as conn:
        yield conn

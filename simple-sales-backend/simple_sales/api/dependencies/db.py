import asyncpg

from simple_sales.services.database import Database
from simple_sales.settings import DB_DSN

db = Database(DB_DSN)


async def get_db() -> asyncpg.Connection:
    async with db.connection() as conn:
        yield conn

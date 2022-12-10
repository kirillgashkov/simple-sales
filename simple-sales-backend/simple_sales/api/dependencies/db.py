from collections.abc import AsyncIterator

from asyncpg import Connection

from simple_sales.services.database import Database
from simple_sales.settings import DB_DSN

db = Database(DB_DSN)


async def get_db() -> AsyncIterator[Connection]:
    async with db.connection() as conn:
        yield conn

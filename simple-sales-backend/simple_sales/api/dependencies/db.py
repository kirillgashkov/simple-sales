from collections.abc import AsyncIterator

from asyncpg import Record
from asyncpg.pool import PoolConnectionProxy

from simple_sales.services.database import Database
from simple_sales.settings import DB_DSN

db = Database(DB_DSN)


async def get_db() -> AsyncIterator["PoolConnectionProxy[Record]"]:
    async with db.connection() as conn:
        yield conn

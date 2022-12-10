import asyncpg

from simple_sales.services.database import Database
from simple_sales.settings import DB_DSN

db = Database(DB_DSN)


async def get_db_connection() -> asyncpg.Connection:
    with db.connection() as conn:
        yield conn

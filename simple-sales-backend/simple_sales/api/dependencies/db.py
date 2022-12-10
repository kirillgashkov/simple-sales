from collections.abc import AsyncIterator

import asyncpg

from simple_sales.api.app import db


async def get_db() -> AsyncIterator[asyncpg.Connection]:
    async with db.connection() as conn:
        yield conn

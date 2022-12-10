from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from asyncpg import Connection, Pool, create_pool

from simple_sales.services.service import Service


class Database(Service):
    def __init__(self, dsn: str) -> None:
        self.dsn = dsn
        self._pool: Pool | None = None

    async def start(self) -> None:
        self._pool = await create_pool(self.dsn)

    async def stop(self) -> None:
        if self._pool:
            await self._pool.close()

    @asynccontextmanager
    async def connection(self) -> AsyncIterator[Connection]:
        if not self._pool:
            raise RuntimeError("Database not started")

        async with self._pool.acquire() as conn:
            yield conn

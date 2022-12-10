import asyncpg

from simple_sales.services.service import Service


class Database(Service):
    def __init__(self, dsn: str) -> None:
        self.dsn = dsn
        self._pool: asyncpg.Pool | None = None

    async def start(self) -> None:
        self._pool = await asyncpg.create_pool(self.dsn)

    async def stop(self) -> None:
        await self._pool.close()

    async def connection(self) -> asyncpg.Connection:
        async with self._pool.acquire() as conn:
            yield conn
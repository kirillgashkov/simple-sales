from uuid import UUID

from asyncpg import Connection
from pydantic import BaseModel


class City(BaseModel):
    id: UUID
    name: str
    region: str | None


async def insert_city(name: str, region: str | None, db: Connection) -> UUID | None:
    return await db.fetchval(
        """
        INSERT INTO cities (name, region)
        VALUES ($1, $2)
        RETURNING id
        """,
        name,
        region,
    )


async def select_cities(db: Connection) -> list[City]:
    records = await db.fetch(
        """
        SELECT id, name, region
        FROM cities
        """
    )
    return [City(**r) for r in records]


async def select_city_by_id(city_id: UUID, db: Connection) -> City | None:
    record = await db.fetchrow(
        """
        SELECT id, name, region
        FROM cities
        WHERE id = $1
        LIMIT 1
        """,
        city_id,
    )
    return City(**record) if record is not None else None


async def select_city_by_name_and_region(
    name: str, region: str | None, db: Connection
) -> City | None:
    record = await db.fetchrow(
        """
        SELECT id, name, region
        FROM cities
        WHERE name = $1 AND region = $2
        LIMIT 1
        """,
        name,
        region,
    )
    return City(**record) if record is not None else None

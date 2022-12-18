from asyncpg import Connection

from simple_sales.db.errors import SelectDidNotReturnAfterInsertError
from simple_sales.db.models import City


async def select_cities(db: Connection) -> list[City]:
    rows = await db.fetch(
        """
        SELECT id, name, region
        FROM cities
        """
    )
    return [City(**row) for row in rows]


async def select_or_insert_city(db: Connection, *, name: str, region: str) -> City:
    city = await _select_city(db, name=name, region=region)
    if city:
        return city

    await _insert_city_on_conflict_do_nothing(db, name=name, region=region)

    city = await _select_city(db, name=name, region=region)
    if not city:
        raise SelectDidNotReturnAfterInsertError()

    return city


async def _select_city(db: Connection, *, name: str, region: str) -> City | None:
    row = await db.fetchrow(
        """
        SELECT id, name, region
        FROM cities
        WHERE name = $1 AND region = $2
        LIMIT 1
        """,
        name,
        region,
    )
    if not row:
        return None

    return City(**row)


async def _insert_city_on_conflict_do_nothing(
    db: Connection, *, name: str, region: str
) -> None:
    await db.execute(
        """
        INSERT INTO cities (name, region)
        VALUES ($1, $2)
        ON CONFLICT DO NOTHING
        """,
        name,
        region,
    )
